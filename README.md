# Walmart Data Engineering Project

An end-to-end data engineering project that ingests Walmart retail data, validates data quality, stores raw datasets in Amazon S3, processes data through Databricks, and builds analytical models using dbt. Apache Airflow orchestrates the complete workflow.

## Architecture

```text
                 CSV Source Data
                       |
                       v
             Python Ingestion Pipeline
                       |
             +---------+---------+
             |         |         |
             v         v         v
          Discovery  Validation  Batch Tracking
                     (Great       (Manifest)
                   Expectations)
                       |
                       v
                Accepted CSV Files
                       |
                       v
                  Amazon S3
                 (Raw Layer)
                       |
                       v
               Databricks ETL Job
                       |
              +--------+--------+
              |                 |
              v                 v
          Data Processing    CDC Handling
              |
              v
         Databricks Tables
              |
              v
          dbt Transformations
              |
       +------+------------------+
       |                         |
       v                         v
  Silver Technical          Silver Business
    Models                    Model
       |                         |
       +------------+------------+
                    |
                    v
              Gold Layer
                    |
           +--------+--------+
           |                 |
           v                 v
     Dimension Models    Fact Model
       (Snapshots)       (fact_orders)
           |                 |
           +--------+--------+
                    |
                    v
             Analytical Data
                    ^
                    |
             Apache Airflow
             Orchestration
```

Airflow coordinates ingestion, Databricks processing, dbt transformations, data tests, and snapshots. The Databricks task waits for the ETL job to finish before downstream dbt tasks begin.

## Technology Stack

| Category                            | Technology                        |
| ----------------------------------- | --------------------------------- |
| Programming                         | Python                            |
| Data Processing                     | Apache Spark, PySpark, Databricks |
| Cloud Storage                       | Amazon S3                         |
| Data Quality                        | Great Expectations                |
| Data Transformation                 | dbt                               |
| Data Warehouse / Analytics Platform | Databricks                        |
| Workflow Orchestration              | Apache Airflow                    |
| Containerization                    | Docker, Docker Compose            |
| Version Control                     | Git, GitHub                       |

## Project Structure

```text
walmart-data-engineering/
│
├── airflow/
│   ├── dags/
│   │   └── orchestrate.py
│   ├── Dockerfile
│   ├── docker-compose.yaml
│   └── requirements.txt
│
├── ingestion/
│   ├── config/
│   │   └── config.yaml
│   ├── data/
│   ├── gx/
│   │   └── expectations/
│   ├── manifests/
│   ├── src/
│   │   ├── main.py
│   │   ├── batch_manager.py
│   │   ├── config_loader.py
│   │   ├── dataset_validator.py
│   │   ├── discovery.py
│   │   ├── expectation_registry.py
│   │   ├── file_tracker.py
│   │   ├── manifest.py
│   │   ├── reader.py
│   │   ├── rejected_handler.py
│   │   ├── s3_uploader.py
│   │   └── validation.py
│   ├── tests/
│   ├── .env.example
│   └── requirements.txt
│
├── dbt_thouhid/
│   ├── example_profile.yml
│   └── walmart_dbt/
│       ├── analyses/
│       ├── macros/
│       ├── models/
│       │   ├── source/
│       │   ├── silver_t/
│       │   ├── silver_b/
│       │   └── gold/
│       │       ├── ephemeral/
│       │       └── fact/
│       ├── snapshots/
│       ├── tests/
│       └── dbt_project.yml
│
└── .gitignore
```

## 1. Python Ingestion Pipeline

The ingestion component is responsible for discovering, validating, tracking, and uploading source CSV files.

### File discovery and identification

- Discovers CSV files from the configured incoming directory.
- Reads CSV files into Pandas DataFrames.
- Collects file metadata, including file name, file size, modification timestamp, and SHA-256 checksum.
- Uses file hashes to identify previously processed files.

### Data quality validation

Great Expectations is used to validate datasets before they are uploaded.

- Maintains expectation suites for individual datasets.
- Validates incoming DataFrames against defined expectations.
- Rejects files that fail validation.
- Moves rejected files into a rejected directory instead of uploading them to S3.

### Batch management and idempotency

Each file is associated with a batch ID.

The ingestion manifest tracks:

- Batch ID
- File name and checksum
- File size
- Load type
- Processing status
- Attempt count
- Creation and update timestamps

The pipeline uses manifest records to avoid reprocessing previously uploaded files and to resume previously validated batches after an interruption.

### S3 ingestion

Validated files are uploaded to Amazon S3 under a dataset-specific raw prefix.

The pipeline supports:

- Initial load
- Incremental load
- Batch-specific file naming
- Existing-object checks
- Recovery of validated but incomplete uploads

Rejected files are not uploaded.

## 2. Databricks Data Processing

Databricks is used for distributed data processing and downstream table preparation.

The existing Databricks ETL pipeline processes the ingested data and maintains the downstream tables used by dbt.

The project also uses Databricks capabilities to support Change Data Capture (CDC) processing.

The Databricks ETL job is triggered by Airflow using the Databricks provider.

## 3. dbt Transformations

The dbt project uses a layered transformation structure.

### Source layer

Defines the Databricks source tables in the `walmart` catalog and `silver` schema.

### Silver Technical Layer

Contains six technical models:

- `customers_t`
- `employees_t`
- `order_items_t`
- `orders_t`
- `products_t`
- `stores_t`

These models use incremental materialization and `updated_timestamp` filtering to process new or updated records.

### Silver Business Layer

The `obt_b` model creates an enriched One Big Table by joining the six technical models.

It combines order, customer, order item, product, store, and employee information.

### Gold Layer

The Gold layer contains five ephemeral models:

- `eph_customers`
- `eph_employees`
- `eph_orders`
- `eph_products`
- `eph_stores`

These models prepare dimension-level datasets from the business model.

The project uses dbt snapshots to maintain historical dimension records.

Five dimension snapshots are configured:

- `dim_customers`
- `dim_employees`
- `dim_orders`
- `dim_products`
- `dim_stores`

The fact model is:

- `fact_orders`

It selects order, order item, product, store, employee, and customer identifiers alongside order and item-level measures from `obt_b`.

The resulting Gold layer provides a dimensional analytical structure consisting of dimension snapshots and a fact table.

### Data testing

The project includes:

- dbt column-level tests such as `not_null` and `unique`
- A custom SQL test for required identifiers in the business model
- Separate test execution for technical and business models

## 4. Apache Airflow Orchestration

Apache Airflow orchestrates the end-to-end workflow.

The DAG is defined in `airflow/dags/orchestrate.py`.

### Execution sequence

| Order | Task                     | Purpose                                                         |
| ----: | ------------------------ | --------------------------------------------------------------- |
|     1 | `python_ingestion`       | Run the Python ingestion pipeline                               |
|     2 | `confirm`                | Confirm ingestion stage completion                              |
|     3 | `databricks_etl`         | Trigger the existing Databricks ETL job and wait for completion |
|     4 | `clean_target`           | Remove generated dbt directories                                |
|     5 | `dbt_deps`               | Install dbt dependencies                                        |
|     6 | `source_freshness`       | Check source freshness                                          |
|     7 | `silver_technical`       | Run technical models                                            |
|     8 | `silver_technical_tests` | Test technical models                                           |
|     9 | `silver_business`        | Run the business model                                          |
|    10 | `silver_business_tests`  | Test the business model                                         |
|    11 | `gold_ephemeral`         | Run the Gold ephemeral model selection                          |
|    12 | `gold_dimensions`        | Execute dbt snapshots                                           |
|    13 | `gold_facts`             | Build the fact model                                            |

Tasks are connected through explicit dependencies so downstream transformations execute only after their upstream tasks succeed.

### Docker deployment

Airflow runs using Docker Compose with a custom image built from the project's Dockerfile.

The custom image includes the Databricks provider and the Python/dbt dependencies required by the workflow.

The Compose setup uses:

- Airflow services
- PostgreSQL metadata database
- Redis message broker
- CeleryExecutor
- Shared project directories for ingestion and dbt

## 5. Configuration

The project requires credentials and connection details for AWS, Databricks, and dbt.

### AWS

Configure AWS credentials through environment variables or an AWS credentials profile.

The ingestion configuration is maintained in:

`ingestion/config/config.yaml`

Example:

```yaml
source:
  directory: data/incoming
  file_pattern: "*.csv"

aws:
  region: ap-south-1
  bucket_name: YOUR_S3_BUCKET

s3:
  raw_prefix: raw/
  load_type: initial_load
```

For incremental ingestion, change the configured load type to `incremental_load`.

### Databricks

Configure an Airflow connection with:

- Connection ID: `databricks_default`
- Connection type: Databricks
- Host: Your Databricks workspace URL
- Password: Your Databricks personal access token

The DAG references the existing Databricks job ID. Configure it to match your own job if deploying another instance.

### dbt

The dbt project uses the `walmart_dbt` profile.

Create a local `profiles.yml` using `dbt_thouhid/example_profile.yml` as a reference, and configure the appropriate Databricks host, SQL warehouse HTTP path, catalog, schema, and token.

Do not commit real credentials or profile files to GitHub.

## 6. Running the Project

### Prerequisites

- Python
- Docker Desktop with Docker Compose
- AWS account and S3 bucket
- Databricks workspace with the required ETL pipeline and job
- dbt Databricks adapter
- Airflow connections and dbt profile configured

### Start Airflow

From the `airflow` directory:

```bash
docker compose up airflow-init
docker compose up -d
```

Open the Airflow interface:

```text
http://localhost:8080
```

Configure the required Airflow connections and credentials, then enable and trigger the `orchestrate` DAG.

The DAG coordinates the ingestion, Databricks, and dbt stages.

## 7. Current Project Scope

The project focuses on batch-based data ingestion, data quality, cloud storage, distributed processing, transformation, dimensional modelling, and workflow orchestration.

The following are outside the current project scope:

- Real-time streaming pipelines
- CI/CD automation
- Automated schema evolution
- A production-grade multi-environment deployment

## 8. Future Improvements

Potential areas for further development include:

- Automated deployment and CI/CD
- Enhanced monitoring and alerting
- Schema evolution handling
- Expanded data quality coverage
- Production deployment configuration

## Repository

GitHub: https://github.com/thouhid-SB/walmart-data-engineering

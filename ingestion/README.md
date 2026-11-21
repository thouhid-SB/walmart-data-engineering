# E-commerce CSV Ingestion Pipeline

## 1. Project Overview

A Python-based data ingestion pipeline designed to read CSV files, validate data using Great Expectations (GX), and upload validated datasets to AWS S3.

The pipeline aims to support:

- Incremental file ingestion
- Duplicate prevention and idempotency
- Batch identification
- Data quality validation
- Failure handling and crash recovery
- Ingestion tracking through manifests

**Tech Stack:** Python, Pandas, Great Expectations, AWS S3, Boto3.

## 2. Project Architecture

The ingestion pipeline follows a simple sequential architecture:

```text
CSV Files
    |
    v
File Discovery
    |
    v
File Identification
    |
    v
CSV Reading
    |
    v
GX Validation
    |
    v
Batch Identification
    |
    v
S3 Upload
    |
    v
Manifest Management
```

## 3. Project Structure

```text
ecom_ingestion/
│
├── data/
│   └── incoming/
│
├── sample_data/
│
├── src/
│   ├── main.py
│   ├── config_loader.py
│   ├── discovery.py
│   ├── file_tracker.py
│   ├── reader.py
│   ├── validation.py
│   ├── batch_manager.py
│   ├── s3_uploader.py
│   └── manifest.py
│
├── gx/
│   └── expectations/
│
├── config/
│   └── config.yaml
│
├── manifests/
├── tests/
│
├── requirements.txt
├── README.md
└── .gitignore
```

## 4. Implementation Progress

### Milestone 1 — Project Initialization and CSV Discovery

**Status: Completed**

#### 4.1 Configuration Management

The pipeline uses a YAML configuration file to separate application settings from Python logic.

`config/config.yaml`

```yaml
source:
  directory: data/incoming
  file_pattern: "*.csv"
```

This allows us to change the source directory and file pattern without modifying application code.

#### 4.2 Configuration Loading

`src/config_loader.py`

- Loads the YAML configuration.
- Uses PyYAML's `safe_load()`.
- Returns configuration as a Python dictionary.

#### 4.3 CSV Discovery

`src/discovery.py`

- Uses Python's pathlib module.
- Identifies CSV files in the configured directory.
- Uses the configured file pattern.
- Returns discovered file paths.
- Handles missing directories.

#### 4.4 Main Execution

`src/main.py`

The main module orchestrates the discovery process:

1. Loads configuration using `config_loader.py`.
2. Extracts the source directory and file pattern.
3. Passes both parameters to `discovery.py`.
4. Receives discovered CSV file paths.
5. Prints the discovered filenames.

**Execution Flow:**

```text
main.py
   |
   v
config_loader.py
   |
   v
Load config.yaml
   |
   v
Extract source directory
and file pattern
   |
   v
discovery.py
   |
   v
Discover matching CSV files
   |
   v
Return file paths to main.py
   |
   v
Print discovered filenames
```

**Current Test Output:**

```text
Discovered: customers.csv
Discovered: orders.csv
```

### Future Milestones

| Milestone | Implementation                        | Status    |
| --------- | ------------------------------------- | --------- |
| M1        | Project setup and CSV discovery       | Completed |
| M2        | File identification and CSV reading   | Pending   |
| M3        | Great Expectations validation         | Pending   |
| M4        | Batch identification                  | Pending   |
| M5        | AWS S3 upload                         | Pending   |
| M6        | Manifest and idempotency              | Pending   |
| M7        | Crash recovery and end-to-end testing | Pending   |

## 5. Git Workflow

Changes will be committed and pushed after each stable milestone.

Commit naming convention:

```text
M1: Implement configurable CSV discovery
M2: Implement file tracking and CSV reading
M3: Implement GX data validation
```

Each milestone will be tested before committing.

### Milestone 2 — File Identification and CSV Reading

**Status: Completed**

#### 4.5 File Identification

`src/file_tracker.py`

Collects metadata for every discovered CSV file.

- File name using `Path.name`.
- File size using `Path.stat()`.
- Last modified timestamp in UTC.
- SHA256 checksum using `hashlib`.

The SHA256 checksum is calculated in 8 KB chunks to avoid loading the entire file into memory.

The checksum will later support file-level incremental ingestion and duplicate detection.

#### 4.6 CSV Reading

`src/reader.py`

Uses Pandas to read discovered CSV files into DataFrames.

- Reads CSV files using `pd.read_csv()`.
- Returns a Pandas DataFrame.
- Captures row count and column names during pipeline execution.

**Test Output:**

```text
File: customers.csv
Rows: 3
Columns: ['customer_id', 'name', 'city']

File: orders.csv
Rows: 3
Columns: ['order_id', 'customer_id', 'amount']
```

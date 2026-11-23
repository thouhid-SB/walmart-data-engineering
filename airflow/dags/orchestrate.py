
from airflow.sdk import dag, task
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator


DBT_PROJECT = "/opt/airflow/dbt_thouhid/walmart_dbt"


@dag()
def orchestrate():

    # 1. Python ingestion
    python_ingestion = BashOperator(
        task_id="python_ingestion",
        cwd="/opt/airflow/ingestion",
        bash_command="python -m src.main"
    )

    # 2. Confirm ingestion
    @task
    def confirm():
        print("Ingestion works")

    confirmation = confirm()

    # 3. Trigger Databricks ETL Job
    databricks_etl = DatabricksRunNowOperator(
        task_id="databricks_etl",
        databricks_conn_id="databricks_default",
        job_id="132262125101371",
        wait_for_termination=True,
        polling_period_seconds=30,
    )

    # 4. Clean dbt generated directories
    @task.bash(cwd=DBT_PROJECT)
    def clean_target():
        return "rm -rf target logs dbt_packages"

    cleanup = clean_target()

    # 5. Install dbt packages
    @task.bash(cwd=DBT_PROJECT)
    def dbt_deps():
        return "dbt deps"

    dependencies = dbt_deps()

    # 6. Check source freshness
    @task.bash(cwd=DBT_PROJECT)
    def source_freshness():
        return "dbt source freshness"

    freshness = source_freshness()

    # 7. Silver technical models
    @task.bash(cwd=DBT_PROJECT)
    def silver_technical():
        return "dbt run --select path:models/silver_t"

    technical = silver_technical()

    # 8. Silver technical tests
    @task.bash(cwd=DBT_PROJECT)
    def silver_technical_tests():
        return "dbt test --select path:models/silver_t"

    technical_tests = silver_technical_tests()

    # 9. Silver business models
    @task.bash(cwd=DBT_PROJECT)
    def silver_business():
        return "dbt run --select path:models/silver_b"

    business = silver_business()

    # 10. Silver business tests
    @task.bash(cwd=DBT_PROJECT)
    def silver_business_tests():
        return "dbt test --select path:models/silver_b"

    business_tests = silver_business_tests()

    # 11. Gold ephemeral models
    @task.bash(cwd=DBT_PROJECT)
    def gold_ephemeral():
        return "dbt run --select path:models/gold/ephemeral"

    ephemeral = gold_ephemeral()

    # 12. Gold dimensions / snapshots
    @task.bash(cwd=DBT_PROJECT)
    def gold_dimensions():
        return "dbt snapshot"

    dimensions = gold_dimensions()

    # 13. Gold fact models
    @task.bash(cwd=DBT_PROJECT)
    def gold_facts():
        return "dbt run --select path:models/gold/fact"

    facts = gold_facts()

    # Task dependencies
    python_ingestion >> confirmation >> databricks_etl

    databricks_etl >> cleanup >> dependencies >> freshness

    freshness >> technical >> technical_tests

    technical_tests >> business >> business_tests

    business_tests >> ephemeral >> dimensions >> facts


orchestrate()

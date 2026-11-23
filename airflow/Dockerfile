
FROM apache/airflow:3.4.0

USER airflow

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir \
    apache-airflow-providers-databricks==7.24.0 \
    -r /requirements.txt

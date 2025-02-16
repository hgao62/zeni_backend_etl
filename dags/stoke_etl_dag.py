from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from main import run_pipeline

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email": ["zhangzz1218@gmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "params": {
        "stock_list": ["AAPL", "AMZN", "MSFT", "GOOGL", "META", "TSLA", "NFLX", "NVDA"],
        "period": "1d",
        "interval": "1d",
    },
}

dag = DAG(
    "stock_data_pipline",
    default_args=default_args,
    description="Run stock data pipeline",
    schedule_interval="0 17 * * *",
    start_date=datetime(2024, 11, 17),
    catchup=False,
    render_template_as_native_obj=True,
)

# Define a task to run the ETL function
task_run_etl = PythonOperator(
    task_id="run_load_stock_data_etl",
    python_callable=run_pipeline,
    op_args=[
        "{{ params.stock_list }}",
        "{{ params.period }}",
        "{{ params.interval }}",
    ],
    dag=dag,
)

# Set the task dependencies to define the execution order
task_run_etl
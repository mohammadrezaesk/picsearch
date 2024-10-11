import json
from typing import Dict, List, Tuple
from airflow.models import Variable
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from src.mongo_client import MongoClient
from src.s3_repository import S3Repository


def prepare_today_s3_key():
    yesterday = datetime.today() + timedelta(days=-2)
    return yesterday.strftime("%Y-%m-%d") + ".json"


def prepare_crawled_data() -> (List[Tuple[str, str]], List[Dict]):
    s3_endpoint = Variable.get("S3_ENDPOINT")
    s3_access_key = Variable.get("S3_ACCESS_KEY")
    s3_secret_key = Variable.get("S3_SECRET_KEY")
    bucket_name = Variable.get("S3_BUCKET_NAME")
    s3_repository = S3Repository(
        endpoint=s3_endpoint,
        bucket=bucket_name,
        access_key=s3_access_key,
        secret_key=s3_secret_key,
    )
    if data := s3_repository.read_binary(prepare_today_s3_key()):
        data = json.loads(data)
    else:
        raise Exception("not crawled yet!")

    return data


def insert_mongo(**kwargs):
    mongo_host_url = Variable.get("MONGO_HOST_URL")
    mongo_db = Variable.get("MONGO_DB")
    mongo_collection = Variable.get("MONGO_COLLECTION")
    mongo_client = MongoClient(mongo_host_url, mongo_db, mongo_collection)
    task_instance = kwargs["ti"]
    data = task_instance.xcom_pull(task_ids="prepare_task")
    mongo_client.insert_documents(data)


default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 10, 9),
    "retries": 1,
}


with DAG(
    dag_id="import_crawled_data_mongo",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
) as dag:
    task1 = PythonOperator(
        task_id="prepare_task",
        python_callable=prepare_crawled_data,
    )
    task2 = PythonOperator(
        task_id="insert_mongo_task",
        python_callable=insert_mongo,
    )

    task1 >> task2

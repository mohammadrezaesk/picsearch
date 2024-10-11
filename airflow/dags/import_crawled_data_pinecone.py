import json
import os
from typing import Dict, List, Tuple
from airflow.models import Variable
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from src.s3_repository import S3Repository
from src.clip_client import ClipClient
from src.pinecone_client import PineconeClient
from src.utils import download_images, remove_file

SAVE_DIR = "/opt/airflow/dags/to_encode/"


def prepare_today_s3_key():
    yesterday = datetime.today() + timedelta(days=-1)
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

    prepared_data: List[Tuple[str, str]] = []
    error_data = []
    for product in data:
        try:
            product_id = product["id"]
            images = product["images"]
            images = [(img, f"{product_id}_{idx}") for idx, img in enumerate(images)]
        except KeyError:
            error_data.append(product)
            continue

        prepared_data = prepared_data + images
    return prepared_data, error_data


def download_images_task(**kwargs):
    task_instance = kwargs["ti"]
    data = task_instance.xcom_pull(task_ids="prepare_task")
    download_images(data[0], SAVE_DIR)


def encode_images():
    clip_client = ClipClient()
    file_paths = []
    file_ids = []
    for filename in os.listdir(SAVE_DIR):
        file_path = os.path.join(SAVE_DIR, filename)
        file_format = filename.split(".")[-1]
        if os.path.isfile(file_path) and file_format in ["jpg", "jpeg", "png"]:
            file_paths.append(file_path)
            file_id = filename.split("/")[-1].split(".")[0]
            file_ids.append(file_id)
        print(len(file_ids))
    return [clip_client.batch_encode_images(file_paths, int(Variable.get("CLIP_ENCODE_SIZE", 64))), file_ids]


def upsert_vectors(**kwargs):
    host_url = Variable.get("PINECONE_HOST_URL")
    index_name = Variable.get("PINECONE_IMAGE_INDEX_NAME")
    api_key = Variable.get("PINECONE_API_KEY")
    pinecone_client = PineconeClient(api_key, host_url, index_name)
    task_instance = kwargs["ti"]
    data = task_instance.xcom_pull(task_ids="encode_task")
    pinecone_client.upsert_image(data[0], data[1])


def remove_downloaded_images(**kwargs):
    for filename in os.listdir(SAVE_DIR):
        file_path = os.path.join(SAVE_DIR, filename)
        remove_file(file_path)


default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 10, 9),
    "retries": 1,
}


with DAG(
    dag_id="import_crawled_data_pinecone",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
) as dag:

    task1 = PythonOperator(
        task_id="prepare_task",
        python_callable=prepare_crawled_data,
    )
    task2 = PythonOperator(
        task_id="download_images_task",
        python_callable=download_images_task,
    )
    task3 = PythonOperator(
        task_id="encode_task",
        python_callable=encode_images,
    )
    task4 = PythonOperator(
        task_id="upsert_vectors_task",
        python_callable=upsert_vectors,
    )
    task5 = PythonOperator(
        task_id="remove_downloaded_images",
        python_callable=remove_downloaded_images,
    )

    task1 >> task2 >> task3 >> task4 >> task5

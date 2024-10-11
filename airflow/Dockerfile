FROM apache/airflow:2.10.2

USER root
RUN apt update && apt install -y git

USER airflow
COPY ./requirements.txt /opt/airflow/
RUN pip install -r requirements.txt

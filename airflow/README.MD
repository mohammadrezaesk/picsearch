# Semantic Search Engine AirFlow #
This project is an airflow instance which manages data pipelines.
It has three main dags:
- import crawled data meilisearch
  - to import the crawled data into meilisearch instance
- import crawled data mongo
   - to import the crawled data into mongo instance
- import crawled dta pinecone
   - to import the crawled data into pinecone instance

## Setup ##
 - Make sure to import variables after deploying via `variables.json` file from `admin->variables` section in panel.
 - Make sure that you ran `setup-network.sh` before. This is file is in the parent directory. This script creates a network in docker to make components connected.
 - Run `docker compose up --build -d`

Now it's ready to work ☀️

## Panels ##
- airflow panel: `localhost:8080`
  - username/password: airflow/airflow

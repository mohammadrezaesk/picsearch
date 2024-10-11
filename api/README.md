# Semantic Search Engine API #
This project is a backend api using python's fast-api for connecting frontend client to data-stores. 

## Setup ##
 - Make sure to create a `.env` file like sample one.
 - Make sure that you ran `setup-network.sh` before. This is file is in the parent directory. This script creates a network in docker to make components connected.
 - Run `docker compose up --build -d`

Now it's ready to answer ☀️

## Panels ##
- mongo panel: `localhost:8081`
  - username/password: admin/pass
- meili panel: `localhost:7700`
  - master-key: check `docker-compose.yml` and `.env`

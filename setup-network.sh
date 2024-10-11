#!/bin/bash

sudo docker network create api-airflow-network

if [ $? -eq 0 ]; then
  echo "Docker network 'api-airflow-network' created successfully."
else
  echo "Failed to create Docker network."
fi


#!/bin/bash

docker rm -f healthcheck_manager
docker build -t health .
docker run --name=healthcheck_manager -dp 8888:5000 health
sleep 5
curl -X get http://127.0.0.1:8888/health_check
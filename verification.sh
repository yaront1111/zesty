#!/bin/bash

# Run Project
docker-compose up --build -d
sleep 5

# Query results
curl -H "Authorization: Bearer test_api" "http://127.0.0.1:5000/secret" | jq '.secretCode'
curl 127.0.0.1:5000/health | jq '.'

# Destroy
docker-compose down

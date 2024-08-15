#!/bin/bash

export ENV_FILE=PROD
docker compose -f docker-compose.yml -f docker-compose-debug.yml up --build
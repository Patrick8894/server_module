#!/bin/bash

export ENV_FILE=DEV
docker compose -f docker-compose.yml -f docker-compose-debug.yml down
docker compose -f docker-compose.yml -f docker-compose-debug.yml up --build
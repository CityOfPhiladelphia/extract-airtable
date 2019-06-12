#!/usr/bin/env bash

set -e

REPO_NAME=airflow-extract-airtable-worker-$ENVIRONMENT

eval $(aws ecr get-login --no-include-email --region us-east-1)
docker build -t $REPO_NAME .
docker tag $REPO_NAME:latest $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/$REPO_NAME:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/$REPO_NAME:latest
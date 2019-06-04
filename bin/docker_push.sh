#!/usr/bin/env bash

echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
docker push ptrhlm/chata-compare-backend
docker push ptrhlm/chata-compare-worker
docker push ptrhlm/chata-compare-frontend

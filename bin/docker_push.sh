#!/usr/bin/env bash

echo "${DOCKER_PASSWORD}" | docker login -u "${DOCKER_USERNAME}" --password-stdin

docker tag ptrhlm/chata-compare-backend:latest ptrhlm/chata-compare-backend:$TRAVIS_TAG
docker tag ptrhlm/chata-compare-worker:latest ptrhlm/chata-compare-worker:$TRAVIS_TAG
docker tag ptrhlm/chata-compare-frontend:latest ptrhlm/chata-compare-frontend:$TRAVIS_TAG

docker push ptrhlm/chata-compare-backend:latest
docker push ptrhlm/chata-compare-worker:latest
docker push ptrhlm/chata-compare-frontend:latest

docker push ptrhlm/chata-compare-backend:$TRAVIS_TAG
docker push ptrhlm/chata-compare-worker:$TRAVIS_TAG
docker push ptrhlm/chata-compare-frontend:$TRAVIS_TAG

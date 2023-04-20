#!/usr/bin/env bash

IMAGE="jepihumet/ecs-deployer"
VERSION="1.12"

docker buildx create --use
docker buildx build --platform=linux/amd64,linux/arm64 -t ${IMAGE} -t ${IMAGE}:${VERSION} -t ${IMAGE}:latest $(dirname $0) --output type=registry --push

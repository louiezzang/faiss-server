#!/bin/bash
DOCKER_IMAGE=$1
CONTAINER_NAME=$2
DIM=$3
$(dirname "$0")/stop $CONTAINER_NAME
$(dirname "$0")/run $DOCKER_IMAGE $CONTAINER_NAME $DIM

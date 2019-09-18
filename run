#!/bin/bash
DOCKER_IMAGE=$1
CONTAINER_NAME=$2
PORT=50051
DIM=200
SAVE_PATH="data/index"
KEYS_PATH=""
NO_SAVE="false"
NPROBE=1
echo "container_name: $CONTAINER_NAME"
echo "port: $PORT"
echo "dim: $DIM"
echo "save_path: $SAVE_PATH"
echo "keys_path: $KEYS_PATH"
echo "no_save: $NO_SAVE"
echo "nprobe: $NPROBE"

ROOT="$(pwd)/$(dirname "$0")"

mkdir -p "${ROOT}/log"
mkdir -p "${ROOT}/data"

docker run -d --name $CONTAINER_NAME -it \
         -p $PORT:50051 \
         -v $(pwd):/app \
         $DOCKER_IMAGE \
         server.py \
           --dim $DIM \
           --log "log/${CONTAINER_NAME}.log" \
           --save_path $SAVE_PATH \
           --debug "true" \
           --no_save "$NO_SAVE" \
           --nprobe $NPROBE

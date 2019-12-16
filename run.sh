#!/bin/bash
DOCKER_IMAGE=$1
CONTAINER_NAME=$2
DIM=$3
MAX_WORKERS=$4
NUM_THREADS=$5
PORT=50051
#DIM=200
SAVE_PATH="data/index/faiss_server.index"
KEYS_PATH=""
NO_SAVE="false"
NPROBE=1

echo "container_name: $CONTAINER_NAME"
echo "port: $PORT"
echo "dim: $DIM"
echo "save_path: $SAVE_PATH"
echo "keys_path: $KEYS_PATH"
echo "no_save: $NO_SAVE"
echo "max_workers: $MAX_WORKERS"
echo "num_threads: $NUM_THREADS"
echo "nprobe: $NPROBE"

ROOT="$(pwd)/$(dirname "$0")"

echo "Stop $CONTAINER_NAME..."
./stop.sh "$CONTAINER_NAME"

echo "Start $CONTAINER_NAME..."
docker run -d --name $CONTAINER_NAME -it \
         -p $PORT:50051 \
         -v $(pwd):/app \
         $DOCKER_IMAGE \
         server.py \
           --dim $DIM \
           --log "logs/${CONTAINER_NAME}.log" \
           --save_path $SAVE_PATH \
           --debug "true" \
           --no_save "$NO_SAVE" \
           --max_workers "$MAX_WORKERS" \
           --num_threads "$NUM_THREADS" \
           --nprobe $NPROBE

echo "Started!"

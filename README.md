# Faiss gRPC Server
## Faiss
A library for efficient similarity search and clustering of dense vectors.

References:
- https://github.com/facebookresearch/faiss
- https://github.com/facebookresearch/faiss/wiki/Threads-and-asynchronous-calls
- https://github.com/daangn/faiss-server


## Protocol buffer compile for gRPC
Install gRPC tool first.
```
pip3 install grpcio==1.15.0 grpcio-tools==1.15.0
```
Compile Protocol buffer.
```
$ python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. faiss.proto
```

## Set application configuration
1. Copy `conf.yaml.sample` to `conf.yaml`
2. Modify `conf.yaml` with your local development environment.

## Build docker image
```
$ docker build -t [YOUR_DOCKER_IMAGE_NAME or YOUR_DOCKER_IMAGE_NAME:VERSION] .
```
or 
```
$ ./build.sh [YOUR_DOCKER_IMAGE_NAME or YOUR_DOCKER_IMAGE_NAME:VERSION]
```
eg.
```
$ ./build.sh nextmining/faiss-server:latest
```

## Run the faiss server
```
$ ./run.sh [YOUR_DOCKER_IMAGE_NAME or YOUR_DOCKER_IMAGE_NAME:VERSION] [YOUR_DOCKER_CONTAINER_NAME] [VECTOR_DIMENSION_SIZE] [MAX_WORKERS] [NUM_THREADS]
```
eg. 
```
$ ./run.sh nextmining/faiss-server:latest faiss-server 200 5 10
```

## Stop the faiss server
Stop and delete docker container.
```
$ ./stop.sh faiss-server
```

## Enter the docker container with shell command and test.
```
$ docker exec -it faiss-server /bin/bash
```
```
$ python client_sample.py test --dim 200 --host localhost --port 50051
```

```
$ python client_sample.py import data/embeds.csv data/ids.csv data/keys.csv --host localhost:50051
$ python client_sample.py search-by-key a2 --host localhost:50051 --count 2
$ python client_sample.py get-embedding 1 --host localhost:50051
$ python client_sample.py search-by-embedding 1 --host localhost:50051 --count 2
```

```
$ python client_sample.py import blobs://recommendation/item_embeddings/all/embeds.csv blobs://recommendation/item_embeddings/all/ids.csv blobs://recommendation/item_embeddings/all/keys.csv --host localhost:50051
```

## Deploy to Kubernetes
### Push docker image to your Container Registries Service
eg. Azure Container Registries(ACR)
```
$ docker image tag nextmining/faiss-server:latest YOUR_CONTAINER_REGISTRIES_SERVICE/faiss-server:1.0.0
$ docker image push YOUR_CONTAINER_REGISTRIES_SERVICE/faiss-server:1.0.0
```

### Deploy to Kubernetes Service
1. Copy `faiss-server.yaml.new.sample` to `faiss-server.yaml`
2. Modify `faiss-server.yaml` with your Kubernetes environment.
```
$ kubectl apply -f /YOUR_LOCAL_PATH/faiss-server.yaml
```


## Protocol buffer compile for gRPC
```
$ python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. faiss.proto
```

## Build docker image
```
$ docker build -t [YOUR DOCKER IMAGE NAME] .
```
or 
```
$ ./build.sh [YOUR DOCKER IMAGE NAME]
```
eg.
```
$ ./build.sh cia/faiss-server
```

## Run the faiss server
```
$ ./run.sh [YOUR DOCKER IMAGE] [YOUR DOCKER CONTAINER NAME] [DIM]
```
eg. 
```
$ ./run.sh cia/faiss-server:latest faiss-server 200
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
```

```
$ python client_sample.py import blobs://recommendation/item_embeddings/all/embeds.csv blobs://recommendation/item_embeddings/all/ids.csv blobs://recommendation/item_embeddings/all/keys.csv --host localhost:50051
```
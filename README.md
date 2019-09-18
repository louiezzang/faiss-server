
## Protocol buffer compile for gRPC
```
$ python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. faiss.proto
```

## Build docker image
```
docker build -t cia/faiss-server .
```

## Run the faiss server
```
$ ./run [YOUR DOCKER IMAGE] [YOUR DOCKER CONTAINER NAME]
```

## Enter the docker container with shell command.
```
docker exec -it faiss-server /bin/bash
```
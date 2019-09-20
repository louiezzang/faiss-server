
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
$ ./build [YOUR DOCKER IMAGE NAME]
```
eg.
```
$ ./build cia/faiss-server
```

## Run the faiss server
```
$ ./run [YOUR DOCKER IMAGE] [YOUR DOCKER CONTAINER NAME]
```
eg. 
```
$ ./run cia/faiss-server:latest faiss-server
```



## Enter the docker container with shell command and test.
```
$ docker exec -it faiss-server /bin/bash
```
```
$ python client_sample.py test --dim 200 --host localhost --port 50051
```
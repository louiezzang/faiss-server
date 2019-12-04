FROM daangn/faiss

ENV GRPC_PYTHON_VERSION 1.15.0
RUN python -m pip install --upgrade pip
RUN pip install grpcio==${GRPC_PYTHON_VERSION} grpcio-tools==${GRPC_PYTHON_VERSION}

RUN pip install pandas
RUN pip install pyyaml
RUN pip install click
RUN pip install gevent==1.3.5
RUN pip install boto3
RUN pip install azure-storage-blob==2.1.0   # Latest version has a major change, some of class names are changed

# Set the working directory to /app
RUN mkdir -p /app
ADD . /app/
WORKDIR /app

# for click library
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

ENTRYPOINT ["python"]
CMD ["server.py"]


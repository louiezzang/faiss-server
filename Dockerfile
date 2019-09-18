FROM daangn/faiss

ENV GRPC_PYTHON_VERSION 1.15.0
RUN python -m pip install --upgrade pip
RUN pip install grpcio==${GRPC_PYTHON_VERSION} grpcio-tools==${GRPC_PYTHON_VERSION}

RUN pip install pandas

# Set the working directory to /app
RUN mkdir -p /app
ADD . /app/
WORKDIR /app

ENTRYPOINT ["python"]
CMD ["server.py"]


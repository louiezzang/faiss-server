import click
import grpc
import numpy as np

import faiss_pb2 as pb2
import faiss_pb2_grpc as pb2_grpc


@click.group()
def cli():
    pass


@click.command()
@click.option('--dim', type=int, help='dimension')
@click.option('--host', default='localhost', help='server host')
@click.option('--port', default=50051, help='server port')
def test(host, port, dim):
    print("host: %s:%d" % (host, port))

    channel = grpc.insecure_channel("%s:%d" % (host, port))
    stub = pb2_grpc.ServerStub(channel)

    response = stub.Total(pb2.EmptyRequest())
    print("total: %d" % response.count)

    embedding = list(np.random.random(dim).astype('float32'))
    print(embedding)
    id = 1
    response = stub.Add(pb2.AddRequest(id=id, embedding=embedding))
    print("response: %s" % response.message)

    embedding = list(np.random.random(dim).astype('float32'))
    print(embedding)
    id = 1
    response = stub.Add(pb2.AddRequest(id=id, embedding=embedding))
    print("response: %s" % response.message)

    embedding = list(np.random.random(dim).astype('float32'))
    id = 2
    response = stub.Add(pb2.AddRequest(id=id, embedding=embedding))
    print("response: %s" % response.message)

    embedding = list(np.random.random(dim).astype('float32'))
    id = 3
    response = stub.Add(pb2.AddRequest(id=id, embedding=embedding))
    print("response: %s" % response.message)

    response = stub.Total(pb2.EmptyRequest())
    print("total: %d" % response.count)

    id = 2
    response = stub.Search(pb2.SearchRequest(id=id, count=5))
    print("response: %s, %s" % (response.ids, response.scores))

    response = stub.Remove(pb2.IdRequest(id=2))
    print("response: %s" % response.message)

    response = stub.Total(pb2.EmptyRequest())
    print("total: %d" % response.count)

    id = 2
    response = stub.Search(pb2.SearchRequest(id=id, count=5))
    print("response: %s, %s" % (response.ids, response.scores))

    # response = stub.Remove(pb2.IdRequest(id=1))
    response = stub.Remove(pb2.IdRequest(id=3))

    response = stub.Total(pb2.EmptyRequest())
    print("total: %d" % response.count)


@click.command("test_key")
@click.option('--dim', type=int, help='dimension')
@click.option('--host', default='localhost', help='server host')
@click.option('--port', default=50051, help='server port')
def test_key(host, port, dim):
    print("host: %s:%d" % (host, port))

    channel = grpc.insecure_channel("%s:%d" % (host, port))
    stub = pb2_grpc.ServerStub(channel)

    response = stub.Total(pb2.EmptyRequest())
    print("total: %d" % response.count)

    embedding = list(np.random.random(dim).astype('float32'))
    print(embedding)
    key = "k1"
    response = stub.Add(pb2.AddRequest(key=key, embedding=embedding))
    print("response: %s" % response.message)

    embedding = list(np.random.random(dim).astype('float32'))
    key = "k1"
    response = stub.Add(pb2.AddRequest(key=key, embedding=embedding))
    print("response: %s" % response.message)

    embedding = list(np.random.random(dim).astype('float32'))
    key = "k2"
    response = stub.Add(pb2.AddRequest(key=key, embedding=embedding))
    print("response: %s" % response.message)

    embedding = list(np.random.random(dim).astype('float32'))
    key = "k3"
    response = stub.Add(pb2.AddRequest(key=key, embedding=embedding))
    print("response: %s" % response.message)

    response = stub.Total(pb2.EmptyRequest())
    print("total: %d" % response.count)

    key = "k1"
    response = stub.Search(pb2.SearchRequest(key=key, count=5))
    print("response: %s, %s" % (response.ids, response.scores))

    key = "k2"
    response = stub.Search(pb2.SearchRequest(key=key, count=5))
    print("response: %s, %s" % (response.ids, response.scores))

    response = stub.Total(pb2.EmptyRequest())
    print("total: %d" % response.count)


@click.command('import')
@click.argument('embs-path')
@click.argument('ids-path')
@click.argument('keys_path')
@click.option('-h', '--host', default='localhost:50051', help='server host:port')
def imports(host, embs_path, ids_path, keys_path):
    print("host: %s" % host)
    channel = grpc.insecure_channel(host)
    stub = pb2_grpc.ServerStub(channel)

    response = stub.Total(pb2.EmptyRequest())
    print("total: %d" % response.count)

    response = stub.Import(pb2.ImportRequest(embs_path=embs_path, ids_path=ids_path, keys_path=keys_path))
    print("response: %s" % response.message)

    response = stub.Total(pb2.EmptyRequest())
    print("total: %d" % response.count)


@click.command()
@click.argument('id', type=int)
@click.option('-h', '--host', default='localhost:50051', help='server host:port')
@click.option('--count', default=10, help='server limit count')
@click.option('-t', '--timeout', default=0.5, help='request timeout')
def search(host, id, count, timeout):
    with grpc.insecure_channel(host) as channel:
        stub = pb2_grpc.ServerStub(channel)
        response = stub.Search(pb2.SearchRequest(id=id, count=count), timeout=timeout)
        print("response: %s, %s" % (response.ids, response.scores))


@click.command()
@click.argument('key', type=str)
@click.option('-h', '--host', default='localhost:50051', help='server host:port')
@click.option('--count', default=10, help='server limit count')
@click.option('-t', '--timeout', default=0.1, help='request timeout')
def search_by_key(host, key, count, timeout):
    print("host: %s" % host)
    with grpc.insecure_channel(host) as channel:
        response = _search_by_key(host, key, count, timeout, channel)
    print("response: %s, %s" % (response.keys, response.scores))


def _search_by_key(host, key, count, timeout, channel):
    stub = pb2_grpc.ServerStub(channel)
    return stub.Search(pb2.SearchRequest(key=key, count=count))

@click.command()
@click.argument('id', type=int)
@click.option('-h', '--host', default='localhost:50051', help='server host:port')
@click.option('-t', '--timeout', default=0.5, help='request timeout')
def get_embedding(host, id, timeout):
    with grpc.insecure_channel(host) as channel:
        stub = pb2_grpc.ServerStub(channel)
        response = stub.GetEmbedding(pb2.SearchRequest(id=id), timeout=timeout)
        print("response: %s" % response.embedding)


@click.command()
@click.argument('id', type=int)
@click.option('-h', '--host', default='localhost:50051', help='server host:port')
@click.option('--count', default=10, help='server limit count')
@click.option('-t', '--timeout', default=0.1, help='request timeout')
def search_by_embedding(host, id, count, timeout):
    with grpc.insecure_channel(host) as channel:
        stub = pb2_grpc.ServerStub(channel)
        emb_response = stub.GetEmbedding(pb2.SearchRequest(id=id), timeout=timeout)
        embedding = emb_response.embedding
        response = stub.SearchByEmbedding(pb2.SearchByEmbeddingRequest(embedding=embedding, count=count), timeout=timeout)
    print("response: %s, %s" % (response.keys, response.scores))


@click.command()
@click.argument('keys-path', type=str)
@click.option('-h', '--host', default='localhost:50051', help='server host:port')
@click.option('--count', default=10, help='server limit count')
@click.option('-t', '--timeout', default=0.1, help='request timeout')
def test_search_perform(host, keys_path, count, timeout):
    print("host: %s" % host)
    from time import time
    import pandas as pd
    from gevent.pool import Pool
    p = Pool(100)
    keys = pd.read_csv(keys_path, header=None, squeeze=True, dtype=('str'))
    channel = grpc.insecure_channel(host)

    def search_fn(key):
        #print(key)
        t = time()
        response = _search_by_key(host, key, count, timeout, channel)
        return time() - t

    t = time()
    result = p.imap_unordered(search_fn, keys.sample(100).values)
    result = list(result)
    print(time() - t)
    print(np.array(result).mean())


if __name__ == '__main__':
    cli.add_command(test)
    cli.add_command(test_key)
    cli.add_command(imports)
    cli.add_command(search)
    cli.add_command(search_by_key)
    cli.add_command(get_embedding)
    cli.add_command(search_by_embedding)
    cli.add_command(test_search_perform)
    cli()


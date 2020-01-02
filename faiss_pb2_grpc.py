# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import faiss_pb2 as faiss__pb2


class ServerStub(object):
  """Service Definition
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Add = channel.unary_unary(
        '/faiss_index.Server/Add',
        request_serializer=faiss__pb2.AddRequest.SerializeToString,
        response_deserializer=faiss__pb2.SimpleResponse.FromString,
        )
    self.Remove = channel.unary_unary(
        '/faiss_index.Server/Remove',
        request_serializer=faiss__pb2.IdRequest.SerializeToString,
        response_deserializer=faiss__pb2.SimpleResponse.FromString,
        )
    self.Search = channel.unary_unary(
        '/faiss_index.Server/Search',
        request_serializer=faiss__pb2.SearchRequest.SerializeToString,
        response_deserializer=faiss__pb2.SearchResponse.FromString,
        )
    self.SearchByEmbedding = channel.unary_unary(
        '/faiss_index.Server/SearchByEmbedding',
        request_serializer=faiss__pb2.SearchByEmbeddingRequest.SerializeToString,
        response_deserializer=faiss__pb2.SearchResponse.FromString,
        )
    self.GetEmbedding = channel.unary_unary(
        '/faiss_index.Server/GetEmbedding',
        request_serializer=faiss__pb2.GetEmbeddingRequest.SerializeToString,
        response_deserializer=faiss__pb2.EmbeddingResponse.FromString,
        )
    self.Restore = channel.unary_unary(
        '/faiss_index.Server/Restore',
        request_serializer=faiss__pb2.RestoreRequest.SerializeToString,
        response_deserializer=faiss__pb2.SimpleResponse.FromString,
        )
    self.Import = channel.unary_unary(
        '/faiss_index.Server/Import',
        request_serializer=faiss__pb2.ImportRequest.SerializeToString,
        response_deserializer=faiss__pb2.SimpleResponse.FromString,
        )
    self.Total = channel.unary_unary(
        '/faiss_index.Server/Total',
        request_serializer=faiss__pb2.EmptyRequest.SerializeToString,
        response_deserializer=faiss__pb2.TotalResponse.FromString,
        )


class ServerServicer(object):
  """Service Definition
  """

  def Add(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Remove(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Search(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SearchByEmbedding(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetEmbedding(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Restore(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Import(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Total(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ServerServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Add': grpc.unary_unary_rpc_method_handler(
          servicer.Add,
          request_deserializer=faiss__pb2.AddRequest.FromString,
          response_serializer=faiss__pb2.SimpleResponse.SerializeToString,
      ),
      'Remove': grpc.unary_unary_rpc_method_handler(
          servicer.Remove,
          request_deserializer=faiss__pb2.IdRequest.FromString,
          response_serializer=faiss__pb2.SimpleResponse.SerializeToString,
      ),
      'Search': grpc.unary_unary_rpc_method_handler(
          servicer.Search,
          request_deserializer=faiss__pb2.SearchRequest.FromString,
          response_serializer=faiss__pb2.SearchResponse.SerializeToString,
      ),
      'SearchByEmbedding': grpc.unary_unary_rpc_method_handler(
          servicer.SearchByEmbedding,
          request_deserializer=faiss__pb2.SearchByEmbeddingRequest.FromString,
          response_serializer=faiss__pb2.SearchResponse.SerializeToString,
      ),
      'GetEmbedding': grpc.unary_unary_rpc_method_handler(
          servicer.GetEmbedding,
          request_deserializer=faiss__pb2.GetEmbeddingRequest.FromString,
          response_serializer=faiss__pb2.EmbeddingResponse.SerializeToString,
      ),
      'Restore': grpc.unary_unary_rpc_method_handler(
          servicer.Restore,
          request_deserializer=faiss__pb2.RestoreRequest.FromString,
          response_serializer=faiss__pb2.SimpleResponse.SerializeToString,
      ),
      'Import': grpc.unary_unary_rpc_method_handler(
          servicer.Import,
          request_deserializer=faiss__pb2.ImportRequest.FromString,
          response_serializer=faiss__pb2.SimpleResponse.SerializeToString,
      ),
      'Total': grpc.unary_unary_rpc_method_handler(
          servicer.Total,
          request_deserializer=faiss__pb2.EmptyRequest.FromString,
          response_serializer=faiss__pb2.TotalResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'faiss_index.Server', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))

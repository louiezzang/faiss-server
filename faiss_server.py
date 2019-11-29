import os
import logging
from tempfile import gettempdirb
from time import time

import pandas as pd
import numpy as np

from faiss_index import FaissIndex
import faiss_pb2 as pb2
import faiss_pb2_grpc as pb2_grpc

import yaml
import boto3
from azure.storage.blob import BlockBlobService


class FaissServer(pb2_grpc.ServerServicer):
    def __init__(self, dim, save_path, keys_path, nprobe, num_threads=None):
        logging.info("dim: %d", dim)
        logging.info("save_path: %s", save_path)
        logging.info("keys_path: %s", keys_path)
        logging.info("nprobe: %d", nprobe)
        if num_threads is not None:
            logging.info("num_threads: %d", num_threads)

        stream = open("conf.yaml", 'r')
        self._conf = yaml.load(stream, Loader=yaml.FullLoader)
        print(self._conf)

        remote_path, save_path = self.down_if_remote_path(save_path)

        self._remote_path = remote_path
        self._save_path = save_path
        self._index = FaissIndex(dim, save_path, num_threads)
        if nprobe > 1:
            self._index.set_nprobe(nprobe)
        self._keys, self._key_index = self._load_keys(keys_path)
        logging.info("ntotal: %d", self._index.ntotal())

    def parse_remote_path(self, save_path):
        if save_path is None or (not save_path.startswith("s3://") and not save_path.startswith("blobs://")):
            return None, save_path
        remote_path = save_path
        filename = os.path.basename(remote_path)
        save_path = "%s/%d-%s" % (gettempdirb().decode("utf-8"), time(), filename)
        return remote_path, save_path

    def down_if_remote_path(self, save_path):
        remote_path, local_path = self.parse_remote_path(save_path)
        if not remote_path:
            return None, local_path
        logging.debug("remote_path=%s", remote_path)
        if remote_path.startswith("s3://"):
            s3 = boto3.resource("s3")
            tokens = remote_path.replace("s3://", "").split("/")
            bucket_name = tokens[0]
            key = "/".join(tokens[1:])
            s3.Bucket(bucket_name).download_file(key, local_path)
        elif remote_path.startswith("blobs://"):
            blob_service = BlockBlobService(account_name=self._conf["azure_blobs"]["storage.account"],
                                            account_key=self._conf["azure_blobs"]["account.key"])
            container_name = self._conf["azure_blobs"]["container"]
            remote_path = remote_path.replace("blobs://", "")
            prefix = remote_path
            generator = blob_service.list_blobs(container_name, prefix=prefix)

            fp = open(local_path, "ab")
            for blob in generator:
                # Using `get_blob_to_bytes`
                b = blob_service.get_blob_to_bytes(container_name, blob.name)
                fp.write(b.content)
                # Or using `get_blob_to_stream`
                # service.get_blob_to_stream(container_name, blob.name, fp)

            fp.flush()
            fp.close()

        return remote_path, local_path

    def _load_keys(self, keys_path):
        if not keys_path:
            return None, None
        _, keys_path = self.down_if_remote_path(keys_path)
        keys = pd.read_csv(keys_path, header=None, squeeze=True, dtype=("str"))
        key_index = pd.Index(keys)
        logging.debug("keys: keys[size=%d]=%s, keys_index[size=%d]=%s",
                      len(keys), keys.values[:10], len(key_index), key_index[:10])
        return keys.values, key_index

    def Total(self, request, context):
        return pb2.TotalResponse(count=self._index.ntotal())

    def Add(self, request, context):
        logging.debug("add - id: %d, %s", request.id, request.key)
        if request.key:
            # if self._key_index is None or not self._key_index.contains(request.key):
            if self._key_index is None or request.key not in self._key_index:
                if self._key_index is None:
                    self._key_index = pd.Index([request.key])
                else:
                    self._key_index = self._key_index.append(pd.Index([request.key]))

                request.id = self._key_index.get_loc(request.key)
                if self._keys is None:
                    self._keys = np.array([request.key])
                else:
                    self._keys = np.append(self._keys, [request.key])
            else:
                request.id = self._key_index.get_loc(request.key)

        # For debugging
        # if self._keys is not None and self._key_index is not None:
        #     logging.debug("keys: keys=%s, keys_index=%s", self._keys, self._key_index)

        xb = np.expand_dims(np.array(request.embedding, dtype=np.float32), 0)
        ids = np.array([request.id], dtype=np.int64)
        self._index.replace(xb, ids)

        return pb2.SimpleResponse(message="Added, %d!" % request.id)

    def Remove(self, request, context):
        logging.debug("remove - id: %d", request.id)
        ids = np.array([request.id], dtype=np.int64)
        removed_count = self._index.remove(ids)

        if removed_count < 1:
            return pb2.SimpleResponse(message="Not existed, %s!" % request.id)
        return pb2.SimpleResponse(message="Removed, %s!" % request.id)

    def Search(self, request, context):
        if request.key:
            # if self._key_index is None or not self._key_index.contains(request.key):
            if self._key_index is None or request.key not in self._key_index:
                logging.debug("search - Key not found: %s", request.key)
                return pb2.SearchResponse()
            request.id = self._key_index.get_loc(request.key)
        # logging.debug("search - id: %d, %s", request.id, request.key)

        D, I = self._index.search_by_id(request.id, request.count)
        K = None
        if request.key:
            K = self._keys[I[0]]
        return pb2.SearchResponse(ids=I[0], scores=D[0], keys=K)

    def SearchByEmbedding(self, request, context):
        # logging.debug("search_by_emb - embedding: %s", request.embedding[:10])
        emb = np.array(request.embedding, dtype=np.float32)
        emb = np.expand_dims(emb, axis=0)
        D, I = self._index.search(emb, request.count)
        return pb2.SearchResponse(ids=I[0], scores=D[0])

    def Restore(self, request, context):
        logging.debug("restore - %s", request.save_path)
        remote_path, save_path = self.down_if_remote_path(request.save_path)
        self._remote_path = remote_path
        self._save_path = save_path
        self._index.restore(request.save_path)
        return pb2.SimpleResponse(message="Restored, %s!" % request.save_path)

    def Import(self, request, context):
        logging.info("importing - %s, %s, %s", request.embs_path, request.ids_path, request.keys_path)
        _, embs_path = self.down_if_remote_path(request.embs_path)
        _, ids_path = self.down_if_remote_path(request.ids_path)
        _, keys_path = self.down_if_remote_path(request.keys_path)
        df = pd.read_csv(embs_path, delimiter="\t", header=None)
        X = df.values
        # logging.debug("X = %s", X)
        df = pd.read_csv(ids_path, header=None)
        ids = df[0].values
        logging.info("ids[size=%d] = %s", len(ids), ids)

        X = np.ascontiguousarray(X, dtype=np.float32)
        ids = np.ascontiguousarray(ids, dtype=np.int64)

        # self._index.replace(X, ids)
        self._index.rebuild(X, ids)

        self._keys, self._key_index = self._load_keys(keys_path)

        return pb2.SimpleResponse(message="Imported, %s, %s, %s!" % (request.embs_path, request.ids_path, request.keys_path))

    def save(self):
        logging.debug("saving index to %s", self._save_path)
        self._index.save(self._save_path)

import logging
from os.path import isfile

import faiss
import numpy as np


class FaissIndex:
    def __init__(self, dim: int, save_path: str, num_threads: int = None):
        """
        Constructor.
        :param dim:
        :param save_path:
        :param num_threads
        """
        self.dim = dim
        if num_threads is not None and num_threads > 0:
            faiss.omp_set_num_threads(num_threads)
        if isfile(save_path):
            logging.debug("restore: %s", save_path)
            self._index = faiss.read_index(save_path)
        else:
            self._sub_index = faiss.IndexFlat(dim)
            self._index = faiss.IndexIDMap2(self._sub_index)

    def replace(self, xb, ids):
        """
        Replaces the index with new data if the id exists already and adds the index if the id does not exist.
        :param xb:
        :param ids:
        :return:
        """
        logging.debug("replace: %s", ids)
        # Remove the existing ones
        self.remove(ids)
        return self._index.add_with_ids(xb, ids)

    def rebuild(self, xb, ids):
        """
        Rebuilds the index with new data. The existing ones will be all deleted.
        :param xb:
        :param ids:
        :return:
        """
        logging.debug("rebuild: %s", ids)
        # Reset the index
        self._index.reset()
        # self._sub_index = faiss.IndexFlat(self.dim)
        # self._index = faiss.IndexIDMap2(self._sub_index)
        return self._index.add_with_ids(xb, ids)

    def add(self, xb, ids):
        """
        Adds data with ids.
        :param xb:
        :param ids:
        :return:
        """
        return self._index.add_with_ids(xb, ids)

    def search(self, xq, k=10):
        """
        Searches by vector.
        :param xq:
        :param k:
        :return:
        """
        return self._index.search(xq, k)

    def search_by_id(self, id, k=10):
        """
        Searches by id.
        :param id:
        :param k:
        :return:
        """
        try:
            x = self._index.reconstruct(id)
            xq = np.expand_dims(x, axis=0)
        except RuntimeError as e:
            if str(e).endswith("not found"):
                return ([None], [None])
            else:
                raise e
        return self.search(xq, k)

    def reconstruct(self, id):
        """
        Returns the embedding vector by id.
        :param id:
        :return:
        """
        try:
            x = self._index.reconstruct(id)
            xq = np.expand_dims(x, axis=0)
            return xq
        except RuntimeError as e:
            if str(e).endswith("not found"):
                return None
            else:
                raise e

    def ntotal(self):
        """
        Returns the total number of rows.
        :return:
        """
        return self._index.ntotal

    def remove(self, ids):
        """
        Removes by ids.
        :param ids:
        :return:
        """
        return self._index.remove_ids(ids)

    def restore(self, filepath):
        """
        Restores with new file path.
        :param filepath:
        :return:
        """
        pre_index = self._index
        self._index = faiss.read_index(filepath)
        if pre_index:
            pre_index.reset()

    def reset(self):
        """
        Resets the index.
        :return:
        """
        self._index.reset()

    def save(self, filepath):
        """
        Saves the index into the file .
        :param filepath:
        :return:
        """
        if self.ntotal() > 0:
            faiss.write_index(self._index, filepath)

    def set_nprobe(self, nprobe):
        faiss.ParameterSpace().set_index_parameter(self._index, "nprobe", nprobe)


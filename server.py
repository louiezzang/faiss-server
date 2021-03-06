import time
import logging
import os
import sys
import signal
import argparse
from concurrent import futures

import grpc

import faiss_pb2_grpc as pb2_grpc
from faiss_server import FaissServer


_ONE_DAY_IN_SECONDS = 60 * 60 * 24


if not os.path.exists(os.getcwd() + "/logs"):
    os.makedirs(os.getcwd() + "/logs")


def main(args):
    dim = args.dim
    save_path = args.save_path
    keys_path = args.keys_path
    log = args.log
    debug = args.debug
    no_save = args.no_save
    max_workers = args.max_workers
    num_threads = args.num_threads
    nprobe = args.nprobe

    if log:
        handler = logging.FileHandler(filename=log)
    else:
        handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s - %(message)s")
    handler.setFormatter(formatter)
    root = logging.getLogger()
    level = debug and logging.DEBUG or logging.INFO
    root.setLevel(level)
    root.addHandler(handler)

    logging.info("server loading...")
    logging.info("max_workers: %d", max_workers)
    if num_threads is not None:
        logging.info("num_threads: %d", num_threads)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    #servicer = FaissServer(dim, save_path, keys_path, nprobe)
    servicer = FaissServer(dim, save_path, keys_path, nprobe, num_threads)
    pb2_grpc.add_ServerServicer_to_server(servicer, server)
    server.add_insecure_port("[::]:50051")
    server.start()
    logging.info("server started")

    # for docker heath check
    with open("/tmp/status", "w") as f:
        f.write("started")

    def stop_serve(signum, frame):
        raise KeyboardInterrupt
    signal.signal(signal.SIGINT, stop_serve)
    signal.signal(signal.SIGTERM, stop_serve)

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)
        if not no_save:
            servicer.save()
        logging.info("server stopped")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--dim',
        type=int,
        default=200,
        help='Dimension')
    parser.add_argument(
        '--save_path',
        type=str,
        default='faiss_server.index',
        help='index save path')
    parser.add_argument(
        '--keys_path',
        type=str,
        help='keys file path')
    parser.add_argument(
        '--log',
        type=str,
        help='log file path')
    parser.add_argument(
        '--debug',
        type=bool,
        default=True,
        help='debug')
    parser.add_argument(
        '--no_save',
        type=bool,
        default=True,
        help='no save when stop service')
    parser.add_argument(
        '--max_workers',
        type=int,
        default=1,
        help='grpc workers count')
    parser.add_argument(
        '--num_threads',
        type=int,
        default=None,
        help='faiss index thread count(omp_set_num_threads)')
    parser.add_argument(
        '--nprobe',
        type=int,
        default=1,
        help='nprobe for the search quality')

    args = parser.parse_args()
    main(args)



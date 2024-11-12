import gzip
import os
from os.path import isfile, join
import numpy as np


def list_files(mnist_path):
    return [
        join(mnist_path, f)
        for f in os.listdir(mnist_path)
        if isfile(join(mnist_path, f))
    ]


def read_images(data):
    _ = int.from_bytes(data.read(4), "big")
    num_images = int.from_bytes(data.read(4), "big")
    rows = int.from_bytes(data.read(4), "big")
    cols = int.from_bytes(data.read(4), "big")
    images = data.read()
    return np.frombuffer(images, dtype=np.uint8).reshape((num_images, rows, cols))


def read_labels(data):
    labels = data.read()[8:]
    return np.frombuffer(labels, dtype=np.uint8)


def get_images(mnist_path):
    x_train, y_train, x_test, y_test = None, None, None, None

    for f in list_files(mnist_path):
        with gzip.open(f, "rb") as data:
            if "train-images" in f:
                x_train = read_images(data)
            elif "train-labels" in f:
                y_train = read_labels(data)
            elif "t10k-images" in f:
                x_test = read_images(data)
            elif "t10k-labels" in f:
                y_test = read_labels(data)

    return x_train, y_train, x_test, y_test

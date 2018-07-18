# coding: utf-8

"""
MNIST digit classification, via eager

adapted by Chris
"""

from __future__ import absolute_import, division, print_function
import argparse
import tensorflow as tf
import tensorflow.contrib.eager as tfe
tf.enable_eager_execution()


def parse_args():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser(description='Train mnist with Eager API')
    parser.add_argument('--log_interval', default=10, type=int, help='batches between logging training status')
    parser.add_argument('--output_dir', default=None, type=str, help='Directory to write TensorBoard summaries')
    parser.add_argument('--learning_rate', default=0.01, type=float, help='Learning rate.')
    parser.add_argument('--momentum', default=0.5, type=float, help='SGD momentum.')
    parser.add_argument('--no_gpu', default=False, type=bool, help='disables GPU usage even if a GPU is available')
    parser.add_argument('--data_dir', '/tmp/tensorflow/mnist/input_data')
    parser.add_argument('--model_dir', '/tmp/tensorflow/mnist/checkpoints/')
    parser.add_argument('--batch_size', 100)
    parser.add_argument('--train_epochs', 10)

    args = parser.parse_args()
    return args


def run_mnist_eager():
    device = '/gpu:0'
    data_format = 'channels_first'


if __name__ == '__main__':
    run_mnist_eager()

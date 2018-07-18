# coding: utf-8

from __future__ import absolute_import, division, print_function

import numpy as np
import tensorflow as tf

#OK
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# not works for tf-r1.4.0
#tf.logging.set_verbosity(tf.logging.INFO)

## fails
#tf.logging.set_verbosity(tf.logging.WARN)
#import logging
#logging.getLogger('tensorflow').setLevel(logging.ERROR)

a = tf.constant(3.0, dtype=tf.float32)
b = tf.constant(4.0) # also tf.float32 implicitly

total = a + b
print(a)
print(b)
print(total)

writer = tf.summary.FileWriter(logdir='logs')
writer.add_graph(tf.get_default_graph())


sess = tf.Session()
print(sess.run(total))

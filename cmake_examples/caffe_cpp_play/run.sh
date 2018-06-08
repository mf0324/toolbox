#!/bin/bash

#Usage: ./im_cls deploy.prototxt network.caffemodel mean.binaryproto labels.txt img.jpg

./build/im_cls \
    /opt/work/caffe-BVLC/models/bvlc_alexnet/deploy.prototxt \
    /opt/work/lesion/data/imagenet_models/bvlc_alexnet.caffemodel \
    /opt/work/caffe-BVLC/data/ilsvrc12/imagenet_mean.binaryproto \
    /opt/work/caffe-BVLC/data/ilsvrc12/synset_words.txt \
    /opt/work/caffe-BVLC/examples/images/cat.jpg

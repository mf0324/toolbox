#!/usr/bin/env python
# coding: utf-8

"""
Description: extract prototxt from a given caffemodel
author：采石工
from：https://www.zhihu.com/question/59597255/answer/168686857
"""

#coding=utf-8
'''
@author: kangkai
'''
import sys
sys.path.insert(0, '/home/zz/work/caffe-BVLC/python')
from caffe.proto import caffe_pb2
import fire

def toPrototxt(modelName, deployName):
    with open(modelName, 'rb') as f:
        caffemodel = caffe_pb2.NetParameter()
        caffemodel.ParseFromString(f.read())

    # 兼容新旧版本
    # LayerParameter 消息中的 blobs 保存着可训练的参数
    for item in caffemodel.layers:
        item.ClearField('blobs')
    for item in caffemodel.layer:
        item.ClearField('blobs')

    # print(caffemodel)
    with open(deployName, 'w') as f:
        f.write(str(caffemodel))

if __name__ == '__main__':
    fire.Fire(toPrototxt)
    #modelName = 'facenet_iter_14000.caffemodel'
    #deployName = 'facenet_deploy.prototxt'
    #toPrototxt(modelName, deployName)

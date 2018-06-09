#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function
import sys, os
import xml.etree.ElementTree as ET
import math
import matplotlib.pyplot as plt
import numpy as np
import cv2
from easydict import EasyDict as edict

# db_dir = '/home/zll/work/py-faster-rcnn/data/VOCdevkit2007/UF11'
# db_dir = '/home/zll/work/py-faster-rcnn/data/VOCdevkit2007/US11'
#db_dir = '/home/zll/work/py-faster-rcnn/data/VOCdevkit2007/HELA2018'
#db_dir = os.path.expandvars('$HOME/chris_faster_rcnn/data/VOCdevkit2007/TT100')
db_dir = os.path.expandvars('$HOME/chris_faster_rcnn/data/VOCdevkit2007/bdci')
db_dir = '/opt/data/PASCAL_VOC/VOCdevkit2007/BDCIRPN2016'
# db_dir = '/home/zll/work/py-faster-rcnn/data/VOCdevkit2007/GOTWS11'

im_dir = os.path.join(db_dir, 'JPEGImages')
#im_ext = '.jpg'
im_ext = '.png'
anno_dir = os.path.join(db_dir, 'Annotations')
splits = ['trainval', 'test']

#RESIZE_AS_INPUT = True  # 是否因为作为frcnn输入而被resize
RAS=True
SCALE = 200 # cfg.TRAIN.SCALES[0]
MAX_SIZE = 300 # cfg.TRAIN.MAX_SIZE

bad_cnt = 0
for split in splits:
    split_txt = os.path.join(db_dir, 'ImageSets', 'Main', split+'.txt')
    fin = open(split_txt)
    im_head_list = [_.rstrip() for _ in fin.readlines()]
    fin.close()
    data = np.zeros([1000,1])
    cc = edict()
    cc.small = 0
    cc.medium = 0
    cc.large = 0
    for im_head in im_head_list:
        xml_pth = os.path.join(anno_dir, im_head+'.xml')
        tree = ET.parse(xml_pth)
        if RAS:
            # 代码从blob.py抄过来的
            im_pth = os.path.join(im_dir, im_head+im_ext)
            im = cv2.imread(im_pth)
            im_shape = im.shape
            im_size_min = np.min(im_shape[0:2])
            im_size_max = np.max(im_shape[0:2])
            im_wt, im_ht, im_dt = im.shape
            im_scale = float(SCALE) / float(im_size_min) # im_scale:相当于图像放大倍数
            # Prevent the biggest axis from being more than MAX_SIZE
            print('before: im_scale is: ', im_scale)
            if np.round(im_scale * im_size_max) > MAX_SIZE:
                im_scale = float(MAX_SIZE) / float(im_size_max)
            print('im_scale is:', im_scale)
        for obj in tree.findall('object'):
            obj_struct = {}
            bbox = obj.find('bndbox')
            x1 = int(float(bbox.find('xmin').text)+0.5)
            y1 = int(float(bbox.find('ymin').text)+0.5)
            x2 = int(float(bbox.find('xmax').text)+0.5)
            y2 = int(float(bbox.find('ymax').text)+0.5)

            if RAS:
                x1 = x1*im_scale
                y1 = y1*im_scale
                x2 = x2*im_scale
                y2 = y2*im_scale
                im_wt = im_wt * im_scale
                im_ht = im_ht * im_scale
            width = x2 - x1 + 1
            height = y2 - y1 + 1
            #if width*height<=32*32:
            if width<=32 and height<=32:
                cc.small += 1
            #elif width*height<=96*96:
            elif width<=96 and height<=96:
                cc.medium += 1
            else:
                cc.large += 1

            if RAS:
                if x1==0 or y1==0 or x1==im_wt or y1==im_ht or width<=1 or height<=1:
                    bad_cnt += 1
            else:
                if x1==0 or y1==0 or width<=1 or height<=1:
                    bad_cnt += 1

            side = int(math.sqrt(width*height))
            data[side] += 1

    tt = 0
    tot = data.sum()
    mean_size = tot / len(data)
    min_len = 600
    for i in range(min_len):
        tt += data[i]
    ratio = tt * 1.0 / tot
    ratio_str = ' ratio of <=%dpx: %f' % (min_len, ratio)
    print('total num of bbox is:', tot)

    t = 200
    #t = len(data)
    # plt.plot(range(0,t), data[0:t], label=split+ ratio_str)
    plt.plot(range(0,t), data[0:t], label=split)
    plt.xlabel(u'size')
    plt.ylabel(u'number')

    print('mean size is : ', mean_size)
    print('bad_cnt is: ', bad_cnt)
    plt.legend()
    tot = cc.small + cc.medium + cc.large
    print('small:medium:large={:d}:{:d}:{:d}={:f}%:{:f}%:{:f}%'.format(cc.small, cc.medium, cc.large, cc.small*1.0/tot, cc.medium*1.0/tot, cc.large*1.0/tot))
plt.show()

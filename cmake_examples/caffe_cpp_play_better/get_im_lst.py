#!/usr/bin/env python
# coding: utf-8

import os


im_dir = '/home/zz/data/BDCI_preliminary/JPEGImages'

fout = open('test_im.lst', 'w')
for im_name in os.listdir(im_dir):
    fout.write(im_name + '\n')
fout.close()


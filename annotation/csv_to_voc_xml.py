#!/usr/bin/env python2
# coding: utf-8

from __future__ import print_function
import os.path as osp
#import alchemy as ac
from alchemy import DetAnno, VocDetAnno, BBox
import os

def csv_to_voc_xml(csv_pth, im_dir, save_dir, cls_name='sign'):
    """
    @param csv_pth: trainval.csv
           each line of csv_pth's content is like:
               003992_6.png,11,15,21,39
               # im_name, x1, y1, x2, y2
    @param im_dir: image folder, to be prepending to each im_name,
               thus forming an abstract image path
    """

    # validate folders
    if os.path.exists(save_dir) is False:
        os.makedirs(save_dir)

    ignore_tiny_small = True
    tiny_small_size = 3

    # parse annotation information to DetAnno objects
    box_lst_dict = dict()
    fin = open(csv_pth)
    for line in fin.readlines():
        im_name, x1, y1, x2, y2 = line.rstrip().split(',')
        x1 = int(float(x1))
        y1 = int(float(y1))
        x2 = int(float(x2))
        y2 = int(float(y2))
        box = BBox(x1, y1, x2, y2, cls=cls_name)
        print('box.width={:d}, box.height={:d}'.format(box.width, box.height))
        if ignore_tiny_small:
            if box.width < tiny_small_size or box.height < tiny_small_size:
                continue
        box_lst_dict[im_name] = box_lst_dict.get(im_name, [])
        box_lst_dict[im_name].append(box)
        box_lst_dict[im_name] = box_lst_dict.get(im_name, [])
    fin.close()

    det_anno_lst = []
    for im_name, box_lst in box_lst_dict.items():
        det_anno = DetAnno(im_name, im_dir, box_lst)
        det_anno_lst.append(det_anno)


    # parse DetAnno objects to VocDetAnno Objects
    for det_anno in det_anno_lst:
        save_pth = osp.join(save_dir, det_anno.im_head+'.xml')
        print('writing to: ', save_pth)
        with open(save_pth, 'w') as fout:
            fout.write(det_anno.voc_xml)


if __name__ == '__main__':
    if 0:
        prefix = '/media/data2/zz/data/crop_rpn_data/BDCI'
        csv_pth = osp.join(prefix, 'trainval.csv')
        im_dir = osp.join(prefix, 'images')
        save_dir = osp.join(prefix, 'Annotations')
        csv_to_voc_xml(csv_pth, im_dir, save_dir)

    if 1:
        prefix = '/media/data2/zz/data/crop_rpn_data/TT100K'
        csv_pth = osp.join(prefix, 'trainval.csv')
        im_dir = osp.join(prefix, 'images')
        save_dir = osp.join(prefix, 'Annotations')
        csv_to_voc_xml(csv_pth, im_dir, save_dir)

    if 0:
        xml_pth = '/media/data2/zz/data/BDCI_preliminary/Annotations/000000.xml'
        voc_anno = VocDetAnno(xml_pth)
        print(voc_anno)

    if 0:
        im_name = '000000.png'
        im_dir = '/media/data2/zz/data/BDCI_preliminary/JPEGImages'
        box_lst = [
            BBox(10, 20, 40, 30),
            BBox(15, 30, 40, 20)
        ]
        det_anno = DetAnno(im_name, im_dir, box_lst)
        print(det_anno.voc_xml)



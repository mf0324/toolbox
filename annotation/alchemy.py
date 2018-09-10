#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function
import os.path as osp
import xml.etree.ElementTree as ET
import sys, os
from lxml.etree import Element, SubElement, tostring
from xml.dom.minidom import parseString
import cv2

def xywh2xyxy(x, y, w, h, bias):
    x2 = x + w - 1 + bias
    y2 = y + h - 1 + bias
    #return [x, y, x2, y2]
    return [x,y,x2,y2]

class BBox(object):
    """bounding box"""
    def __init__(self, x1, y1, x2, y2, cls=None, difficult=0, det_anno=None, score=1):
        """
        @param cls: class of bounding box object
        """
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.cls = cls
        self.difficult = difficult
        self.det_anno = det_anno
        self.score = score

    def translate(self, x, y):
        self.x1 += x
        self.y1 += y
        self.x2 += x
        self.y2 += y
        assert(self.x1>=0)
        assert(self.y1>=0)

    def rescale(self, ratio):
        self.x1 = max(0, int(self.x1 * ratio))
        self.y1 = max(0, int(self.y1 * ratio))
        self.x2 = int(self.x2 * ratio)
        self.y2 = int(self.y2 * ratio)

    @property
    def width(self):
        return self.x2 - self.x1 + 1

    @property
    def height(self):
        return self.y2 - self.y1 + 1

    @property
    def area(self):
        return self.width * self.height

    def uppack(self):
        return [self.x1, self.y1, self.x2, self.y2]

    def __str__(self):
        ret_str = 'score={:f}, x1={:d}, y1={:d}, x2={:d}, y2={:d}'.format(
            self.score, self.x1, self.y1, self.x2, self.y2
        )
        if self.det_anno is not None:
            ret_str = self.det_anno.im_name + ' ' + ret_str
        if self.cls is not None:
            ret_str += ', cls={:s}'.format(self.cls)
        return ret_str


class ImageAnno(object):
    def __init__(self, im_name, im_dir):
        self.im_name = im_name
        self.im_dir = im_dir

    @property
    def im_pth(self):
        return osp.join(self.im_dir, self.im_name)

    @property
    def im_head(self):
        return '.'.join(self.im_name.split('.')[:-1])

    @property
    def im_ext(self):
        return self.im_name.split('.')[-1]

    def __str__(self):
        str_content_lst = [
            'im_name: {:s}'.format(self.im_name),
            'im_dir: {:s}'.format(self.im_dir)
        ]
        ret_str = '\n'.join(str_content_lst)
        return ret_str


class DetAnno(ImageAnno):
    """Detection Annotation of one image. Including image name, path, GT boxes, etc"""
    def __init__(self, im_name, im_dir, box_lst=[], im=None):
        """
        @param im_name: image's name. e.g. lena.jpg
        @param im_dir:  folder that contains this image. can be relative or abstract directory path
        @param box_lst: list of BBox objects.
        @param im: nd-array type, opencv read image. can be empty ('')
        """
        self.im_name = im_name
        self.im_dir = im_dir
        self.box_lst = box_lst
        self.im = im
        for box in self.box_lst:
            box.det_anno = self

    def __str__(self):
        str_content_lst = [
            'im_name: {:s}'.format(self.im_name),
            'im_dir: {:s}'.format(self.im_dir)
        ]
        for box in self.box_lst:
            str_content_lst.append(str(box))
        ret_str = '\n'.join(str_content_lst)
        return ret_str

    def __cmp__(self, other):
        return cmp(self.im_name, other.im_name)

    @property
    def voc_xml(self):
        """Parse detection annotation to VOC xml content string"""
        nd_root = Element('annotation')

        nd_folder = SubElement(nd_root, 'folder')
        nd_folder.text = osp.split(self.im_dir)[-1]

        nd_filename = SubElement(nd_root, 'filename')
        nd_filename.text = self.im_name

        if self.im is None:
            print('self.im_pth is:', self.im_pth)
            self.im = cv2.imread(self.im_pth)
        im_ht, im_wt, im_dt = self.im.shape

        nd_size = SubElement(nd_root, 'size')
        nd_width = SubElement(nd_size, 'width')
        nd_width.text = str(im_wt)

        nd_height = SubElement(nd_size, 'height')
        nd_height.text = str(im_ht)

        nd_depth = SubElement(nd_size, 'depth')
        nd_depth.text = str(im_dt) # assume being 3

        for box in self.box_lst:
            nd_object = SubElement(nd_root, 'object')
            nd_name = SubElement(nd_object, 'name')
            if box.cls is not None:
                nd_name.text = box.cls
            else:
                nd_name.text = 'object'

            nd_difficult = SubElement(nd_object, 'difficult')
            nd_difficult.text = str(box.difficult)

            # It's important to add 1 to each of [x1, y1, x2, y2]
            # Since VOC XML is 1-begin-indexed
            nd_bndbox = SubElement(nd_object, 'bndbox')
            nd_xmin = SubElement(nd_bndbox, 'xmin')
            nd_xmin.text = str(box.x1+1)
            nd_ymin = SubElement(nd_bndbox, 'ymin')
            nd_ymin.text = str(box.y1+1)
            nd_xmax = SubElement(nd_bndbox, 'xmax')
            nd_xmax.text = str(box.x2+1)
            nd_ymax = SubElement(nd_bndbox, 'ymax')
            nd_ymax.text = str(box.y2+1)

        xml_str = tostring(nd_root, pretty_print=True)
        return xml_str


class VocDetAnno(DetAnno):
    """Describes an PASCAL VOC annotation"""
    def __init__(self, im_name, im_dir, box_lst):
        super(VocDetAnno, self).__init__(im_name, im_dir, box_lst)

    def __init__(self, xml_pth):
        # parse xml
        tree = ET.parse(xml_pth)
        self.im_name = tree.find('filename').text
        self.im_width = tree.find('size').find('width').text
        self.im_height = tree.find('size').find('height').text
        self.box_lst = []

        for obj in tree.findall('object'):
            obj_struct = {}
            bbox = obj.find('bndbox')
            x1 = int(float(bbox.find('xmin').text))
            y1 = int(float(bbox.find('ymin').text))
            x2 = int(float(bbox.find('xmax').text))
            y2 = int(float(bbox.find('ymax').text))
            cls_name = obj.find('name').text
            difficult = obj.find('difficult').text
            self.box_lst.append(BBox(x1, y1, x2, y2, cls_name))


class WeboxAnno(ImageAnno):
    """WeBox Annotations. Using the GT Boxes as weak edges and label them in an label image"""
    def __init__(self, im, im_name, im_dir, label, label_name, label_dir, box_lst):
        """
        @param im_name: image name
        @param im_dir: folder of im_name
        @param box_lst: list of annotated boxes. each box is type of BBox
        """
        self.im = im
        self.im_name = im_name
        self.im_dir = im_dir

        self.label = label
        self.label_name = label_name
        self.label_dir = label_dir

        self.box_lst = box_lst

    @property
    def label_pth(self):
        return osp.join(self.label_dir, self.label_name)

    def __str__(self):
        str_content_lst = [
            'im_name: {:s}'.format(self.im_name),
            'im_dir: {:s}'.format(self.im_dir),
            'label_name: {:s}'.format(self.label_name),
            'label_dir: {:s}'.format(self.label_dir)
        ]
        for box in self.box_lst:
            str_content_lst.append(str(box))
        ret_str = '\n'.join(str_content_lst)
        return ret_str


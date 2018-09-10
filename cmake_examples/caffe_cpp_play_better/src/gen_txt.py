import os
import os.path as osp


im_dir = '/home/zz/data/VOC/VOCdevkit2007/VOC2007/JPEGImages'

fin = open('/home/zz/data/VOC/train.txt')
fout = open('test.txt', 'w')

for line in fin.readlines():
    im_name = line.rstrip('\n')
    im_pth = osp.join(im_dir, im_name) + '.jpg'
    fout.write(im_pth+'\n')

fout.close()

print('\nDone')

import os
import glob
import cv2
import json

from coords import toInt
from dataset import *

dataset_path = 'dataset_actual/'

image_filenames = get_image_filenames(dataset_path)
annotation_filenames = get_annotation_filenames(image_filenames)
color_map = get_colors(dataset_path)

print('Imgs found: ' + str(len(image_filenames)))

for img_fname, ann_fname in zip(image_filenames, annotation_filenames):
    with open(ann_fname) as f:
        img = cv2.imread(img_fname)
        for obj in json.load(f)['objects']:
            class_title = obj['classTitle']
            pts = obj['points']['exterior']
            pts = [tuple(toInt(pt)) for pt in pts]
            class_color = color_map[class_title]
            cv2.rectangle(img, pts[0], pts[1], class_color)
            cv2.putText(img, class_title, pts[0], cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255))
        cv2.imshow('img', img)
        if cv2.waitKey(0) == 27:
            exit()
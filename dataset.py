import glob
import json
import os

from color_conversions import *

def get_image_filenames(dataset_path):
    return [f for f in glob.glob(dataset_path + "ds*/img/*.png")]

def get_annotation_filenames(image_filenames):
    return [f.replace('img', 'ann') + '.json' for f in image_filenames]

def get_colors(dataset_path):
    color_map = {}
    meta_path = os.path.join(dataset_path, 'meta.json')
    with open(meta_path) as f:
        for class_ in json.load(f)['classes']:
            color_map[class_['title']] = rgb_to_bgr(hex_to_rgb(class_['color']))
    
    return color_map
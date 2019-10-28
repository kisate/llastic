import tensorflow as tf
import cv2
from coords import toInt

from object_detection.utils import dataset_util

flags = tf.app.flags
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
FLAGS = flags.FLAGS

def create_tf_example(imgpath):
    class_map = {
        'Balka': 1,
        'Hren': 2,
        'N-ka': 3,
        'OS': 4,
        'Shesternya': 5,
        'Shtift': 6,
        'Ugol_balka': 7
    }

    annpath = imgpath.replace('img', 'ann') + '.json'
    height = 480 # Image height
    width = 640 # Image width

    with tf.gfile.GFile(imgpath, 'rb') as fid:
        encoded_jpg = fid.read()

    encoded_image_data = encoded_jpg # Encoded image bytes
    image_format = b'png' # b'jpeg' or b'png'

    xmins = [] # List of normalized left x coordinates in bounding box (1 per box)
    xmaxs = [] # List of normalized right x coordinates in bounding box
                # (1 per box)
    ymins = [] # List of normalized top y coordinates in bounding box (1 per box)
    ymaxs = [] # List of normalized bottom y coordinates in bounding box
                # (1 per box)
    classes_text = [] # List of string class name of bounding box (1 per box)
    classes = [] # List of integer class id of bounding box (1 per box)
    
    with open(annpath, 'r') as annotaion_file:
        for obj in json.load(annotaion_file)['objects']:
            class_title = obj['classTitle']
            pts = obj['points']['exterior']
            pts = [tuple(toInt(pt)) for pt in pts]

            xmins.append(pts[0][0] / width)
            xmaxs.append(pts[1][0] / width)
            ymins.append(pts[0][1] / height)
            ymaxs.append(pts[1][1] / height)

            classes.append(class_map[class_title])
            classes_text.append(class_title)

    print(xmins, xmaxs, ymins, ymaxs, image_format, height, width, imgpath, classes, classes_text)
    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(bytes(os.path.basename(imgpath), 'utf-8')),
        'image/source_id': dataset_util.bytes_feature(bytes(os.path.basename(imgpath), 'utf-8')),
        'image/encoded': dataset_util.bytes_feature(encoded_image_data),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature([bytes(x, 'utf-8') for x in classes_text]),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))
    return tf_example

import os
from dataset import *
import json

def main(_):
    dataset_path = 'dataset_actual/'
    writer_train = tf.python_io.TFRecordWriter(os.path.join(dataset_path, 'dataset_train.record'))
    writer_eval = tf.python_io.TFRecordWriter(os.path.join(dataset_path, 'dataset_eval.record'))

    image_filenames = get_image_filenames(dataset_path)
    color_map = get_colors(dataset_path)

    cnt = 0
    for img_fname in image_filenames:
        example = create_tf_example(img_fname)
        if example is not None:
            if cnt % 5 == 0:
                writer_eval.write(example.SerializeToString())
            else:
                writer_train.write(example.SerializeToString())
            cnt+=1
    print(cnt)
    writer_train.close()
    writer_eval.close()

if __name__ == '__main__':
    tf.app.run()
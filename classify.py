import tensorflow as tf
import numpy as np

# Tensorflow model wrapper
# TODO: move to cv2.dnn module
class Classifier(object):
    def __init__(self):
        PATH_TO_MODEL = r'/home/tlab/repos/lastic/inference_graphs/frozen_inference_graph.pb'
        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(PATH_TO_MODEL, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
            self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
            self.d_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
            self.d_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
            self.d_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
            self.num_d = self.detection_graph.get_tensor_by_name('num_detections:0')
        self.sess = tf.Session(graph=self.detection_graph)

    def get_classification(self, img):
        with self.detection_graph.as_default():
            img_expanded = np.expand_dims(img, axis=0)  
            (boxes, scores, classes, num) = self.sess.run(
                [self.d_boxes, self.d_scores,    self.d_classes, self.num_d],
                feed_dict={self.image_tensor: img_expanded})
        return boxes, scores, classes, num

from dataset import get_image_filenames, get_colors
from coords import mul, toInt, split, diff
import cv2

nn = Classifier()
dataset_path = 'dataset_actual/'
color_map = get_colors(dataset_path)
name_map = {
    1: 'Balka',
    2: 'Fiks',
    3: 'N-ka',
    4: 'OS',
    5: 'Shesternya',
    6: 'Shtift',
    7: 'Ugol_balka'
}

# for image_filename in get_image_filenames(dataset_path):
    # img = cv2.imread(image_filename)
# cap = cv2.VideoCapture(1)
#  while True:
#     ok, img = cap.read()
#     boxes, scores, classes, num = nn.get_classification(img)
#     for box, score, class_num in zip(boxes[0], scores[0], classes[0]):
#         class_num = int(class_num)
#         class_name = name_map[class_num]
#         color = color_map[class_name]
        
#         if score > 0.5:
#             pt1, pt2 = split(box)
#             pt1 = pt1[::-1]
#             pt1 = mul(pt1, 640, 480) # cast normalized coords to image size
#             pt1 = toInt(pt1)
#             pt2 = pt2[::-1]
#             pt2 = mul(pt2, 640, 480) # cast normalized coords to image size
#             pt2 = toInt(pt2)

#             cv2.rectangle(img, pt1, pt2, color)
#             cv2.putText(img, class_name, pt1, cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)
#             cv2.putText(img, str(score), diff((0, 20), pt1), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)
    
#     cv2.imshow('img', img)
#     cv2.waitKey(1)
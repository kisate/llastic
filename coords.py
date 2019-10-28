# 2d coord operations

from math import sqrt

# pt2 - pt1
def diff(pt1, pt2):
    return pt2[0] - pt1[0], pt2[1] - pt1[1]

def add(pt1, pt2):
    return pt1[0] + pt2[0], pt1[1] + pt2[1]

# (pt2 + pt1) // 2
def avg(pt1, pt2):
    return (pt2[0] + pt1[0]) // 2, (pt2[1] + pt1[1]) // 2

# distance between two pts
def dist(pt1, pt2):
    d = diff(pt1, pt2)
    return sqrt(d[0] * d[0] + d[1] * d[1])

# * const
def mul(pt, n1, n2):
    return (pt[0] * n1, pt[1] * n2)

def split(arr):
    return (arr[0], arr[1]), (arr[2], arr[3])

# implicit casting to integer
def toInt(pt):
    return tuple([int(x) for x in pt])

def from_cv2_to_mm_centered(pt, width, height):
    pix_to_mm = 0   
    return [(pt[0] - width/2)*pix_to_mm, (pt[1] - height/2)*pix_to_mm]
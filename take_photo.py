#takes pictures for a dataset

import cv2
import os

cnt = 0
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 20)

while True:
    ok, frame = cap.read()
    if ok:
        cv2.imshow('frame', frame)
        k = cv2.waitKey(1)
        
        if k == 27:
            exit()

        if k == ord('a'):
            cnt += 1
            path = "dataset/pics/" + str(cnt) + '.png'
            while os.path.isfile(path):
                cnt += 1
                path = "dataset/pics/" + str(cnt) + '.png'

            print(path)
            if not cv2.imwrite(path, frame):
                print("couldn't save the image, but do i ever give a fuck about trying to fix it")
                cnt -= 1
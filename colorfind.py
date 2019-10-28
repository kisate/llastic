# -*- coding: utf-8 -*-

'''
Color-based object detection in python
Created by Maxim Mikhaylov, 2018
'''

import cv2
import numpy as np
from coords import toInt, add
from sys import argv

def pick_color(event,x,y,flags,param):
	if event == 0:
		global img
		print(cv2.cvtColor(img, cv2.COLOR_BGR2HSV)[y][x])
		color = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)[y][x]
		colorMat = np.full((200, 200, 3), color)
		cv2.imshow("color", cv2.cvtColor(colorMat, cv2.COLOR_HSV2BGR))

def nothing(x):
    pass

def loadScalars(filename):
	if filename == None:
		return ((0, 0, 0), (0, 0, 0))
	f = open(filename, 'r')
	scalars = []
	for line in f:
		scalars.append(tuple([int(s) for s in line.split()]))
	return tuple(scalars)

def colorfind(img, lowerBound, upperBound, lowerBound2=None, upperBound2=None, drawPos=False, showMask=False, threshold=1):
	'''
	Находит в изображении img объект на основе его цвета. 
	
	Цвет задается границами lowerBound и upperBound.
	
	lowerBound2 и upperBound2 используются в случае, если искомый цвет - красный, т.к. он "обворачивается" вокруг HSV кольца.
	
	drawPos - рисует круг, где находится объект и показывает результируеще изображение.
	
	threshold - число пикселей искомого цвета, при котором считается, что объект есть в изображении.
	
	Если искомых пикселей меньше чем threshold, то возвращается (-1, -1). 
	
	Иначе - кортеж из координат объекта.
	'''

	# Перевод изображения в HSV
	imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	# Создание бинарного изображения - маски, где пиксель имеет значение 1, 
	# если на его месте в оригинальном изображении пискель цвета между upperBound и lowerBound
	mask = cv2.inRange(imgHSV, lowerBound, upperBound)
	# Дополнительная фильтрация, если использются две пары границ
	if lowerBound2 is not None and upperBound2 is not None:
		mask += cv2.inRange(imgHSV, lowerBound2, upperBound2)

	# Удаление отдельно стоящих точек из маски
	# mask = cv2.erode(mask, np.ones((2,2)), iterations=1)
	# mask = cv2.dilate(mask, np.ones((2,2)), iterations=1)
	# mask = cv2.dilate(mask, np.ones((5,5)), iterations=1)
	# mask = cv2.erode(mask, np.ones((5,5)), iterations=1)

	# Создание моментов
	moments = cv2.moments(mask)

	# Нахождение координат объекта
	if moments['m00'] < threshold:
		return (-1, -1, np.zeros_like(mask))	
	cx = int(moments['m10'] / moments['m00'])
	cy = int(moments['m01'] / moments['m00'])

	if showMask:
		cv2.imshow("mask", mask)
		cv2.waitKey(1)

	if drawPos:
		cv2.circle(img, (cx, cy), 10, (0,0,255), 3)
		cv2.imshow("img", img)
		cv2.waitKey(1)
	
	return (cx, cy, mask)

# a wrapper on cv2.connectedComponents
def connComps(mask, minArea=0, connectivity=8, leftEdge=0, rightEdge=np.inf):
	# mask = cv2.GaussianBlur(mask, (7, 7), 0, 0)
	num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity)
	
	rects = []
	areas = []
	goodCentroids = []
	
	for stat, centroid in zip(stats, centroids):
		if stat[4] < minArea:
			continue
		if stat[2] == mask.shape[1] or stat[3] == mask.shape[0]:
			continue
		if centroid[0] < leftEdge or centroid[0] > rightEdge:
			continue
		cv2.circle(mask, toInt(centroid), 3, (255, 255, 255))
		cv2.putText(mask, str(stat[4]), toInt(centroid), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
		rects.append(list(stat[:4]))
		areas.append(stat[4])
		goodCentroids.append(toInt(centroid))
	
	zipped = zip(rects, areas, goodCentroids)
	zipped = sorted(zipped, key = lambda t: -t[1])
	return list(zipped)

if __name__ == "__main__":
	cap = cv2.VideoCapture(0)
	cap.set(5, 20)
	
	if len(argv) < 2:
		argv.append(None)
	res = loadScalars(argv[1])

	# Трэкбары для управления границамии
	cv2.namedWindow("img")
	cv2.createTrackbar("H1", "img", res[0][0], 180, nothing)
	cv2.createTrackbar("S1", "img", res[0][1], 255, nothing)
	cv2.createTrackbar("V1", "img", res[0][2], 255, nothing)
	cv2.createTrackbar("H2", "img", res[1][0], 180, nothing)
	cv2.createTrackbar("S2", "img", res[1][1], 255, nothing)
	cv2.createTrackbar("V2", "img", res[1][2], 255, nothing)

	# cv2.setMouseCallback("img", pick_color)

	while True:
		# Считывание изображения с камеры
		a, img = cap.read()
		
		# Считывание данных с трекбаров
		lowerBound = (
			cv2.getTrackbarPos('H1', 'img'),
			cv2.getTrackbarPos('S1', 'img'),
			cv2.getTrackbarPos('V1', 'img')
		)
		
		upperBound = (
			cv2.getTrackbarPos('H2', 'img'),
			cv2.getTrackbarPos('S2', 'img'),
			cv2.getTrackbarPos('V2', 'img')
		)

		x,y,mask = colorfind(img, lowerBound, upperBound, drawPos=True, showMask=True, threshold=10000)
		comps = connComps(mask, minArea=10)
		for comp in comps:
			rect = comp[0]
			rectLeftPt = (rect[0], rect[1])
			rectRightPt = add(rectLeftPt, (rect[2], rect[3]))
			cv2.rectangle(img, rectLeftPt, rectRightPt, color=(128,128,0), thickness=2)
		""" if x != -1:
			num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask, 8)
			for label, stat, centroid in zip(labels, stats, centroids):
				centroid = [int(x) for x in centroid]
				if stat[2] > 20 and stat[3] > 20 and stat[2] < 640:
					# print(stat, centroid)
					cv2.rectangle(img, (stat[0], stat[1]), (stat[0]+stat[2], stat[1]+stat[3]), color=(128,128,0))
				# cv2.circle(img, tuple(centroid), 20, color=(128,128,0), thickness=3) """
		cv2.imshow("rofl", img)
		key = cv2.waitKey(1)
		# Выход из программы по нажатию esc
		if key == 27:
			exit()
		# Сохранение скаляров
		if key > 0:
			print("where to save the scalars?")
			print("the path must be in '  ' ")
			savepath = str(input())
			f = open(savepath, 'w')
			f.write(' '.join(str(e) for e in lowerBound) + '\n')
			f.write(' '.join(str(e) for e in upperBound))
			f.close()
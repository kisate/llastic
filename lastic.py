import cv2
# from cv2 import cv2
import numpy as np
from coords import diff, avg, dist
from sys import argv
import math
import time
import sender
import socket, threading
import pickle 
from mailbox import Client, MessageHandler
from colorfind import colorfind, loadScalars, connComps
from sys import argv
from coords import avg ,mul, toInt, split, diff, from_cv2_to_mm_centered
from classify import Classifier

cap = cv2.VideoCapture(1)
cap2 = cv2.VideoCapture(2)
host = '192.168.43.83'
port = 6164 # fix number
msg = [0]
n = 0
stop_event = threading.Event()
# cap.set(cv2.CAP_PROP_POS_MSEC, 15000)
nn = Classifier()

def nothing(x):
    return x 

def sign(x):
	if x > 0:
		return 1.
	elif x < 0:
		return -1.
	elif x == 0:
		return 0.
	else:
		return x

def determinant(x1, y1, x2, y2):
	d = x1*y2 - x2*y1
	return d

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def get_side(x1,y1,x2,y2,xc,yc):

	# if ((x2-x1) != 0) :
	# 	y_predict = (xc-x1)*(y2-y1)/(x2-x1)+y1
	# else:
	# 	return 0

	# print((y_predict-yc))
	# return (sign(y_predict-yc))

	d = determinant(x2-x1, y2- y1, xc - x2, yc - y2)
	print (d)

	return (-sign(d))

def collect_part(coords):
	return

def send_next_step(step):
	pass

def wait_for_answer():
	time.sleep(1)

def make_next_step(step):
	return step

def image_coords_to_real(coords):
	length = 0
	shift = [0, 0]
	center = [(coords[0][0]+coords[1][0])/2 + shift[0], (coords[0][1]+coords[1][1])/2 + shift[1]]
	radius = math.sqrt(center[1]**2 + length**2)
	angle = math.atan(center[0]/(center[1]+length))
	return [radius, angle]

def get_classifications(image, width, height):
	global nn
	
	boxes, scores, classes, num_classes = nn.get_classification(image)
	
	classifications = []
	for index in range(int(num_classes[0])):
		if (scores[0][index] > 0.9):
			box = boxes[0][index]
			classID = int(classes[0][index])

			pt1, pt2 = split(box)
			pt1 = pt1[::-1]
			pt1 = mul(pt1, width, height) # cast normalized coords to image size
			pt1 = toInt(pt1)
			pt2 = pt2[::-1]
			pt2 = mul(pt2, width, height) # cast normalized coords to image size
			pt2 = toInt(pt2)
			classifications.append({'id' : classID, 'points' : [pt1, pt2]})
	return classifications

def lampa_thread(cap, event:threading.Event):
	cur_step = 0
	width, height = 301, 226

	while not event.is_set():
		_, frame = cap.read()
		objects = get_classifications(frame, width, height)
		if objects:
			part = objects[0]
			points = [from_cv2_to_mm_centered(pt, width, height) for pt in part['points']]
			coords = image_coords_to_real(points)
			collect_part(coords)
			wait_for_answer()
		else:
			cur_step = make_next_step(cur_step)
			send_next_step(cur_step)
			wait_for_answer()


if __name__ == "__main__":
	# don't use the robot if anything is passed as arg
	if len(argv) == 1:
		useRobot = True
	else:
		useRobot = False

	if useRobot:
		client = Client(host,port)
		messagehandler = sender.MyMessageHandler()
		print("connecting")
		client.connect(messagehandler)
		print("connected")
	n12 = 0

	threading.Thread(target=lampa_thread, args=(cap2,)).start()

	while True:
		time.sleep(0.05)
		_, img = cap.read()

		# load all color bounds
		yellowBounds = loadScalars('colors/yellow') # ([19,145,68], [59,255,255])
		blueBounds = loadScalars('colors/blue') # ([104,95,14], [117,255,255])
		greenBounds = loadScalars('colors/green') # ([73, 34, 123], [100, 131, 156])

		coords = []
		masks = []
		x1 = 230
		x2 = 550
		# get masks
		#[y : 0 + 480, x : x1 + (x1 - x2)]
		img = img[0 : 480, x1 : x2]
		for bounds in [yellowBounds, blueBounds, greenBounds]:
			x, y, mask = colorfind(img, bounds[0], bounds[1], drawPos=False, showMask=False, threshold=1)
			# coords.append((x, y))
			masks.append(mask)

		# find connected components in the masks
		for mask in masks:
			comps = connComps(mask, minArea=40, rightEdge=450)
			if len(comps) != 0:
				coords.append(comps[0][2])
			else:
				coords.append((-1, -1))

		# for cleaner access
		yellow_coord = coords[0]
		blue_coord = coords[1]
		if n12 == 0:
			green_coord = coords[2]
		robot_coord = avg(yellow_coord, blue_coord)
		robot_direction = diff(yellow_coord, blue_coord)

		mask = np.zeros((img.shape[0], img.shape[1]), np.uint8)
		mask += sum(masks)
		for idx, _mask in enumerate(masks):
			cv2.imshow("mask" + str(idx), cv2.bitwise_and(img, img, mask=_mask))
		cv2.imshow("mask", mask)
  
		if yellow_coord == (-1, -1) or blue_coord == (-1, -1):
			print('robot not found')
			if useRobot:
				client.send(0)
			print("STOP")
			cv2.imshow("img", img)
			cv2.waitKey(1)
			continue

		cv2.arrowedLine(img, yellow_coord, blue_coord, (0,0,255), 2)
		#cv2.arrowedLine(img, (x1, 0), (x1, 480), (250,250,0), 2)
		#cv2.arrowedLine(img, (x2, 0), (x2, 480), (250,250,0), 2)
		cv2.circle(img, robot_coord, 3, (0,0,255), 3)
		cv2.putText(img, "robot", robot_coord, cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255))
		cv2.arrowedLine(img, robot_coord, green_coord, (0,255,0), 2)
		
		cv2.imshow("img", img)
		k = cv2.waitKey(1) & 0xFF
		if k != ord('f') and n12 == 0:
			continue
		elif n12 == 0:
			green_coord = (green_coord[0], green_coord[1] - 20)
			n12 = 1
		key = cv2.waitKey(1)
		if green_coord != (-1, -1):
			# angle between robot direction and its' direction towards the green thing
			angle = angle_between(robot_direction, diff(robot_coord, green_coord))
			side = get_side(yellow_coord[0],yellow_coord[1],blue_coord[0],blue_coord[1],green_coord[0],green_coord[1])

			print("%.2f" % (angle))
			print("%.1f" % (side))

			# wiper rotation
			if dist(robot_coord, green_coord) < 70:
				if useRobot:
					client.send(254)
					print('start rotating')
			else:
				if useRobot:
					client.send(255)
            
			sendval = 0
			if side > 0:
				if angle > 0.01:
					sendval = 2 # left direction
					sendval += 4 * int(angle * 45) # angle for rotation
					print("GO_Left")
				else:
					sendval = 3 # forward
					print("GO")
			elif side < 0:
				if angle > 0.01:
					sendval = 1 # right direction
					sendval += 4 * int(angle * 45) # angle for rotation
					print("GO_Right")
				else:
					sendval = 3 # forward
					print("GO")
			elif (side == 0):
				n+=1
				print(n)
				# print("ДЕЛЕНИЕ НА НОЛЬ")
		else:
			print('target not found')
			sendval = 0
			print("STOP")
		if useRobot:
			client.send(sendval)
		# Выход из программы по нажатию esc
		if key == 27:
			stop_event.set()
			cv2.destroyAllWindows()
			cap.release()
			cap2.release()
			exit()
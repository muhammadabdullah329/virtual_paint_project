import cv2
import numpy as np

#for webcam
cap = cv2.VideoCapture(0)
cap.set(3,1920)	#width
cap.set(4,1080)	#height
cap.set(10,150)	#brightness

#HSV min and max values define color
myColors = [11,140,139,27,255,255]

mypoints = []

def findColor(img,color):
	newPoints=[]
	imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	lower = np.array(color[:3])
	upper = np.array(color[3:6])
	mask = cv2.inRange(imgHSV,lower,upper)
	x,y = getContours(mask)
	cv2.circle(imgResult,(x,y),10,(51,153,255),cv2.FILLED)
	if x!=0 and y!=0:
		newPoints.append([x,y])
	return [x,y]
	#cv2.imshow("img",mask)

def getContours(img):
	x,y, w, h= 0,0,0,0
	contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
	
	for cnt in contours:
		area = cv2.contourArea(cnt)
		if area>500:
				cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
				perimeter = cv2.arcLength(cnt,True)
				approx = cv2.approxPolyDP(cnt,0.02*perimeter,True)
				x, y, w, h = cv2.boundingRect(approx)
	return x+w//2,y+h//2

def drawOnCanvas(points):
	for point in points:
		cv2.circle(imgResult,(point[0],point[1]),10,(51,153,255),cv2.FILLED)


while True:
	success, img = cap.read()
	img = cv2.flip(img,1)
	img = cv2.resize(img, (1280,720))
	imgResult=img.copy()
	points = findColor(img,myColors)
	if len(points) !=0:
		mypoints.append(points)
		
	if len(mypoints)!=0:
		drawOnCanvas(mypoints)
	cv2.imshow("Video",imgResult)
	if cv2.waitKey(1) & 0xFF ==ord('q'):
		break
	
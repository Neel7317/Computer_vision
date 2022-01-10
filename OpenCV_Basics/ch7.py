##color detection using cv2...

import cv2
import numpy as np

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver



def empty(a):
    pass
# crete tackbar
cv2.namedWindow("Tracker")
cv2.resizeWindow("Tracker",640,400)
cv2.createTrackbar("Hue min","Tracker",2,179,empty)
cv2.createTrackbar("Hue max","Tracker",9,179,empty)
cv2.createTrackbar("Set min","Tracker",22,255,empty)
cv2.createTrackbar("Set max","Tracker",198,255,empty)
cv2.createTrackbar("val min","Tracker",153,255,empty)
cv2.createTrackbar("val max","Tracker",255,255,empty)

while True:
    img=cv2.imread('resources/images.jpg')

    img2=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    h_min=cv2.getTrackbarPos("Hue min","Tracker")
    h_max=cv2.getTrackbarPos("Hue max","Tracker")
    s_min=cv2.getTrackbarPos("Set min","Tracker")
    s_max=cv2.getTrackbarPos("Set max","Tracker")
    v_min=cv2.getTrackbarPos("val min","Tracker")
    v_max=cv2.getTrackbarPos("val max","Tracker")
    #print(h_min,h_max,s_min,s_max,v_min,v_max)
    lower=np.array([h_min,s_min,v_min])
    upper=np.array([h_max,s_max,v_max])
    mask=cv2.inRange(img2,lower,upper)
    result=cv2.bitwise_and(img,img,mask=mask)
    """cv2.imshow("original",img)
    cv2.imshow("original2",img2)
    cv2.imshow("Mask",mask)
    cv2.imshow("Result",result)"""

    stackimg=stackImages(1,[img,img2,mask,result])
    cv2.imshow("stacked images",stackimg)
    cv2.waitKey(1)
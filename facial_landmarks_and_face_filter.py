# -*- coding: utf-8 -*-
"""Facial Landmarks and Face Filter.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oomEWm6fM19RNQzXPytxcWKr56FpbJt2

# **Initialization**
"""

import cv2
import numpy as np
import dlib
import matplotlib.pyplot as plt

"""# **Read Image file**"""

img = cv2.imread('/content/sample_data/superman-face.jpg')
img = cv2.resize(img, (0,0), None, 0.5, 0.5)
imgOriginal = img.copy()

plt.imshow(imgOriginal)
plt.show()

"""# **Face Detection**"""

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("/content/sample_data/shape_predictor_68_face_landmarks.dat")
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = detector(imgGray)

for face in faces:
  x1,y1 = face.left(), face.top()
  x2,y2 = face.right(), face.bottom()
  imgOriginal = cv2.rectangle(img, (x1,y1), (x2,y2), (0,255,0),2)
  landmarks = predictor(imgGray, face)
  myPoints = []

  for n in range(68):
    x = landmarks.part(n).x
    y = landmarks.part(n).y
    myPoints.append([x,y])
    #cv2.circle(imgOriginal, (x,y),5,(50,50,255), cv2.FILLED)
    #cv2.putText(imgOriginal, str(n), (x,y-10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (0,0,255), 1)
  print(myPoints)

plt.imshow(imgOriginal)
plt.show()

def createBox(img, points, scale=5, masked=False, cropped = True):

  if(masked):
    mask = np.zeros_like(img)
    mask = cv2.fillPoly(mask, [points], (255,255,255)) 
    img = cv2.bitwise_and(img, mask)  
  if(cropped):
    bbox = cv2.boundingRect(points)
    x,y,w,h = bbox
    imgCrop = img[y: y+h, x: x+w]
    imgCrop = cv2.resize(imgCrop, (0,0), None, scale, scale)
    return imgCrop
  else:
    return mask

#left eye crop

myPoints = np.array(myPoints)
imgLeftEye = createBox(img, myPoints[36:42])
plt.imshow(imgLeftEye)
plt.show()

#right eye crop

myPoints = np.array(myPoints)
imgRightEye = createBox(img, myPoints[42:48])
plt.imshow(imgRightEye)
plt.show()

#crop eyes
imgLips = createBox(img, myPoints[36:48],3, masked=True,cropped=False)
plt.imshow(imgLips)
plt.show()

#color for lips
imgColorLips = np.zeros_like(imgLips)
imgColorLips[:] = 255,0,0
plt.imshow(imgColorLips)
plt.show()

#bitwise and operation for coloring the lip region
imgColorLips = cv2.bitwise_and(imgLips, imgColorLips)
plt.imshow(imgColorLips)
plt.show()

#merging original image and the colored lip region

imgColorLips = cv2.GaussianBlur(imgColorLips, (7,7), 10)
imgOriginalGray = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2GRAY)
imgOriginalGray = cv2.cvtColor(imgOriginalGray, cv2.COLOR_GRAY2BGR)
imgColorLips = cv2.addWeighted(imgOriginalGray,1,imgColorLips, 0.4,0)
plt.imshow(imgColorLips)
plt.show()


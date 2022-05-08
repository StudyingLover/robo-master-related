# -*- coding: utf-8 -*-
"""
Created on Sun May  8 18:44:38 2022

@author: Ni Jingzhe
"""

import cv2
import numpy as np

def nothing(x):
    pass
#通过Opencv读取图片信息
#src = cv2.imread('image.jpg')
img = cv2.imread('red1.png')
rows,cols,channels = img.shape
cv2.namedWindow('img2',1)
#cv2.resizeWindow("img2", 1000, 400) #创建一个500*500大小的窗口

# 创建6个滑条用来操作HSV3个分量的上下截取界限
cv2.createTrackbar('Hlow','img2',62,180,nothing)
cv2.createTrackbar('Hup','img2',99,180,nothing)
cv2.createTrackbar('Slow','img2',198,255,nothing)
cv2.createTrackbar('Sup','img2',255,255,nothing)
cv2.createTrackbar('Vlow','img2',150,255,nothing)
cv2.createTrackbar('Vup','img2',255,255,nothing)

# lower_red = np.array([55,30,30])
# upper_red = np.array([99,255,255])
img_gsb = cv2.GaussianBlur(img, (7, 7), 0)
hsv = cv2.cvtColor(img_gsb, cv2.COLOR_BGR2HSV)
while(1):
    # mask = cv2.inRange(hsv, lower_red, upper_red)
    #将制定像素点的数据设置为0, 要注意的是这三个参数对应的值是Blue, Green, Red。
    hlow = cv2.getTrackbarPos('Hlow', 'img2')
    hup = cv2.getTrackbarPos('Hup', 'img2')
    slow = cv2.getTrackbarPos('Slow', 'img2')
    sup = cv2.getTrackbarPos('Sup', 'img2')
    vlow = cv2.getTrackbarPos('Vlow', 'img2')
    vup = cv2.getTrackbarPos('Vup', 'img2')
    lower_red = np.array([hlow, slow, vlow])
    upper_red = np.array([hup, sup, vup])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    img2 = cv2.bitwise_and(img_gsb, img_gsb, mask=mask)

   # cv2.imshow("src", src)
    cv2.imshow("img2", img2)
    k = cv2.waitKey(1)&0xFF
    if k == 27: #esc exit
        break
#cv2.waitKey(0)
cv2.destroyAllWindows()

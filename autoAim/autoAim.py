# -*- coding: utf-8 -*-
"""
Created on Wed May  4 23:50:12 2022

@author: Ni Jingzhe
"""

import cv2
import numpy as np

#input img
img = cv2.imread("red1.png")

#高斯模糊降噪
img_gsb = cv2.GaussianBlur(img, (7, 7), 0)
cv2.imshow("img_gsb", img_gsb.copy())
cv2.waitKey(0)
#转hsv色彩模式
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
cv2.imshow("img_hsv", img_hsv.copy())
cv2.waitKey(0)
#设置红色hsv参数范围，用inRange输出保留红色的二值化图像
#三个参数依次是h,s,v
lower_red = np.array([0, 210, 210])  
upper_red = np.array([180, 255, 255])
inRange_hsv = cv2.inRange(img_hsv, lower_red, upper_red)
cv2.imshow("inRange_hsv", inRange_hsv.copy())
cv2.waitKey(0)
#找轮廓
cnts, h = cv2.findContours(inRange_hsv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# loop over the contours
draw_img = img.copy()
cnts_data = []
for c in cnts:
    # compute the center of the contour
    M = cv2.moments(c)
    S = int(M["m00"])
    C = int(cv2.arcLength(c, True))
    cX = int(M["m10"] / (M["m00"]+0.00000001))
    cY = int(M["m01"] / (M["m00"]+0.00000001))
    cnts_data.append([S,C,cX,cY])
    # draw the contour and center of the shape on the image
    cv2.drawContours(draw_img, [c], -1, (0, 255, 0), 2)
    cv2.circle(draw_img, (cX, cY), 7, (255, 255, 255), -1)
    cv2.putText(draw_img, "center S:"+str(S)+" C:"+str(C), (cX - 20, cY - 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    # show the image
    cv2.imshow("cnts_and_center", draw_img)
    cv2.waitKey(0)


cv2.waitKey(0)
cv2.destroyAllWindows()

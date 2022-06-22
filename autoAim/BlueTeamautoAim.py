# -*- coding: utf-8 -*-
"""
Created on Wed May  4 23:50:12 2022

@author: Ni Jingzhe
"""

import cv2
import numpy as np

def count_corner(c):
    ep = 0.01*cv2.arcLength(c, True)
    ap = cv2.approxPolyDP(c, ep, True)
    corner = len(ap)
    return corner


def gamma_trans(img, gamma):
    gamma_table = [np.power(x / 255.0, gamma) * 255.0 for x in range(256)]  # 建立映射表
    gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)  # 颜色值为整数
    return cv2.LUT(img, gamma_table)  # 图片颜色查表。另外可以根据光强（颜色）均匀化原则设计自适应算法。



# input img
img = cv2.imread("frame3.jpg")
#img = cv2.imread("red1.png")
# 高斯模糊降噪
img_gsb = cv2.GaussianBlur(img, (7, 7), 0)
cv2.imshow("img_gsb", img_gsb.copy())
cv2.waitKey(0)

img_low_gamma = gamma_trans(img_gsb, 690*0.01)

b, g, r = cv2.split(img_low_gamma)
#img_sub = cv2.subtract(r, b)
img_sub = cv2.subtract(r, b)
cv2.imshow("img_sub", img_sub.copy())
cv2.waitKey(0)

ret, binary = cv2.threshold(
    img_sub, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
cv2.imshow("binary", binary.copy())
cv2.waitKey(0)

# 找轮廓
cnts, h = cv2.findContours(
    binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# loop over the contours
draw_img = img.copy()
cnts_data = []
k = 1
for c in cnts:

    # compute the center of the contour
    M = cv2.moments(c)
    S = int(M["m00"])
    C = int(cv2.arcLength(c, True))
    #if 15 > count_corner(c) > 10 and 0.07 > S / (C*C) > 0.06:
    cX = int(M["m10"] / (M["m00"]+0.00000001))
    cY = int(M["m01"] / (M["m00"]+0.00000001))
    cnts_data.append([S, C, cX, cY])
    # draw the contour and center of the shape on the image
    cv2.drawContours(draw_img, [c], -1, (0, 255, 0), 2)
    cv2.circle(draw_img, (cX, cY), 7, (255, 255, 255), -1)
    cv2.putText(draw_img, "center S:"+str(S)+" C:"+str(C), (cX - 100, cY - 20*k),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    # show the image
    cv2.imshow("cnts_and_center", draw_img)
    cv2.waitKey(0)
    k = -k

cv2.waitKey(0)
cv2.destroyAllWindows()

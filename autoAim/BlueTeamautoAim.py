# -*- coding: utf-8 -*-
"""
Created on Wed May  4 23:50:12 2022

@author: Ni Jingzhe
"""

import cv2

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_EXPOSURE, -10)

# input img
while (cap.isOpened()):
    ret, img = cap.read()
    

    #img = cv2.imread("red1.png")
    # 高斯模糊降噪
    img_gsb = cv2.GaussianBlur(img, (5, 5), 0)
    cv2.imshow("img_gsb", img_gsb.copy())
    if cv2.waitKey(1) & 0xFF == ord('q'):    #等待按键q按下
        break

    b, g, r = cv2.split(img_gsb)
    #img_sub = cv2.subtract(r, b)
    img_sub = cv2.subtract(r, b)
    cv2.imshow("img_sub", img_sub.copy())
    if cv2.waitKey(1) & 0xFF == ord('q'):    #等待按键q按下
        break

    
    ret, binary = cv2.threshold(
        img_sub, 80, 255, cv2.THRESH_BINARY)
    cv2.imshow("binary", binary.copy())
    if cv2.waitKey(1) & 0xFF == ord('q'):    #等待按键q按下
        break

    
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
    cnts = []
    cnts_data = []    
    if cv2.waitKey(1) & 0xFF == ord('q'):    #等待按键q按下
        break


cv2.waitKey(0)
cv2.destroyAllWindows()

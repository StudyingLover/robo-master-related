# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 14:25:39 2022

@author: HUAWEI
"""

from math import *
from cv2 import SOLVEPNP_IPPE
import serial as ser
import cv2
import numpy as np


ARMOR_HEIGHT = 2.75
ARMOR_WIDTH = 5.25
ARMOR_POINTS = np.array([[-ARMOR_WIDTH / 2, -ARMOR_HEIGHT / 2, 0],
                        [ARMOR_WIDTH / 2, -ARMOR_HEIGHT / 2, 0],
                        [ARMOR_WIDTH / 2, ARMOR_HEIGHT / 2, 0],
                        [-ARMOR_WIDTH / 2, ARMOR_HEIGHT / 2, 0]], dtype=np.float)

CAM_INTRINSIC_MATRIX = np.array([[1.1012e+03, 0, 592.2217],
                                [0, 1.0075e+03, 234.5529],
                                [0, 0, 1]], dtype=np.float)

TANGENTIAL_P1 = 0.0033
TANGENTIAL_P2 = 0.0015
RADIAL_K1 = -0.0680
RADIAL_K2 = 0.1569
RADIAL_K3 = -0.2281

def create_cam():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    cap.set(cv2.CAP_PROP_EXPOSURE, 0)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FPS, 60)
    return cap


def pre_process(img):
    '''
    Parameters
    ----------
    img : imagin

    Returns
    -------
    processed img.

    '''

    img_gsb = cv2.GaussianBlur(img, (7, 7), 0)
    b, g, r = cv2.split(img_gsb)
    img_sub = cv2.subtract(b, r)
    #img_sub = cv2.subtract(r, b)
    return img_sub


def binary(img, threshold):
    '''
    Parameters
    ----------
    img : img
    threshold : 阈值
    Returns
    -------
    a binary img.

    '''

    ret, binary = cv2.threshold(
        img, threshold, 255, cv2.THRESH_BINARY)
    cv2.imshow("binary", binary.copy())
    if cv2.waitKey(1) & 0xFF == ord('q'):  # 等待按键q按下
        cv2.destroyAllWindows()

    return binary


def sort_contours(cnts, method='bottom-to-top'):
    # initialize the reverse flag and sort index
    reverse = False
    i = 0
    # handle if sort in reverse
    if method == 'right-to-left' or method == 'bottom-to-top':
        reverse = True
    # handle if sort against y rather than x of the bounding box
    if method == 'bottom-to-top' or method == 'top-to-bottom':
        i = 1

    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes), key=lambda b: b[1][i], reverse=reverse))
    return (cnts, boundingBoxes)



def find_armor(img):
    '''
    Parameters
    ----------
    img : original_img
    Returns
    -------
    a list containing armor information

    '''
    binary_img = binary(pre_process(img),110)
    
    cnts, h = cv2.findContours(
        binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(cnts) >= 1:
        draw_img = img.copy()
        # loop over the contours
        Smax = -9
        cYmin = 1280
        changed = False
        for c in cnts:
            M = cv2.moments(c)
            S = int(M["m00"])
            if S < 50:
                cnts.remove(c)
                
            cY = int(M["m01"] / (M["m00"] + 0.00000001))
            cX = int(M["m10"] / (M["m00"] + 0.00000001))
           

def uart_send(uart, shoot_yaw,shoot_pitch):
    shoot_yaw=round(shoot_yaw,1)
    shoot_pitch=round(shoot_pitch,1)
    shoot_yaw=str(shoot_yaw)
    shoot_pitch=str(shoot_pitch)
    pos=shoot_yaw+"|"+shoot_pitch+" "+";"
    uart.write(str(pos).encode('utf-8'))

if __name__ == '__main__':

    #uart = ser.Serial('/dev/ttyTHS1',9600,timeout=1)
    cap = create_cam()
    ret, frame = cap.read()
    while True:
        
        for i in range(6):

            ret, frame = cap.read()
            
            if ret:
                four_points_for_armor = find_armor(frame)
                #print(four_points_for_armor)
                if type(four_points_for_armor) == type([]) and len(four_points_for_armor) == 4:

                    four_points_for_armor = np.array(four_points_for_armor, np.float)
                    retval, R, t = cv2.solvePnP(ARMOR_POINTS, four_points_for_armor, CAM_INTRINSIC_MATRIX, None, flags = SOLVEPNP_IPPE)
                    R, Jacobian = cv2.Rodrigues(R)
                    yaw, pitch = angle_calc(R)
                    print("(degree)yaw: ",yaw," (degree)pitch: ", pitch)
                    #uart_send(uart, yaw, pitch)

            if cv2.waitKey(1)==ord('q'):
                break
                break
    
    
    
    
    
    
    

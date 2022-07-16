# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 14:25:39 2022

@author: HUAWEI
"""

import cv2
from autoAimer import autoAimer

myAutoAimer = autoAimer("red")


def create_cam():
    cap = cv2.VideoCapture(cv2.CAP_DSHOW)
    #cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)  # 有时候你的摄像头需要手动关闭自动曝光
    cap.set(cv2.CAP_PROP_EXPOSURE, -5)  # 具体曝光参数自己调试
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    return cap


def uart_send(uart, shoot_yaw, shoot_pitch):   # 这里抄的是张旭dalao的下位机通讯（其实我也不太明白，具体可以问他本人）
    shoot_yaw = round(shoot_yaw, 1)
    shoot_pitch = round(shoot_pitch, 1)
    shoot_yaw = str(shoot_yaw)
    shoot_pitch = str(shoot_pitch)
    pos = shoot_yaw+"|"+shoot_pitch+" "+";"
    uart.write(str(pos).encode('utf-8'))


if __name__ == '__main__':

    #uart = ser.Serial('/dev/ttyTHS1',9600,timeout=1)
    cap = create_cam()
    ret, frame = cap.read()
    myAutoAimer.setBinaryThreshold(80)  # 具体阈值也请自己调试
    while True:

        for i in range(6):

            ret, frame = cap.read()

            if ret:
                cX, cY = myAutoAimer.findArmor(frame)
                print("cX is: ", cX, "cY is: ", cY)  # 至此你已经找到了轮廓中心点了

                #下面的代码就是下位机通讯啦
                #你也可以考虑把pid也放在上位机算完
                #也可以尝试加上卡尔曼滤波的运动预测（后续版本我也会加上）

            if cv2.waitKey(1) == ord('q'):
                break
                break

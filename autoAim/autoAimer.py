# -*- coding: utf-8 -*-
"""
Created on Sat Jul 16 20:27:52 2022

@author: HUAWEI
"""
import cv2
import numpy as np
from kalmanfilter import KalmanFilter


class autoAimer:

    def __init__(self, colour):
        self.colour = colour
        self.setThreshold = False
        self.kalmanFilter = KalmanFilter()
        self.postionCache = []

    def setBinaryThreshold(self, threshold):
        '''
        Parameters
        ----------
        threshold : INT
            设置预处理图像过程中二值化的阈值.

        Returns
        -------
        None.

        '''
        self.setThreshold = True
        self.threshold = threshold

    def imgProcess(self, originalImage):
        '''
        Returns
        -------
        imgAfterProcess
            经过预处理的图像.

        '''
        if not self.setThreshold:  # 确保阈值已经设置
            print("Haven't set binary threshold !")
            return "Error"

        imgGsb = cv2.GaussianBlur(originalImage, (7, 7), 0)  # 通过高斯模糊降噪
        b, g, r = cv2.split(imgGsb)  # 通道分离

        if self.colour == 'red':
            imgSub = cv2.subtract(b, r)  # 通道减除 b - r 会使蓝色区域有更高的值
        elif self.colour == 'blue':
            imgSub = cv2.subtract(r, b)

        ret, imgBinary = cv2.threshold(
            imgSub, self.threshold, 255, cv2.THRESH_BINARY)  # 二值化

        # 将二值化图品再次高斯模糊是为了除去白色面积中的小黑色噪点，防止轮廓破裂
        imgAfterProcess = cv2.GaussianBlur(imgBinary, (7, 7), 0)
        cv2.imshow("binary",imgAfterProcess.copy())

        return np.array(imgAfterProcess)

    def findArmor(self, inputImage):
        '''
        

        Parameters
        ----------
        inputImage : image
            从相机获取的逐帧图像.

        Returns
        -------
        cX, cY : int
            （被认为的）装甲板轮廓在opencv的像素坐标系下的中心坐标.
            说被认为的是因为，我们只寻找视野中最大的一个轮廓，至于是不是装甲板
            只能说大概率是的，但并不能保证
            （椭圆拟合或者卷积网络应该是确保找到装甲板的利器）

        '''
        if not self.setThreshold:
            print("Haven't set binary threshold !")
            return 0, 0
        
        imgProcessed = self.imgProcess(inputImage)

        cnts, h = cv2.findContours(
            imgProcessed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # 找轮廓

        if len(cnts) >= 1:
            drawImage = inputImage.copy()
            cntsInfo = [[0, 0]]
            for c in cnts:
                M = cv2.moments(c)  # M是图像矩
                S = int(M["m00"])  # 求面积
                if S > 50:
                    # 求中心坐标（具体可以去看CSDN上关于图像矩的博客）
                    cY = int(M["m01"] / (M["m00"] + 0.00000001))
                    cX = int(M["m10"] / (M["m00"] + 0.00000001))
                    # 拿出面积，中心位置，轮廓本身单独存放，便于后续处理
                    cntsInfo.append([S, cX, cY, c])

            cntsInfo.sort(reverse=True)  # 这样会根据S从大到小排列轮廓
            cX = cntsInfo[0][1]     # 取出最后被认为是装甲板的轮廓（面积最大）的中心位置坐标（像素坐标系）
            cY = cntsInfo[0][2]
            #Rect = cv2.boundingRect(cntsInfo[0][3])    # 创建轮廓矩形
            # 这里将轮廓索引设置为-1,绘制出所有轮廓的boundingRect,颜色设置为绿色，宽度为2为例
            #cv2.drawContours(drawImage, Rect, -1, (0, 255, 0), 2)
            cv2.circle(drawImage, [cX, cY], 5, (0, 255, 0), 3)
            cv2.imshow("cnts", drawImage)

            #self.postionCache.append([cX, cY])

            return cX, cY    # 返回中心坐标
        else:
            return "No contours", "No contours"

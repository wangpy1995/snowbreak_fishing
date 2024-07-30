import datetime
import os
import time
from time import sleep

import cv2
import numpy as np
from skimage.metrics import peak_signal_noise_ratio as psnr
from win32api import GetKeyState
from win32con import VK_SCROLL

import controller
from GDICapture import GDICapture

# 按钮图标
fishButtonRect = {'left': 1740, 'top': 970, 'width': 89, 'height': 67}
castLineImg = img = cv2.imread('png/cast_line.png')
biteImg = cv2.imread('png/bite.png')
dragImg = cv2.imread('png/drag.png')
# 钓鱼表盘
fishCircleRect = {'left': 1170, 'top': 300, 'width': 321, 'height': 311}


def initImg(img: cv2.Mat):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_green = np.array([10, 70, 220])
    upper_green = np.array([20, 95, 235])
    mask = cv2.inRange(img, lower_green, upper_green)
    # cv2.imshow('Contours', mask)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    filteredImg = cv2.bitwise_and(img, img, mask=mask)
    filteredImg = cv2.cvtColor(filteredImg, cv2.COLOR_HSV2BGR)
    filteredImg = cv2.cvtColor(filteredImg, cv2.COLOR_BGR2GRAY)
    return filteredImg


def is_scroll_on() -> bool:
    return GetKeyState(VK_SCROLL) == 1


def check_or_create_directory():
    qteDirName = 'fish_result'
    targetDirName = 'target'
    if not os.path.exists(qteDirName) or not os.path.isdir(qteDirName):
        os.makedirs(qteDirName)
    if not os.path.exists(targetDirName) or not os.path.isdir(targetDirName):
        os.makedirs(targetDirName)


def castButtonDetected(capture: GDICapture):
    img = capture.grab(fishButtonRect)
    img = initImg(img)
    cast = psnr(castLineImg, img)
    return cast > 25


def dragButtonDetected(capture: GDICapture):
    img = capture.grab(fishButtonRect)
    img = initImg(img)
    bite = psnr(dragImg, img)
    return bite > 25


def biteButtonDetected(capture: GDICapture):
    img = capture.grab(fishButtonRect)
    img = initImg(img)
    bite = psnr(biteImg, img)
    return bite > 25


def detectQTE(capture: GDICapture):
    img = capture.grab(fishCircleRect)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_green = np.array([20, 252, 255])
    upper_green = np.array([70, 255, 255])
    mask = cv2.inRange(img, lower_green, upper_green)
    filteredImg = cv2.bitwise_and(img, img, mask=mask)
    filteredImg = cv2.cvtColor(filteredImg, cv2.COLOR_HSV2BGR)
    filteredImg = cv2.cvtColor(filteredImg, cv2.COLOR_BGR2GRAY)
    contours, _ = cv2.findContours(filteredImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return len(contours) >= 2


def testQTE():
    img = cv2.imread('d:/snowbreak_fish3.png')
    imgCopy = img.copy()
    # b, g, r = cv2.split(img)
    # _, g = cv2.threshold(g, 250, 255, cv2.THRESH_BINARY)
    # _, r = cv2.threshold(r, 180, 255, cv2.THRESH_BINARY)
    # img = cv2.merge([b, g, r])
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_green = np.array([20, 252, 255])
    upper_green = np.array([70, 255, 255])
    mask = cv2.inRange(img, lower_green, upper_green)

    filteredImg = cv2.bitwise_and(img, img, mask=mask)
    filteredImg = cv2.cvtColor(filteredImg, cv2.COLOR_HSV2BGR)
    filteredImg = cv2.cvtColor(filteredImg, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Contours', filteredImg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    contours, _ = cv2.findContours(filteredImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        # 计算轮廓区域的像素数量
        area = cv2.contourArea(contour)
        print(f"轮廓区域的像素数量: {area}")

        # 可以绘制轮廓（如果需要）
        cv2.drawContours(imgCopy, [contour], -1, (255, 0, 0), 2)
        cv2.imshow('Contours', imgCopy)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def testSave():
    capture = GDICapture('尘白禁区')
    img = capture.grab(fishButtonRect)
    filename = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    cv2.imwrite('test/' + filename + '.png', img)


def testThresh():
    img = cv2.imread('png/bite.png', cv2.IMREAD_UNCHANGED)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_green = np.array([10, 70, 220])
    upper_green = np.array([20, 95, 235])
    mask = cv2.inRange(img, lower_green, upper_green)
    cv2.imshow('Contours', mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    filteredImg = cv2.bitwise_and(img, img, mask=mask)
    filteredImg = cv2.cvtColor(filteredImg, cv2.COLOR_HSV2BGR)
    filteredImg = cv2.cvtColor(filteredImg, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Contours', filteredImg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # testQTE()
    # testSave()
    # testThresh()
    # exit(0)
    castLineImg = initImg(castLineImg)
    biteImg = initImg(biteImg)
    dragImg = initImg(dragImg)

    check_or_create_directory()
    capture = GDICapture('尘白禁区')
    while True:
        if is_scroll_on():
            sleepTimes = 30
            if castButtonDetected(capture) and is_scroll_on():
                print('钓鱼开始')
                controller.pressAndReleaseGPadA()
                sleep(1000 / 1000)
                if castButtonDetected(capture) and is_scroll_on():
                    continue
                while not dragButtonDetected(capture) and is_scroll_on():
                    sleep(50 / 1000)
                print('扔杆开始')
                controller.pressAndReleaseGPadA()
                while not biteButtonDetected(capture) and is_scroll_on():
                    sleep(50 / 1000)
            if not is_scroll_on():
                continue
            while biteButtonDetected(capture) and is_scroll_on():

                if detectQTE(capture):
                    controller.pressAndReleaseGPadA()
                    print('qte拉线')
                    sleep(200 / 1000)
                else:
                    sleep(20 / 1000)

            if not is_scroll_on():
                break
            # 等三秒结算并截图保存
            print('等待结算')
            sleep(3000 / 1000)
            img = capture.grab(capture.fullWindow)
            filename = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            cv2.imwrite('fish_result/' + filename + '.png', img)
            controller.pressAndReleaseGpadB()
            while not castButtonDetected(capture) and is_scroll_on():
                sleep(100 / 1000)
        else:
            sleep(200 / 1000)

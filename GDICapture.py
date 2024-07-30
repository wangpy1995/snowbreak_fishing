from ctypes import windll

import cv2
import numpy as np
import win32gui
from win32con import SRCCOPY
from win32gui import GetDesktopWindow, GetWindowDC, DeleteObject
from win32ui import CreateDCFromHandle, CreateBitmap


class GDICapture(object):
    def __init__(self, windowTitle: str):
        window = win32gui.FindWindow(None, windowTitle)
        windll.user32.SetProcessDPIAware()
        self.left, self.top, self.right, self.bottom = win32gui.GetWindowRect(window)
        self.fullWindow = {'left': 0, 'top': 0, 'width': self.right - self.left,
                           'height': self.bottom - self.top}
        hWin = GetDesktopWindow()
        # hWin = FindWindow(完整类名, 完整窗体标题名)
        hWinDC = GetWindowDC(hWin)
        self.srcDC = CreateDCFromHandle(hWinDC)
        self.memDC = self.srcDC.CreateCompatibleDC()
        self.bmp = CreateBitmap()

    # 从显卡直接取数据存在截图黑屏问题
    def grab(self, captureSetting: dict[str, int]):
        left = captureSetting.get('left') + self.left
        top = captureSetting.get('top') + self.top
        width = captureSetting.get('width')
        height = captureSetting.get('height')

        # hWin = GetDesktopWindow()
        # hWin = FindWindow(完整类名, 完整窗体标题名)
        # hWinDC = GetWindowDC(hWin)
        # srcDC = CreateDCFromHandle(hWinDC)
        # memDC = srcDC.CreateCompatibleDC()
        # bmp = CreateBitmap()
        bmp, srcDC, memDC = self.bmp, self.srcDC, self.memDC
        bmp.CreateCompatibleBitmap(srcDC, width, height)
        memDC.SelectObject(bmp)
        memDC.BitBlt((0, 0), (width, height), srcDC, (left, top), SRCCOPY)
        array = bmp.GetBitmapBits(True)
        DeleteObject(bmp.GetHandle())
        # memDC.DeleteDC()
        # srcDC.DeleteDC()
        # ReleaseDC(hWin, hWinDC)
        img = np.frombuffer(array, dtype='uint8')
        img.shape = (height, width, 4)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img

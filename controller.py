import random

import vgamepad as vg
from vgamepad import XUSB_BUTTON as XB
from time import sleep

gpad = vg.VX360Gamepad()


# xbox手柄按钮A
def pressAndReleaseGPadA():
    gpad.press_button(XB.XUSB_GAMEPAD_A)
    gpad.update()
    sleep(random.randrange(50, 150) / 1000)
    gpad.release_button(XB.XUSB_GAMEPAD_A)
    gpad.update()
    sleep(random.randrange(50, 100) / 1000)

# xbox手柄按钮B
def pressAndReleaseGpadB():
    gpad.press_button(XB.XUSB_GAMEPAD_B)
    gpad.update()
    sleep(random.randrange(50, 150) / 1000)
    gpad.release_button(XB.XUSB_GAMEPAD_B)
    gpad.update()
    sleep(random.randrange(300, 500) / 1000)

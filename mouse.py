import pyautogui as auto
from time import sleep

while True:
    x, y = auto.position()
    print(x, y, "    ",auto.pixel(x, y))
    # print(auto.pixel(x, y))
    sleep(0.5)
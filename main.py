import os
import time
import keyboard
import ctypes
import random

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

running = True

while running:
    
    print(ctypes.windll.user32.FindWindowW(None, "smth"))
    width = ctypes.windll.user32.GetSystemMetrics(0)
    height = ctypes.windll.user32.GetSystemMetrics(1)
    print(width, height)
    a = ctypes.windll.user32.FindWindowW(None, "smth")

    user32.ShowWindow(ctypes.windll.user32.FindWindowW(None, "smth"), 3)

    active_window = user32.GetForegroundWindow()
    current_window = kernel32.GetConsoleWindow()

    if keyboard.is_pressed("alt"):
        script_path = os.path.abspath(__file__)
        script_directory = os.path.dirname(script_path)

        os.system('start "smth"')

    if  keyboard.is_pressed("shift"):
        ctypes.windll.user32.MoveWindow(a, (width+14)//2, (height-14)//2, (width)//2, (height-28)//2, True)
    
    if  keyboard.is_pressed("`"):
        running = False


    time.sleep(0.01)

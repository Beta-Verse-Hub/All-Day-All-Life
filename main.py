import os
import time
import keyboard
import ctypes
import random

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

active_window = user32.GetForegroundWindow()
current_window = kernel32.GetConsoleWindow()

running = True

windows = {"main_window" : current_window}

while running:
    
    active_window = user32.GetForegroundWindow()
    current_window = kernel32.GetConsoleWindow()

    print(windows)
    width = ctypes.windll.user32.GetSystemMetrics(0)
    height = ctypes.windll.user32.GetSystemMetrics(1)
    print(width, height)
    a = ctypes.windll.user32.FindWindowW(None, "smth")

    user32.ShowWindow(ctypes.windll.user32.FindWindowW(None, "smth"), 3)

    if keyboard.is_pressed("alt"):
        script_path = os.path.abspath(__file__)
        script_directory = os.path.dirname(script_path)

        os.system(f'start "window_{len(windows)}"')
        windows[f"window_{len(windows)}"] = ctypes.windll.user32.FindWindowW(None, f"window_{len(windows)}")

    if keyboard.is_p("shift"):
        if keyboard.is_pressed("left"):
            ctypes.windll.user32.MoveWindow(active_window, 0, 0, (width+14)//2, (height-28), True)
        if keyboard.is_pressed("right"):
            ctypes.windll.user32.MoveWindow(active_window, (width)//2, 0, (width+14)//2, (height-28), True)
        if keyboard.is_pressed("up"):
            ctypes.windll.user32.MoveWindow(active_window, 0, 0, (width+14), (height-14)//2, True)
        if keyboard.is_pressed("down"):
            ctypes.windll.user32.MoveWindow(active_window, 0, (height)//2, (width+14), (height-28)//2, True)
    
    if keyboard.is_pressed("`"):
        running = False

    for i in list(windows.keys()):
        windows[i] = ctypes.windll.user32.FindWindowW(None, f"window_{len(windows)}")
    
    time.sleep(0.01)

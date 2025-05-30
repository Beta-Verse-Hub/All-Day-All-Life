import os
import time
import keyboard
import ctypes
from ctypes import wintypes
import random
import threading


global windows
global running
global FindWindowW


def check_for_windows():
    while running:
        remove_windows = []
        for i in range(len(windows)):
            hwnd = FindWindowW(None, str(list(windows.keys())[i]+' - "C:\\Users\\DELL\\OneDrive\\Desktop\\PythonProjects\\All Day All Life\\main_program.py"'))
            if hwnd and list(windows.keys())[i] != "window_0":
                remove_windows.append(i)
        for i in reversed(remove_windows):
            windows.pop(f"window_{i}")

def position_window(window, main_grid, new_grid, screen_width, screen_height):
    
    user32.MoveWindow(window, new_grid[0][0], new_grid[0][1], (screen_width+14)*new_grid[1][0]//main_grid[0], (screen_height-28)*new_grid[1][1]//main_grid[1], True)


user32 = ctypes.WinDLL('user32', use_last_error=True)
kernel32 = ctypes.windll.kernel32

active_window = user32.GetForegroundWindow()
current_window = kernel32.GetConsoleWindow()

FindWindowW = user32.FindWindowW
FindWindowW.argtypes = [wintypes.LPCWSTR, wintypes.LPCWSTR]
FindWindowW.restype = wintypes.HWND

os.system('echo "\033]0;window_0\007"')

running = True

windows = {"window_0" : [[0,0], [1,2]]}
grid = [2,2]

checking_window_thread = threading.Thread(target=check_for_windows, daemon=True)
checking_window_thread.start()

while running:
    
    active_window = user32.GetForegroundWindow()
    current_window = kernel32.GetConsoleWindow()

    length = user32.GetWindowTextLengthW(active_window)
    if length == 0:
        buffer = None
    buffer = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(active_window, buffer, length + 1)

    width = user32.GetSystemMetrics(0)
    height =  user32.GetSystemMetrics(1)

    user32.ShowWindow(user32.FindWindowW(None, "win"), 3)

    hwnd = FindWindowW(None, "window_1")

    print(windows, active_window, hwnd)

    if keyboard.is_pressed("alt"):
        script_path = os.path.abspath(__file__)
        script_directory = os.path.dirname(script_path)

        os.system(f'start "window_{len(windows)}" cmd /k python "{os.path.abspath("main_program.py")}" "window_{len(windows)}"')
        hwnd = FindWindowW(None, f"window_{len(windows)}")
        print(hwnd)
        windows[f"window_{len(windows)}"] = [[1,0], [2,2]]

        while hwnd == None:
            FindWindowW = user32.FindWindowW
            FindWindowW.argtypes = [wintypes.LPCWSTR, wintypes.LPCWSTR]
            FindWindowW.restype = wintypes.HWND
            hwnd = FindWindowW(None, f"window_{len(windows)}")
            print(hwnd, width, height)
            time.sleep(0.01)

    if keyboard.is_pressed("-"):
        if keyboard.is_pressed("left"):
            windows[buffer.value] = [[windows[buffer.value][0][0]-1, windows[buffer.value][0][1]],windows[buffer.value][1]]
            position_window(active_window, grid, windows[buffer.value], width, height)

        if keyboard.is_pressed("right"):
            windows[buffer.value] = [[windows[buffer.value][0][0]+1, windows[buffer.value][0][1]],windows[buffer.value][1]]
            position_window(active_window, grid, windows[buffer.value], width, height)

        if keyboard.is_pressed("up"):
            windows[buffer.value] = [[windows[buffer.value][0][0], windows[buffer.value][0][1]-1],windows[buffer.value][1]]
            position_window(active_window, grid, windows[buffer.value], width, height)

        if keyboard.is_pressed("down"):
            windows[buffer.value] = [[windows[buffer.value][0][0], windows[buffer.value][0][1]+1],windows[buffer.value][1]]
            position_window(active_window, grid, windows[buffer.value], width, height)
    
    if keyboard.is_pressed("`"):
        running = False
    
    time.sleep(0.01)

checking_window_thread.join()

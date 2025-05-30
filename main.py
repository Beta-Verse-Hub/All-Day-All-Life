import os
import time
import keyboard
import ctypes
import random
import threading

global windows
global running

def check_for_windows():
    while running:
        remove_windows = []
        for i in range(len(windows)):
            if int( user32.FindWindowW(None, windows[i])) != 0 and windows[i] != "window_0":
                remove_windows.append(i)
        for i in reversed(remove_windows):
            windows.pop(i)


def position_window(window, grid, position_in_grid, screen_width, screen_height):
    
    position_in_grid = [position_in_grid[0]*screen_width//len(grid[0]), position_in_grid[1]*screen_height//len(grid)]
    user32.MoveWindow(window, position_in_grid[0], position_in_grid[1], (width+14)//len(grid[0]), (height-28)//len(grid), True)

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

active_window = user32.GetForegroundWindow()
current_window = kernel32.GetConsoleWindow()

os.system('echo "\033]0;window_0\007"')

running = True

windows = ["window_0"]
grid = [["0", "1"],
        ["2", "3"]]

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

    a = user32.FindWindowW(None, "smth")

    user32.ShowWindow( user32.FindWindowW(None, "smth"), 3)

    print(windows)

    if keyboard.is_pressed("alt"):
        script_path = os.path.abspath(__file__)
        script_directory = os.path.dirname(script_path)

        os.system(f'start "window_{len(windows)}" cmd /k title window_{len(windows)}')
        windows.append(f"window_{len(windows)}")

    if keyboard.is_pressed("left"):
        user32.MoveWindow(active_window, 0, 0, (width+14)//2, (height-28), True)
    if keyboard.is_pressed("right"):
        user32.MoveWindow(active_window, (width)//2, 0, (width+14)//2, (height-28), True)
    if keyboard.is_pressed("up"):
        user32.MoveWindow(active_window, 0, 0, (width+14), (height-14)//2, True)
    if keyboard.is_pressed("down"):
        user32.MoveWindow(active_window, 0, (height)//2, (width+14), (height-28)//2, True)

    if keyboard.is_pressed("shift"):
        
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if buffer.value[-1] == grid[i][j]:
                    position_window(active_window, grid, [i, j], width, height)
                    break
    
    if keyboard.is_pressed("`"):
        running = False
    
    time.sleep(0.01)

checking_window_thread.join()

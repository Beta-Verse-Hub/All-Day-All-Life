#importing important libraries
import os
import time
import keyboard
import datetime
import ctypes
from ctypes import wintypes


# This function takes a window, a main grid, a new grid, the width of the screen and the height of the screen, and moves the window to the new grid position on the screen.
def position_window(window, main_grid, new_grid, screen_width, screen_height):
    
    x = (new_grid[0][0]*(screen_width//main_grid[0]))-5
    y = (new_grid[0][1]*(screen_height//main_grid[1]))-1
    width = (new_grid[1][0]*(screen_width+14)//main_grid[0])+10
    height = (new_grid[1][1]*(screen_height+14)//main_grid[1])+2

    user32.MoveWindow(window, x, y, width, height, True)


# Prints out the details of the windows and the active window at the current time
def print_out_details(windows, active_window):

    size = os.get_terminal_size()
    total_lines = 3

    details = ""

    # Adding the top border
    details += "-"*size.columns

    # Time
    details += f" Time : {datetime.datetime.now().strftime('%H:%M:%S')}\n"

    # The active window
    details += f" Active Window ID : {active_window}\n"

    # All the windows
    for i in range(len(windows)):
        details +=  f" {list(windows.keys())[i]} : {list(windows.values())[i][0]} : {list(windows.values())[i][1]}\n"
        total_lines += 1

    # Adding the bottom border
    details += "-"*size.columns
    total_lines += 1

    # Print out the details
    print(f"\033[H{details}", flush=True, end="")



user32 = ctypes.WinDLL("user32", use_last_error=True)
kernel32 = ctypes.windll.kernel32

active_window = user32.GetForegroundWindow()
current_window = kernel32.GetConsoleWindow()

FindWindowW = user32.FindWindowW
FindWindowW.argtypes = [wintypes.LPCWSTR, wintypes.LPCWSTR]
FindWindowW.restype = wintypes.HWND

os.system('echo "\033]0;window_0\007"')
os.system("cls")

running = True

windows = {"window_0" : [[0,0], [1,2]]}
with open("Data/grid.txt", "r") as grid_data:
    grid_data = grid_data.readlines()
    grid = [int(grid_data[0]), int(grid_data[1])]

up_key_pressed = True
down_key_pressed = True
left_key_pressed = True
right_key_pressed = True


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

    print_out_details(windows, active_window)

    remove_windows = []
    for i in range(len(windows)):
        hwnd = FindWindowW(None, str(list(windows.keys())[i]))
        select_hwnd = FindWindowW(None, "Select "+str(list(windows.keys())[i]))
        if hwnd == None and select_hwnd == None and list(windows.keys())[i] != "window_0":
            remove_windows.append(i)
        user32.ShowWindow(user32.FindWindowW(None,list(windows.keys())[i]), 3)

    for i in reversed(remove_windows):
        windows.pop(list(windows.keys())[i])

    if active_window == current_window:

        if keyboard.is_pressed("shift"):
            os.system("cls")
            window_name = input("Give the window title that you want to manage : ")
            
            if FindWindowW(None, window_name) == None:
                os.system(f'start "{window_name}" cmd /k main_program.exe "{window_name}"')

            hwnd = FindWindowW(None, window_name)
            print(hwnd)
            windows[window_name] = [[1,0], [2,2]]

            while hwnd == None:
                FindWindowW = user32.FindWindowW
                FindWindowW.argtypes = [wintypes.LPCWSTR, wintypes.LPCWSTR]
                FindWindowW.restype = wintypes.HWND
                hwnd = FindWindowW(None, window_name)
                print(hwnd, width, height)
                time.sleep(0.01)

            os.system("cls")
            time.sleep(3)
            windows[window_name] = [[1,0], [2,2]]
        
        if keyboard.is_pressed("ctrl"):
            os.system("cls")
            try:
                x_grid = int(input("No of columns in the grid : "))
                if x_grid < 1:
                    x_grid = 1
                    print("Please set the number of columns more than 1")
                    print("Number of columns have been set to 1 for now")
                
                y_grid = int(input("No of rows in the grid : "))
                if y_grid < 1:
                    y_grid = 1
                    print("Please set the number of rows more than 1")
                    print("Number of rows have been set to 1 for now")

                grid = [x_grid, y_grid]
            except ValueError as e:
                print("Please enter an integer")
                time.sleep(1)
            os.system("cls")

        if keyboard.is_pressed("esc"):
            running = False


    if keyboard.is_pressed("tab"):
        if keyboard.is_pressed("left") and not left_key_pressed:
            windows[buffer.value] = [[windows[buffer.value][0][0]-1, windows[buffer.value][0][1]], windows[buffer.value][1]]
            position_window(active_window, grid, windows[buffer.value], width, height)
            
            left_key_pressed = True
        elif not keyboard.is_pressed("left"):
            left_key_pressed = False

        if keyboard.is_pressed("right") and not right_key_pressed:
            windows[buffer.value] = [[windows[buffer.value][0][0]+1, windows[buffer.value][0][1]], windows[buffer.value][1]]
            position_window(active_window, grid, windows[buffer.value], width, height)
            
            right_key_pressed = True
        elif not keyboard.is_pressed("right"):
            right_key_pressed = False

        if keyboard.is_pressed("up") and not up_key_pressed:
            windows[buffer.value] = [[windows[buffer.value][0][0], windows[buffer.value][0][1]-1], windows[buffer.value][1]]
            position_window(active_window, grid, windows[buffer.value], width, height)
            
            up_key_pressed = True
        elif not keyboard.is_pressed("up"):
            up_key_pressed = False

        if keyboard.is_pressed("down") and not down_key_pressed:
            windows[buffer.value] = [[windows[buffer.value][0][0], windows[buffer.value][0][1]+1], windows[buffer.value][1]]
            position_window(active_window, grid, windows[buffer.value], width, height)
            
            down_key_pressed = True
        elif not keyboard.is_pressed("down"):
            down_key_pressed = False


    if keyboard.is_pressed("alt"):
        if keyboard.is_pressed("left") and not left_key_pressed and windows[buffer.value][1][0] > 1:
            windows[buffer.value] = [windows[buffer.value][0], [windows[buffer.value][1][0]-1, windows[buffer.value][1][1]]]
            position_window(active_window, grid, windows[buffer.value], width, height)
            
            left_key_pressed = True
        elif not keyboard.is_pressed("left"):
            left_key_pressed = False

        if keyboard.is_pressed("right") and not right_key_pressed:
            windows[buffer.value] = [windows[buffer.value][0], [windows[buffer.value][1][0]+1, windows[buffer.value][1][1]]]
            position_window(active_window, grid, windows[buffer.value], width, height)
            
            right_key_pressed = True
        elif not keyboard.is_pressed("right"):
            right_key_pressed = False

        if keyboard.is_pressed("up") and not up_key_pressed and windows[buffer.value][1][1] > 1:
            windows[buffer.value] = [windows[buffer.value][0], [windows[buffer.value][1][0], windows[buffer.value][1][1]-1]]
            position_window(active_window, grid, windows[buffer.value], width, height)
            
            up_key_pressed = True
        elif not keyboard.is_pressed("up"):
            up_key_pressed = False

        if keyboard.is_pressed("down") and not down_key_pressed:
            windows[buffer.value] = [windows[buffer.value][0], [windows[buffer.value][1][0], windows[buffer.value][1][1]+1]]
            position_window(active_window, grid, windows[buffer.value], width, height)

            down_key_pressed = True
        elif not keyboard.is_pressed("down"):
            down_key_pressed = False
    
    time.sleep(0.01)

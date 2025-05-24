import os
import time
import keyboard
import ctypes

key = keyboard.read_key(suppress=True)

while key != "`":
    
    print(ctypes.windll.user32.FindWindowW(None, "smth"))

    key = keyboard.read_key(suppress=True)

    if key == "alt":
        script_path = os.path.abspath(__file__)
        script_directory = os.path.dirname(script_path)

        os.system('start "smth"')
    
    time.sleep(0.05)
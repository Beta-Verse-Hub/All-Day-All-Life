import os
import time
import threading
import keyboard
import ctypes

key = None

def key_listener_thread_func():
    global key
    while True:
        key = keyboard.read_key(suppress=True)

listener_thread = threading.Thread(target=key_listener_thread_func, daemon=True)
listener_thread.start()

while key != "`":
    
    print(ctypes.windll.user32.FindWindowW(None, "smth"))

    if key == "alt":
        script_path = os.path.abspath(__file__)
        script_directory = os.path.dirname(script_path)

        os.system('start "smth"')
    
    time.sleep(0.01)

import os
import time
import threading
import keyboard
import ctypes

key = None
running = True

def key_listener_thread_func():
    global key
    while True:
        key = keyboard.read_key(suppress=True)

listener_thread = threading.Thread(target=key_listener_thread_func, daemon=True)
listener_thread.start()

key_detected = False

while running:
    
    print(ctypes.windll.user32.FindWindowW(None, "smth"))
    a = ctypes.windll.user32.FindWindowW(None, "smth")

    if key == "alt":
        script_path = os.path.abspath(__file__)
        script_directory = os.path.dirname(script_path)

        os.system('start "smth"')
        key_detected = True

    if key == "shift":
        ctypes.windll.user32.MoveWindow(a, 2, 2, 100, 100, False)
        key_detected = True
    
    if key == "`":
        running = False
        key_detected = True

    time.sleep(0.01)

    if key_detected:
        key = None
        key_detected = False
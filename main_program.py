# Imports
import os
import keyboard
import time
import random
import ctypes
import sys
import config
import KeyDetectorWrapper as KDW
import platform
import subprocess
import psutil
import datetime
from pynput.mouse import Controller, Button



# Initializes variables (user32, kernel32, size, width and height)
def init_variables():
    
    # Globalize them
    global user32, kernel32, size, width, height, configuration

    # Get user32 and kernel32
    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32

    # Get terminal size
    size = os.get_terminal_size()
    width = size.columns
    height = size.lines

    # Get configuration
    configuration = config.get_config()


# Updates the size of the terminal
def update_size():
    global size, width, height

    size = os.get_terminal_size()
    width = size.columns
    height = size.lines


# Updates the 'Data/config.txt' file with the current configuration.
def update_config():

    configuration = config

    with open("Data/config.txt", "w") as config:
        # Clears the file
        config.truncate()
    
        # Writes the configuration
        config.write("config = {\n")
        for i in configuration:
            config.write(f"\t'{i}' : {configuration[i]}\n")
        config.write("}\n")
    
    # Reloads the configuration
    from config import config


# List all available drives on the system.
def list_drives():

    drives = []
    for letter in range(ord('A'), ord('Z') + 1):
        drive = f"{chr(letter)}:\\"

        # Check if the drive exists
        if os.path.exists(drive):
            drives.append(drive) # Add the drive to the list if it exists
    
    return drives


# Reads and returns the to-do list's data from the 'Data/to-do-data.txt' file as a list of lists.
def get_to_do_data():

    with open("Data/to-do-data.txt","r+") as data:
        data = data.readlines()
    
    modified_data = []
    
    for i in range(len(data)//2):
        
        # Fetches the text
        if data[i*2][-1] =="\n":
            a = data[i*2][0:-1]
        else:
            a = data[i*2]

        # Fetches the tick
        if data[(i*2)+1][-1] =="\n":
            b = data[(i*2)+1][0:-1]
        else:
            b = data[(i*2)+1]

        # Appends the data
        modified_data.append([a, b])

    return modified_data


# Writes the to-do list's data to the 'Data/to-do-data.txt' file
def set_to_do_data(to_do_data):

    modified_data = []
    for i in to_do_data:
        # Appends the text
        modified_data.append(i[0])

        # Appends the tick
        modified_data.append(i[1])

    # Clears and then writes the data
    with open("Data/to-do-data.txt","r+") as data:
        data.truncate()
        data.write("\n".join(modified_data))
    

# Converts a logo string from a special syntax to an ansi coloured string
def colorise_logo(logo):
    
    """
    The syntax is as follows:

    -;r;g;b- part of the logo -m- -;r2;g2;b2- other part of the logo -m- ...
    
    -;r;g;b- => set the rgb value in decimals integer.
    part of the logo => the logo's part in ascii art form
    -m- => to stop using the previous color
    """
    
    logo = str(logo)
    logo = list(logo.split("-"))
    new_logo = ""

    for i in logo:
        # Skips empty lines
        if i == "":
            continue

        # Adds the text
        if not (i[0] in ["m",";"]):
            new_logo += i

        # Changes the color
        elif not (i[0] in ["m"]):
            j = list(i.split(";"))
            new_logo += f"\033[38;2;{ j[1] };{ j[2] };{ j[3] }m"
        
        # Resets the color
        else:
            new_logo += f"\033[0m"


    return new_logo


# Prints a formatted screen by joining each line of the screen matrix into a single string.
def output(screen, select:list=None):

    formatted_screen = []
    # Rows
    for line in range(len(screen)):
        a = ""
        # Columns
        for char in range(len(screen[line])):
            if select == [char, line]:
                a += "\033[48;2;255;255;255m\033[38;2;0;0;0m" + screen[line][char] + "\033[0m"
                continue
            a += screen[line][char]
        formatted_screen.append(a)

    # Prints out the formatted screen
    print("\n"*50 + "".join(formatted_screen)[0:-1], end="")


# Makes an empty screen with border
def makeScreen(screen, width, height):

    # Each Column
    for y in range(height):
        screen.append([])

        # Each Cell
        for x in range(width):
            screen[y].append(" ")


# A mode for editing the game of life screen's screen
def screenChangeMode(screen):
    
    init_variables()

    # Initialises the key press booleans
    up_pressed = True
    down_pressed = True
    left_pressed = True
    right_pressed = True
    shift_pressed = True
    space_pressed = True

    running = True
    select = [2,2]

    while running:

        active_window = user32.GetForegroundWindow()
        current_window = kernel32.GetConsoleWindow()

        if active_window == current_window:

            # Select goes up 
            if keyboard.is_pressed("up") and not up_pressed:
                select[1] -= 1
                up_pressed = True
            elif not keyboard.is_pressed("up"):
                up_pressed = False
            
            # Select goes down
            if keyboard.is_pressed("down") and not down_pressed:
                select[1] += 1
                down_pressed = True
            elif not keyboard.is_pressed("down"):
                down_pressed = False
            
            # Select goes left
            if keyboard.is_pressed("left") and not left_pressed:
                select[0] -= 1
                left_pressed = True
            elif not keyboard.is_pressed("left"):
                left_pressed = False
            
            # Select goes right
            if keyboard.is_pressed("right") and not right_pressed:
                select[0] += 1
                right_pressed = True
            elif not keyboard.is_pressed("right"):
                right_pressed = False

            # Change select
            if keyboard.is_pressed("space") and not space_pressed:
                if screen[select[1]][select[0]] == "#":
                    screen[select[1]][select[0]] = " "
                else:
                    screen[select[1]][select[0]] = "#"
                space_pressed = True
            elif not keyboard.is_pressed("space"):
                space_pressed = False
            
            # Stop
            if keyboard.is_pressed("shift") and not shift_pressed:
                running = False
                shift_pressed = True
            elif not keyboard.is_pressed("shift"):
                shift_pressed = False
        
        # output the screen
        output(screen, select)
        time.sleep(0.01)
    
    return screen


def next_generation(screen, new_screen):
    for y in range(len(screen)):
        new_screen.append([])
        for x in range(len(screen[y])):
            if screen[y][x] == "\033[38;2;0;0;0m\033[48;2;255;255;255m#\033[0m":
                screen[y][x] = "#"
            elif screen[y][x] == "\033[38;2;0;0;0m\033[48;2;255;255;255m \033[0m":
                screen[y][x] = " "
            alive_neighbours = 0

            for i in range(-1,2):
                for j in range(-1,2):
                    if i == 0 and j == 0: # Skip the current cell
                        continue
                    if y+i < 0 or y+i >= len(screen): # Skip the row which is out of bounds
                        continue
                    if x+j < 0 or x+j >= len(screen[y+i]): # Skip the column which is out of bounds
                        continue
                    if screen[y+i][x+j] == "#": # Check if the neighbour is alive
                        alive_neighbours += 1

            if screen[y][x] == "#" and alive_neighbours < 2 or alive_neighbours > 3: # underpopulation and overpopulation
                new_screen[y].append(" ")
            elif screen[y][x] == " " and alive_neighbours == 3: # reproduction
                new_screen[y].append("#")
            elif screen[y][x] == "#" and alive_neighbours in [2,3]: # survival
                new_screen[y].append("#")
            else: # no change
                new_screen[y].append(screen[y][x])


def output_expression(expression, height):
    new_expression = "\n"*height
    configuration = config.get_config()

    for i in range(len(expression)):
        if expression[i] in ["0","1","2","3","4","5","6","7","8","9"]:
            new_expression += f"\033[48;2;0;0;0m\033[38;2;{configuration["Calculator Color 1"][0][0]};{configuration["Calculator Color 1"][0][1]};{configuration["Calculator Color 1"][0][2]}m{expression[i]}\033[0m"
        else:
            new_expression += f"\033[48;2;0;0;0m\033[38;2;{configuration["Calculator Color 2"][0][0]};{configuration["Calculator Color 2"][0][1]};{configuration["Calculator Color 2"][0][2]}m{expression[i]}\033[0m"
    
    print(new_expression, end="")


# Screens

def settings_screen():

    init_variables()

    screen = []
    select = 1

    up_key_pressed = True
    down_key_pressed = True

    running = True
    while running:

        active_window = user32.GetForegroundWindow()
        current_window = kernel32.GetConsoleWindow()

        update_size()

        configuration = config.get_config()

        if active_window == current_window:

            pressed_key = KDW.getKey()

            if keyboard.is_pressed("up") and select > 1 and not up_key_pressed:
                select -= 1
                up_key_pressed = True
            
            elif not keyboard.is_pressed("up"):
                up_key_pressed = False

            if keyboard.is_pressed("down") and select < len(configuration)-1 and not down_key_pressed:
                select += 1
                down_key_pressed = True
            
            elif not keyboard.is_pressed("down"):
                down_key_pressed = False

            if keyboard.is_pressed("shift"):
                config.get_input(select)

            if pressed_key == 27: # esc
                running = False
        
        output(["\n"*height, config.format_settings_screen(configuration, width, select), "\n"])
        time.sleep(0.01)


def a_shooter_game_screen():
    try:
        subprocess.run(["./Game.exe"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the game: {e}")
    except FileNotFoundError:
        print("The game executable was not found.")


def calculator_screen():
    
    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32

    size = os.get_terminal_size()
    width = size.columns
    height = size.lines

    valid_keys = {
        # Numbers
        48: "0",  # 0x30
        49: "1",  # 0x31
        50: "2",  # 0x32
        51: "3",  # 0x33
        52: "4",  # 0x34
        53: "5",  # 0x35
        54: "6",  # 0x36
        55: "7",  # 0x37
        56: "8",  # 0x38
        57: "9",  # 0x39

        # Operator characters
        43: "+",  # 0x2B (ASCII for plus)
        45: "-",  # 0x2D (ASCII for minus)
        42: "*",  # 0x2A (ASCII for asterisk)
        47: "/",  # 0x2F (ASCII for slash)

        # Parentheses
        40: "(",  # 0x28 (ASCII for left parenthesis)
        41: ")",  # 0x29 (ASCII for right parenthesis)

        # Curly braces
        123: "{", # 0x7B (ASCII for left curly brace)
        125: "}", # 0x7D (ASCII for right curly brace)

        # Square brackets
        91: "[",  # 0x5B (ASCII for left square bracket)
        93: "]",  # 0x5D (ASCII for right square bracket)
    
        # Period
        46: "."   # 0x2E (ASCII for period)
    }
    expression = ""
    key_pressed = 0

    running = True
    while running:

        active_window = user32.GetForegroundWindow()
        current_window = kernel32.GetConsoleWindow()

        if active_window == current_window:

            pressed_key = KDW.getKey()

            if key_pressed == 0:
                key_pressed += 1

            if pressed_key in list(valid_keys.keys()) and key_pressed == 1:
                expression += str(valid_keys[pressed_key])
                key_pressed = 0
            elif key_pressed == 0:
                key_pressed = 1
                pressed_key = KDW.getKey()

            if pressed_key == 8: # backspace
                expression = expression[:-1]
            if pressed_key == 61: # =
                while expression[0] == "0":
                    expression = expression[1:]
                try:
                    expression = str(eval(expression))
                except SyntaxError as e:
                    print("Invalid expression")
                    time.sleep(3)
            if pressed_key == 27: # esc
                running = False
        
        output_expression(expression, height)
        time.sleep(0.01)


def matrix_screen():
    try:
        subprocess.run(["./matrix_screen.exe"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the matrix program: {e}")
    except FileNotFoundError:
        print("The matrix program executable was not found.")


def game_of_life_screen():

    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32

    size = os.get_terminal_size()
    width = size.columns
    height = size.lines

    screen = []
    new_screen = []
    makeScreen(screen, width, height)

    shift_pressed = True

    running = True
    while running:

        active_window = user32.GetForegroundWindow()
        current_window = kernel32.GetConsoleWindow()
        
        new_screen = []
        next_generation(screen, new_screen)
        screen = new_screen.copy()

        if active_window == current_window:

            if keyboard.is_pressed("shift") and not shift_pressed:
                screen = screenChangeMode(screen)
                shift_pressed = True
            elif not keyboard.is_pressed("shift"):
                shift_pressed = False
            
            if keyboard.is_pressed("esc"):
                running = False
        
        output(screen)
        time.sleep(0.01)


def about_screen():

    with open(f"Data/custom_logo_file_path.txt", "r") as custom_logo_file_path:
        
        custom_logo_file_path = custom_logo_file_path.read()

        if custom_logo_file_path and os.path.exists(custom_logo_file_path):
            logo_file_path = custom_logo_file_path
        else:
            logo_file_path = f"Logos/Windows{platform.release()}.txt"

    with open(logo_file_path, "r", encoding="UTF-8") as logo:
        logo = logo.read()
        logo = colorise_logo(logo)
        print(logo)
    
    user32 = ctypes.windll.user32

    width = str(user32.GetSystemMetrics(0))
    height =  str(user32.GetSystemMetrics(1))

    boot_time_timestamp = psutil.boot_time()
    boot_time_datetime = datetime.datetime.fromtimestamp(boot_time_timestamp)
    current_time = datetime.datetime.now()
    uptime_delta = current_time - boot_time_datetime

    days = uptime_delta.days
    hours, remainder = divmod(uptime_delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    mem = psutil.virtual_memory()
    total_mem_gb = mem.total / (1024**3)
    available_mem_gb = mem.available / (1024**3)
    used_mem_gb = mem.used / (1024**3)

    info = {"OS"                   : platform.system() + " " + platform.release(),
            "HOST"                 : platform.node(),
            "UP TIME"              : f"{days} days, {hours} hours, {minutes} minutes",
            "RESOLUTION"           : width + "x" + height,
            "ARCHITECTURE"         : platform.machine(),
            "PROCESSOR"            : platform.processor(),
            "MEMORY"               : f"{used_mem_gb:.2f} GiB / {total_mem_gb:.2f} GiB (Available : {available_mem_gb:.2f} GiB)",
            }
    for i in list(info.keys()):
        print(i, info[i])

    while not keyboard.is_pressed("esc"):
        pass


def pipes_screen():
    
    size = os.get_terminal_size()
    width = size.columns
    height = size.lines

    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32

    pipes = {
        "║" : [ [[ 0, 1], [ 0, 1]], [[ 0,-1], [ 0,-1]] ],
        "═" : [ [[ 1, 0], [ 1, 0]], [[-1, 0], [-1, 0]] ],
        "╔" : [ [[ 0,-1], [ 1, 0]], [[-1, 0], [ 0, 1]] ],
        "╗" : [ [[ 0,-1], [-1, 0]], [[ 1, 0], [ 0, 1]] ],
        "╚" : [ [[ 0, 1], [ 1, 0]], [[-1, 0], [ 0,-1]] ],
        "╝" : [ [[ 0, 1], [-1, 0]], [[ 1, 0], [ 0,-1]] ]
    }
    all_directions = list(pipes.values())
    all_pipes = list(pipes.keys())

    direction = [[0,1],[0,1]]
    pos = [random.randint(1,width-1),random.randint(1,height-1)]
    directionint = a = 2
    directionint_to_direction = {
        "1":[-1, 0],
        "2":[ 0,-1],
        "3":[ 1, 0],
        "4":[ 0, 1]
    }
    length_need_to_be_travelled = 1

    """
        2
        |
     1--+--3
        |
        4
    """

    screen = []
    makeScreen(screen, width, height)
    running = True

    while running:

        size = os.get_terminal_size()
        width = size.columns
        height = size.lines      
            
        active_window = user32.GetForegroundWindow()
        current_window = kernel32.GetConsoleWindow()
        
        direction[0] = direction[1]

        if length_need_to_be_travelled == 0:
            length_need_to_be_travelled += 1
            a = random.randint(1,4)
        
        if (directionint == 1 and a == 3) or (directionint == 3 and a == 1) or (directionint == 2 and a == 4) or (directionint == 4 and a == 2):
            a = directionint

        if a == directionint or a > 4:
            pos[0] += direction[0][0]
            pos[1] += direction[0][1]
            length_need_to_be_travelled -= 1
        else:
            length_need_to_be_travelled = random.randint(3,15)
            directionint = a
            direction[1] = directionint_to_direction[str(directionint)]
            
        if pos[0] > width-1:
            pos[0] = 0
        if pos[0] < 0:
            pos[0] = width-1
        if pos[1] > height-1:
            pos[1] = 0
        if pos[1] < 0:
            pos[1] = height-1

        for i in range(len(pipes)):
            if direction in all_directions[i]:
                screen[pos[1]][pos[0]] = all_pipes[i]
        
        if active_window == current_window:

            if keyboard.is_pressed("esc"):
                running = False

        output(screen)
        time.sleep(0.01)


def dvd_screen():

    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32

    dvd_pos = [1,1]
    x_direction = 1
    y_direction = 1

    running = True

    colors = ["\033[38;2;255;0;0m", "\033[38;2;0;255;0m", "\033[38;2;0;0;255m", "\033[38;2;255;255;m", "\033[38;2;255;0;255m", "\033[38;2;0;255;255m", "\033[38;2;255;255;255m"]
    color_number = random.randint(0,len(colors)-1)

    while running:

        size = os.get_terminal_size()
        width = size.columns
        height = size.lines

        active_window = user32.GetForegroundWindow()
        current_window = kernel32.GetConsoleWindow()

        highest_dvd_x_pos = width-3
        highest_dvd_y_pos = height-1

        screen = []

        makeScreen(screen, width, height)

        dvd_pos[0] += x_direction
        dvd_pos[1] += y_direction

        if not(1 <= dvd_pos[0] < highest_dvd_x_pos):
            if x_direction == 1:
                x_direction = -1
            elif x_direction == -1:
                x_direction = 1
            color_number = random.randint(0,len(colors)-1)
        if not(1 <= dvd_pos[1] < highest_dvd_y_pos):
            if y_direction == 1:
                y_direction = -1
            elif y_direction == -1:
                y_direction = 1
            color_number = random.randint(0,len(colors)-1)

        if dvd_pos[0] > highest_dvd_x_pos:
            dvd_pos[0] = highest_dvd_x_pos
        elif dvd_pos[0] < 0:
            dvd_pos[0] = 0

        if dvd_pos[1] > highest_dvd_y_pos:
            dvd_pos[1] = highest_dvd_y_pos
        elif dvd_pos[1] < 0:
            dvd_pos[1] = 0

        screen[dvd_pos[1]][dvd_pos[0]] = colors[color_number] + "D" + "\033[0m"
        screen[dvd_pos[1]][dvd_pos[0]+1] = colors[color_number] + "V" + "\033[0m"
        screen[dvd_pos[1]][dvd_pos[0]+2] = colors[color_number] + "D" + "\033[0m"

        
        if active_window == current_window:

            if keyboard.is_pressed("esc"):
                running = False

        output(screen)
        time.sleep(0.03)


def auto_clicker():

    os.system("cls")
    mouse = Controller()

    print("press enter to start the program")

    while not keyboard.is_pressed("enter"):
        input()
        
    delay = float(input("start autoclicking after how many seconds : "))
    each_delay = float(input("delay between each click in seconds : "))
    button = int(input("button to click, 0 for left, 1 for right"))

    if button:
        button = Button.right
    else:
        button = Button.left

    print("press esc to stop")

    time.sleep(delay)
    
    while not keyboard.is_pressed("esc"):
        mouse.click(button)
        time.sleep(each_delay)


def file_manager_screen():
    
    init_variables()

    select = 0
    path = config["Main Path"]
    available_drives = list_drives()

    up_key_pressed = False
    down_key_pressed = False
    esc_pressed = False
    right_key_pressed = False
    left_key_pressed = False

    running = True

    while running:

        update_size()

        active_window = user32.GetForegroundWindow()
        current_window = kernel32.GetConsoleWindow()

        screen = []

        makeScreen(screen, width, height)

        formatted_path = "\\".join(path)+"\\"
        if path != []:
            directories = os.listdir(formatted_path)
        else:
            directories = available_drives

        for x in range(len(formatted_path)):
            try:
                screen[2][x+2] = "\033[48;2;135;135;135m\033[38;2;100;0;200m" + formatted_path[x] + "\033[0m"
            except:
                break

        for y in range(len(directories)):
            try:
                if y != 0:
                    for x in range(len(directories[y+select])):
                        try:
                            screen[y*2+4][x+3] = directories[y+select][x]
                        except:
                            break
                else:
                    for x in range(len(directories[y+select])):
                        try:
                            screen[y*2+4][x+2] = "\033[48;2;255;255;255m\033[38;2;0;0;0m" + directories[y+select][x] + "\033[0m"
                        except:
                            break
            except:
                break

        
        if active_window == current_window:

            if keyboard.is_pressed("up") and select > 0 and not up_key_pressed:
                select -= 1
                up_key_pressed = True
            
            elif not keyboard.is_pressed("up"):
                up_key_pressed = False

            if keyboard.is_pressed("down") and select < len(directories)-1 and not down_key_pressed:
                select += 1
                down_key_pressed = True
            
            elif not keyboard.is_pressed("down"):
                down_key_pressed = False

            if keyboard.is_pressed("right") and not right_key_pressed:
                path.append(directories[select])
                try:
                    os.listdir("/".join(path)+"/")
                except PermissionError as e:
                    os.system("cls")
                    print("permission denied")
                    time.sleep(0.5)
                    path.pop()
                except NotADirectoryError as e:
                    os.startfile("/".join(path))
                    path.pop()
                select = 0
                right_key_pressed = True
            
            elif not keyboard.is_pressed("right"):
                right_key_pressed = False

            if keyboard.is_pressed("left") and not left_key_pressed and len(path) != 0:
                path.pop()
                select = 0
                left_key_pressed = True
            
            elif not keyboard.is_pressed("left"):
                left_key_pressed = False

            if keyboard.is_pressed("esc") and not esc_pressed:
                running = False

            elif not keyboard.is_pressed("esc"):
                esc_pressed = False

        output(screen)
        time.sleep(0.001)


def to_do_screen():
    
    init_variables()
    
    to_do_data = get_to_do_data()

    insert_key_pressed = False
    del_key_pressed = False
    shift_key_pressed = False
    up_key_pressed = False
    down_key_pressed = False
    enter_key_pressed = True

    rgb = [0,127,255]
    increase_rgb = [1,1,1]

    select = 1
    start_element = 0
    running = True

    while running:

        active_window = user32.GetForegroundWindow()
        current_window = kernel32.GetConsoleWindow()

        size = os.get_terminal_size()
        width = size.columns
        height = size.lines

        screen = []
        start_element = select-1

        
        if keyboard.is_pressed("shift") and active_window == current_window:
            makeScreen(screen, width, height-1)
            shift_key_pressed = True
        else:
            makeScreen(screen, width, height)
            shift_key_pressed = False

        for y in range((height//2)-1):

            try:
                to_do_data[y+start_element][1]
            except:
                break

            ticked = False

            if int(to_do_data[y+start_element][1]):
                screen[y*2+1][2] = "\033[38;2;0;255;0m\u221A\033[0m"
                ticked = True
            else:
                screen[y*2+1][2] = "\033[38;2;255;0;0mX\033[0m"

            screen[y*2+1][4] = f"\033[38;2;{configuration["To Do List Color"][0][0]};{configuration["To Do List Color"][0][1]};{configuration["To Do List Color"][0][2]}m "

            for x in range(width - 6):
                if len(str(to_do_data[y+start_element][0]))-2 < x:
                    break

                screen[y*2+1][x+5] = str(to_do_data[y+start_element][0])[x]

            screen[y*2+1][width-6] = f" \033[0m"

            if y == 0:
                for x in range(width - 2):
                    try:
                        screen[y*2+1][x+2]
                    except:
                        break
                    screen[y*2+1][x+1] = f"\033[48;2;{str(rgb[0])};{str(rgb[1])};{str(rgb[2])}m\033[38;2;0;0;0m" + screen[y*2+1][x+2] + "\033[0m"

        rgb[0] += increase_rgb[0]
        if rgb[0] > 255:
            increase_rgb[0] = -1
            rgb[0] = 255
        if rgb[0] < 0:
            increase_rgb[0] = 1
            rgb[0] = 0

        rgb[1] += increase_rgb[1]
        if rgb[1] > 255:
            increase_rgb[1] = -1
            rgb[1] = 255
        if rgb[1] < 0:
            increase_rgb[1] = 1
            rgb[1] = 0

        rgb[2] += increase_rgb[2]
        if rgb[2] > 255:
            increase_rgb[2] = -1
            rgb[2] = 255
        if rgb[2] < 0:
            increase_rgb[2] = 1
            rgb[2] = 0

        
        if active_window == current_window:

            if keyboard.is_pressed("esc"):
                running = False

            if keyboard.is_pressed("del") and not del_key_pressed:
                to_do_data.pop(select-1)
                if select > len(to_do_data):
                    select = len(to_do_data)
                del_key_pressed = True
            elif not keyboard.is_pressed("del"):
                del_key_pressed = False

            if keyboard.is_pressed("insert") and not insert_key_pressed:
                to_do_data.insert(select,["","0"])
                insert_key_pressed = True
            elif not keyboard.is_pressed("insert"):
                insert_key_pressed = False

            if keyboard.is_pressed("up") and select > 1 and not up_key_pressed:
                select -= 1
                up_key_pressed = True
            
            elif not keyboard.is_pressed("up"):
                up_key_pressed = False

            if keyboard.is_pressed("down") and select < len(to_do_data) and not down_key_pressed:
                select += 1
                down_key_pressed = True
            
            elif not keyboard.is_pressed("down"):
                down_key_pressed = False

            if keyboard.is_pressed("enter") and not enter_key_pressed:
                if to_do_data[select-1][1] == "1":
                    to_do_data[select-1][1] = "0"
                elif to_do_data[select-1][1] == "0":
                    to_do_data[select-1][1] = "1"
                enter_key_pressed = True
            
            elif not keyboard.is_pressed("enter"):
                enter_key_pressed = False

            if shift_key_pressed:
                text = input(" " + str(select) + ": ") + " "
                to_do_data[select-1][0] = text
                enter_key_pressed = True

            if keyboard.is_pressed("ctrl"):
                os.system("cls")
                print(to_do_data[select-1][0])
                while active_window == current_window and keyboard.is_pressed("ctrl"):
                    time.sleep(0.01)

        output(screen)
        time.sleep(0.01)

    set_to_do_data(to_do_data)


def main_screen():
    """The main menu"""

    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32
    
    if len(sys.argv) > 1:
        unique_title = sys.argv[1]
        kernel32.SetConsoleTitleW(unique_title)

    os.system("")
    size = os.get_terminal_size()
    width = size.columns
    height = size.lines

    options_and_screens = {"[ ] About"          : about_screen         ,
                           "[ ] DVD"            : dvd_screen           ,
                           "[ ] Pipes"          : pipes_screen         ,
                           "[ ] Matrix"         : matrix_screen        ,
                           "[ ] Calculator"     : calculator_screen    ,
                           "[ ] Game of Life"   : game_of_life_screen  ,
                           "[ ] A Shooter Game" : a_shooter_game_screen,
                           "[ ] To-do List"     : to_do_screen         ,
                           "[ ] File Manager"   : file_manager_screen  ,
                           "[ ] Auto Clicker"   : auto_clicker         ,
                           "[ ] Settings"       : settings_screen      }
    options = list(options_and_screens.keys())
    screens = list(options_and_screens.values())
    select = 0
    
    up_pressed = False
    down_pressed = False
    esc_pressed = False

    rgb = [0,127,255]
    increase_rgb = [1,1,1]

    running = True

    while running:

        active_window = user32.GetForegroundWindow()
        current_window = kernel32.GetConsoleWindow()

        size = os.get_terminal_size()
        width = size.columns
        height = size.lines

        screen = []

        makeScreen(screen, width, height)

        for i in range(len(options)):

            for j in range(len(options[i])):
                try:
                    screen[i+2][j+2] = f"\033[38;2;{str(rgb[0])};{str(rgb[1])};{str(rgb[2])}m" + options[i][j] + "\033[0m"
                except:
                    break

            if select == i:
                screen[i+2][3] = "\267"

        rgb[0] += increase_rgb[0]
        if rgb[0] > 255:
            increase_rgb[0] = -1
            rgb[0] = 255
        if rgb[0] < 0:
            increase_rgb[0] = 1
            rgb[0] = 0

        rgb[1] += increase_rgb[1]
        if rgb[1] > 255:
            increase_rgb[1] = -1
            rgb[1] = 255
        if rgb[1] < 0:
            increase_rgb[1] = 1
            rgb[1] = 0

        rgb[2] += increase_rgb[2]
        if rgb[2] > 255:
            increase_rgb[2] = -1
            rgb[2] = 255
        if rgb[2] < 0:
            increase_rgb[2] = 1
            rgb[2] = 0

        if active_window == current_window:

            if keyboard.is_pressed("up") and select > 0 and not up_pressed:
                select -= 1
                up_pressed = True
            elif not keyboard.is_pressed("up"):
                up_pressed = False
            
            if keyboard.is_pressed("down") and select < len(options)-1 and not down_pressed:
                select += 1
                down_pressed = True
            elif not keyboard.is_pressed("down"):
                down_pressed = False

            if keyboard.is_pressed("enter"):
                os.system("cls")
                screens[select]()
                esc_pressed = True

            if keyboard.is_pressed("esc") and not esc_pressed:
                running = False

            elif not keyboard.is_pressed("esc"):
                esc_pressed = False

        output(screen)
        time.sleep(0.001)


if __name__ == "__main__":
    main_screen()

import os
import keyboard
import time
import random
import ctypes
import sys
import platform
import subprocess
import psutil
import datetime
from pynput.mouse import Controller, Button


def list_drives():
    
    drives = []
    for letter in range(ord('A'), ord('Z') + 1):
        drive = f"{chr(letter)}:\\"
        if os.path.exists(drive):
            drives.append(drive)
    return drives


def get_to_do_data():
    """Get the data for the todo list from the txt file"""

    with open("to-do-data.txt","r+") as data:
        data = data.readlines()
    modified_data = []
    
    for i in range(len(data)//2):
        if data[i*2][-1] =="\n": a = data[i*2][0:-1]
        else: a = data[i*2]
        if data[(i*2)+1][-1] =="\n": b = data[(i*2)+1][0:-1]
        else: b = data[(i*2)+1]
        modified_data.append([a, b])

    return modified_data


def set_to_do_data(to_do_data):
    """Get the data for the todo list from the txt file"""

    modified_data = []
    for i in to_do_data:
        modified_data.append(i[0])
        modified_data.append(i[1])

    with open("to-do-data.txt","r+") as data:
        data.truncate()
        data.write("\n".join(modified_data))
    

def colorise_logo(logo):
    
    logo = str(logo)
    logo = list(logo.split("-"))
    new_logo = ""

    for i in logo:
        if i == "":
            continue
        if not (i[0] in ["m",";"]):
            new_logo += i
        elif not (i[0] in ["m"]):
            j = list(i.split(";"))
            new_logo += f"\033[38;2;{ j[1] };{ j[2] };{ j[3] }m"
        else:
            new_logo += f"\033[0m"


    return new_logo


def output(screen):

    formatted_screen = []
    for line in range(len(screen)):
        a = ""
        for char in range(len(screen[line])):
            a += screen[line][char]
        formatted_screen.append(a)
    print("\n"*50+"".join(formatted_screen)[0:-1], end="")


def makeScreen(screen, width, height):
    """Makes an empty screen with border"""

    for y in range(height):
        screen.append([])
        for x in range(width):
            screen[y].append(" ")


class Vertical_Text():

    def __init__(self, width:int):
        self.length = random.randint(7, 20)
        self.characters = []
        for i in range(self.length):
            self.characters.append(chr(random.randint(32, 126)))
        self.position = [random.randint(0, width-1), -self.length]

    def move(self, height:int):
        self.position[1] += 1
        if self.position[1] > height-1:
            return True
        return False
    
    def add_to_screen(self, screen:list):
        for i in range(len(self.characters)):
            try:
                if self.position[1]+i >-1:
                    screen[self.position[1]+i][self.position[0]] = "\033[38;2;0;255;0m" + self.characters[i] + "\033[0m"
            except IndexError as e:
                break
            finally:
                try:
                    screen[self.position[1]-1][self.position[0]] = " "
                except IndexError as e:
                    break



def matrix_screen():

    # size = os.get_terminal_size()
    # width = size.columns
    # height = size.lines

    # user32 = ctypes.windll.user32
    # kernel32 = ctypes.windll.kernel32

    # screen = []
    # running = True

    # texts = []
    # spawn_a_text = 0

    # while running:

    #     size = os.get_terminal_size()
    #     width = size.columns
    #     height = size.lines      

    #     screen = []
    #     makeScreen(screen, width, height)

    #     active_window = user32.GetForegroundWindow()
    #     current_window = kernel32.GetConsoleWindow()

    #     spawn_a_text = random.randint(0, 6)
                
    #     if spawn_a_text < 1:
    #         texts.append(Vertical_Text(width))
            
    #     at_end = []
    #     for i in range(len(texts)):
    #         if texts[i].move(height):
    #             at_end.append(i)
    #         texts[i].add_to_screen(screen)
            
    #     for i in range(len(at_end)-1, -1, -1):
    #         texts.pop(i)

    #     if active_window == current_window:

    #         if keyboard.is_pressed("esc"):
    #             running = False

    #     output(screen)
    #     time.sleep(0.01)

    try:
        # Call the external C++ program
        subprocess.run(["./matrix_program.exe"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the matrix program: {e}")
    except FileNotFoundError:
        print("The matrix program executable was not found.")




def about_screen():

    with open(f"custom_logo_file_path.txt", "r") as custom_logo_file_path:
        
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
            "MEMORY"               : f"{used_mem_gb} GiB / {total_mem_gb} GiB"
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

    print("press space to start the program")

    while not keyboard.is_pressed("enter"):
        input()
        
    delay = int(input("start autoclicking after how many seconds : "))
    each_delay = int(input("delay between each click in seconds : "))
    button = int(input("button to click, 0 for left, 1 for right"))

    if button:
        button = Button.right
    else:
        button = Button.left

    print("press esc to stop")

    for i in reversed(range(delay)):
        print(i+1)
        time.sleep(1)
    
    while not keyboard.is_pressed("esc"):
        mouse.click(button)
        time.sleep(each_delay)


def terminal_screen():

    os.system("cls")

    size = os.get_terminal_size()
    width = size.columns
    height = size.lines

    path = ["C:"]
    
    up_key_pressed = False
    down_key_pressed = False
    esc_pressed = False
    right_key_pressed = False
    left_key_pressed = False

    running = True

    while running:

        size = os.get_terminal_size()
        width = size.columns
        height = size.lines

        screen = []

        makeScreen(screen, width, height)

        formatted_path = "\\".join(path)+"\\"
        command = input("\033[48;2;255;255;0m\033[38;2;0;0;0m" + formatted_path + " \033[0m" + "\033[48;2;255;255;0m\033[38;2;0;0;0m" + "\u25BA" + " \033[0m")

        os.system(command)

        time.sleep(0.001)

        if keyboard.is_pressed("esc") and not esc_pressed:
            running = False

        elif not keyboard.is_pressed("esc"):
            esc_pressed = False


def file_manager_screen():
    
    size = os.get_terminal_size()
    width = size.columns
    height = size.lines

    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32

    select = 0
    path = ["C:"]
    available_drives = list_drives()

    up_key_pressed = False
    down_key_pressed = False
    esc_pressed = False
    right_key_pressed = False
    left_key_pressed = False

    running = True

    while running:

        size = os.get_terminal_size()
        width = size.columns
        height = size.lines

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
                        screen[y*2+4][x+3] = directories[y+select][x]
                else:
                    for x in range(len(directories[y+select])):
                        screen[y*2+4][x+2] = "\033[48;2;255;255;255m\033[38;2;0;0;0m" + directories[y+select][x] + "\033[0m"
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

    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32

    to_do_data = get_to_do_data()
    size = os.get_terminal_size()
    width = size.columns
    height = size.lines

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

                if not(start_element > select):

                    ticked = False

                    if int(to_do_data[y+start_element][1]):
                        screen[y*2+2][3] = "\u221A"
                        ticked = True
                    else:
                        screen[y*2+2][3] = "X"

                    for x in range(len(to_do_data[y+start_element][0])):
                        if ticked:
                            screen[y*2+2][x+6] = "\033[4m" + str(to_do_data[y+start_element][0])[x] + "\033[0m"
                        else:
                            screen[y*2+2][x+6] = str(to_do_data[y+start_element][0])[x]

                    if y == 0:
                        for x in range(width - 4):
                            screen[y*2+2][x+2] = f"\033[48;2;{str(rgb[0])};{str(rgb[1])};{str(rgb[2])}m\033[38;2;0;0;0m" + screen[y*2+2][x+3] + "\033[0m"

            except:
                pass

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
                
                text = input(" " + str(select) + ": ")
                to_do_data[select-1][0] = text
                enter_key_pressed = True

        output(screen)
        time.sleep(0.01)

    set_to_do_data(to_do_data)


def main_screen():
    """The main menu"""

    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32
    
    unique_title = sys.argv[1]
    kernel32.SetConsoleTitleW(unique_title)

    os.system("")
    size = os.get_terminal_size()
    width = size.columns
    height = size.lines

    options_and_screens = {"[ ] About" : about_screen,
                           "[ ] To-do List" : to_do_screen,
                           "[ ] Terminal" : terminal_screen,
                           "[ ] File Manager" : file_manager_screen,
                           "[ ] DVD" : dvd_screen,
                           "[ ] Pipes" : pipes_screen,
                           "[ ] Matrix" : matrix_screen,
                           "[ ] Auto Clicker" : auto_clicker}
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

                screen[i+2][j+2] = f"\033[38;2;{str(rgb[0])};{str(rgb[1])};{str(rgb[2])}m" + options[i][j] + "\033[0m"
            
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

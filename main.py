import os
import keyboard
import time
import random
from pynput.mouse import Controller, Button


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
        if y == 0 or y == height-1:
            screen[y].append(" ")
            for x in range(width-2):
                screen[y].append("#")
            screen[y].append(" ")
        else:
            screen[y].append("#")
            for x in range(width-2):
                screen[y].append(" ")
            screen[y].append("#")
            


def pipes_screen():
    
    size = os.get_terminal_size()
    width = size.columns
    height = size.lines

    pipes = {
        "║" : [ [[ 0, 1], [ 0, 1]], [[ 0,-1], [ 0,-1]] ],
        "=" : [ [[ 1, 0], [ 1, 0]], [[-1, 0], [-1, 0]] ],
        "╔" : [ [[ 0,-1], [ 1, 0]], [[-1, 0], [ 0, 1]] ],
        "╗" : [ [[ 0,-1], [-1, 0]], [[ 1, 0], [ 0, 1]] ],
        "╚" : [ [[ 0, 1], [ 1, 0]], [[-1, 0], [ 0,-1]] ],
        "╝" : [ [[ 0, 1], [-1, 0]], [[ 1, 0], [ 0,-1]] ]
    }
    all_directions = list(pipes.values())
    all_pipes = list(pipes.keys())

    direction = [[0,1],[0,1]]
    pos = [random.randint(1,width-1),random.randint(1,height-1)]
    directionint = 2
    directionint_to_direction = {
        "1":[-1, 0],
        "2":[ 0,-1],
        "3":[ 1, 0],
        "4":[ 0, 1]
    }

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
            
        direction[0] = direction[1]

        a = random.randint(1,15)
        
        if (directionint == 1 and a == 3) or (directionint == 3 and a == 1) or (directionint == 2 and a == 4) or (directionint == 4 and a == 2):
            a = directionint

        if a == directionint or a > 4:
            pos[0] += direction[0][0]
            pos[1] += direction[0][1]
        else:
            directionint = a
            direction[1] = directionint_to_direction[str(directionint)]
            
        if pos[0] > width-2:
            pos[0] = 1
        if pos[0] < 1:
            pos[0] = width-2
        if pos[1] > height-2:
            pos[1] = 1
        if pos[1] < 1:
            pos[1] = height-2

        for i in range(len(pipes)):
            if direction in all_directions[i]:
                screen[pos[1]][pos[0]] = all_pipes[i]

        if keyboard.is_pressed("esc"):
            running = False

        output(screen)
        time.sleep(0.001)


def dvd_screen():
    dvd_pos = [1,1]
    x_direction = 1
    y_direction = 1
    running = True

    while running:

        size = os.get_terminal_size()
        width = size.columns
        height = size.lines

        highest_dvd_x_pos = width-4
        highest_dvd_y_pos = height-2

        screen = []

        makeScreen(screen, width, height)

        dvd_pos[0] += x_direction
        dvd_pos[1] += y_direction

        if not(1 <= dvd_pos[0] < highest_dvd_x_pos):
            if x_direction == 1:
                x_direction = -1
            elif x_direction == -1:
                x_direction = 1
        if not(1 <= dvd_pos[1] < highest_dvd_y_pos):
            if y_direction == 1:
                y_direction = -1
            elif y_direction == -1:
                y_direction = 1

        if dvd_pos[0] > highest_dvd_x_pos:
            dvd_pos[0] = highest_dvd_x_pos
        elif dvd_pos[0] < 1:
            dvd_pos[0] = 1

        if dvd_pos[1] > highest_dvd_y_pos:
            dvd_pos[1] = highest_dvd_y_pos
        elif dvd_pos[1] < 1:
            dvd_pos[1] = 1

        screen[dvd_pos[1]][dvd_pos[0]] = "D"
        screen[dvd_pos[1]][dvd_pos[0]+1] = "V"
        screen[dvd_pos[1]][dvd_pos[0]+2] = "D"

        if keyboard.is_pressed("esc"):
            running = False

        output(screen)
        time.sleep(0.07)


def auto_clicker():

    size = os.get_terminal_size()
    width = size.columns
    height = size.lines

    screen = []
    os.system("cls")
    mouse = Controller()

    print("press space to start the program")

    while not keyboard.is_pressed("space"):
        pass

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


def file_manager_screen():
    pass


def to_do_screen():

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

    select = 1
    start_element = 0
    end_element = start_element + (height//2) - 1
    running = True

    while running:
        size = os.get_terminal_size()
        width = size.columns
        height = size.lines

        screen = []
        start_element = select-1
        end_element = start_element + ((height)//2)-1

        if keyboard.is_pressed("shift"):
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
                            screen[y*2+2][x+2] = "\033[48;2;255;255;255m\033[38;2;0;0;0m" + screen[y*2+2][x+3] + "\033[0m"

            except:
                pass

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
            to_do_data.insert(0,["","0"])
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

    os.system("")
    size = os.get_terminal_size()
    width = size.columns
    height = size.lines

    options_and_screens = {"[ ] To-do List" : to_do_screen,
                           "[ ] Terminal" : None,
                           "[ ] File Manager" : None,
                           "[ ] DVD" : dvd_screen,
                           "[ ] Pipes" : pipes_screen,
                           "[ ] Auto Clicker" : auto_clicker}
    options = list(options_and_screens.keys())
    screens = list(options_and_screens.values())
    select = 0
    
    up_pressed = False
    down_pressed = False
    esc_pressed = False

    running = True

    while running:

        size = os.get_terminal_size()
        width = size.columns
        height = size.lines

        screen = []

        makeScreen(screen, width, height)

        for i in range(len(options)):

            for j in range(len(options[i])):
                screen[i+2][j+2] = options[i][j]
            
            if select == i:
                screen[i+2][3] = "\267"

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

        output(screen)
        time.sleep(0.001)

        if keyboard.is_pressed("enter"):
            screens[select]()
            esc_pressed = True

        if keyboard.is_pressed("esc") and not esc_pressed:
            running = False

        elif not keyboard.is_pressed("esc"):
            esc_pressed = False



if __name__ == "__main__":
    main_screen()

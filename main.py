import os
import keyboard
import time


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



def dvd_screen():
    dvd_pos = [1,1]
    running = True

    while running:

        size = os.get_terminal_size()
        width = size.columns
        height = size.lines

        highest_dvd_x_pos = width-2
        highest_dvd_y_pos = height-1

        screen = []

        makeScreen(screen, width, height)

        if not(dvd_pos[0] < highest_dvd_x_pos or dvd_pos[1] < highest_dvd_y_pos):
            dvd_pos[0] += 1
            dvd_pos[1] += 1

        screen[dvd_pos[1]][dvd_pos[0]] = "D"
        screen[dvd_pos[1]][dvd_pos[0]+1] = "V"
        screen[dvd_pos[1]][dvd_pos[0]+2] = "D"

        if keyboard.is_pressed("esc"):
            running = False

        output(screen)
        time.sleep(0.05)


def to_do_screen():

    to_do_data = get_to_do_data()
    size = os.get_terminal_size()
    width = size.columns
    height = size.lines

    valid_keys = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","1","2","3","4","5","6","7","8","9","0"]

    ticking_key_pressed = True
    key_press_order = 0

    select = 1

    running = True

    while running:

        size = os.get_terminal_size()
        width = size.columns
        height = size.lines

        screen = []

        makeScreen(screen, width, height)

        # adding the to do list to the screen

        for y in range(len(to_do_data)):
            
            ticked = False
            
            if int(to_do_data[y][1]):
                screen[y*2+4][3] = "\u221A"
                ticked = True
            else:
                screen[y*2+4][3] = "X"

            for x in range(len(to_do_data[y][0])):
                if ticked:
                    screen[y*2+4][x+6] = "\033[4m" + str(to_do_data[y][0])[x] + "\033[0m"
                else:
                    screen[y*2+4][x+6] = str(to_do_data[y][0])[x]

            if select == y+1:
                for x in range(width - 4):
                    screen[y*2+4][x+2] = "\033[48;2;255;255;255m\033[38;2;0;0;0m" + screen[y*2+4][x+3] + "\033[0m"             

        if keyboard.is_pressed("esc"):
            running = False
        
        if keyboard.is_pressed("up") and select >= 0 and not up_pressed:
            select -= 1
            up_pressed = True
        elif not keyboard.is_pressed("up"):
            up_pressed = False
        
        if keyboard.is_pressed("down") and select <= len(to_do_data)-1 and not down_pressed:
            select += 1
            down_pressed = True
        elif not keyboard.is_pressed("down"):
            down_pressed = False

        if keyboard.is_pressed("enter") and not ticking_key_pressed:
            if to_do_data[select-1][1] == "1":
                to_do_data[select-1][1] = "0"
            elif to_do_data[select-1][1] == "0":
                to_do_data[select-1][1] = "1"
            print(to_do_data[select-1][1])
            ticking_key_pressed = True
        elif not keyboard.is_pressed("enter"):
            ticking_key_pressed = False
        
        pressed_key = keyboard.read_key()

        
        if pressed_key == "space":
            to_do_data[select-1][0] = to_do_data[select-1][0] + " "
        elif pressed_key == "backspace":
            to_do_data[select-1][0] = to_do_data[select-1][0][0:-1]
        elif pressed_key in valid_keys:
            to_do_data[select-1][0] = to_do_data[select-1][0] + pressed_key

        output(screen)
        time.sleep(0.05)

    set_to_do_data(to_do_data)


def main_screen():
    """The main menu"""

    os.system("")
    size = os.get_terminal_size()
    width = size.columns
    height = size.lines

    options_and_screens = {"[ ] To-do List" : to_do_screen,
                           "[ ] Terminal" : None,
                           "[ ] DVD" : None}
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

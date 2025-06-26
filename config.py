import json
import time


config = json.load(open("config.json"))
config_keys = list(config.keys())
config_values = list(config.values())


def get_config():
    return config


def update_config(given_configuration):
    with open("config.json", "w") as out_file:
        json.dump(given_configuration, out_file, indent = 6)


def get_input(select):
    settings_type = config_values[select][1]

    if settings_type == "unchangable":
        pass
    elif settings_type == "rgb":
        config_values[select][0] = rgb_input()
    elif settings_type == "text":
        config_values[select][0] = input(f"Give {config_keys[select]} : ")


# Checks Values limit and corrects
def check_value_limit(val : int, type : str):
    if val < 0:
        val = 0
        print(f"The {type} value should be more than 0! (it has been set to 0 for now)")
        time.sleep(1)
    elif val > 255:
        val = 255
        print(f"The {type} value should be less than 255! (it has been set to 255 for now)")
        time.sleep(1)
    return val


# A function that takes input for RGB values and checks if the values are in the correct range (0 to 255)
def rgb_input():

    r = int(input("Give red value (0 to 255) : "))
    r = check_value_limit(r, "red")
    
    g = int(input("Give green value (0 to 255) : "))
    g = check_value_limit(g, "green")

    b = int(input("Give blue value (0 to 255) : "))
    b = check_value_limit(b, "blue")

    return [str(r), str(g), str(b)]

def format_settings_screen(configuration : list, screen_width : int, select : int):
    formatted_configuration = ""
    keys = list(configuration.keys())

    for index in range(len(configuration)):
        i = configuration[keys[index]]

        if select == index:
            formatted_configuration += f" {keys[index]}{(screen_width-len(keys[index])-len(str(i[0]))-2)*" "}\033[38;2;0;0;0m\033[48;2;255;255;255m{i[0]}\033[0m\n"    
            continue

        formatted_configuration += f" {keys[index]}{(screen_width-len(keys[index])-len(str(i[0]))-2)*" "}{i[0]}\n"

    return formatted_configuration
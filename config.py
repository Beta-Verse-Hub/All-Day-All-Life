import json


config = json.load(open("config.json"))


types = ("unchangable",
         "rgb",
         "text",
         "value")


def get_config():
    return config

def check_value_limit(val, type):
    if val < 0:
        val = 0
        print(f"The {type} value should be more than 0! (it has been set to 0 for now)")
    elif val > 255:
        val = 255
        print(f"The {type} value should be less than 255! (it has been set to 255 for now)")


# A function that takes input for RGB values and checks if the values are in the correct range (0 to 255)
def rgb_input():

    r = input("Give red value (0 to 255) : ")
    check_value_limit(r, "red")
    
    g = input("Give green value (0 to 255) : ")
    check_value_limit(g, "green")

    b = input("Give blue value (0 to 255) : ")
    check_value_limit(b, "blue")

    return [r, g, b]
    
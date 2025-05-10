def output(screen):
    for y in screen:
        for x in y:
            print(x, end="")
        print()


def makeScreen(screen, width, height):
    for y in range(height):
        screen.append([])
        if y == 0 or y == height-1:
            for x in range(width):
                screen[y].append("#")
        else:
            screen[y].append("#")
            for x in range(width-2):
                screen[y].append(" ")
            screen[y].append("#")


if __name__ == "__main__":
    width = 100
    height = 40
    screen = []
    makeScreen(screen, width, height)
    output(screen)
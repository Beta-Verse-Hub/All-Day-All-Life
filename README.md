# ALL DAY ALL LIFE
Ever wanted to run re is a game in progress to pipes.sh, cmatrix, etc on your terminal but then you realised that you need to setup WSL for that because you are a windows user which you think might take time. That is why, I have made this project named **All Day All Life** which contains not only a replica of those scripts but also a to do list, a file manager, an auto clicker, etc. with a cli-based interface

Note: This program is windows-only

## Installation
This program uses the following libraries(the ones that are not preinstalled are marked with *):

python :-

- datetime
- os
- time
- random
- ctypes
- sys
- platform
- subprocess
- keyboard*
- pynput*
- psutil*

c++ :-

- iostream
- vector
- cstdlib
- ctime
- string
- conio.h
- windows.h

To download the non-preinstalled ones type the following command:

```pip install -r requirements.txt```


Then, download the source code from this github repository and place it in the same directory as the main.py file.

## Running it
To run the program, simply execute the main.py file on the standard cmd:

```python main.py```

This will launch a window manager program which uses windows' title for management.
It will show a list containing the windows' title and it position according to the grid (default grid size is (4,4)).

esc - stop the program.
shift - to add a screen according to it's title
- if it exists - it will add the title to list an then you can manupulate it's place.
- if it doesn't exists - it will make a new window will run the main_program.py and maximize it.
Main_program.py will launch the main menu, where you can select from various options such as "About", "To-do List",  "File Manager", "DVD", "Pipes", "Matrix", and "Auto Clicker".
ctrl - change the grid size
tab + arrow keys - to change the place of the selected screen according to the screen
alt + arrow keys - to change the size of the selected screen according to the screen

### About
It is a replica of neofetch but it uses the windows api so it is exclusive for windows.
You can make your own custom logo with this syntax:-

```-;r;g;b- part of the logo -m- -;r2;g2;b2- other part of the logo -m- ...```

-;r;g;b- => set the rgb value in decimals integer.
part of the logo => the logo's part in ascii art form
-m- => to stop using the previous color

It uses ANSI sequences to display colored text, so using ```-m-``` before each new color and at the end is necessary.

Make the logo in a txt file, save it in the Logos directory and add it's correct path to the custom_logo_file_path.txt.

esc - to exit

### DVD
Remember the animation where a dvd logo bounces around the screen. This program is a replicated version of that animation but it is very responsive to window size changes and it changes color when it hits the border.

esc - to exit

### Pipes
pipes.sh but windows-only!
Don't changes the window size after running it (if you want to then exit to the main menu and then change the window size)

esc - to exit

### Matrix
A cmatrix program on windows? yes.

esc - to exit
### Calculator
...

### Game of Life
The classic conway's game of life n the terminal!

There are two modes:
- Simulation mode
- Edit mode

In the simulation mode the following rules apply:
1. Each cell is either dead or alive.
2. Living cells with 2 or 3 living neighbours lives (Survival).
3. Living cells with less than 2 living neighbours dies (Underpopulation).
4. Living cells with more than 3 living neighbours dies (Overpopulation).
5. Dead cells with exactly 3 living neighbours becomes alive  (Reproduction).


### To-Do List
It is a to-do list which stores the data in a txt file in this format:

```
<the data>
<ticked(1) or not(0)>
.
.
.
```

up arrow / down arrow - to scroll through the entries
insert - to add an entry
delete - to delete an entry
shift - to change an entry
hold ctrl - view the total entry
enter - to tick or untick the entry
esc - to exit

### File Manager
It is a file and folder viewer which can be used to not only view files and folders including the hidden ones but also run them.

up arrow / down arrow - to scroll through the files and folders
left arrow - go outside a folder or drive
right arrow - go inside a folder or drive or run a file
esc - to exit

### Auto Clicker
**It is still in development so don't use it for now**

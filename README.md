# ALL DAY ALL LIFE
Ever wanted to run the pipes.sh, cmatrix, etc on your terminal but then you realised that you need to setup WSL for that because you are a windows user which you think might take time. That is why, I have made this project named **All Day All Life** which contains not only a replica of those scripts but also a to do list, a file manager, an auto clicker, etc. with a cli-based interface

## Installation
To use this program, you will need to have the following dependencies installed:

- os
- keyboard    => ```pip install keyboard```
- time
- random
- ctypes
- sys
- platform
- subprocess
- pynput      => ```pip install pynput```

## Running it
To run the program, simply execute the main_program.py file:

```python main_program.py```

This will launch the main menu, where you can select from various options such as "About", "To-do List",  "File Manager", "DVD", "Pipes", "Matrix", and "Auto Clicker".

### About
It is a replica of neofetch but it uses the windows api so it is exclusive for windows.
You can make a custom logo with this syntax:-

```-;r;g;b- part of the logo -m- -;r2;g2;b2- other part of the logo -m- ...```

-;r;g;b- => set the rgb value in decimals integer.
part of the logo => the logo's part in ascii art form
-m- => to stop using the previous color

It uses ANSI sequences to display colored text, so using ```-m-``` before each new color and at the end is necessary.

Make the logo in a txt file and save it in the Logos directory.

### To-Do List
It is a to-do list which stores the data in a txt file in this format:

```
<the data>
<ticked(1) or not(0)>
.
.
.
```
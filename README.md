# Welcome to my Terminal_game

## Basic information on the game
[^, >, v, <] - Player "models"<br>
\# - Boxes<br>
X - Box goal point<br>
P - Player goal point<br>
O - Completed box goal<br>
[-, |, +] - Walls<br>
Number pairs [1-1, 2-2] - Player teleporters<br>

Key codes / commands in game(case insensitive):<br>
    - **W A S D** - Movement<br>
    - **Esc** - Exit and save<br>
    - **Info** - Displays this window<br>
    - **Return** / **Main menu** - return to the Main menu (Dosen't save progress)

## Requirements
1. Works on Python 3.12 and up (doesn't work on 3.11 and lower)

## How to import your custom level
1. Make your level in import_level.txt
    - Outer edges MUST be walls **"-"** and **"|'** (and corners preferably **"+"** but thats not required)
    - Player must start as **"^"**
    - Level must me a rectangle (obviously)
    - Number of box goals must be lower or equal to the number of boxes
    - Each PAIR of teleporters must be a number (1 or 2. going to 9 will decrease readability so no)
2. Run import_to_json.py (either by convert_to_json_start.bat or normal python) and name your custom_level
3. Enter your level name in-game. 
    - Start > Load custom level > Enter level name
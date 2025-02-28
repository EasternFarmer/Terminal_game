## In-game tiles
[^, >, v, <] - Player "models" <br>
\# - Boxes<br>
X - Box goal point<br>
P - Player goal point<br>
O - Completed box goal (don't put it in level)<br> 
[-, |, +] - Walls<br>
Number pairs [1-1, 2-2, ..., 9-9] - Player teleporters
 
## Custom level creation
1. Make your level in import_level.txt
    - Outer edges MUST be walls **"-"** and **"|"** (and corners preferably **"+"** but that's not required)
    - Player must start as **"^"**
    - Level must be a rectangle (obviously)
    - Number of box goals must be lower or equal to the number of boxes
    - Each PAIR of teleporters must be a number (1 to 9)
2. Run import_to_json.py (either by convert_to_json_start.bat or normal python) and name your custom_level
3. Enter your level name in-game. 
    - Start > Load custom level > Enter level name
# Welcome to my Terminal_game
## How to import your custom level
1. Make your level in import_level.txt
    - Outer edges MUST be walls "-" and "|' (and corners preferably "+" but thats not required)
    - Player must start as "^"
    - Level must me a rectangle (obviously)
    - Number of box goals must be lower or equal to the number of boxes
    - Each PAIR of teleporters must be a number (1 or 2. going to 9 will decrease readability so no)
2. Run import_to_json.py and name your custom_level
3. Enter your level name in-game. 
    - start > Load custom level > Enter level name
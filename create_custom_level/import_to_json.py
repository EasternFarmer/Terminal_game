import json
from os import makedirs


with open('import_level.txt') as f:
    level = [[char for char in line] for line in f.read().splitlines()]

next_level = "7146f77ac5c047a41c9728936fa4d43586c58432c9c8235ad6f95604e6c530f2"

boxes_goal_pos: list[tuple[int, int]] = []
num_boxes: int = 0
player_pos: tuple[int, int] = (-1, -1)
player_pos_goal: tuple[int, int] = (-1, -1)
teleporter_pairs: dict[str, list[int, int]] = {}
for i in range(len(level)):
    for j in range(len(level[0])):
        if level[i][j] == '#':
            num_boxes += 1
        elif level[i][j] == 'X':
            boxes_goal_pos.append((i, j))
        elif level[i][j] in '^><v':
            player_pos = (i, j)
        elif level[i][j] == 'P':
            player_pos_goal = (i, j)
        elif level[i][j] == 'O':
            raise ValueError("You're not supposed to use this in a level!")
        elif level[i][j] in '123456789':
            if teleporter_pairs.get(level[i][j]) is None:
                teleporter_pairs[level[i][j]] = []
            teleporter_pairs[level[i][j]].append((i, j))

            if len(teleporter_pairs[level[i][j]]) > 2:
                raise ValueError(
                    f"Too much Teleporters of one kind ({level[i][j]}) spotted!"
                    )

if num_boxes < len(boxes_goal_pos):
    raise ValueError('Not enough boxes to complete the level!')

for key in teleporter_pairs:
    if len(teleporter_pairs[key]) < 2:
        raise ValueError(f"Not enough teleporters spotted (type: {key!r})")

if player_pos == (-1, -1):
    raise ValueError("No player spotted!")

if player_pos_goal == (-1, -1):
    raise ValueError('No player goal spotted')

z: dict[str, list | dict] = {
    "level": level,
    "level_data": {
        "player_pos": player_pos,
        "player_pos_goal": player_pos_goal,
        "boxes_pos_goal": boxes_goal_pos,
        "teleporter_pairs": teleporter_pairs,
        "next_level": next_level
    }
}

user_input = input("Please select a name for your custom level. ")

BASE_PATH = '../src/assets/custom_levels'

path = BASE_PATH + '/custom_' + user_input + '.json'

try:
    with open(path, 'w') as f:
        f.write(json.dumps(z))
except FileNotFoundError:
    makedirs(BASE_PATH)
    with open(path, 'w') as f:
        f.write(json.dumps(z))

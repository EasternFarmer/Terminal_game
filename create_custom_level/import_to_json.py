import json
from os import mkdir


with open('import_level.txt') as f:
    level = []
    for line in f.read().splitlines():
        row = []
        for char in line:
            row.append(char)
        level.append(row)
next_level = "7146f77ac5c047a41c9728936fa4d43586c58432c9c8235ad6f95604e6c530f2"

boxes_goal_pos: list[tuple[int, int]] = []
num_boxes: int = 0
player_pos: tuple[int, int] = (-1,-1)
player_pos_goal: tuple[int, int]
teleporter_pairs: dict[str, list[int, int]] = {}
for i in range(len(level)):
    for j in range(len(level[0])):
        match level[i][j]:
            case '#':
                num_boxes += 1
            case 'X':
                boxes_goal_pos.append((i,j))
            case '^':
                player_pos = (i,j)
            case 'P':
                player_pos_goal = (i,j)
            case _ if level[i][j] in ['1', '2', '3','4', '5', '6', '7', '8', '9']:
                if teleporter_pairs.get(level[i][j]) is None:
                    teleporter_pairs[level[i][j]] = []
                teleporter_pairs[level[i][j]].append((i,j))
                if len(teleporter_pairs[level[i][j]]) > 2:
                    raise ValueError("More than two teleporters spotted")

if num_boxes < len(boxes_goal_pos):
    raise ValueError('Not enough boxes to complete the level!')
for key in teleporter_pairs:
    if len(teleporter_pairs[key]) < 2:
        raise ValueError(f"Too much Teleporters of one kind ({key}) spotted!")
if player_pos == (-1,-1):
    raise ValueError("No player spotted!")

z = ''
dict_string = 'z = {"level": ' + str(level) + ', "level_data": {"player_pos": ' + str(player_pos) + ', "player_pos_goal": ' + str(player_pos_goal) + ', "boxes_pos_goal": ' + str(boxes_goal_pos) + ', "teleporter_pairs": ' + str(teleporter_pairs) +', "next_level": "' + next_level + '"}}'
exec(dict_string)

user_input = input("Please select a name for your custom level. ")

path = '../src/assets/custom_levels/custom_' + user_input + '.json'
try:
    with open(path,'w') as f:
        f.write(json.dumps(z))
except FileNotFoundError:
    mkdir('../src/assets/custom_levels')
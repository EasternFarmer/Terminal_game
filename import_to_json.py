import json


with open('import_level.txt') as f:
    level = []
    for line in f.read().splitlines():
        row = []
        for char in line:
            row.append(char)
        level.append(row)
next_level = "7146f77ac5c047a41c9728936fa4d43586c58432c9c8235ad6f95604e6c530f2"

boxes_goal_pos = []
player_pos: tuple
player_pos_goal: tuple
teleporter_pairs: dict = {}
for i in range(len(level)):
    for j in range(len(level[0])):
        match level[i][j]:
            case 'X':
                boxes_goal_pos.append((i,j))
            case '^':
                player_pos = (i,j)
            case 'P':
                player_pos_goal = (i,j)
            case _ if level[i][j] in ['1','2']: #did this incase i decide to add more nubers
                if teleporter_pairs.get(level[i][j]) is None:
                    teleporter_pairs[level[i][j]] = []
                teleporter_pairs[level[i][j]].append((i,j))
                if len(teleporter_pairs[level[i][j]]) > 2:
                    raise ValueError("More than two teleporters spotted")

z = ''
dict_string = 'z = {"level": ' + str(level) + ', "level_data": {"player_pos": ' + str(player_pos) + ', "player_pos_goal": ' + str(player_pos_goal) + ', "boxes_pos_goal": ' + str(boxes_goal_pos) + ', "teleporter_pairs": ' + str(teleporter_pairs) +', "next_level": "' + next_level + '"}}'
exec(dict_string)

user_input = input("Please select a name for your custom level. ")

path = 'assets/custom_' + user_input + '.json'
with open(path,'w') as f:
    f.write(json.dumps(z))
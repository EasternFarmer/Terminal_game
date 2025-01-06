import os
import sys
from time import sleep
import json
import keyboard


from assets._colors import *

def clear() -> None: os.system('cls' if os.name == 'nt' else 'clear')


def print_joined_board(board: list[list[str]]) -> None:
    for line in board:
        for char in line:
            if char in ['^','>','<','v']:
                print(f'{BOLD}{BLUE}{char}{RESET}', end='')
            elif char in ['|','-','+']:
                print(f'{MAGENTA}{char}{RESET}', end='')
            elif char in ['X','P', 'O']:
                print(f'{GREEN}{char}{RESET}', end='')
            elif char == '#':
                print(f'{CYAN}{char}{RESET}', end='')
            elif char in ['1','2','3','4','5','6','7','8','9']:
                print(f'{YELLOW}{char}{RESET}', end='')
            elif char == '.':
                print(f'{'\033[90m'}{char}{RESET}', end='')
            else:
                print(char, end='')
        print('')

    # print('\n'.join([''.join(lst) for lst in board]))

def load_json(data_path: str, default: dict | None = None) -> dict:
    try:
        with open(data_path, 'r') as file:
            return json.loads(file.read())
    except FileNotFoundError:
        if default is not None:
            return default
        return {}

class Game:
    def __init__(self, save_path: str = 'saves/save.json') -> None:
        default_save_data: dict = {
            "1":{"save_name":None},
            "2":{"save_name":None},
            "3":{"save_name":None},
            "4":{"save_name":None}
            }
        self.level_data = load_json('assets/levels.json')
        self.save_data = load_json(save_path, default_save_data)
        self.save_path = save_path
        self.main_loop()

    def main_loop(self) -> None:
        clear()
        while True:
            print(f'{'Menu':=^20}')
            print('1. Start')
            #print('2. Options (Not implemented)')
            print('2. Exit')
            user_input = input('\nChoose an option ')
            match user_input:
                case '1':
                    self.save_select()
                # case '2':
                #     raise NotImplementedError
                case '2':
                    self.exiting()
                case _:
                    clear()
                    print(f'{RED}Invalid option!! Try again!{RESET}\n')

    def quick_info(self) -> None:
        print(f'{'Quick Info':=^50}')
        print(f"""
    [{BLUE}{BOLD}^{RESET}, {BLUE}{BOLD}>{RESET}, {BLUE}{BOLD}v{RESET}, {BLUE}{BOLD}<{RESET}] - Player "models"
    {CYAN}#{RESET} - Boxes
    {GREEN}X{RESET} - Box goal point
    {GREEN}O{RESET} - Completed box goal
    {GREEN}P{RESET} - Player goal point
    [{MAGENTA}-{RESET}, {MAGENTA}|{RESET}, {MAGENTA}+{RESET}] - Walls
    Number pairs [{YELLOW}1-1{RESET}, {YELLOW}2-2{RESET}] - Player teleporters
    
    Key codes / commands in game(case insensitive):
        - W A S D - Movement
        - delete - Exit and save
        - ? - Displays this window
        - esc - return to the Main menu (Dosen't save progress)
""")
        input('\nPress Enter to continue. ')
        clear()

    def load_custom_level_tutorial(self) -> None:
        print(f'{'Load custom level Tutorial':=^50}')
        print("""
    1. Make your level in import_level.txt
        - Outer edges MUST be walls "-" and "|' (and corners preferably "+" but thats not required)
        - Player must start as "^"
        - Level must me a rectangle (obviously)
        - Number of box goals must be lower or equal to the number of boxes
        - Each PAIR of teleporters must be a number (1 or 2. going to 9 will decrease readability so no)
    2. Run import_to_json.py and name your custom_level
    3. Enter your level name in-game. 
""")
        # raise NotImplementedError

    def save_select(self) -> None:
        clear()
        while True:
            print(f'{'Select your save':=^20}')
            print(f'1. {self.save_data["1"]['save_name'] if self.save_data["1"]['save_name'] is not None else 'New Game'}')
            print(f'2. {self.save_data["2"]['save_name'] if self.save_data["2"]['save_name'] is not None else 'New Game'}')
            print(f'3. {self.save_data["3"]['save_name'] if self.save_data["3"]['save_name'] is not None else 'New Game'}')
            print(f'4. {self.save_data["4"]['save_name'] if self.save_data["4"]['save_name'] is not None else 'New Game'}')
            print(f'{'Options':=^20}')
            print(f'5. Load custom level.')
            print(f'6. Delete save.')
            print(f'7. Display save data. (Json)')
            print(f'8. Return to main menu.')
            sys.stdin.flush()
            user_input = input('\nChoose an option. ')
            match user_input:
                case '1':
                    if self.save_data["1"].get('save_name') is None:
                        self.create_save(save_id='1')
                    else: self.play(save_id='1')
                case '2':
                    if self.save_data["2"].get('save_name') is None:
                        self.create_save(save_id='2')
                    else: self.play(save_id='2')
                case '3':
                    if self.save_data["3"].get('save_name') is None:
                        self.create_save(save_id='3')
                    else: self.play(save_id='3')
                case '4':
                    if self.save_data["4"].get('save_name') is None:
                        self.create_save(save_id='4')
                    else: self.play(save_id='4')
                case '5':
                    self.load_custom_level_tutorial()
                    level_name = input('Please enter level name. (same as you put in import_to_json.py) ')
                    try:
                        level = load_json('assets/custom_levels/custom_'+level_name + '.json')
                        if level == {}: raise FileNotFoundError
                        self.play("0", custom_level=level)
                    except FileNotFoundError:
                        clear()
                        print(f'{RED}File not found.{RESET}')
                case '6':
                    to_delete = input('\nChoose a save to delete. (1-4) ')
                    if to_delete in ['1','2','3','4']:
                        if input('Are you sure? (Y/N) ').lower() in ['y','yes']:    
                            self.save_data[to_delete] = {"save_name":None}
                            clear()
                    else: 
                        clear()
                        print(f'{RED}Invalid number!{RESET}')
                case '7':
                    to_display = input('\nChoose a save to display. (1-4) ')
                    if to_display in ['1','2','3','4']:
                        clear()
                        print(json.dumps(self.save_data[to_display], indent=4), end='\n\n')
                    else: 
                        clear()
                        print(f'{RED}Invalid number!{RESET}')
                case '8':
                    clear()
                    return
                case 'esc':
                    self.exiting()
                case _:
                    clear()
                    print(f'{RED}Invalid option!! Try again!{RESET}\n')

    def create_save(self, save_id: str) -> None:
        current_save = self.save_data[save_id]
        current_save['current_level'] = "1"
        current_save['character'] = {}
        clear()
        user_input = input('Please enter Save file name. ')
        current_save['save_name'] = user_input
        clear()
        user_input = input('Please enter Character name. ')
        current_save['character']["name"] = user_input
        clear()
        self.play(save_id)

    def play(self, save_id: str, *, custom_level: dict | None = None) -> None:
        clear()
        self.quick_info()
        if custom_level is None:
            current_save = self.save_data[save_id]
            current_level = self.level_data[current_save["current_level"]]["level"]
            current_level_data = self.level_data[current_save["current_level"]]["level_data"]
        else:
            current_level = custom_level["level"]
            current_level_data = custom_level["level_data"]
        
        player_pos = current_level_data["player_pos"].copy()
        teleporter_pairs = current_level_data["teleporter_pairs"]

        on_special_tile: bool = False
        special_tile: str = ''
        cant_move: bool = False
        invalid_command: bool = False
        
        while True:
            print_joined_board(current_level)
            if cant_move:
                print(f"{RED}You can't move there!{RESET}")
                cant_move = False
            elif invalid_command:
                print(f'{RED}Invalid command! use `info` for avalible entries.{RESET}')
                invalid_command = False
            sleep(0.1)
            user_input = keyboard.read_key()
            clear()
            match user_input.lower():
                case 'w':
                    if current_level[player_pos[0]-1][player_pos[1]] not in ['+','-','|','#']:
                        current_level[player_pos[0]][player_pos[1]] = '.' if not on_special_tile else special_tile
                        player_pos = [player_pos[0]-1,player_pos[1]]
                        if current_level[player_pos[0]][player_pos[1]] in ['X','P','O']:
                            on_special_tile = True
                            special_tile = current_level[player_pos[0]][player_pos[1]]
                            current_level[player_pos[0]][player_pos[1]] = '^'
                        elif current_level[player_pos[0]][player_pos[1]] == '1':
                            temp_teleporter_pairs = [coords.copy() for coords in teleporter_pairs['1']]
                            temp_teleporter_pairs.remove(player_pos)
                            player_pos = temp_teleporter_pairs[0]
                            on_special_tile = True
                            special_tile = '1'
                            current_level[player_pos[0]][player_pos[1]] = '^'
                        elif current_level[player_pos[0]][player_pos[1]] == '2':
                            temp_teleporter_pairs = [coords.copy() for coords in teleporter_pairs['2']]
                            temp_teleporter_pairs.remove(player_pos)
                            player_pos = temp_teleporter_pairs[0]
                            on_special_tile = True
                            special_tile = '2'
                            current_level[player_pos[0]][player_pos[1]] = '^'
                        else:
                            current_level[player_pos[0]][player_pos[1]] = '^'
                            on_special_tile = False
                    elif current_level[player_pos[0]-1][player_pos[1]] == '#':
                        if current_level[player_pos[0]-2][player_pos[1]] == 'X':
                            current_level[player_pos[0]-2][player_pos[1]] = 'O'
                            current_level[player_pos[0]-1][player_pos[1]] = '^'
                            current_level[player_pos[0]][player_pos[1]] = '.' if not on_special_tile else special_tile
                            on_special_tile = False
                            player_pos = [player_pos[0]-1,player_pos[1]]
                        elif current_level[player_pos[0]-2][player_pos[1]] == '.':
                            current_level[player_pos[0]-2][player_pos[1]] = '#'
                            current_level[player_pos[0]-1][player_pos[1]] = '^'
                            current_level[player_pos[0]][player_pos[1]] = '.' if not on_special_tile else special_tile
                            on_special_tile = False
                            player_pos = [player_pos[0]-1,player_pos[1]]
                        else: cant_move = True
                    else: cant_move = True
                case 'a':
                    if current_level[player_pos[0]][player_pos[1]-1] not in ['+','-','|','#']:
                        current_level[player_pos[0]][player_pos[1]] = '.' if not on_special_tile else special_tile
                        player_pos = [player_pos[0],player_pos[1]-1]
                        if current_level[player_pos[0]][player_pos[1]] in ['X','P','O']:
                            on_special_tile = True
                            special_tile = current_level[player_pos[0]][player_pos[1]]
                            current_level[player_pos[0]][player_pos[1]] = '<'
                        elif current_level[player_pos[0]][player_pos[1]] == '1':
                            temp_teleporter_pairs = [coords.copy() for coords in teleporter_pairs['1']]
                            temp_teleporter_pairs.remove(player_pos)
                            player_pos = temp_teleporter_pairs[0]
                            on_special_tile = True
                            special_tile = '1'
                            current_level[player_pos[0]][player_pos[1]] = '<'
                        elif current_level[player_pos[0]][player_pos[1]] == '2':
                            temp_teleporter_pairs = [coords.copy() for coords in teleporter_pairs['2']]
                            temp_teleporter_pairs.remove(player_pos)
                            player_pos = temp_teleporter_pairs[0]
                            on_special_tile = True
                            special_tile = '2'
                            current_level[player_pos[0]][player_pos[1]] = '<'
                        else:
                            current_level[player_pos[0]][player_pos[1]] = '<'
                            on_special_tile = False
                    elif current_level[player_pos[0]][player_pos[1]-1] == '#':
                        if current_level[player_pos[0]][player_pos[1]-2] == 'X':
                            current_level[player_pos[0]][player_pos[1]-2] = 'O'
                            current_level[player_pos[0]][player_pos[1]-1] = '<'
                            current_level[player_pos[0]][player_pos[1]] = '.' if not on_special_tile else special_tile
                            on_special_tile = False
                            player_pos = [player_pos[0],player_pos[1]-1]
                        elif current_level[player_pos[0]][player_pos[1]-2] == '.':
                            current_level[player_pos[0]][player_pos[1]-2] = '#'
                            current_level[player_pos[0]][player_pos[1]-1] = '<'
                            current_level[player_pos[0]][player_pos[1]] = '.' if not on_special_tile else special_tile
                            on_special_tile = False
                            player_pos = [player_pos[0],player_pos[1]-1]
                        else: cant_move = True
                    else: cant_move = True
                case 's':
                    if current_level[player_pos[0]+1][player_pos[1]] not in ['+','-','|','#']:
                        current_level[player_pos[0]][player_pos[1]] = '.' if not on_special_tile else special_tile
                        player_pos = [player_pos[0]+1,player_pos[1]]
                        if current_level[player_pos[0]][player_pos[1]] in ['X','P','O']:
                            on_special_tile = True
                            special_tile = current_level[player_pos[0]][player_pos[1]]
                            current_level[player_pos[0]][player_pos[1]] = 'v'
                        elif current_level[player_pos[0]][player_pos[1]] == '1':
                            temp_teleporter_pairs = [coords.copy() for coords in teleporter_pairs['1']]
                            temp_teleporter_pairs.remove(player_pos)
                            player_pos = temp_teleporter_pairs[0]
                            on_special_tile = True
                            special_tile = '1'
                            current_level[player_pos[0]][player_pos[1]] = 'v'
                        elif current_level[player_pos[0]][player_pos[1]] == '2':
                            temp_teleporter_pairs = [coords.copy() for coords in teleporter_pairs['2']]
                            temp_teleporter_pairs.remove(player_pos)
                            player_pos = temp_teleporter_pairs[0]
                            on_special_tile = True
                            special_tile = '2'
                            current_level[player_pos[0]][player_pos[1]] = 'v'
                        else:
                            current_level[player_pos[0]][player_pos[1]] = 'v'
                            on_special_tile = False
                    elif current_level[player_pos[0]+1][player_pos[1]] == '#':
                        if current_level[player_pos[0]+2][player_pos[1]] == 'X':
                            current_level[player_pos[0]+2][player_pos[1]] = 'O'
                            current_level[player_pos[0]+1][player_pos[1]] = 'v'
                            current_level[player_pos[0]][player_pos[1]] = '.' if not on_special_tile else special_tile
                            on_special_tile = False
                            player_pos = [player_pos[0]+1,player_pos[1]]
                        elif current_level[player_pos[0]+2][player_pos[1]] == '.':
                            current_level[player_pos[0]+2][player_pos[1]] = '#'
                            current_level[player_pos[0]+1][player_pos[1]] = 'v'
                            current_level[player_pos[0]][player_pos[1]] = '.' if not on_special_tile else special_tile
                            on_special_tile = False
                            player_pos = [player_pos[0]+1,player_pos[1]]
                        else: cant_move = True
                    else: cant_move = True
                case 'd':
                    if current_level[player_pos[0]][player_pos[1]+1] not in ['+','-','|','#']:
                        current_level[player_pos[0]][player_pos[1]] = '.' if not on_special_tile else special_tile
                        player_pos = [player_pos[0],player_pos[1]+1]
                        if current_level[player_pos[0]][player_pos[1]] in ['X','P','O']:
                            on_special_tile = True
                            special_tile = current_level[player_pos[0]][player_pos[1]]
                            current_level[player_pos[0]][player_pos[1]] = '>'
                        elif current_level[player_pos[0]][player_pos[1]] == '1':
                            temp_teleporter_pairs = [coords.copy() for coords in teleporter_pairs['1']]
                            temp_teleporter_pairs.remove(player_pos)
                            player_pos = temp_teleporter_pairs[0]
                            on_special_tile = True
                            special_tile = '1'
                            current_level[player_pos[0]][player_pos[1]] = '>'
                        elif current_level[player_pos[0]][player_pos[1]] == '2':
                            temp_teleporter_pairs = [coords.copy() for coords in teleporter_pairs['2']]
                            temp_teleporter_pairs.remove(player_pos)
                            player_pos = temp_teleporter_pairs[0]
                            on_special_tile = True
                            special_tile = '2'
                            current_level[player_pos[0]][player_pos[1]] = '>'
                        else:
                            current_level[player_pos[0]][player_pos[1]] = '>'
                            on_special_tile = False
                    elif current_level[player_pos[0]][player_pos[1]+1] == '#':
                        if current_level[player_pos[0]][player_pos[1]+2] == 'X':
                            current_level[player_pos[0]][player_pos[1]+2] = 'O'
                            current_level[player_pos[0]][player_pos[1]+1] = '>'
                            current_level[player_pos[0]][player_pos[1]] = '.' if not on_special_tile else special_tile
                            on_special_tile = False
                            player_pos = [player_pos[0],player_pos[1]+1]
                        elif current_level[player_pos[0]][player_pos[1]+2] == '.':
                            current_level[player_pos[0]][player_pos[1]+2] = '#'
                            current_level[player_pos[0]][player_pos[1]+1] = '>'
                            current_level[player_pos[0]][player_pos[1]] = '.' if not on_special_tile else special_tile
                            on_special_tile = False
                            player_pos = [player_pos[0],player_pos[1]+1]
                        else: cant_move = True
                    else: cant_move = True
                case 'delete':
                    self.exiting()
                case '?' | '/':
                    self.quick_info()
                case 'esc':
                    return
                case _:
                    invalid_command = True
            # level complete check
            if len(current_level_data["boxes_pos_goal"]) != 0:
                boxes_y_goal = [coords[0] for coords in current_level_data["boxes_pos_goal"]]
                boxes_x_goal = [coords[1] for coords in current_level_data["boxes_pos_goal"]]
                boxes_at_goal = all(['O' == current_level[boxes_y_goal[n]][pos] for n, pos in enumerate(boxes_x_goal)])
            else:
                boxes_at_goal = True
            if boxes_at_goal and player_pos == current_level_data["player_pos_goal"]:
                if current_level_data["next_level"] == "7146f77ac5c047a41c9728936fa4d43586c58432c9c8235ad6f95604e6c530f2":
                    print("Congratulations on completing this custom level.")
                    sleep(2)
                    return
                if current_level_data["next_level"] is not None:
                    current_save["current_level"] = current_level_data["next_level"]
                else: self.complete()
                return

    def complete(self) -> None:
        raise NotImplementedError
    
    def save(self) -> None:
        try:
            with open(self.save_path, 'w') as file:
                file.write(json.dumps(self.save_data, indent=4))
        except FileNotFoundError:
            os.mkdir('saves')
            self.save()
    
    def exiting(self, *, save: bool = True) -> None:
        for i in range(3):
            clear()
            print('Exiting' + '.'*(i+1))
            sleep(0.25)
        clear()
        if save:
            self.save()
        exit()




Game()
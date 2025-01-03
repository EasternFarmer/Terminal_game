from dataclasses import dataclass
import os
from time import sleep
import json

def clear() -> None: os.system('cls' if os.name == 'nt' else 'clear')

def load_json(data_path: str, default: dict) -> dict:
    try:
        with open(data_path, 'r') as file:
            return json.loads(file.read())
    except FileNotFoundError:
        return default

class Game:
    def __init__(self, save_path: str = 'saves/save.json') -> None:
        default: dict = {
            "1":{"save_name":None},
            "2":{"save_name":None},
            "3":{"save_name":None},
            "4":{"save_name":None}
            }
        self.data = load_json(save_path, default)
        self.save_path = save_path
        self.menu()

    def menu(self) -> None:
        clear()
        while True:
            print(f'{'Menu':=^20}')
            print('1. Start')
            print('2. Options (Not implemented)')
            print('3. Exit')
            user_input = input('\nChoose an option ')
            match user_input:
                case '1':
                    self.save_select()
                # case '2':
                #     raise NotImplementedError
                case '3':
                    self.exiting()
                case _:
                    clear()
                    print('Invalid option!! Try again!\n')

    def save_select(self) -> None:
        clear()
        while True:
            print(f'{'Select your save':=^20}')
            print(f'1. {self.data["1"]['save_name'] if self.data["1"]['save_name'] is not None else 'New Game'}')
            print(f'2. {self.data["2"]['save_name'] if self.data["2"]['save_name'] is not None else 'New Game'}')
            print(f'3. {self.data["3"]['save_name'] if self.data["3"]['save_name'] is not None else 'New Game'}')
            print(f'4. {self.data["4"]['save_name'] if self.data["4"]['save_name'] is not None else 'New Game'}')
            print('5. Delete save')
            print('6. Display save data. (Json)')
            print('7. Return to main menu')
            user_input = input('\nChoose an option. ')
            match user_input:
                case '1':
                    if self.data["1"].get('save_name') is None:
                        self.create_save(save_id='1')
                    else: self.play(save_id='1')
                case '2':
                    if self.data["2"].get('save_name') is None:
                        self.create_save(save_id='2')
                    else: self.play(save_id='2')
                case '3':
                    if self.data["3"].get('save_name') is None:
                        self.create_save(save_id='3')
                    else: self.play(save_id='3')
                case '4':
                    if self.data["4"].get('save_name') is None:
                        self.create_save(save_id='4')
                    else: self.play(save_id='4')
                case '5':
                    to_delete = input('\nChoose a save to delete. (1-4) ')
                    if to_delete in ['1','2','3','4']:
                        if input('Are you sure? (Y/N) ').lower() in ['y','n','yes','no']:    
                            self.data[to_delete] = {"save_name":None}
                    else: 
                        clear()
                        print('Invalid number!')
                case '6':
                    to_display = input('\nChoose a save to display. (1-4) ')
                    if to_display in ['1','2','3','4']:
                        clear()
                        print(json.dumps(self.data[to_display], indent=4), end='\n\n')
                    else: 
                        clear()
                        print('Invalid number!')
                case '7':
                    clear()
                    return
                case _:
                    clear()
                    print('Invalid option!! Try again!\n')

    def create_save(self, save_id: str) -> None:
        current_save = self.data[save_id]
        current_save['character'] = {}
        clear()
        user_input = input('Please enter Save file name. ')
        current_save['save_name'] = user_input
        clear()
        user_input = input('Please enter Character name. ')
        current_save['character']["name"] = user_input
        clear()
        while type(user_input) != int:
            try:
                user_input = int(input('Please enter valid Character age. ')) #type: ignore
                current_save['character']['age'] = user_input
            except ValueError:
                clear()
                print('Invalid Entry!! Try again!\n')
        current_save['character']['level_data'] = {"id":1, "pos_xy":(0,0), "pos_goal":(60,20)}

    def play(self, save_id: str) -> None:
        current_save = self.data[save_id]
        clear()
    
    def exiting(self, save: bool = True) -> None:
        for i in range(3):
            clear()
            print('Exiting' + '.'*(i+1))
            sleep(0.25)
        clear()
        if save:
            with open(self.save_path, 'w') as file:
                file.write(json.dumps(self.data, indent=4))
        exit()




Game()
def get_level(level_id: int):# -> list[list]:
    """board 60x20"""
    levels: dict[int,list[list[str]]] = {
        0:None        }
    return levels[level_id]
def print_formated_board(board: list[list[str]]) -> None: print('\n'.join([''.join(lst) for lst in board]))

get_level(1)

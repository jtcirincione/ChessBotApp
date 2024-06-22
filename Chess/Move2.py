import numpy as np
from enums.MoveType import MoveType
class Move2:


    @staticmethod
    def convert_idx_to_rc(idx):
        row = idx//8
        col = idx % 8
        return row, col
    
    def __init__(self, move_board, start_square, end_square, move_type: MoveType):
        self.attack_board: np.uint64 = move_board
        self.start_square = start_square
        self.end_square = end_square
        self.move_type = move_type
        
        
    def get_move_board(self):
        return self.attack_board
    
    def get_initial_idx(self) -> int:
        return self.start_square

    def get_final_idx(self) -> int:
        return self.end_square
    
    def get_move_type(self):
        return self.move_type
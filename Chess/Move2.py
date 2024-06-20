import numpy as np
class Move2:
    
    def __init__(self, init_board, fin_board):
        self.init_board: np.uint64 = init_board
        self.fin_board: np.uint64 = fin_board
        
        
    def get_initial_board(self):
        return self.init_board
    
    def get_final_board(self):
        return self.fin_board
    
    def get_initial_idxs(self) -> list[tuple[int, int]]:
        return self.init_board.get_idxs()

    def get_final_idxs(self) -> list[tuple[int, int]]:
        return self.fin_board.get_idxs()
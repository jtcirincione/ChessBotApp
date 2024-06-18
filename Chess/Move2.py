class Move2:
    
    def __init__(self, init_board, fin_board):
        self.init_board = init_board
        self.fin_board = fin_board
        
        
    def get_initial(self):
        return self.init_board
    
    def get_final(self):
        return self.fin_board
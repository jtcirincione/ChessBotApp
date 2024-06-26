class Move:
    
    def __init__(self, init_row:int, init_col:int, fin_row, fin_col):
        self.init_row = init_row
        self.init_col = init_col
        self.fin_row = fin_row
        self.fin_col = fin_col
        
        
    def get_initial(self) -> tuple:
        return (self.init_row, self.init_col)
    
    def get_final(self) -> tuple:
        return (self.fin_row, self.fin_col)
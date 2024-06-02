class Move:
    
    def __init__(self, piece, row:int, col:int):
        self.piece = piece
        self.row = row
        self.col = col
        
    def get_coordinates(self) -> tuple:
        return (self.row, self.col)
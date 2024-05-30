from Piece import Piece
class Dragger:
    def __init__(self):
        self.prevRow = self.prevCol =self.postRow = self.postCol = 0
        self.piece = None
        self.is_dragging = False
    
    def update_pos(self, board: list, x: int, y: int) -> None:
        self.prevRow = x
        self.prevCol = y
        self.piece = board[x][y]
        self.is_dragging = True
    
    def drag(self, board: list, x: int, y: int) -> list:
        self.postRow = x
        self.postCol = y
        self.is_dragging = False
        board[self.prevRow][self.prevCol] = "--"
        print(f"prevRow: {self.prevRow}, prevCol: {self.prevCol}\npostRow:{self.postRow}, postCol: {self.postCol}")
        board[self.postRow][self.postCol] = self.piece
        
    
        return board

    def get_piece(self)-> Piece:
        return self.piece
from Piece import Piece, Pawn, Rook, Knight, King, Queen, Bishop
class Dragger:
    def __init__(self):
        self.prevRow = self.prevCol =self.postRow = self.postCol = 0
        self.piece = None
        self.is_dragging = False
    
    def update_pos(self, board: list, x: int, y: int) -> None:
        if board[x][y] == '--': return
        self.piece = board[x][y]
        self.prevRow = x
        self.prevCol = y
        self.is_dragging = True
    
    def drag(self, board: list, x: int, y: int) -> list:
        self.postRow = x
        self.postCol = y
        self.is_dragging = False
        board[self.prevRow][self.prevCol] = "--"
        board[self.postRow][self.postCol] = self.piece
        ## if pawn, set moved to true
        if isinstance(self.piece, Pawn):
            self.piece.moved()
                
        return board
   
    def undrag(self):
        self.is_dragging = False
        self.prevRow = self.prevCol =self.postRow = self.postCol = 0
        self.piece = None

    def get_piece(self)-> Piece:
        return self.piece
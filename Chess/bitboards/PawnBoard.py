from bitboards.BitBoard import BitBoard
from Move2 import Move2
BLACK_2MOVE_ROW = 0b0000000000000000000000001111111100000000000000000000000000000000
WHITE_2MOVE_ROW = 0b0000000000000000000000000000000011111111000000000000000000000000
class PawnBoard(BitBoard):
    def __init__(self, color):
        board = self.initialize_board(color)
        super().__init__(color, board)

    def initialize_board(self, color) -> int:
        if color == "white":
            return 0b0000000000000000000000000000000000000000000000001111111100000000
        return 0b0000000011111111000000000000000000000000000000000000000000000000
    
    def reset(self):
        self.board = self.initialize_board(self.color)
    

    ##TODO: Add masking logic for moving up 2
    def valid_moves(self) -> BitBoard:
        if self.color == "white":
            two_moves = WHITE_2MOVE_ROW & (self.board << 16)
            one_move = self.board << 8
            move_board = one_move | two_moves
        if self.color == "black":
            two_moves = WHITE_2MOVE_ROW & (self.board >> 16)
            one_move = self.board >> 8
            move_board = one_move | two_moves
        return move_board
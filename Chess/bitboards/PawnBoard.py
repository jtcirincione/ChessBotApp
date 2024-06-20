from bitboards.BitBoard import BitBoard
from Move2 import Move2
import numpy as np
BLACK_2MOVE_ROW = np.uint64(0b0000000000000000000000001111111100000000000000000000000000000000)
WHITE_2MOVE_ROW = np.uint64(0b0000000000000000000000000000000011111111000000000000000000000000)
BLACK_PASSANT_ROW = np.uint64(0b0000000000000000111111110000000000000000000000000000000000000000)
WHITE_PASSANT_ROW = np.uint64(0b0000000000000000000000000000000000000000111111110000000000000000)
FILE_H_MASK = np.uint64(0b1111111011111110111111101111111011111110111111101111111011111110)
FILE_A_MASK = np.uint64(0b0111111101111111011111110111111101111111011111110111111101111111)

class PawnBoard(BitBoard):
    def __init__(self, color):
        board = self.initialize_board(color)
        self.previous_board = board
        name = "bp" if color == "black" else "wp"
        super().__init__(color, board, name)

    def initialize_board(self, color) -> int:
        if color == "white":
            return np.uint64(0b0000000000000000000000000000000000000000000000001111111100000000)
        return np.uint64(0b0000000011111111000000000000000000000000000000000000000000000000)
    
    def reset(self):
        self.board = self.initialize_board(self.color)
    

    ##TODO: Add masking logic for moving up 2
    def valid_moves(self) -> np.uint64:
        if self.color == "white":
            two_moves = WHITE_2MOVE_ROW & (self.board << 16)
            one_move = self.board << 8
            move_board = one_move | two_moves
            ## CAPTURES
        if self.color == "black":
            two_moves = BLACK_2MOVE_ROW & (self.board >> 16)
            one_move = self.board >> 8
            move_board = one_move | two_moves
        return move_board
    
    def attacking_squares(self, pieceIdx:int, enemy_board:np.uint64, my_color_board:np.uint64) -> np.uint64:
        board = self.get_single_piece_board(self.board, pieceIdx)
        if self.color == "white":
            two_moves = np.uint64(WHITE_2MOVE_ROW & (board << 16))
            one_move = np.uint64(board << 8)
            move_board = np.uint64(one_move | two_moves)
        if self.color == "black":
            two_moves = np.uint64(BLACK_2MOVE_ROW & (board >> 16))
            one_move = board >> 8
            print(type(one_move))
            move_board = one_move | two_moves
        return move_board
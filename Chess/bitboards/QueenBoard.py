from bitboards.BitBoard import BitBoard
from Move2 import Move2
from enums.MoveType import MoveType
import numpy as np, warnings

class QueenBoard(BitBoard):
    def __init__(self, color):
        board = self.initialize_board(color)
        name = "bQ" if color == "black" else "wQ"
        super().__init__(color, board, name)

    def initialize_board(self, color) -> int:
        if color == "white":
            return np.uint64(0b0000000000000000000000000000000000000000000000000000000000010000)
        return np.uint64(0b0001000000000000000000000000000000000000000000000000000000000000)
    
    def reset(self):
        self.board = self.initialize_board(self.color)

    def h_v_moves(self, idx, occupied: np.uint64):
        s = self.get_single_piece_board(self.board, idx)
        # s = np.uint64(1 << idx)
        occ_h = occupied & self.rank_masks[idx//8]
        occ_v = occupied & self.file_masks[idx%8]
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            horizontal = (occ_h - (np.uint64(2) * s)) ^ self.reverse_bits(self.reverse_bits(occ_h) - np.uint64(2) * self.reverse_bits(s))
            vertical = (occ_v - (np.uint64(2) * s)) ^ self.reverse_bits(self.reverse_bits(occ_v) - np.uint64(2) * self.reverse_bits(s))
        return ((horizontal & self.rank_masks[idx//8]) | (vertical & self.file_masks[idx%8]))

    def d_anti_moves(self, idx, occupied: np.uint64):
        s = self.get_single_piece_board(self.board, idx)
        # s = np.uint64(1 << idx)
        occ_d = occupied & self.diagonal_masks[(idx//8) + (idx%8)]
        occ_a = occupied & self.antidiagonal_masks[(idx//8) + 7 - (idx%8)]
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            diagonal = (occ_d - (np.uint64(2) * s)) ^ self.reverse_bits(self.reverse_bits(occ_d) - np.uint64(2) * self.reverse_bits(s)) 
            antidiagonal = (occ_a - (np.uint64(2) * s)) ^ self.reverse_bits(self.reverse_bits(occ_a) - np.uint64(2) * self.reverse_bits(s))
        return ((diagonal & self.diagonal_masks[(idx//8) + (idx%8)]) | (antidiagonal & self.antidiagonal_masks[(idx//8) + 7 - (idx%8)]))


    
    def valid_moves(self, my_color_board, enemy_board, move_history):
        attack_board = np.uint64(0)
        for i in range(64):
            if self.get_bit(i):
                attack_board |= self.d_anti_moves(i, enemy_board | my_color_board) | self.h_v_moves(i, enemy_board | my_color_board) & ~my_color_board
        return attack_board


    def attacking_squares(self, pieceIdx, my_color_board:np.uint64, enemy_board:np.uint64, move_history: list[Move2]) -> tuple[np.uint64, list[Move2]]:
        attack_board = (self.d_anti_moves(pieceIdx, enemy_board | my_color_board) | self.h_v_moves(pieceIdx, enemy_board | my_color_board)) & ~my_color_board
        moves = BitBoard.get_moves(self.board, attack_board, pieceIdx)
        return (attack_board, moves)
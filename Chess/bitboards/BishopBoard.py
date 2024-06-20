from bitboards.BitBoard import BitBoard
import numpy as np
class BishopBoard(BitBoard):
    def __init__(self, color):
        board = self.initialize_board(color)
        name = "bB" if color == "black" else "wB"
        super().__init__(color, board, name)

    def initialize_board(self, color) -> int:
        if color == "white":
            return np.uint64(0b0000000000000000000000000000000000000000000000000000000000100100)
        return np.uint64(0b0010010000000000000000000000000000000000000000000000000000000000)
    
    def reset(self):
        self.board = self.initialize_board(self.color)

    def d_anti_moves(self, idx, occupied: np.uint64):
        s = self.get_single_piece_board(self.board, idx)
        occ_d = occupied & self.diagonal_masks[(idx//8) + (idx%8)]
        occ_a = occupied & self.antidiagonal_masks[(idx//8) + 7 - (idx%8)]
        diagonal = (occ_d - (np.uint64(2) * s)) ^ self.reverse_bits(self.reverse_bits(occ_d) - self.reverse_bits(np.uint64(2) * s))
        antidiagonal = (occ_a - (np.uint64(2) * s)) ^ self.reverse_bits(self.reverse_bits(occ_a) - self.reverse_bits(np.uint64(2) * s))
        return (diagonal | antidiagonal)

    def valid_moves(self):
        pass

    def attacking_squares(self, pieceIdx, enemy_board:np.uint64, my_color_board:np.uint64):
        board = self.get_single_piece_board(self.board, pieceIdx)
        return self.d_anti_moves(pieceIdx, enemy_board | my_color_board)
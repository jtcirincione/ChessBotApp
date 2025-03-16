from bitboards.BitBoard import BitBoard
from enums.MoveType import MoveType
import numpy as np, warnings
from Move2 import Move2
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
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            diagonal = (occ_d - (np.uint64(2) * s)) ^ self.reverse_bits(self.reverse_bits(occ_d) - np.uint64(2) * self.reverse_bits(s))
            antidiagonal = (occ_a - (np.uint64(2) * s)) ^ self.reverse_bits(self.reverse_bits(occ_a) - np.uint64(2) * self.reverse_bits(s))
        return ((diagonal & self.diagonal_masks[(idx//8) + (idx%8)]) | (antidiagonal & self.antidiagonal_masks[(idx//8) + 7 - (idx%8)]))

    def valid_moves(self, my_color_board, enemy_board, move_history):
        attack_board = np.uint64(0)
        for i in range(64):
            if self.get_bit(i):
                attack_board |= self.d_anti_moves(i, enemy_board | my_color_board)
        return attack_board


    def generate_moves(self, empty: np.uint64, opponent_board: np.uint64, move_history: list[Move2]) -> list[Move2]:
        my_color_board = ~(empty | opponent_board)
        moves = []
        for i in range(64):
            if self.get_bit(i):
                attack_board = self.d_anti_moves(i, opponent_board | my_color_board) & ~my_color_board
                for j in range(64):
                    if BitBoard.get_bit_on_board(j, attack_board):
                        moves.append(Move2(self, i, j, MoveType.QUIET))
        
        return moves

    def attacking_squares(self, pieceIdx, my_color_board:np.uint64, enemy_board:np.uint64, move_history: list[Move2]):
        attack_board = self.d_anti_moves(pieceIdx, enemy_board | my_color_board) & ~my_color_board
        moves = BitBoard.get_moves(self, attack_board, pieceIdx)
        return (attack_board, moves)
from bitboards.BitBoard import BitBoard
from Move2 import Move2
from enums.MoveType import MoveType
import numpy as np, warnings

FILE_H_MASK = np.uint64(0b1000000010000000100000001000000010000000100000001000000010000000)
RANK_8_MASK = np.uint64(0b1111111100000000000000000000000000000000000000000000000000000000)
RANK_1_MASK = np.uint64(0b0000000000000000000000000000000000000000000000000000000011111111)
class RookBoard(BitBoard):
    def __init__(self, color):
        board = self.initialize_board(color)
        self.left_rook_moved = False
        self.right_rook_moved = False
        name = "bR" if color == "black" else "wR"
        super().__init__(color, board, name)

    def initialize_board(self, color) -> np.uint64:
        if color == "white":
            return np.uint64(0b0000000000000000000000000000000000000000000000000000000010000001)
        return np.uint64(0b1000000100000000000000000000000000000000000000000000000000000000)
    
    def reset(self):
        self.board = self.initialize_board(self.color)
        self.left_rook_moved = self.right_rook_moved = False

    def move_piece(self, clrIdx, setIdx) -> None:
        if not (0 <= setIdx < 64) or not (0 <= clrIdx < 64):
            raise Exception("Square must be from 0 to 63")
        self.set_bit(setIdx)
        self.clear_bit(clrIdx)
        if self.color == "white":
            if clrIdx == 56:
                self.left_rook_moved = True
            elif clrIdx == 63:
                self.right_rook_moved = True
        else:
            if clrIdx == 0:
                self.left_rook_moved = True
            elif clrIdx == 7:
                self.right_rook_moved = True



    def h_v_moves(self, idx, occupied: np.uint64) -> np.uint64:
        s = self.get_single_piece_board(self.board, idx)
        # s = np.uint64(1 << idx)
        occ_h = occupied & self.rank_masks[idx//8]
        occ_v = occupied & self.file_masks[idx%8]
        # with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        horizontal = (occ_h - (np.uint64(2) * s)) ^ self.reverse_bits(self.reverse_bits(occ_h) - np.uint64(2) * self.reverse_bits(s))
        vertical = (occ_v - (np.uint64(2) * s)) ^ self.reverse_bits(self.reverse_bits(occ_v) - np.uint64(2) * self.reverse_bits(s))
        return ((horizontal & self.rank_masks[idx//8]) | (vertical & self.file_masks[idx%8]))

    # mask all ranks above/below rook for horizontal moves
    # mask out files to left/right of rook for vertical moves
    def valid_moves(self, my_color_board, enemy_board, move_history) -> np.uint64:
        attack_board = np.uint64(0)
        for i in range(64):
            if self.get_bit(i):
                attack_board |= self.h_v_moves(i, enemy_board | my_color_board) & ~my_color_board
        return attack_board
    
    def generate_moves(self, empty: np.uint64, opponent_board: np.uint64, move_history: list[Move2])  -> list[Move2]:
        my_color_board = ~(empty | opponent_board)
        moves = []
        for i in range(64):
            if self.get_bit(i):
                attack_board = self.h_v_moves(i, opponent_board | my_color_board) & ~my_color_board
                for j in range(64):
                    if BitBoard.get_bit_on_board(j, attack_board):
                        moves.append(Move2(self, i, j, MoveType.QUIET))
        
        return moves

    def attacking_squares(self, pieceIdx, my_color_board:np.uint64, enemy_board:np.uint64, move_history: list[Move2]) -> tuple[np.uint64, list[Move2]]:
        attack_board = self.h_v_moves(pieceIdx, enemy_board | my_color_board) & ~my_color_board
        moves = BitBoard.get_moves(self, attack_board, pieceIdx)
        return (attack_board, moves)
from bitboards.BitBoard import BitBoard
import numpy as np
from Move2 import Move2
from enums.MoveType import MoveType

FILE_AB_MASK = np.uint64(
    0b0011111100111111001111110011111100111111001111110011111100111111)
FILE_GH_MASK = np.uint64(
    0b1111110011111100111111001111110011111100111111001111110011111100)
FILE_A_MASK = np.uint64(
    0b0111111101111111011111110111111101111111011111110111111101111111)
FILE_B_MASK = np.uint64(
    0b1011111110111111101111111011111110111111101111111011111110111111)
FILE_G_MASK = np.uint64(
    0b1111110111111101111111011111110111111101111111011111110111111101)
FILE_H_MASK = np.uint64(
    0b1111111011111110111111101111111011111110111111101111111011111110)


class KnightBoard(BitBoard):
    def __init__(self, color):
        board = self.initialize_board(color)
        name = "bN" if color == "black" else "wN"
        super().__init__(color, board, name)
        self.moves = [
            6,  # top right move restrict from A and B
            15,  # top right move restrict from A
            10,  # top left move, # restrict from G and H
            17,  # top left move, # restrict from H
            -6,  # bottom left move # restrict from G and H
            -15,  # bottom left move # restrict from H
            -10,  # bottom right move # restrict from A and B
            -17  # bottom right move # restrict from B


        ]

    def initialize_board(self, color) -> np.uint64:
        if color == "white":
            return np.uint64(0b0000000000000000000000000000000000000000000000000000000001000010)
        return np.uint64(0b0100001000000000000000000000000000000000000000000000000000000000)

    def reset(self):
        self.board = self.initialize_board(self.color)

    # Apply mask if piece is on A, B or G, H ranks
    # AB mask for right bit shifts, GH for left
    def valid_moves(self, my_color_board, enemy_board, move_history):
        board = self.board
        valid_moves = np.uint64(0)
        for move in self.moves:
            if move > 0:
                position = (board << np.uint64(move))
            else:
                position = (board >> np.uint64(-move))
            if move == 6 or move == -10:
                position &= FILE_AB_MASK
            if move == 15 or move == -17:
                position &= FILE_A_MASK
            if move == 10 or move == -6:
                position &= FILE_GH_MASK
            if move == -15 or move == 17:
                position &= FILE_H_MASK
            valid_moves |= position
        valid_moves &= ~my_color_board
        return valid_moves

    def attacking_squares(self, pieceIdx, my_color_board: np.uint64, enemy_board: np.uint64, move_history: list[Move2]) -> tuple[np.uint64, list[Move2]]:
        board = self.get_single_piece_board(self.board, pieceIdx)
        valid_moves = np.uint64(0)
        for move in self.moves:
            if move > 0:
                position = (board << np.uint64(move))
            else:
                position = (board >> np.uint64(-move))
            if move == 6 or move == -10:
                position &= FILE_AB_MASK
            if move == 15 or move == -17:
                position &= FILE_A_MASK
            if move == 10 or move == -6:
                position &= FILE_GH_MASK
            if move == -15 or move == 17:
                position &= FILE_H_MASK
            valid_moves |= position
        valid_moves &= ~my_color_board
        moves = BitBoard.get_moves(self.board, valid_moves, pieceIdx)
        return (valid_moves, moves)

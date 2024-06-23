from bitboards.BitBoard import BitBoard
from Move2 import Move2
from enums.MoveType import MoveType
import numpy as np
FILE_A_MASK = np.uint64(0b0111111101111111011111110111111101111111011111110111111101111111)
FILE_H_MASK = np.uint64(0b1111111011111110111111101111111011111110111111101111111011111110)

W_CASTLE_RIGHT_MASK = np.uint64(0b0000000000000000000000000000000000000000000000000000000000000110)
W_CASTLE_LEFT_MASK = np.uint64(0b0000000000000000000000000000000000000000000000000000000001110000)
B_CASTLE_RIGHT_MASK = np.uint64(0b0000011000000000000000000000000000000000000000000000000000000000)
B_CASTLE_LEFT_MASK = np.uint64(0b0111000000000000000000000000000000000000000000000000000000000000)
class KingBoard(BitBoard):
    def __init__(self, color):
        board = self.initialize_board(color)
        self.moved = False
        name = "bK" if color == "black" else "wK"
        super().__init__(color, board, name)
        self.moves = [8, -8, 1, -1, 7, 9, -7, -9]

    def initialize_board(self, color) -> np.uint64:
        if color == "white":
            return np.uint64(0b0000000000000000000000000000000000000000000000000000000000001000)
        return np.uint64(0b0000100000000000000000000000000000000000000000000000000000000000)
    
    def reset(self):
        self.board = self.initialize_board(self.color)
        self.moved = False

    def move_piece(self, clrIdx, setIdx) -> None:
        print("KING MOVED")
        if not (0 <= setIdx < 64) or not (0 <= clrIdx < 64):
            raise Exception("Square must be from 0 to 63")
        self.set_bit(setIdx)
        self.clear_bit(clrIdx)
        self.moved = True

    def valid_moves(self, my_color_board, enemy_board, move_history):
        ## if king is moving to the right, apply A mask
        # Vice versa for left
        
        board = self.board
        ## if king is moving to the right, apply A mask
        # Vice versa for left
        valid_moves = np.uint64(0)
        for move in self.moves:
            if move > 0:
                potential_move = (board << np.uint64(move))
            else:
                potential_move = (board >> np.uint64(-move))

            if move == -1 or move == -9 or move == 7: ## if piece is moving to the right
                potential_move &= FILE_A_MASK
            if move == 1 or move == 9 or move == -7: ## if piece is moving to the left
                potential_move &= FILE_H_MASK

            valid_moves |= potential_move
            valid_moves &= ~my_color_board
            ## Castling
            if not self.moved:
                castling_move = np.uint64(0)
                occupied = my_color_board | enemy_board
                if self.color == "white":
                    if occupied & W_CASTLE_LEFT_MASK == 0:
                        castling_move = self.board << np.uint64(2)
                    if occupied & W_CASTLE_RIGHT_MASK == 0:
                        castling_move = self.board >> np.uint64(2)
                if self.color == "black":
                    if occupied & B_CASTLE_LEFT_MASK == 0:
                        castling_move = self.board << np.uint64(2)
                    if occupied & B_CASTLE_RIGHT_MASK == 0:
                        castling_move = self.board >> np.uint64(2)
                valid_moves |= castling_move
        return valid_moves
    
    def attacking_squares(self, pieceIdx, my_color_board:np.uint64, enemy_board:np.uint64, move_history: list[Move2]) -> tuple[np.uint64, list[Move2]]:
        board = self.get_single_piece_board(self.board, pieceIdx)
        ## if king is moving to the right, apply A mask
        # Vice versa for left
        valid_moves = np.uint64(0)
        for move in self.moves:
            if move > 0:
                potential_move = (board << np.uint64(move))
            else:
                potential_move = (board >> np.uint64(-move))

            if move == -1 or move == -9 or move == 7: ## if piece is moving to the right
                potential_move &= FILE_A_MASK
            if move == 1 or move == 9 or move == -7: ## if piece is moving to the left
                potential_move &= FILE_H_MASK

            valid_moves |= potential_move
            valid_moves &= ~my_color_board
            moves = BitBoard.get_moves(self.board, valid_moves, pieceIdx)
            ## Castling
            if not self.moved:
                castling_move = np.uint64(0)
                occupied = my_color_board | enemy_board
                if self.color == "white":
                    if occupied & W_CASTLE_LEFT_MASK == 0:
                        move1 = Move2(self.board, pieceIdx, pieceIdx - 2, MoveType.CASTLE_LEFT)
                        moves.append(move1)
                    if occupied & W_CASTLE_RIGHT_MASK == 0:
                        move2 = Move2(self.board, pieceIdx, pieceIdx + 2, MoveType.CASTLE_RIGHT)
                        moves.append(move2)
                if self.color == "black":
                    if occupied & B_CASTLE_LEFT_MASK == 0:
                        move1 = Move2(self.board, pieceIdx, pieceIdx - 2, MoveType.CASTLE_LEFT)
                        moves.append(move1)
                    if occupied & B_CASTLE_RIGHT_MASK == 0:
                        move2 = Move2(self.board, pieceIdx, pieceIdx + 2, MoveType.CASTLE_RIGHT)
                        moves.append(move2)
        return (valid_moves, moves)
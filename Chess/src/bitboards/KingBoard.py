from bitboards.BitBoard import BitBoard
from Move2 import Move2
from enums.MoveType import MoveType
import numpy as np, warnings, math
FILE_A_MASK = np.uint64(0b0111111101111111011111110111111101111111011111110111111101111111)
FILE_H_MASK = np.uint64(0b1111111011111110111111101111111011111110111111101111111011111110)

W_CASTLE_RIGHT_MASK = np.uint64(0b0000000000000000000000000000000000000000000000000000000000000110)
W_CASTLE_LEFT_MASK = np.uint64(0b0000000000000000000000000000000000000000000000000000000001110000)
B_CASTLE_RIGHT_MASK = np.uint64(0b0000011000000000000000000000000000000000000000000000000000000000)
B_CASTLE_LEFT_MASK = np.uint64(0b0111000000000000000000000000000000000000000000000000000000000000)
index64 = [
    0, 47,  1, 56, 48, 27,  2, 60,
   57, 49, 41, 37, 28, 16,  3, 61,
   54, 58, 35, 52, 50, 42, 21, 44,
   38, 32, 29, 23, 17, 11,  4, 62,
   46, 55, 26, 59, 40, 36, 15, 53,
   34, 51, 20, 43, 31, 22, 10, 45,
   25, 39, 14, 33, 19, 30,  9, 24,
   13, 18,  8, 12,  7,  6,  5, 63
]
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
    
    def get_idx_of_king(self):
        if (self.board == 0):
            return -1
        i = index64[np.uint64((self.board ^ (self.board - np.uint64(1))) * np.uint64(0x03f79d71b4cb0a89)) >> np.uint64(58)]
        # if self.board == 0 or (self.board & (self.board - np.uint64(1))) != 0:
        #     return -1
    
        # i = int(math.log2(self.board & -self.board)) + 1
        i = 63 - i
        # print(f"idx of {self.color} king: {i}")
        return i


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
    
    def d_anti_moves(self, idx, occupied: np.uint64):
        s = self.board
        occ_d = occupied & self.diagonal_masks[(idx//8) + (idx%8)]
        occ_a = occupied & self.antidiagonal_masks[(idx//8) + 7 - (idx%8)]
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            diagonal = (occ_d - (np.uint64(2) * s)) ^ self.reverse_bits(self.reverse_bits(occ_d) - np.uint64(2) * self.reverse_bits(s))
            antidiagonal = (occ_a - (np.uint64(2) * s)) ^ self.reverse_bits(self.reverse_bits(occ_a) - np.uint64(2) * self.reverse_bits(s))
        return ((diagonal & self.diagonal_masks[(idx//8) + (idx%8)]) | (antidiagonal & self.antidiagonal_masks[(idx//8) + 7 - (idx%8)]))


    def h_v_moves(self, idx, occupied: np.uint64):
        s = self.board
        # s = np.uint64(1 << idx)
        occ_h = occupied & self.rank_masks[idx//8]
        occ_v = occupied & self.file_masks[idx%8]
        # with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        horizontal = (occ_h - (np.uint64(2) * s)) ^ self.reverse_bits(self.reverse_bits(occ_h) - np.uint64(2) * self.reverse_bits(s))
        vertical = (occ_v - (np.uint64(2) * s)) ^ self.reverse_bits(self.reverse_bits(occ_v) - np.uint64(2) * self.reverse_bits(s))
        return ((horizontal & self.rank_masks[idx//8]) | (vertical & self.file_masks[idx%8]))


    def get_d_anti_squares(self, pieceIdx: int, enemy_board: np.uint64, my_color_board:np.uint64):
        attack_board = self.d_anti_moves(pieceIdx, enemy_board | my_color_board) & ~my_color_board
        return attack_board

    def get_h_v_squares(self, pieceIdx: int, enemy_board: np.uint64, my_color_board:np.uint64):
        attack_board = self.h_v_moves(pieceIdx, enemy_board | my_color_board) & ~my_color_board
        return attack_board
    
    def generate_moves(self, empty: np.uint64, opponent_board: np.uint64, move_history: list[Move2]) -> list[Move2]:
        my_color_board = ~(empty | opponent_board)
        board = self.board
        valid_moves = np.uint64(0)
        idx = -1
        # Get index of king
        idx = self.get_idx_of_king()
        # for i in range(64):
        #     if self.get_bit(i):
        #         idx = i
        #         break


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
            moves = BitBoard.get_moves(self, valid_moves, idx)
            ## Castling
            if not self.moved:
                castling_move = np.uint64(0)
                occupied = my_color_board | opponent_board
                if self.color == "white":
                    if occupied & W_CASTLE_LEFT_MASK == 0:
                        move1 = Move2(self, idx, idx - 2, MoveType.CASTLE_LEFT)
                        moves.append(move1)
                    if occupied & W_CASTLE_RIGHT_MASK == 0:
                        move2 = Move2(self, idx, idx + 2, MoveType.CASTLE_RIGHT)
                        moves.append(move2)
                if self.color == "black":
                    if occupied & B_CASTLE_LEFT_MASK == 0:
                        move1 = Move2(self, idx, idx - 2, MoveType.CASTLE_LEFT)
                        moves.append(move1)
                    if occupied & B_CASTLE_RIGHT_MASK == 0:
                        move2 = Move2(self, idx, idx + 2, MoveType.CASTLE_RIGHT)
                        moves.append(move2)
        return moves

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
            moves = BitBoard.get_moves(self, valid_moves, pieceIdx)
            ## Castling
            if not self.moved:
                castling_move = np.uint64(0)
                occupied = my_color_board | enemy_board
                if self.color == "white":
                    if occupied & W_CASTLE_LEFT_MASK == 0:
                        move1 = Move2(self, pieceIdx, pieceIdx - 2, MoveType.CASTLE_LEFT)
                        moves.append(move1)
                    if occupied & W_CASTLE_RIGHT_MASK == 0:
                        move2 = Move2(self, pieceIdx, pieceIdx + 2, MoveType.CASTLE_RIGHT)
                        moves.append(move2)
                if self.color == "black":
                    if occupied & B_CASTLE_LEFT_MASK == 0:
                        move1 = Move2(self, pieceIdx, pieceIdx - 2, MoveType.CASTLE_LEFT)
                        moves.append(move1)
                    if occupied & B_CASTLE_RIGHT_MASK == 0:
                        move2 = Move2(self, pieceIdx, pieceIdx + 2, MoveType.CASTLE_RIGHT)
                        moves.append(move2)
        return (valid_moves, moves)
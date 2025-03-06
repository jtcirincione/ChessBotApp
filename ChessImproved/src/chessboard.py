from bitboards.BitBoard import BitBoard
import numpy as np
STARTING_POSITIONS = {
    "wp":  np.uint64(0b0000000000000000000000000000000000000000000000001111111100000000),
    "bp":  np.uint64(0b0000000011111111000000000000000000000000000000000000000000000000),
    "wN":  np.uint64(0b0000000000000000000000000000000000000000000000000000000001000010),  # B1, G1
    "bN":  np.uint64(0b0100001000000000000000000000000000000000000000000000000000000000),  # B8, G8
    "wB":  np.uint64(0b0000000000000000000000000000000000000000000000000000000000100100),  # C1, F1
    "bB":  np.uint64(0b0010010000000000000000000000000000000000000000000000000000000000),  # C8, F8
    "wR":  np.uint64(0b0000000000000000000000000000000000000000000000000000000010000001),  # A1, H1
    "bR":  np.uint64(0b1000000100000000000000000000000000000000000000000000000000000000),  # A8, H8
    "wQ":  np.uint64(0b0000000000000000000000000000000000000000000000000000000000010000),  # D1
    "bQ":  np.uint64(0b0001000000000000000000000000000000000000000000000000000000000000),  # D8
    "wK":  np.uint64(0b0000000000000000000000000000000000000000000000000000000000001000),  # E1
    "bK":  np.uint64(0b0000100000000000000000000000000000000000000000000000000000000000),  # E8
    }

NOT_AB_MASK = np.uint64(
    0b0011111100111111001111110011111100111111001111110011111100111111)
NOT_GH_MASK = np.uint64(
    0b1111110011111100111111001111110011111100111111001111110011111100)
NOT_A_MASK = np.uint64(
    0b0111111101111111011111110111111101111111011111110111111101111111)
NOT_B_MASK = np.uint64(
    0b1011111110111111101111111011111110111111101111111011111110111111)
NOT_G_MASK = np.uint64(
    0b1111110111111101111111011111110111111101111111011111110111111101)
NOT_H_MASK = np.uint64(
    0b1111111011111110111111101111111011111110111111101111111011111110)

"""
Starts from idx 0 at bottom right, goes up from right to left to 63 at top left
"""
class Chessboard:
    

    def __init__(self):
        self.bitboards = {
            key: BitBoard(val, key) for key, val in STARTING_POSITIONS.items()
        }
        self.bitboards["white_pieces"] = BitBoard(np.uint64(0))
        for p in self.bitboards:
            if "w" in p and p != "white_pieces":  # Exclude self OR
                self.bitboards["white_pieces"].board |= self.bitboards[p].board
        
        self.bitboards["black_pieces"] = BitBoard(np.uint64(0))
        for p in self.bitboards:
            if "b" in p and p != "black_pieces":  # Exclude self OR
                self.bitboards["black_pieces"].board |= self.bitboards[p].board

        self.bitboards["occupied"] = BitBoard(self.bitboards["white_pieces"].board | self.bitboards["black_pieces"].board)

        self.KNIGHT_MOVES = [0] * 64

        self.KING_MOVES = [0] * 64
        self.precompute_knights()
        self.precompute_kings()

    def get_piece_boards(self) -> dict[str, BitBoard]:
        return {
            key: val for key, val in self.bitboards.items() if key != "white_pieces" and key != "black_pieces" and key != "occupied"
        }

    def precompute_knights(self):
        for i in range(64):
            self.KNIGHT_MOVES[i] = self.generate_knight_moves(i)
    
    def generate_knight_moves(self, idx):
        knight_move = np.uint64(0)
        board = np.uint64(0)
        BitBoard.static_set_bit(board, idx)
        moves = [
            6,  # top right move restrict from A and B
            15,  # top right move restrict from A
            10,  # top left move, # restrict from G and H
            17,  # top left move, # restrict from H
            -6,  # bottom left move # restrict from G and H
            -15,  # bottom left move # restrict from H
            -10,  # bottom right move # restrict from A and B
            -17  # bottom right move # restrict from B
        ]

        for move in moves:
            if move > 0:
                position = (board << np.uint64(move))
            else:
                position = (board >> np.uint64(-move))
            if move == 6 or move == -10:
                position &= NOT_AB_MASK
            if move == 15 or move == -17:
                position &= NOT_A_MASK
            if move == 10 or move == -6:
                position &= NOT_GH_MASK
            if move == -15 or move == 17:
                position &= NOT_H_MASK
            knight_move |= position

        return knight_move


    def precompute_kings(self):
        for i in range(64):
            self.KNIGHT_MOVES[i] = self.generate_king_moves(i)
    
    def generate_king_moves(self, idx):
        king_move = np.uint64(0)
        board = np.uint64(0)
        BitBoard.static_set_bit(board, idx)

        moves = [8, -8, 1, -1, 7, 9, -7, -9] 
        for move in moves:
            if move > 0:
                potential_move = (board << np.uint64(move))
            else:
                potential_move = (board >> np.uint64(-move))

            if move == -1 or move == -9 or move == 7: ## if piece is moving to the right
                potential_move &= NOT_A_MASK
            if move == 1 or move == 9 or move == -7: ## if piece is moving to the left
                potential_move &= NOT_H_MASK

            king_move |= potential_move
        return king_move

    def mask_pawn_attacks(self, white):
        attack_squares = np.uint64(0)
        if white:
            pawns = self.bitboards['wp']
            attack_squares |= (pawns << 9) & NOT_H_MASK ## left attack
            attack_squares |= (pawns << 7) & NOT_A_MASK ## right attack
            attack_squares &= ~self.bitboards['white_pieces']
        else:
            pawns = self.bitboards['bp']
            attack_squares |= (pawns >> 7) & NOT_H_MASK ## left attack
            attack_squares |= (pawns >> 9) & NOT_A_MASK ## right attack
            attack_squares &= ~self.bitboards['black_pieces']
        return attack_squares
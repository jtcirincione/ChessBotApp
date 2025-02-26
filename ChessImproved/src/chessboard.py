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
class Chessboard:
    

    def __init__(self):
        self.bitboards = {
            key: BitBoard(val) for key, val in STARTING_POSITIONS.items()
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

    def get_piece_boards(self) -> dict:
        return {
            key: val for key, val in self.bitboards.items() if key != "white_pieces" and key != "black_pieces"
        }
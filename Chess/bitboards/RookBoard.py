from bitboards.BitBoard import BitBoard
import numpy as np, warnings
FILE_H_MASK = np.uint64(0b1000000010000000100000001000000010000000100000001000000010000000)
RANK_8_MASK = np.uint64(0b1111111100000000000000000000000000000000000000000000000000000000)
RANK_1_MASK = np.uint64(0b0000000000000000000000000000000000000000000000000000000011111111)
class RookBoard(BitBoard):
    def __init__(self, color):
        board = self.initialize_board(color)
        name = "bR" if color == "black" else "wR"
        super().__init__(color, board, name)

    def initialize_board(self, color) -> np.uint64:
        if color == "white":
            return np.uint64(0b0000000000000000000000000000000000000000000000000000000010000001)
        return np.uint64(0b1000000100000000000000000000000000000000000000000000000000000000)
    
    def reset(self):
        self.board = self.initialize_board(self.color)

    def get_rook_locs(self, board: np.uint64) -> tuple[list[int],list[int]]:
        ranks = []
        files = []
        for rank in range(8):
            for file in range(8):
                idx = rank * 8 + file
                if self.get_bit(board, idx):
                    ranks.append(rank)
                    files.append(file)

        return (ranks, files)

    def h_v_moves(self, idx, occupied: np.uint64):
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
    def valid_moves(self) -> np.uint64:
        ranks, files = self.get_rook_locs(self.board)
        valid_moves = 0
        return valid_moves
    
    def attacking_squares(self, pieceIdx, my_color_board:np.uint64, enemy_board:np.uint64) -> np.uint64:
        return self.h_v_moves(pieceIdx, enemy_board | my_color_board) & ~my_color_board
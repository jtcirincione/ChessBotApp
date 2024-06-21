from bitboards.BitBoard import BitBoard
import numpy as np
FILE_A_MASK = np.uint64(0b0111111101111111011111110111111101111111011111110111111101111111)
FILE_H_MASK = np.uint64(0b1111111011111110111111101111111011111110111111101111111011111110)
class KingBoard(BitBoard):
    def __init__(self, color):
        board = self.initialize_board(color)
        name = "bK" if color == "black" else "wK"
        super().__init__(color, board, name)
        self.moves = [8, -8, 1, -1, 7, 9, -7, -9]

    def initialize_board(self, color) -> np.uint64:
        if color == "white":
            return np.uint64(0b0000000000000000000000000000000000000000000000000000000000001000)
        return np.uint64(0b0000100000000000000000000000000000000000000000000000000000000000)
    
    def reset(self):
        self.board = self.initialize_board(self.color)

    def valid_moves(self, square):
        ## if king is moving to the right, apply A mask
        # Vice versa for left
        
        valid_moves = np.uint64(0x0000000000000000)
        for move in self.moves:
            if move > 0:
                potential_move = (self.board << move)
            else:
                potential_move = (self.board >> -move)

            if move == -1 or move == -9 or move == 7: ## if piece is moving to the right
                potential_move &= FILE_A_MASK
            if move == 1 or move == 9 or move == -7: ## if piece is moving to the left
                potential_move &= FILE_H_MASK

            valid_moves |= potential_move
        return valid_moves
    
    def attacking_squares(self, pieceIdx, my_color_board:np.uint64, enemy_board:np.uint64) -> np.uint64:
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
        return valid_moves & ~my_color_board
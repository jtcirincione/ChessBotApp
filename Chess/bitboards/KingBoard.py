from bitboards.BitBoard import BitBoard
FILE_A_MASK = 0b0111111101111111011111110111111101111111011111110111111101111111
FILE_H_MASK = 0b1111111011111110111111101111111011111110111111101111111011111110
class KingBoard(BitBoard):
    def __init__(self, color):
        board = self.initialize_board(color)
        super().__init__(color, board)
        self.moves = [8, -8, 1, -1, 7, 9, -7, -9]

    def initialize_board(self, color) -> int:
        if color == "white":
            return 0b0000000000000000000000000000000000000000000000000000000000001000
        return 0b0000100000000000000000000000000000000000000000000000000000000000
    
    def reset(self):
        self.board = self.initialize_board(self.color)

    def valid_moves(self):
        ## if left bit shift, apply file_h mask
        # Vice versa for right
        valid_moves = 0
        mask = 0xFFFFFFFFFFFFFFFF
        for move in self.moves:
            if move > 0:
                potential_move = (self.board >> move) & FILE_A_MASK  ## right moves
            else:
                potential_move = (self.board << -move) & FILE_H_MASK  ## left moves
            valid_moves |= potential_move
        return valid_moves
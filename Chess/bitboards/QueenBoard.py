from bitboards.BitBoard import BitBoard
class QueenBoard(BitBoard):
    def __init__(self, color):
        board = self.initialize_board(color)
        super().__init__(color, board)

    def initialize_board(self, color) -> int:
        if color == "white":
            return 0b0000000000000000000000000000000000000000000000000000000000010000
        return 0b0001000000000000000000000000000000000000000000000000000000000000
    
    def reset(self):
        self.board = self.initialize_board(self.color)
from bitboards.BitBoard import BitBoard
class RookBoard(BitBoard):
    def __init__(self, color):
        board = self.initialize_board(color)
        super().__init__(color, board)

    def initialize_board(self, color) -> int:
        if color == "white":
            return 0b0000000000000000000000000000000000000000000000000000000010000001
        return 0b1000000100000000000000000000000000000000000000000000000000000000
    
    def reset(self):
        self.board = self.initialize_board(self.color)
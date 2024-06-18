from bitboards.BitBoard import BitBoard
FILE_AB_MASK = 0b0011111100111111001111110011111100111111001111110011111100111111
FILE_GH_MASK = 0b1111110011111100111111001111110011111100111111001111110011111100
class KnightBoard(BitBoard):
    def __init__(self, color):
        board = self.initialize_board(color)
        super().__init__(color, board)
        self.moves = [
            6, ## top right move
            15, ## top right move
            10, # top left move
            17, # top left move
            
        ]

    def initialize_board(self, color) -> int:
        if color == "white":
            return 0b0000000000000000000000000000000000000000000000000000000001000010
        return 0b0100001000000000000000000000000000000000000000000000000000000000
    
    def reset(self):
        self.board = self.initialize_board(self.color)

    # Apply mask if piece is on A, B or G, H ranks
    def valid_moves(self):
        pass
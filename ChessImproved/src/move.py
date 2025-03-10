import numpy as np

"""
Moves will be incoded as uint16:
0000 0000 0000 0000

0000 0000 0011 1111 <-- index of square origin

0000 1111 1100 0000 <-- index of square destination

1111 0000 0000 0000 <-- flags


flag cheat sheet:
code | promotion | capture | special 1 | special 0 | type
__________________________________________________________
  0  |     0     |    0    |    0      |     0     | quiet moves
________________________________________________________________
  1  |     0     |    0    |    0      |     1     | double pawn push
_______________________________________________________________
  2  |     0     |    0    |    1      |     0     | king castle
_______________________________________________________________
  3  |     0     |    0    |    1      |     1     | queen castle
_______________________________________________________________
  4  |     0     |    1    |    0      |     0     | captures
_______________________________________________________________
  5  |     0     |    1    |    0      |     1     | ep-capture
_______________________________________________________________
  8  |     1     |    0    |    0      |     0     | knight-promo
_______________________________________________________________
  9  |     1     |    0    |    0      |     1     | bishop-promo
_______________________________________________________________
  10 |     1     |    0    |    1      |     0     | rook-promo
_______________________________________________________________
  11 |     1     |    0    |    1      |     1     | queen-promo
_______________________________________________________________
  12 |     1     |    1    |    0      |     0     | knight-promo capture
_______________________________________________________________
  13 |     1     |    1    |    0      |     1     | bishop-promo capture
_______________________________________________________________
  14 |     1     |    1    |    1      |     0     | rook-promo capture
_______________________________________________________________
  15 |     1     |    1    |    1      |     1     | queen-promo capture
_______________________________________________________________
"""
class Move:
    QUIET = 0
    DOUBLE_PAWN_PUSH = 1
    KING_CASTLE = 2
    QUEEN_CASTLE = 3
    CAPTURE = 4
    KNIGHT_PROMO = 8
    BISHOP_PROMO = 9
    ROOK_PROMO = 10
    QUEEN_PROMO = 11
    KNIGHT_CAP_PROMO = 12
    BISHOP_CAP_PROMO = 13
    ROOK_CAP_PROMO = 14
    QUEEN_CAP_PROMO = 15
    
    @staticmethod
    def get_move_type(board_to_set, board_to_clear, start, end):
        move_flags = np.uint16(0)
        if board_to_clear is not None:
            move_flags |= np.uint16(1 << 2) # set capture bit
        
        return 1


    def __init__(self, frum: np.uint, to, flags):
        self.move = (np.uint16(flags) << 12) | (np.uint16(to) << 6) | (np.uint16(frum))
    
    def get_move(self) -> np.uint16:
        return self.move
    
    def get_from_idx(self):
        return self.move & 0x3F
    
    def get_to_idx(self):
        return (self.move >> 6) & 0x3F

    def print_move(self):
        print(f"encoded: {self.move}")
        from_move = self.move & 0x3F
        to_move = (self.move >> 6) & 0x3F
        flag = self.move >> 12

        print(f"decoded: \nfrom: {from_move}\nto: {to_move}\nflag: {flag}")
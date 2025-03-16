from enum import Enum
class MoveType(Enum):
    QUIET = 0
    DOUBLE = 1
    EN_PASSANT_CAPTURE = 2
    CASTLE_LEFT = 3
    CASTLE_RIGHT = 4
    PROMOTE = 5
    EN_PASSANT = 6


# move = MoveType(0)

# print(move)
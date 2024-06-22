from enum import Enum
class MoveType(Enum):
    QUIET = 0
    EN_PASSANT = 1
    EN_PASSANT_CAPTURE = 2
    CASTLE_LEFT = 3
    CASTLE_RIGHT = 4


# move = MoveType(0)

# print(move)
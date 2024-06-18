from abc import ABC, abstractmethod


class BitBoard(ABC):
    def __init__(self, color: str, board: int):
        self.color = color
        self.board = board

    # Shift bits by "idx" amount to move
    # the piece to the very end of the string.
    # and with 1 to return true if bit is there and false if not
    def get_bit(self, idx):
        if not (0 <= idx < 64):
            raise Exception("Square must be from 0 to 63")
        bshift = 63 - idx
        return (self.board >> bshift) & 1

    def print_board(self):
        print(f"The color i am printing for is {self.color}")
        for rank in range(8):
            for file in range(8):
                square = rank * 8 + file
                # print(f"idx of the square i am printing: {square}")
                print(self.get_bit(square), end=" ")
            print("")

    @abstractmethod
    def initialize_board(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def valid_moves(self):
        pass

    def move_piece(self, clrIdx, setIdx) -> None:
        if not (0 <= setIdx < 64) or not (0 <= clrIdx < 64):
            raise Exception("Square must be from 0 to 63")
        self.set_bit(setIdx)
        self.clear_bit(clrIdx)

    def set_bit(self, idx: int) -> None:
        bshift = 63 - idx
        self.board |= (1 << bshift)

    # Clears the bit at location idx
    # shifts 1 bit by bshift amount
    # negates shifted int then &'s with board to clear bit
    def clear_bit(self, idx) -> None:
        bshift = 63 - idx
        self.board &= ~(1 << bshift)
import os
import numpy as np



class BitBoard():
    def __init__(self, color: str, board: np.uint64, name: str):
        self.color = color
        self.board = board
        self.name = name
        self.file = self.set_file()

    def set_file(self) -> str:
        path = os.path.abspath(os.path.dirname(__file__))
        chess_dir = os.path.dirname(path)
        fin = os.path.join(chess_dir, "images", self.name + ".png")
        # path = f"images/{self.name}.png"
        return fin
    
    # Shift bits by "idx" amount to move
    # the piece to the very end of the string.
    # and with 1 to return true if bit is there and false if not
    def get_bit(self, idx) -> int:
        if not (0 <= idx < 64):
            raise Exception("Square must be from 0 to 63")
        return (self.board >> np.uint64(63 - idx)) & np.uint64(1)
    
    def move_piece(self, clrIdx, setIdx) -> None:
        if not (0 <= setIdx < 64) or not (0 <= clrIdx < 64):
            raise Exception("Square must be from 0 to 63")
        self.set_bit(setIdx)
        self.clear_bit(clrIdx)

    def set_bit(self, idx: int) -> None:
        bshift = np.uint64(63 - idx)
        self.board |= (np.uint64(1) << bshift)

    # Clears the bit at location idx
    # shifts 1 bit by bshift amount
    # negates shifted int then &'s with board to clear bit
    def clear_bit(self, idx) -> None:
        bshift = np.uint64(63 - idx)
        self.board &= ~(np.uint64(1) << bshift)
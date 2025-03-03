import os
import numpy as np



class BitBoard():
    
    # Shift bits by "idx" amount to move
    # the piece to the very end of the string.
    # and with 1 to return true if bit is there and false if not
    @staticmethod
    def get_bit(board, idx) -> int:
        if not (0 <= idx < 64):
            raise Exception("Square must be from 0 to 63")
        return (board >> np.uint64(63 - idx)) & np.uint64(1)
    
    @staticmethod
    def set_bit(board, idx: int) -> None:
        bshift = np.uint64(63 - idx)
        board |= (np.uint64(1) << bshift)

    
    # Clears the bit at location idx
    # shifts 1 bit by bshift amount
    # negates shifted int then &'s with board to clear bit
    @staticmethod
    def clear_bit(self, idx) -> None:
        bshift = np.uint64(63 - idx)
        self.board &= ~(np.uint64(1) << bshift)

    def __init__(self, board: np.uint64, name: str=""): 
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
    
    # prints board in readable way
    def print(self):
        for rank in range(0, 8):
            for file in range(0, 8):
                if not file:
                    print(8 - rank, end="  ")
                square = rank * 8 + file
                print(self.get_bit(idx=square), end=" ")
            print()
        
        print("\n   A B C D E F G H\n\n", end="")
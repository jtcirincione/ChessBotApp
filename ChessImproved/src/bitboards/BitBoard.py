import os
import numpy as np



class BitBoard():
    
    # Shift bits by "idx" amount to move
    # the piece to the very end of the string.
    # and with 1 to return true if bit is there and false if not
    @staticmethod
    def static_get_bit(board, idx) -> int:
        if not (0 <= idx < 64):
            raise Exception("Square must be from 0 to 63")
        return (board >> np.uint64(idx)) & np.uint64(1)
    
    @staticmethod
    def static_set_bit(board, idx: int) -> np.uint64:
        board |= (np.uint64(1) << np.uint64(idx))
        return board
    
    @staticmethod
    def generate_rook_mask(idx):
        mask = np.uint64(0)
        rank = idx // 8
        file = idx % 8

        #vertical moves
        for r in range(rank + 1, 7): # Exclude board edges
            mask |= np.uint64(1) << np.uint64(r * 8 + file)
        for r in range(rank - 1, 0, -1):  # Exclude board edges
            mask |= np.uint64(1) << np.uint64(r * 8 + file)

        #horizontal moves
        for f in range(file + 1, 7):
            mask |= np.uint64(1) << np.uint64(rank*8 + f)
        for f in range (file -1, 0, -1):
            mask |= np.uint64(1) << np.uint64(rank*8 + f)
    
        return mask
    
    @staticmethod
    def generate_bishop_mask(idx):
        mask = np.uint64(0)
        rank = idx // 8
        file = idx % 8
        # Diagonal (↗ and ↙)
        for i in range(1, 7):
            if rank + i < 7 and file + i < 7:
                mask |= np.uint64(1) << np.uint64((rank + i) * 8 + (file + i))
            if rank - i > 0 and file - i > 0:
                mask |= np.uint64(1) << np.uint64((rank - i) * 8 + (file - i))

        # Anti-diagonal (↖ and ↘)
        for i in range(1, 7):
            if rank + i < 7 and file - i > 0:
                mask |= np.uint64(1) << np.uint64((rank + i) * 8 + (file - i))
            if rank - i > 0 and file + i < 7:
                mask |= np.uint64(1) << np.uint64((rank - i) * 8 + (file + i))

        return mask

    @staticmethod
    def static_print(board):
        for rank in range(7, -1, -1):
            for file in range(0, 8):
                if not file:
                    print(rank + 1, end="  ")
                square = rank * 8 + file
                print(BitBoard.static_get_bit(board, idx=square), end=" ")
            print()
        
        print("\n   A B C D E F G H\n\n", end="")

    
    # Clears the bit at location idx
    # shifts 1 bit by bshift amount
    # negates shifted int then &'s with board to clear bit
    @staticmethod
    def static_clear_bit(self, idx) -> None:
        self.board &= ~(np.uint64(1) << np.uint64(idx))

    @staticmethod
    def bit_scan_forward(bitboard: np.uint64) -> int:
        """Returns the index of the least significant bit (LSB) in the bitboard."""
        bitboard: int = int(bitboard)  # Convert to Python int to avoid overflow
        return (bitboard & -bitboard).bit_length() - 1

    def __init__(self, board: np.uint64, name: str=""): 
        self.board = board
        self.name = name
        self.file = self.set_file()
        self.color = "white" if name.startswith("w") else "black"

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
        return (self.board >> np.uint64(idx)) & np.uint64(1)
    
    def move_piece(self, clrIdx, setIdx) -> None:
        if not (0 <= setIdx < 64) or not (0 <= clrIdx < 64):
            raise Exception("Square must be from 0 to 63")
        self.set_bit(setIdx)
        self.clear_bit(clrIdx)

    def set_bit(self, idx: int) -> None:
        bshift = np.uint64(63 - idx)
        self.board |= (np.uint64(1) << np.uint64(idx))

    # Clears the bit at location idx
    # shifts 1 bit by bshift amount
    # negates shifted int then &'s with board to clear bit
    def clear_bit(self, idx) -> None:
        bshift = np.uint64(63 - idx)
        self.board &= ~(np.uint64(1) << np.uint64(idx))
    
    # prints board in readable way
    def print(self):
        for rank in range(7, -1, -1):
            for file in range(0, 8):
                if not file:
                    print(rank + 1, end="  ")
                square = rank * 8 + file
                print(self.get_bit(idx=square), end=" ")
            print()
        
        print("\n   A B C D E F G H\n\n", end="")
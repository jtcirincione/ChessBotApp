from abc import ABC, abstractmethod
import os
import numpy as np

# from top right to bottom left
diagonal_masks = [
    np.uint64(0x8000000000000000), np.uint64(0X4080000000000000), np.uint64(0X2040800000000000), np.uint64(0x1020408000000000), 
    np.uint64(0x810204080000000), np.uint64(0x408102040800000), np.uint64(0x204081020408000), np.uint64(0x102040810204080), 
    np.uint64(0x1020408102040), np.uint64(0x10204081020), np.uint64(0x102040810), np.uint64(0x1020408),
    np.uint64(0x10204), np.uint64(0x102), np.uint64(0x1)

]
# from top left to bottom right
antidiagonal_masks = [ np.uint64(0x100000000000000), np.uint64(0x201000000000000), np.uint64(0x402010000000000), np.uint64(0x804020100000000),
                 np.uint64(0x1008040201000000), np.uint64(0x2010080402010000), np.uint64(0x4020100804020100), np.uint64(0x8040201008040201),
                 np.uint64(0x80402010080402), np.uint64(0x804020100804), np.uint64(0x8040201008), np.uint64(0x80402010), np.uint64(0x804020), 
                 np.uint64(0x8040), np.uint64(0x80)
]

## from rank 1 to 8
rank_masks = [np.uint64(0xFF00000000000000), np.uint64(0xFF000000000000), np.uint64(0xFF0000000000), np.uint64(0xFF00000000),
              np.uint64(0xFF000000), np.uint64(0xFF0000), np.uint64(0xFF00), np.uint64(0xFF)]

# from file H to A
file_masks = [
    np.uint64(0x8080808080808080),
    np.uint64(0x4040404040404040),
    np.uint64(0x2020202020202020),
    np.uint64(0x1010101010101010),
    np.uint64(0x808080808080808),
    np.uint64(0x404040404040404),
    np.uint64(0x202020202020202),
    np.uint64(0x101010101010101)
]


piece_loc = 8

def get_bit_on_board(idx, board: np.uint64):
        if not (0 <= idx < 64):
            raise Exception("Square must be from 0 to 63")
        bshift = np.uint64(np.uint64(63) - np.uint64(idx))
        return ((board >> bshift) & np.uint64(1))
    
# Function to print a single mask as a grid
def print_board_2(board):
    for i in range(8):
        for j in range(8):
            idx = np.uint64(i * 8 + j)
            if (get_bit_on_board(idx, board)):
                print('1', end=' ')
            else:
                print('0', end=' ')
        print()
    print("\n\n")


mask = rank_masks[piece_loc//8] | file_masks[piece_loc%8] | diagonal_masks[(piece_loc//8) + (piece_loc%8)] | antidiagonal_masks[(piece_loc//8)+7-(piece_loc%8)]
# mask = diagonal_masks[(piece_loc//8)+(piece_loc%8)] | antidiagonal_masks[(piece_loc//8)+7-(piece_loc%8)]
print_board_2(mask)


def reverse_bits(x: np.uint64) -> np.uint64:
    x = ((x & np.uint64(0x5555555555555555)) << np.uint64(1)) | ((x & np.uint64(0xAAAAAAAAAAAAAAAA)) >> np.uint64(1))
    x = ((x & np.uint64(0x3333333333333333)) << np.uint64(2)) | ((x & np.uint64(0xCCCCCCCCCCCCCCCC)) >> np.uint64(2))
    x = ((x & np.uint64(0x0F0F0F0F0F0F0F0F)) << np.uint64(4)) | ((x & np.uint64(0xF0F0F0F0F0F0F0F0)) >> np.uint64(4))
    x = ((x & np.uint64(0x00FF00FF00FF00FF)) << np.uint64(8)) | ((x & np.uint64(0xFF00FF00FF00FF00)) >> np.uint64(8))
    x = ((x & np.uint64(0x0000FFFF0000FFFF)) << np.uint64(16)) | ((x & np.uint64(0xFFFF0000FFFF0000)) >> np.uint64(16))
    x = (x << np.uint64(32)) | (x >> np.uint64(32))
    return x & np.uint64(0xFFFFFFFFFFFFFFFF)

# Example usage
value = np.uint64(0x00000000000200001)
reversed_value = reverse_bits(value)
print(bin(value))
print(bin(reversed_value))
# 1000111101111011001111010101100100011110011010100010110001001
# 1000111101111011001111010101100100011110011010100010110001001000

class BitBoard(ABC):
    # # from top left to bottom right
    # diagonal_masks = [
    #     np.uint64(0x1), np.uint64(0x102), np.uint64(0x10204), np.uint64(0x1020408), np.uint64(0x102040810), 
    #     np.uint64(0x10204081020), np.uint64(0x1020408102040), np.uint64(0x102040810204080),
    #     np.uint64(0x204081020408000), np.uint64(0x408102040800000), np.uint64(0x810204080000000),
    #     np.uint64(0x1020408000000000), np.uint64(0X2040800000000000), np.uint64(0X4080000000000000),
    #     np.uint64(0x8000000000000000)

    # ]
    # # from top right to bottom left
    # antidiagonal_masks = [ np.uint64(0x80), np.uint64(0x8040), np.uint64(0x804020), np.uint64(0x80402010),
    #     np.uint64(0x8040201008), np.uint64(0x804020100804),np.uint64(0x80402010080402) , np.uint64(0x8040201008040201),
    #     np.uint64(0x4020100804020100), np.uint64(0x2010080402010000), np.uint64(0x1008040201000000),
    #     np.uint64(0x804020100000000), np.uint64(0x402010000000000), np.uint64(0x201000000000000),
    #     np.uint64(0x100000000000000)
    # ]

    # ## from rank 8 to 1
    # rank_masks = [np.uint64(0xFF), np.uint64(0xFF00), np.uint64(0xFF0000), np.uint64(0xFF000000), np.uint64(0xFF00000000), np.uint64(0xFF0000000000), 
    #                 np.uint64(0xFF000000000000), np.uint64(0xFF00000000000000)]

    # # from file A to H
    # file_masks = [ np.uint64(0x101010101010101), np.uint64(0x202020202020202),
    #     np.uint64(0x404040404040404),
    #     np.uint64(0x808080808080808),
    #     np.uint64(0x1010101010101010),
    #     np.uint64(0x2020202020202020),
    #     np.uint64(0x4040404040404040),
    #     np.uint64(0x8080808080808080),
    #     ]



    # from top right to bottom left
    diagonal_masks = [
        np.uint64(0x8000000000000000), np.uint64(0X4080000000000000), np.uint64(0X2040800000000000), np.uint64(0x1020408000000000), 
        np.uint64(0x810204080000000), np.uint64(0x408102040800000), np.uint64(0x204081020408000), np.uint64(0x102040810204080), 
        np.uint64(0x1020408102040), np.uint64(0x10204081020), np.uint64(0x102040810), np.uint64(0x1020408),
        np.uint64(0x10204), np.uint64(0x102), np.uint64(0x1)

    ]
    # from top left to bottom right
    antidiagonal_masks = [ np.uint64(0x100000000000000), np.uint64(0x201000000000000), np.uint64(0x402010000000000), np.uint64(0x804020100000000),
                    np.uint64(0x1008040201000000), np.uint64(0x2010080402010000), np.uint64(0x4020100804020100), np.uint64(0x8040201008040201),
                    np.uint64(0x80402010080402), np.uint64(0x804020100804), np.uint64(0x8040201008), np.uint64(0x80402010), np.uint64(0x804020), 
                    np.uint64(0x8040), np.uint64(0x80)
    ]

    ## from rank 1 to 8
    rank_masks = [np.uint64(0xFF00000000000000), np.uint64(0xFF000000000000), np.uint64(0xFF0000000000), np.uint64(0xFF00000000),
                np.uint64(0xFF000000), np.uint64(0xFF0000), np.uint64(0xFF00), np.uint64(0xFF)]

    # from file H to A
    file_masks = [
        np.uint64(0x8080808080808080),
        np.uint64(0x4040404040404040),
        np.uint64(0x2020202020202020),
        np.uint64(0x1010101010101010),
        np.uint64(0x808080808080808),
        np.uint64(0x404040404040404),
        np.uint64(0x202020202020202),
        np.uint64(0x101010101010101)
    ]
    
    @staticmethod
    def get_bit_on_board(idx, board: np.uint64):
        if not (0 <= idx < 64):
            raise Exception("Square must be from 0 to 63")
        bshift = np.uint64(np.uint64(63) - np.uint64(idx))
        return ((board >> bshift) & np.uint64(1))
    
    @staticmethod
    # Function to print a single mask as a grid
    def print_board_2(board):
        for i in range(8):
            for j in range(8):
                idx = np.uint64(i * 8 + j)
                if (BitBoard.get_bit_on_board(idx, board)):
                    print('1', end=' ')
                else:
                    print('0', end=' ')
            print()
        print("\n\n")

    def reverse_bits(self, x: np.uint64) -> np.uint64:
        x = ((x & np.uint64(0x5555555555555555)) << np.uint64(1)) | ((x & np.uint64(0xAAAAAAAAAAAAAAAA)) >> np.uint64(1))
        x = ((x & np.uint64(0x3333333333333333)) << np.uint64(2)) | ((x & np.uint64(0xCCCCCCCCCCCCCCCC)) >> np.uint64(2))
        x = ((x & np.uint64(0x0F0F0F0F0F0F0F0F)) << np.uint64(4)) | ((x & np.uint64(0xF0F0F0F0F0F0F0F0)) >> np.uint64(4))
        x = ((x & np.uint64(0x00FF00FF00FF00FF)) << np.uint64(8)) | ((x & np.uint64(0xFF00FF00FF00FF00)) >> np.uint64(8))
        x = ((x & np.uint64(0x0000FFFF0000FFFF)) << np.uint64(16)) | ((x & np.uint64(0xFFFF0000FFFF0000)) >> np.uint64(16))
        x = (x << np.uint64(32)) | (x >> np.uint64(32))
        return x & np.uint64(0xFFFFFFFFFFFFFFFF)
    
    # def reverse_bits(self, b: np.uint64):
    #     b = (b & np.uint64(0x5555555555555555)) << np.uint64(1) | ((b >> np.uint64(1)) & np.uint64(0x5555555555555555))
    #     b = (b & np.uint64(0x3333333333333333)) << np.uint64(2) | ((b >> np.uint64(2)) & np.uint64(0x3333333333333333))
    #     b = (b & np.uint64(0x0f0f0f0f0f0f0f0f)) << np.uint64(4) | ((b >> np.uint64(4)) & np.uint64(0x0f0f0f0f0f0f0f0f))
    #     b = (b & np.uint64(0x00ff00ff00ff00ff)) << np.uint64(8) | ((b >> np.uint64(8)) & np.uint64(0x00ff00ff00ff00ff))
    #     return (b << np.uint64(48)) | ((b & np.uint64(0xffff0000)) << np.uint64(16)) | ((b >> np.uint64(16)) & np.uint64(0xffff0000)) | (b >> np.uint64(48))

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
        bshift = np.uint64(63 - idx)
        return (self.board >> bshift) & np.uint64(1)
    
    ## returns a board with a single bit set at idx
    def get_single_piece_board(self, board:np.uint64, idx: int) -> np.uint64:
        if not (0 <= idx < 64):
            raise Exception(f"Square {idx} must be from 0 to 63")
        bshift = np.uint64(63 - idx)
        if not self.get_bit(idx):
            raise Exception(f"There is not a piece at index {idx}")
        return board & (np.uint64(1)<<bshift)

    def print_board(self) -> None:
        print(f"The color i am printing for is {self.color}")
        for rank in range(8):
            for file in range(8):
                square = rank * 8 + file
                # print(f"idx of the square i am printing: {square}")
                print(self.get_bit(square), end=" ")
            print("")

    # Function to print a single mask as a grid
    def print_mask(mask):
        for i in range(8):
            for j in range(8):
                idx = np.uint64(i * 8 + j)
                if (mask >> idx) & np.uint64(1):
                    print('1', end=' ')
                else:
                    print('0', end=' ')
            print()
        print("\n\n")


    @abstractmethod
    def initialize_board(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def valid_moves(self):
        pass

    @abstractmethod
    def attacking_squares(self, pieceIdx:int, enemy_board:'BitBoard', my_board:'BitBoard') -> np.uint64:
        pass

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

    def get_idxs(self) -> list[tuple[int, int]]:
        idxs: list[tuple[int, int]] = []
        for rank in range(8):
            for file in range(8):
                idx = rank * 8 + file
                if self.get_bit(idx):
                    idxs.append(rank, file)
        return idxs

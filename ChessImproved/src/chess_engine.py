from bitboards.BitBoard import BitBoard
from chessboard import Chessboard
import pygame, numpy as np
WIDTH = HEIGHT = 512
# Dimensions of the board
DIMENSION = ROWS = COLS = 8
SQ_SIZE = HEIGHT // DIMENSION

class GameState:

    def __init__(self, surface):
        self.board = Chessboard()
        self.surface = surface


    """
    Returns square index from 0-63.
     0 top-left, 63 bottom right
    """
    def coord_to_idx(self, posX: int, posY: int) -> tuple:
        x = posX // SQ_SIZE
        y = posY // SQ_SIZE
        # print(posX, posY)
        return y*8 + x

    def load(self, images: dict) -> None:
        for i in range(64):
            for key, board in self.board.get_piece_boards().items():
                if board.get_bit(i):
                    self.surface.blit(images[key], ((i%8) * SQ_SIZE, (i//8) * SQ_SIZE))
                    break
    
    def show_bg(self):
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = (234, 235, 200)
                else:
                    color = (119, 154, 88)
                rect = (col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                pygame.draw.rect(self.surface, color, rect)

    def show_valid_moves(self, whites_turn):
        if whites_turn:
            pass
        else:
            pass
    
    def get_proper_board(self, idx, white_turn):
        for board in self.board.get_piece_boards().values():
            if board.get_bit(idx) == 1:
                return board
            
        return np.uint64(0)
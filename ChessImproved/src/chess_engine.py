from bitboards.BitBoard import BitBoard
from chessboard import Chessboard
import pygame, numpy as np
from move import Move
WIDTH = HEIGHT = 512
# Dimensions of the board
DIMENSION = ROWS = COLS = 8
SQ_SIZE = HEIGHT // DIMENSION

class GameState:

    def __init__(self, surface):
        self.board = Chessboard()
        self.surface = surface
        self.move_history: list[Move] = []


    """
    Returns square index from 0-63.
     0 top-left, 63 bottom right
    """
    def coord_to_idx(self, posX: int, posY: int) -> tuple:
        x = posX // SQ_SIZE
        y = posY // SQ_SIZE
        # print(posX, posY)
        return (7 - y) * 8 + x

    def load(self, images: dict) -> None:
        for i in range(64):
            for key, board in self.board.get_piece_boards().items():
                if board.get_bit(i):
                    self.surface.blit(images[key], ((i % 8) * SQ_SIZE, (7 - (i // 8)) * SQ_SIZE))
                    # print(board.name)
                    # board.print()
                    # print()
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

    def show_valid_moves(self, white_turn):
        if white_turn:
            pass
        else:
            pass
    
    def get_proper_board(self, idx, white_turn) -> BitBoard:
        for key, board in self.board.get_piece_boards().items():
            if board.get_bit(idx) == 1:
                if white_turn and key.startswith("w"):
                    return board
                if not white_turn and key.startswith("b"):
                    return board
            
        return None

    """
    Moves piece. returns true on success.
    """
    def move(self, start, end, board_to_set, white_turn, undo=False) -> bool:
        if not board_to_set: return False
        board_to_clear = self.get_proper_board(end, not white_turn) # negate turn because we want opposite board to be captured
        if not undo:
            board_to_set.move_piece(start, end)
            if board_to_clear:
                board_to_clear.clear_bit(end)
            self.move_history.append(Move(start, end, 0)) # TODO: change flag based on move type
        else:
            board_to_set.move_piece(end, start)
            if board_to_clear:
                board_to_clear.set_bit(end)
            self.move_history.pop()
        return True
import pygame, numpy as np
from bitboards.BitBoard import BitBoard

WIDTH = HEIGHT = 512
# Dimensions of the board
DIMENSION = ROWS = COLS = 8
SQ_SIZE = HEIGHT // DIMENSION

class Dragger():

    def __init__(self):
        self.is_dragging = False
        self.mouseX = -100
        self.mouseY = -100
        self.old_idx = 0
        self.new_idx = 0
        self.piece: BitBoard = None

    def update_mouse(self, pos) -> None:
        self.mouseX, self.mouseY = pos

    def update_blit(self, surface) -> None:
        img = pygame.image.load(self.piece.file)
        img_center = (self.mouseX, self.mouseY)
        surface.blit(img, img.get_rect(center=img_center))

    def get_old_idx(self) -> int:
        return self.old_idx

    def drag(self, new_idx):
        self.new_idx = new_idx
        self.is_dragging = False

    def update_pos(self, board: BitBoard, idx) -> None:
        if not board:
            return
        if not board.get_bit(idx):
            return
        self.old_idx = idx
        self.is_dragging = True
        self.piece = board
        board.clear_bit(idx)
    
    def reset(self):
        self.is_dragging = False
        self.piece = None
        self.mouseX = -100
        self.mouseY = -100
        self.old_idx = 0
        self.new_idx = 0
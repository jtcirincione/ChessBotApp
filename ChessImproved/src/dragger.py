import pygame, numpy as np
from bitboards.BitBoard import BitBoard

WIDTH = HEIGHT = 512
# Dimensions of the board
DIMENSION = ROWS = COLS = 8
SQ_SIZE = HEIGHT // DIMENSION

class Dragger():

    def __init__(self):
        self.dragging = False
        self.mouseX = -100
        self.mouseY = -100
        self.old_idx = 0
        self.new_idx = 0

    def update_mouse(self, pos) -> None:
        self.mouseX, self.mouseY = pos

    def update_blit(self, surface) -> None:
        piece = self.piece_board
        img = pygame.image.load(piece.file)
        img_center = (self.mouseX, self.mouseY)
        surface.blit(img, img.get_rect(center=img_center))

    def drag(self, new_idx, bitboard: BitBoard, board_to_clear: BitBoard=np.uint64):
        if not bitboard:
            print(f"invalid move")
        bitboard.move_piece(self.old_idx, new_idx)
        self.old_idx = new_idx
        if board_to_clear:
            board_to_clear.clear_bit(new_idx)
        self.new_idx = new_idx
        self.is_dragging = False

    def update_pos(self, board: BitBoard, idx) -> None:
        if not board:
            return
        if not board.get_bit(idx):
            return
        self.oldIdx = idx
        self.is_dragging = True
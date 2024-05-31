"""
Deals with user input
"""

import pygame as p
import ChessEngine
from Dragger import Dragger

# Size of board
WIDTH = HEIGHT = 512
# Dimensions of the board
DIMENSION = ROWS = COLS = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
'''
Load images initializes a global dict of images.
'''
def loadImages():
  pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', "bQ"]
  for piece in pieces:
    IMAGES[piece] = p.image.load("images/" + piece + ".png")

def show_bg(surface):
  for row in range(ROWS):
    for col in range(COLS):
      if (row + col) % 2 == 0:
        color = (234, 235, 200)
      else:
        color = (119, 154, 88)
      rect = (col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
      p.draw.rect(surface, color, rect)
      
def coord_to_idx(posX:int, posY:int) -> tuple:
  x = posX // SQ_SIZE
  y = posY // SQ_SIZE
  # print(posX, posY)
  return (x, y)

p.init()
canvas = p.display.set_mode((WIDTH,HEIGHT))
exit=False

loadImages()
game = ChessEngine.GameState()
dragger = Dragger()
while not exit: 
    show_bg(canvas)
    game.load(canvas, IMAGES)
    for event in p.event.get(): 
        if event.type == p.QUIT: 
            exit = True
            
        if event.type == p.MOUSEBUTTONDOWN:
          posX, posY = p.mouse.get_pos()
          col, row = coord_to_idx(posX, posY)
          if not dragger.is_dragging:
            dragger.update_pos(game.board, row, col)
          else:
            v = game.is_valid_move(piece=dragger.get_piece(), board=game.board, init_row=dragger.prevRow, init_col=dragger.prevCol, move_row=row, move_col=col, canvas=canvas)
            if v:
              game.board = dragger.drag(game.board, row, col)
              dragger.undrag()
            else:
              dragger.undrag()
              continue
    p.display.update() 
    
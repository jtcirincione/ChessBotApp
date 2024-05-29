"""
Deals with user input
"""

import pygame as p
import ChessEngine

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
      

p.init()
canvas = p.display.set_mode((WIDTH,HEIGHT))
exit=False

loadImages()
game = ChessEngine.GameState()
while not exit: 
    show_bg(canvas)
    game.load(canvas, IMAGES)
    for event in p.event.get(): 
        if event.type == p.QUIT: 
            exit = True
    p.display.update() 
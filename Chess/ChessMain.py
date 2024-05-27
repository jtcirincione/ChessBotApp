"""
Deals with user input
"""

import pygame as p
from Chess import ChessEngine

# Size of board
WIDTH = HEIGHT = 512
# Dimensions of the board
DIMENSION = 8
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

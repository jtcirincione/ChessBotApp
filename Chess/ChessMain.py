"""
Deals with user input
"""

import pygame as p
import ChessEngine
from Dragger import Dragger
from Piece import Pawn

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
  ## add promotion pieces
  promotion_pieces = [('promotewQ', 'wQ'), ('promotewR', 'wR'), ('promotewB', 'wB'), ('promotewN', 'wN'), ('promotebQ', 'bQ'), ('promotebR', 'bR'), ('promotebB', 'bB'), ('promotebN', 'bN')]
  for piece, name in promotion_pieces:
    IMAGES[piece] = p.image.load("images/" + name + ".png")
     
p.init()
canvas = p.display.set_mode((WIDTH,HEIGHT))
exit=False

loadImages()
game = ChessEngine.GameState(canvas)
dragger = Dragger()
promoting = False
while not exit: 
    game.show_bg()
    game.load(IMAGES)
    if promoting:
      game.draw_promotions(piece=dragger.get_piece(), images=IMAGES)
    for event in p.event.get(): 
        if event.type == p.QUIT: exit = True
            
        if event.type == p.MOUSEBUTTONDOWN:
          posX, posY = p.mouse.get_pos()
          col, row = game.coord_to_idx(posX, posY)
          if promoting:
            move_row, move_col = dragger.get_moved_location()            
            promoting = game.promote(move_row=move_row, move_col=move_col, men_row=row, men_col=col, color=dragger.get_piece().color)
            continue
          if not dragger.is_dragging: dragger.update_pos(game.board, row, col)
          else:
            valid_move = game.is_valid_move(piece=dragger.get_piece(), board=game.board, init_row=dragger.prevRow, init_col=dragger.prevCol, move_row=row, move_col=col, canvas=game.surface)
            
            if valid_move:
              if isinstance(dragger.get_piece(), Pawn):
                ## check if promotion move
                if dragger.get_piece().promote_row == row:
                  print("PROMOTING")
                  promoting = True
                  game.board = dragger.drag(game.board, row, col)
                  game.draw_promotions(piece=dragger.get_piece(), images=IMAGES)
                  continue
              game.board = dragger.drag(game.board, row, col)
                
              dragger.undrag()
            ## undo move for invalid
            else:
              dragger.undrag()
              continue
    p.display.update() 
    
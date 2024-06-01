"""
Responsible for storing all info about the current state of a chess game and validates moves. Keeps a move log.
"""
WIDTH = HEIGHT = 512
# Dimensions of the board
DIMENSION = ROWS = COLS = 8
SQ_SIZE = HEIGHT // DIMENSION
import pygame
from Piece import Piece, Pawn, Rook, Knight, King, Queen, Bishop
class GameState():
  # Size of board
  def __init__(self, surface):
    # 8x8 2d list representing the board
    self.board = [
      [Rook("bR", "black"), Knight("bN", "black"), Bishop("bB", "black"), Queen("bQ", "black"), King("bK", "black"), Bishop("bB", "black"), Knight("bN", "black"), Rook("bR", "black")],
      [Pawn("bp", "black"), Pawn("bp", "black"), Pawn("bp", "black"), Pawn("bp", "black"), Pawn("bp", "black"), Pawn("bp", "black"), Pawn("bp", "black"), Pawn("bp", "black")],
      ["--", "--", "--", "--", "--", "--", "--", "--"],
      ["--", "--", "--", "--", "--", "--", "--", "--"],
      ["--", "--", "--", "--", "--", "--", "--", "--"],
      ["--", "--", "--", "--", "--", "--", "--", "--"],
      [Pawn("wp", "white"), Pawn("wp", "white"), Pawn("wp", "white"), Pawn("wp", "white"), Pawn("wp", "white"), Pawn("wp", "white"), Pawn("wp", "white"), Pawn("wp", "white")],
      [Rook("wR", "white"), Knight("wN", "white"), Bishop("wB", "white"), Queen("wQ", "white"), King("wK", "white"), Bishop("wB", "white"), Knight("wN", "white"), Rook("wR", "white")]
    ]
    self.whiteToMove: bool = True
    self.moveLog: list = []
    self.surface = surface
    self.promotions = {
      "Knight": [(7, 7), (0, 6)],
      "Queen": [(7, 6), (0, 7)],
      "Rook": [(7, 5), (0, 5)],
      "Bishop": [(7 , 4), (0, 4)]
    }
  
  def coord_to_idx(self, posX:int, posY:int) -> tuple:
    x = posX // SQ_SIZE
    y = posY // SQ_SIZE
    # print(posX, posY)
    return (x, y)
  
  def show_bg(self):
    for row in range(ROWS):
      for col in range(COLS):
        if (row + col) % 2 == 0:
          color = (234, 235, 200)
        else:
          color = (119, 154, 88)
        rect = (col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        pygame.draw.rect(self.surface, color, rect)
      
    
  def load(self, images:dict) -> None:
    for row in range(len(self.board)):
      for col in range(len(self.board[row])):
        if self.board[row][col] != "--":
          self.surface.blit(images[self.board[row][col].name], (col * SQ_SIZE, row * SQ_SIZE))
          
  # After a move has been made, reblit the moved piece
  # def draw_move(self, surface: pygame.Surface, row: int, col: int, images: dict) -> None:
  #   # surface.blit(images[self.board[row][col].name], (col * SQ_SIZE, row * SQ_SIZE))
  #   pass
    
  def is_valid_move(self, piece:Piece, board:list, init_row:int, init_col:int, move_row:int, move_col:int, canvas) -> bool:
    return piece.is_valid(board=board, row=init_row, col=init_col, moveRow=move_row, moveCol=move_col)
  
  def draw_promotions(self, piece: Piece, images:dict) -> None:
    if not isinstance(piece, Pawn):
      return
    if piece.color == "black":
      self.surface.blit(images["promotebN"], (7 * SQ_SIZE, 7 * SQ_SIZE))
      self.surface.blit(images["promotebQ"], (6 * SQ_SIZE, 7 * SQ_SIZE))
      self.surface.blit(images["promotebR"], (5 * SQ_SIZE, 7 * SQ_SIZE))
      self.surface.blit(images["promotebB"], (4 * SQ_SIZE, 7 * SQ_SIZE))
    else:
      self.surface.blit(images["promotewQ"], (7 * SQ_SIZE, 0 * SQ_SIZE))
      self.surface.blit(images["promotewN"], (6 * SQ_SIZE, 0 * SQ_SIZE))
      self.surface.blit(images["promotewR"], (5 * SQ_SIZE, 0 * SQ_SIZE))
      self.surface.blit(images["promotewB"], (4 * SQ_SIZE, 0 * SQ_SIZE))
  
  ## Might fix later but return true if method fails (didn't promote), return false if promoted
  def promote(self, move_row:int, move_col:int, men_row:int, men_col:int, color:str) -> bool:
    print(f"indices: ({men_row}, {men_col})")
    for key, val in self.promotions.items():
      if (men_row, men_col) in val:
        print(f"Selected item: {key}, {val}")
        if key == "Queen":
          if color == "black":
            self.board[move_row][move_col] = Queen("bQ", color)
          else:
            self.board[move_row][move_col] = Queen("wQ", color)
        elif key == "Knight":
          if color == "black":
            self.board[move_row][move_col] = Knight("bN", color)
          else:
            self.board[move_row][move_col] = Knight("wN", color)
        elif key == "Bishop":
          if color == "black":
            self.board[move_row][move_col] = Bishop("bB", color)
          else:
            self.board[move_row][move_col] = Bishop("wB", color)
        elif key == "Rook":
          if color == "black":
            self.board[move_row][move_col] = Rook("bR", color)
          else:
            self.board[move_row][move_col] = Rook("wR", color)
            
        return False
    return True
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
  def __init__(self):
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
    
  def load(self, surface: pygame.Surface, images:dict) -> None:
    for row in range(len(self.board)):
      for col in range(len(self.board[row])):
        if self.board[row][col] != "--":
          surface.blit(images[self.board[row][col].name], (col * SQ_SIZE, row * SQ_SIZE))
          
  # After a move has been made, reblit the moved piece
  # def draw_move(self, surface: pygame.Surface, row: int, col: int, images: dict) -> None:
  #   # surface.blit(images[self.board[row][col].name], (col * SQ_SIZE, row * SQ_SIZE))
  #   pass
    
  def is_valid_move(self, piece, init_row, init_col, move_row, move_col) -> bool:
    if isinstance(piece, Pawn):
      pass
    elif isinstance(piece, Rook):
      pass
    elif isinstance(piece, Knight):
      pass
    elif isinstance(piece, Bishop):
      pass
    elif isinstance(piece, Queen):
      pass
    elif isinstance(piece, King):
      pass
    
    ## cut down on code and instead write valid move logic in piece classes for each piece, and just make 1 method call here.
    return 0
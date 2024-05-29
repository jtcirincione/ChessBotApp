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
    self.whiteToMove = True
    self.moveLog = []
    
  def load(self, surface: pygame.Surface, images:dict) -> None:
    for row in range(len(self.board)):
      for col in range(len(self.board[row])):
        if self.board[row][col] != "--":
          surface.blit(images[self.board[row][col].name], (col * SQ_SIZE, row * SQ_SIZE))
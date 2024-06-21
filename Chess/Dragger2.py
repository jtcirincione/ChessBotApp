from Piece import Piece, Pawn, Rook, Knight, King, Queen, Bishop
from ChessEngine import GameState
from bitboards.BitBoard import BitBoard
from bitboards.PawnBoard import PawnBoard
from bitboards.RookBoard import RookBoard
from bitboards.BishopBoard import BishopBoard
from bitboards.KingBoard import KingBoard
from bitboards.QueenBoard import QueenBoard
from bitboards.KnightBoard import KnightBoard
import copy
import pygame, numpy as np
WIDTH = HEIGHT = 512
# Dimensions of the board
DIMENSION = ROWS = COLS = 8
SQ_SIZE = HEIGHT // DIMENSION

class Dragger2:
    def __init__(self):
        self.oldIdx = 0
        self.piece_board: BitBoard = None
        self.is_dragging = False
        self.mouseX = -100
        self.mouseY = -100

    def update_pos(self, board: BitBoard, idx, game: GameState) -> None:
        if not board.get_bit(idx):
            return
        if board.color == 'black' and game.white_to_move() == True or board.color == 'white' and game.white_to_move() == False:
            return
        self.piece_board = board
        self.oldIdx = idx
        self.is_dragging = True

    def update_mouse(self, pos) -> None:
        self.mouseX, self.mouseY = pos

    def update_blit(self, surface) -> None:
        piece = self.piece_board
        img = pygame.image.load(piece.file)
        img_center = (self.mouseX, self.mouseY)
        surface.blit(img, img.get_rect(center=img_center))

    def illuminate_moves(self, surface, my_board, opp_board) -> None:
        moves = self.piece_board.attacking_squares(self.oldIdx, my_board, opp_board)

        for row in range(8):
            for col in range(8):
                idx = row * 8 + col
                if BitBoard.get_bit_on_board(idx, moves) == 1:
                    rect = (col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                    color = (255,255,102)
                    pygame.draw.rect(surface=surface, color=color, rect=rect)

    def illuminate_all_moves(self, surface, boards: list[BitBoard], color):
        moves = np.uint64(0)
        for i in range(8):
            for j in range(8):
                idx = np.uint64(i * 8 + j)
                for board in boards:
                    if board.get_bit(idx):
                        if board.color == color:
                            moves |= board.attacking_squares(idx)
        print(f"I, {color}, have {len(moves)} valid moves.")
        for row in range(8):
            for col in range(8):
                idx = np.uint64(row * 8 + col)
                if BitBoard.get_bit_on_board(idx, moves):
                    rect = (col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                    color = (255,255,102)
                    pygame.draw.rect(surface=surface, color=color, rect=rect)


    def drag2(self, bitboard: BitBoard, newIdx, my_board, opp_board, board_to_clear: BitBoard=np.uint64(0)):
        dragged: bool = False
        if bitboard.get_bit_on_board(newIdx, bitboard.attacking_squares(self.oldIdx, my_board, opp_board)):
            bitboard.move_piece(self.oldIdx, newIdx)
            self.oldIdx = newIdx
            dragged = True
        self.is_dragging = False
        if board_to_clear:
            board_to_clear.clear_bit(newIdx)
        return dragged

    
    def simulate_drag(self, board: list, x: int, y: int) -> list:
        tmp_board = copy.deepcopy(board)
        tmp_board[self.prevRow][self.prevCol] = "--"
        tmp_board[x][y] = self.piece
        return tmp_board


    def simulate_drag_v2(self, board, prev_row:int, prev_col:int, move_row:int, move_col:int) -> list[list]:
        tmp_board = copy.deepcopy(board)
        piece = tmp_board[prev_row][prev_col]
        if isinstance(piece, Pawn) or isinstance(piece, Rook) or isinstance(piece, King):
            piece.has_moved = True

        
        if isinstance(piece, Pawn):
            piece.moved()
            # TODO: Refactor elsewhere
            # If pawn moved 2 spots, set en passant to true
            if abs(move_row - prev_row) == 2:
                piece.set_passant_active()
            else:
                piece.set_passant_inactive()
            # TODO: Now check if we are moving diagonally to an empty square.
            # if we are, remove the piece ether behind or in front of the move location
            # depending on current piece's color
            if tmp_board[move_row][move_col] == "--" and abs(move_row - prev_row) == 1 and abs(move_col - prev_col) == 1:
                if piece.color == "white":
                    tmp_board[move_row + 1][move_col] = "--"
                else:
                    tmp_board[move_row - 1][move_col] = "--"

            ## CASTLING LOGIC
        if isinstance(piece, King):
            piece.has_moved = True
            if abs(move_col - prev_col == 2):
                ## if castling left
                if prev_col - move_col > 0:
                    ## move rook one space to the right of moved king
                    rook = tmp_board[move_row][0]
                    tmp_board[move_row][0] = "--"
                    tmp_board[move_row][move_col+1] = rook
                    rook.has_moved = True
                ## castling right
                else:
                    ## move rook one space to the left of moved king
                    rook = tmp_board[move_row][7]
                    tmp_board[move_row][7] = "--"
                    tmp_board[move_row][move_col-1] = rook
                    rook.has_moved = True

        tmp_board[prev_row][prev_col] = "--"
        tmp_board[move_row][move_col] = piece
        return tmp_board


    # def simulate_drag_v2(self, board, prev_row, prev_col, move_row, move_col):
    #     tmp_board = copy.deepcopy(board)
    #     piece = tmp_board[prev_row][prev_col]
    #     tmp_board[prev_row][prev_col] = "--"
    #     tmp_board[move_row][move_col] = piece
    #     return tmp_board

    def undrag(self):
        self.is_dragging = False
        self.oldIdx = 0
        self.piece = None
        self.mouseX = 0
        self.mouseY = 0

    def get_piece(self) -> Piece:
        return self.piece

    def get_moves(self) -> list:
        return None

    def get_moved_location(self) -> tuple:
        return (self.postRow, self.postCol)

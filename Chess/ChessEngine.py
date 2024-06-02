"""
Responsible for storing all info about the current state of a chess game and validates moves. Keeps a move log.
"""
from Piece import Piece, Pawn, Rook, Knight, King, Queen, Bishop
import pygame
WIDTH = HEIGHT = 512
# Dimensions of the board
DIMENSION = ROWS = COLS = 8
SQ_SIZE = HEIGHT // DIMENSION


class GameState():
    # Size of board
    def __init__(self, surface):
        # 8x8 2d list representing the board
        self.board = [
            [Rook("bR", "black"), Knight("bN", "black"), Bishop("bB", "black"), Queen("bQ", "black"), King(
                "bK", "black"), Bishop("bB", "black"), Knight("bN", "black"), Rook("bR", "black")],
            [Pawn("bp", "black"), Pawn("bp", "black"), Pawn("bp", "black"), Pawn("bp", "black"), Pawn(
                "bp", "black"), Pawn("bp", "black"), Pawn("bp", "black"), Pawn("bp", "black")],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            [Pawn("wp", "white"), Pawn("wp", "white"), Pawn("wp", "white"), Pawn("wp", "white"), Pawn(
                "wp", "white"), Pawn("wp", "white"), Pawn("wp", "white"), Pawn("wp", "white")],
            [Rook("wR", "white"), Knight("wN", "white"), Bishop("wB", "white"), Queen("wQ", "white"), King(
                "wK", "white"), Bishop("wB", "white"), Knight("wN", "white"), Rook("wR", "white")]
        ]
        self.whiteToMove: bool = True
        self.moveLog: list = []
        self.black_king_check = False
        self.white_king_check = True
        self.surface = surface
        self.promotions = {
            "Knight": [(7, 7), (0, 6)],
            "Queen": [(7, 6), (0, 7)],
            "Rook": [(7, 5), (0, 5)],
            "Bishop": [(7, 4), (0, 4)]
        }

    def coord_to_idx(self, posX: int, posY: int) -> tuple:
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

    def load(self, images: dict) -> None:
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] != "--":
                    self.surface.blit(
                        images[self.board[row][col].name], (col * SQ_SIZE, row * SQ_SIZE))

    # After a move has been made, reblit the moved piece
    # def draw_move(self, surface: pygame.Surface, row: int, col: int, images: dict) -> None:
    #   # surface.blit(images[self.board[row][col].name], (col * SQ_SIZE, row * SQ_SIZE))
    #   pass

    def is_valid_move(self, piece: Piece, board: list, init_row: int, init_col: int, move_row: int, move_col: int, canvas) -> bool:
        return piece.is_valid(board=board, row=init_row, col=init_col, moveRow=move_row, moveCol=move_col)

    def draw_promotions(self, piece: Piece, images: dict) -> None:
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

    # Might fix later but return true if method fails (didn't promote), return false if promoted
    def promote(self, move_row: int, move_col: int, men_row: int, men_col: int, color: str) -> bool:
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

    # Switch turn to next player
    def finish_turn(self) -> None:
        self.whiteToMove = False if self.whiteToMove == True else True

    def white_to_move(self) -> bool:
        return self.whiteToMove

    def rank_moves(self, row, col, opposing_color):
        moves = []
        # look at each move to the left of piece
        for i in range(col - 1, -1, -1):
            if self.board[row][i] == "--":
                moves.append((row, i))
            elif self.board[row][i].color == self.opponent:
                moves.append((row, i))
                break
            else:
                break
        # look at each move to the right of piece
        for i in range(col + 1, 8):
            if self.board[row][i] == "--":
                moves.append((row, i))
            elif self.board[row][i].color == self.opponent:
                moves.append((row, i))
                break
            else:
                break
        return moves

    def file_moves(self, board, row, col, opposing_color):
        moves = []
        # look at each move above a piece
        for i in range(row - 1, -1, -1):
            piece = board[i][col]
            if board[i][col] == "--":
                pass
            elif piece.color == opposing_color:
                if isinstance(piece, Rook) or isinstance(piece, Queen):
                    return True
                break
            else:
                break
        # look at each move to below a piece
        for i in range(row+1, 8):
            if board[i][col] == "--":
                moves.append((i, col))
            elif board[i][col].color == self.opponent:
                moves.append((i, col))
                break
            else:
                break
        return moves

    def left_diagonal(self, board, row, col) -> list:
        moves = []
        # Top left diagonal
        j = col - 1
        for i in range(row-1, -1, -1):
            if j < 0:
                break
            piece = board[i][j]
            if piece == "--":
                pass
            elif piece.color == self.opponent:
                if isinstance(piece, Bishop) or isinstance(piece, Queen):
                    return True
                break
            else:
                break
            j -= 1

        # Bottom part of diagonal
        leave = False
        j = col + 1
        for i in range(row+1, 8,):
            if j > 7:
                break
            if board[i][j] == "--":
                pass
            elif board[i][j].color == self.opponent:
                if isinstance(piece, Bishop) or isinstance(piece, Queen):
                    return True
                break
            else:
                break
            j += 1
        return moves
    # check if king is safe on right diagonal

    def right_diagonal(self, board, row, col, opposing_color) -> list:
        moves = []
        # Top right diagonal
        j = col + 1
        for i in range(row-1, -1, -1):
            if j > 7:
                break
            piece = board[i][j]
            if piece == "--":
                pass
            elif piece.color == opposing_color:
                if isinstance(piece, Bishop) or isinstance(piece, Queen):
                    return True
                break
            else:
                break
            j += 1

        # Bottom part of diagonal
        j = col-1
        for i in range(row+1, 8,):
            if j < 0:
                break
            piece = board[i][j]
            if piece == "--":
                pass
            elif piece.color == opposing_color:
                if isinstance(piece, Bishop) or isinstance(piece, Queen):
                    return True
                break
            else:
                break
            j -= 1
        return False

    # take in a board as a parameter instead of using self,
    # as we send a board copy simulating a move to check if
    # it exposes the king
    def king_in_check(self, king_chk_color: str, board: list) -> bool:
        piece = None
        c = "black" if king_chk_color == "white" else "black"
        for i in range(0, 8):
            for j in range(0, 8):
                if isinstance(board[i][j], King):
                    if board[i][j].color == king_chk_color:
                        piece = board[i][j]

        return False

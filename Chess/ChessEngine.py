"""
Responsible for storing all info about the current state of a chess game and validates moves. Keeps a move log.
"""
from Piece import Piece, Pawn, Rook, Knight, King, Queen, Bishop
from Move import Move
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
        self.white_king_check = False
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

    def reset(self):
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
        self.white_king_check = False

    # After a move has been made, reblit the moved piece
    # def draw_move(self, surface: pygame.Surface, row: int, col: int, images: dict) -> None:
    #   # surface.blit(images[self.board[row][col].name], (col * SQ_SIZE, row * SQ_SIZE))
    #   pass

    def is_valid_move(self, piece: Piece, board: list, init_row: int, init_col: int, move_row: int, move_col: int, canvas) -> bool:
        moves:list[Move] = piece.valid_moves(board=board, row=init_row, col=init_col)
        for move in moves:
            if (move_row, move_col) == move.get_final():
                return True
        return False

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
    
    def current_turn(self) -> str:
        return "white" if self.white_to_move() else "black"
    
    def opponent(self) -> str:
        return "black" if self.white_to_move() else "white"
    
    def iam_checked(self) -> bool:
        if self.current_turn() == 'white':
            if self.white_king_check == True:
                return True
        else:
            if self.black_king_check == True:
                return True
        return False
    
    #Set the white or black king to checked based on color parameter
    def set_king_checked(self, color) -> None:
        if color == "white":
            self.white_king_check = True 
        else:
            self.black_king_check = True
        

    def rank_moves(self, board, row, col, opposing_color):
        # look at each move to the left of piece
        for i in range(col - 1, -1, -1):
            piece = board[row][i]
            if piece == "--":
                pass
            elif piece.color == opposing_color:
                if isinstance(piece, Rook) or isinstance(piece, Queen):
                    return True
                break
            else:
                break
        # look at each move to the right of piece
        for i in range(col + 1, 8):
            piece = board[row][i]
            if piece == "--":
                pass
            elif piece.color == opposing_color:
                if isinstance(piece, Rook) or isinstance(piece, Queen):
                    return True
                break
            else:
                break
        return False

    def file_moves(self, board: list[list[Piece]], row, col, opposing_color):
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
            piece = board[i][col]
            if piece == "--":
                pass
            elif piece.color == opposing_color:
                if isinstance(piece, Rook) or isinstance(piece, Queen):
                    return True
                break
            else:
                break
        return False

    def left_diagonal(self, board, row, col, opposing_color) -> list:
        moves = []
        # Top left diagonal
        j = col - 1
        for i in range(row-1, -1, -1):
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

        # Bottom part of diagonal
        leave = False
        j = col + 1
        for i in range(row+1, 8,):
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

    def knight_moves(self, board, row:int, col:int, opposing_color):
        idxs = [
            (row-2, col-1),
            (row-1, col-2),
            (row-2, col+1),
            (row-1, col+2),
            (row+2, col-1),
            (row+1, col-2),
            (row+2, col+1),
            (row+1, col+2)
        ]
        for i, j in idxs:
            if (i < 0 or i > 7 or j < 0 or j > 7):
                continue
            piece = board[i][j]
            if piece == "--":
                pass
            elif piece.color == opposing_color:
                if isinstance(piece, Knight):
                    return True

        return False

    def pawn_danger(self, board, row:int, col:int, opposing_color):
        dangerColLeft = col-1
        dangerColRight = col + 1
        if opposing_color == "black":
            dangerRow = row - 1
            if dangerRow < 0:
                return False
        else:
            dangerRow = row + 1
            if dangerRow > 7:
                return False

        if dangerColLeft >= 0:
            piece = board[dangerRow][dangerColLeft]
            if isinstance(piece, Pawn) and piece.color == opposing_color:
                return True
        if dangerColRight < 8:
            piece = board[dangerRow][dangerColRight]
            if isinstance(piece, Pawn) and piece.color == opposing_color:
                return True
        return False

    # take in a board as a parameter instead of using self,
    # as we send a board copy simulating a move to check if
    # it exposes the king
    def king_in_check(self, king_chk_color: str, board: list) -> bool:
        piece = None
        opposing_color = "black" if king_chk_color == "white" else "white"
        row = col = None
        tmp = False
        for i in range(8):
            for j in range(8):
                if isinstance(board[i][j], King):
                    if board[i][j].color == king_chk_color:
                        tmp = True
                        piece = board[i][j]
                        row, col = i, j
                        break
        if tmp == False:
            self.board= board
        in_check = self.pawn_danger(board, row, col, opposing_color) or self.right_diagonal(board, row, col, opposing_color) or self.left_diagonal(board, row, col, opposing_color) or self.file_moves(board, row, col, opposing_color) or self.rank_moves(board, row, col, opposing_color) or self.knight_moves(board, row, col, opposing_color)
        if in_check:
            self.set_king_checked(king_chk_color)
            print("CHECKED")
            print(f"King being checked: {king_chk_color}")
            print(f"Should be true: {self.iam_checked()}")
        return in_check
    
    def has_valid_moves(self, board, dragger):
        moves:list[Move] = []
        for i in range(8):
            for j in range(8):
                if isinstance(board[i][j], Piece):
                    if board[i][j].color == self.current_turn():
                        piece = board[i][j]
                        moves += piece.valid_moves(board, i, j)

        for move in moves:
            init_row, init_col = move.get_initial()
            fin_row, fin_col = move.get_final()
            b = dragger.simulate_drag_v2(board, init_row, init_col, fin_row, fin_col)
            if not self.king_in_check(self.current_turn(), b):
                return True
        
        return False

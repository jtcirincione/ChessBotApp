# Size of board
from Move import Move
import pygame as p
WIDTH = HEIGHT = 512
# Dimensions of the board
DIMENSION = ROWS = COLS = 8
SQ_SIZE = HEIGHT // DIMENSION


class Piece:
    def __init__(self, name, color):
        self.color: str = color
        self.name: str = name
        self.opponent: str = "white" if color == "black" else "black"


    def rank_moves(self, board, row, col):
        moves = []
        # look at each move to the left of piece
        for i in range(col - 1, -1, -1):
            if board[row][i] == "--":
                moves.append(Move(init_row=row, init_col=col, fin_row=row, fin_col=i))
            elif board[row][i].color == self.opponent:
                moves.append(Move(init_row=row, init_col=col, fin_row=row, fin_col=i))
                break
            else:
                break
        # look at each move to the right of piece
        for i in range(col + 1, 8):
            if board[row][i] == "--":
                moves.append(Move(init_row=row, init_col=col, fin_row=row, fin_col=i))
            elif board[row][i].color == self.opponent:
                moves.append(Move(init_row=row, init_col=col, fin_row=row, fin_col=i))
                break
            else:
                break
        return moves

    def file_moves(self, board, row, col):
        moves = []
        # look at each move above a piece
        for i in range(row - 1, -1, -1):
            if board[i][col] == "--":
                moves.append(Move(init_row=row, init_col=col, fin_row=i, fin_col=col))
            elif board[i][col].color == self.opponent:
                moves.append(Move(init_row=row, init_col=col, fin_row=i, fin_col=col))
                break
            else:
                break
        # look at each move to below a piece
        for i in range(row+1, 8):
            if board[i][col] == "--":
                moves.append(Move(init_row=row, init_col=col, fin_row=i, fin_col=col))
            elif board[i][col].color == self.opponent:
                moves.append(Move(init_row=row, init_col=col, fin_row=i, fin_col=col))
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
            if board[i][j] == "--":
                moves.append(Move(init_row=row, init_col=col, fin_row=i, fin_col=j))
            elif board[i][j].color == self.opponent:
                moves.append(Move(init_row=row, init_col=col, fin_row=i, fin_col=j))
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
                moves.append(Move(init_row=row, init_col=col, fin_row=i, fin_col=j))
            elif board[i][j].color == self.opponent:
                moves.append(Move(init_row=row, init_col=col, fin_row=i, fin_col=j))
                leave = True
                break
            else:
                leave = True
                break
            j += 1
        return moves

    def right_diagonal(self, board, row, col) -> list:
        moves = []
        # Top right diagonal
        j = col + 1
        for i in range(row-1, -1, -1):
            if j > 7:
                break
            if board[i][j] == "--":
                moves.append(Move(init_row=row, init_col=col, fin_row=i, fin_col=j))
            elif board[i][j].color == self.opponent:
                moves.append(Move(init_row=row, init_col=col, fin_row=i, fin_col=j))
                leave = True
                break
            else:
                leave = True
                break
            j += 1

        # Bottom part of diagonal
        j = col-1
        for i in range(row+1, 8,):
            if j < 0:
                break
            if board[i][j] == "--":
                moves.append(Move(init_row=row, init_col=col, fin_row=i, fin_col=j))
            elif board[i][j].color == self.opponent:
                moves.append(Move(init_row=row, init_col=col, fin_row=i, fin_col=j))
                break
            else:
                break
            j -= 1
        return moves


class Pawn(Piece):
    def __init__(self, name, color):
        super().__init__(name, color)
        self.has_moved = False
        self.promote_row = 0 if self.color == 'white' else 7
        self.en_passant = False

    def moved(self) -> None:
        self.has_moved = True

    def can_be_passanted(self):
        return self.en_passant
    
    def set_passant_active(self):
        self.en_passant = True
    
    def set_passant_inactive(self):
        self.en_passant = False

    def valid_moves(self, board: list, row: int, col: int):
        moves = []
        is_blocked = False

        if self.has_moved == False:
            if self.color == "white":
                if row - 1 >= 0 and board[row-1][col] == "--":
                    moves.append(Move(init_row=row, init_col=col, fin_row=row - 1, fin_col=col))
                if row - 2 >= 0 and board[row-2][col] == "--" and board[row-1][col] == "--":
                    moves.append(Move(init_row=row, init_col=col, fin_row=row - 2, fin_col=col))
            # if black pawn being moved
            else:
                if row + 1 < 8 and board[row+1][col] == "--":
                    moves.append(Move(init_row=row, init_col=col, fin_row=row + 1, fin_col=col))
                if row + 2 < 8 and board[row+2][col] == "--" and board[row+1][col] == "--":
                    moves.append(Move(init_row=row, init_col=col, fin_row=row + 2, fin_col=col))
        else:
            if self.color == "white":
                if row - 1 >= 0 and board[row-1][col] == "--":
                    moves.append(Move(init_row=row, init_col=col, fin_row=row - 1, fin_col=col))
            else:
                if row + 1 >= 0 and board[row+1][col] == "--":
                    moves.append(Move(init_row=row, init_col=col, fin_row=row + 1, fin_col=col))

        if self.color == "white":
            # check diagonal left piece
            if row - 1 >= 0 and col-1 >= 0:
                if board[row-1][col-1] != "--":
                    if board[row-1][col-1].color == self.opponent:
                        moves.append(Move(init_row=row, init_col=col, fin_row=row-1, fin_col=col-1))
                else:
                    ## En passant logic
                    if isinstance(board[row][col-1], Pawn):
                        if board[row][col-1].can_be_passanted() and board[row][col-1].color == self.opponent:
                            moves.append(Move(init_row=row, init_col=col, fin_row=row-1, fin_col=col-1))
                    pass

            # check diagonal right piece
            if row - 1 >= 0 and col+1 < 8:
                if board[row-1][col+1] != "--":
                    if board[row-1][col+1].color == self.opponent:
                        moves.append(Move(init_row=row, init_col=col, fin_row=row-1, fin_col=col+1))
                else:
                    ## En passant logic
                    if isinstance(board[row][col+1], Pawn):
                        if board[row][col+1].can_be_passanted() and board[row][col+1].color == self.opponent:
                            moves.append(Move(init_row=row, init_col=col, fin_row=row-1, fin_col=col+1))
                    pass
        # if piece is black
        else:
            # check diagonal left piece
            if row+1 <= 8 and col-1 >= 0:
                if board[row+1][col-1] != "--":
                    if board[row+1][col-1].color == self.opponent:
                        moves.append(Move(init_row=row, init_col=col, fin_row=row+1, fin_col=col-1))
                else:
                    ## En passant logic
                    if isinstance(board[row][col-1], Pawn):
                        if board[row][col-1].can_be_passanted() and board[row][col-1].color == self.opponent:
                            moves.append(Move(init_row=row, init_col=col, fin_row=row-1, fin_col=col-1))
                    pass

            # check diagonal right piece
            if row+1 <= 8 and col+1 < 8:
                if board[row+1][col+1] != "--":
                    if board[row+1][col+1].color == self.opponent:
                        moves.append(Move(init_row=row, init_col=col, fin_row=row+1, fin_col=col+1))
                else:
                    ## En passant logic
                    if isinstance(board[row][col+1], Pawn):
                        if board[row][col+1].can_be_passanted() and board[row][col+1].color == self.opponent:
                            moves.append(Move(init_row=row, init_col=col, fin_row=row-1, fin_col=col+1))
                    pass
        return moves


class Knight(Piece):
    def __init__(self, name, color):
        super().__init__(name, color)

    def valid_moves(self, board, row, col):
        idxs = [
            Move(init_row=row, init_col=col, fin_row=row-2, fin_col=col-1),
            Move(init_row=row, init_col=col, fin_row=row-1, fin_col=col-2),
            Move(init_row=row, init_col=col, fin_row=row-2, fin_col=col+1),
            Move(init_row=row, init_col=col, fin_row=row-1, fin_col=col+2),
            Move(init_row=row, init_col=col, fin_row=row+2, fin_col=col-1),
            Move(init_row=row, init_col=col, fin_row=row+1, fin_col=col-2),
            Move(init_row=row, init_col=col, fin_row=row+2, fin_col=col+1),
            Move(init_row=row, init_col=col, fin_row=row+1, fin_col=col+2)
        ]
        moves = []
        for move in idxs:
            i, j = move.get_final()
            if (i < 0 or i > 7 or j < 0 or j > 7):
                continue
            if board[i][j] == "--":
                moves.append(Move(init_row=row, init_col=col, fin_row=i, fin_col=j))
            elif board[i][j].color == self.opponent:
                moves.append(Move(init_row=row, init_col=col, fin_row=i, fin_col=j))

        return moves


class Bishop(Piece):
    def __init__(self, name, color):
        super().__init__(name, color)

    def valid_moves(self, board: list, row: int, col: int) -> bool:
        moves = []
        moves = self.left_diagonal(board=board, row=row, col=col)
        moves += self.right_diagonal(board=board, row=row, col=col)
        return moves


class Rook(Piece):
    def __init__(self, name, color):
        super().__init__(name, color)

    def valid_moves(self, board, row, col):
        moves = self.rank_moves(board, row, col)
        moves += self.file_moves(board, row, col)
        return moves


class King(Piece):
    def __init__(self, name, color):
        super().__init__(name, color)

    def valid_moves(self, board, row, col):
        moves = []
        # look at rank above piece
        if row-1 >= 0:
            for j in range(col-1, col + 2):
                if j > 7:
                    break
                if j >= 0:
                    if board[row-1][j] == '--' or board[row-1][j].color == self.opponent:
                        moves.append(Move(init_row=row, init_col=col, fin_row=row-1, fin_col=j))
        # look at rank above piece
        if row+1 < 8:
            for j in range(col-1, col + 2):
                if j > 7:
                    break
                if j >= 0:
                    if board[row+1][j] == '--' or board[row+1][j].color == self.opponent:
                        moves.append(Move(init_row=row, init_col=col, fin_row=row+1, fin_col=j))

        # look at pieces to right/left
        if col-1 >= 0:
            if board[row][col-1] == '--' or board[row][col-1].color == self.opponent:
                moves.append(Move(init_row=row, init_col=col, fin_row=row, fin_col=col-1))
        if col+1 < 8:
            if board[row][col+1] == '--' or board[row][col+1].color == self.opponent:
                moves.append(Move(init_row=row, init_col=col, fin_row=row, fin_col=col+1))
        return moves


class Queen(Piece):
    def __init__(self, name, color):
        super().__init__(name, color)

    def valid_moves(self, board: list, row: int, col: int) -> bool:
        moves = []
        moves += self.rank_moves(board=board, row=row, col=col)
        moves += self.file_moves(board=board, row=row, col=col)
        moves += self.left_diagonal(board=board, row=row, col=col)
        moves += self.right_diagonal(board=board, row=row, col=col)

        return moves

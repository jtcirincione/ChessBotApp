# Size of board
from Move import Move
import pygame as p
import copy
WIDTH = HEIGHT = 512
# Dimensions of the board
DIMENSION = ROWS = COLS = 8
SQ_SIZE = HEIGHT // DIMENSION

##FIXME: Extremely messy circular import refactor
def rank_moves( board, row, col, opposing_color):
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

def file_moves( board, row, col, opposing_color):
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

def left_diagonal( board, row, col, opposing_color) -> list:
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

def right_diagonal( board, row, col, opposing_color) -> list:
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

def knight_moves( board, row:int, col:int, opposing_color):
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

def pawn_danger( board, row:int, col:int, opposing_color):
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

# take in a board as a parameter instead of using 
# as we send a board copy simulating a move to check if
# it exposes the king
def king_in_check( king_chk_color, king_row: int, king_col:int, board: list) -> bool:
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
        board= board
    in_check = pawn_danger(board, king_row, king_col, opposing_color) or right_diagonal(board, king_row, king_col, opposing_color) or left_diagonal(board, king_row, king_col, opposing_color) or file_moves(board, king_row, king_col, opposing_color) or rank_moves(board, king_row, king_col, opposing_color) or knight_moves(board, king_row, king_col, opposing_color)
    return in_check


def simulate_drag_v2(board, prev_row, prev_col, move_row, move_col):
        tmp_board = copy.deepcopy(board)
        piece = tmp_board[prev_row][prev_col]
        tmp_board[prev_row][prev_col] = "--"
        tmp_board[move_row][move_col] = piece
        return tmp_board



class Piece:
    def __init__(self, name, color):
        self.color: str = color
        self.name: str = name
        self.opponent: str = "white" if color == "black" else "black"
        self.file = self.set_file()

    def set_file(self) -> str:
        path = f"images/{self.name}.png"
        return path

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
                            moves.append(Move(init_row=row, init_col=col, fin_row=row+1, fin_col=col-1))
                    

            # check diagonal right piece
            if row+1 <= 8 and col+1 < 8:
                if board[row+1][col+1] != "--":
                    if board[row+1][col+1].color == self.opponent:
                        moves.append(Move(init_row=row, init_col=col, fin_row=row+1, fin_col=col+1))
                else:
                    ## En passant logic
                    if isinstance(board[row][col+1], Pawn):
                        if board[row][col+1].can_be_passanted() and board[row][col+1].color == self.opponent:
                            moves.append(Move(init_row=row, init_col=col, fin_row=row+1, fin_col=col+1))
                    
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

    def valid_moves(self, board: list[list[Piece]], row: int, col: int) -> bool:
        moves = []
        moves = self.left_diagonal(board=board, row=row, col=col)
        moves += self.right_diagonal(board=board, row=row, col=col)
        return moves


class Rook(Piece):
    def __init__(self, name, color):
        super().__init__(name, color)
        self.has_moved = False

    def valid_moves(self, board, row, col):
        moves = self.rank_moves(board, row, col)
        moves += self.file_moves(board, row, col)
        return moves
    
    def set_moved(self) -> None:
        self.has_moved = True

    def piece_moved(self) -> bool:
        return self.has_moved


class King(Piece):
    def __init__(self, name, color):
        super().__init__(name, color)
        self.has_moved = False
    
    def set_moved(self) -> None:
        self.has_moved = True

    def piece_moved(self) -> bool:
        return self.has_moved

    def can_see_left_rook(self, board, row, col) -> bool:
        for i in range(col-1, -1, -1):
                ##skip blanks
                if board[row][i] == '--':
                    continue
                ##If rook of my color hasn't moved, we can see it
                if isinstance(board[row][i], Rook):
                    if board[row][i].has_moved == False and board[row][i].color == self.color:
                        return True
                else:
                    return False
        return False

    def can_see_right_rook(self, board, row, col) -> bool:
        for i in range(col+1, 8):
                ##skip blanks
                if board[row][i] == '--':
                    continue
                ##If rook of my color hasn't moved, we can see it
                if isinstance(board[row][i], Rook):
                    if board[row][i].has_moved == False and board[row][i].color == self.color:
                        return True
                else:
                    return False
        return False

    def get_left_rook(self, board) -> Rook:
        pass
    
    def get_right_rook(self, board) -> Rook:
        pass

    def in_check(self, board, king_row, king_col, left):
        if left:
            board1 = simulate_drag_v2(board, king_row, king_col, king_row, king_col - 1)
            board2 = simulate_drag_v2(board, king_row, king_col, king_row, king_col - 2)
            if king_in_check(self.color, king_row, king_col-1, board1) or king_in_check(self.color, king_row, king_col-2, board2):
                return True
        else:
            board1 = simulate_drag_v2(board, king_row, king_col, king_row, king_col + 1)
            board2 = simulate_drag_v2(board, king_row, king_col, king_row, king_col + 2)
            if king_in_check(self.color, king_row, king_col-1, board1) or king_in_check(self.color, king_row, king_col-2, board2):
                return True
        return False
    
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

        ## Castling move check
        if not self.piece_moved():
            if self.can_see_left_rook(board, row, col):
                if not self.in_check(board, row, col, left=True):
                    moves.append(Move(init_row=row, init_col=col, fin_row=row, fin_col=col-2))
            elif self.can_see_right_rook(board, row, col):
                if not self.in_check(board, row, col, left=False):
                    moves.append(Move(init_row=row, init_col=col, fin_row=row, fin_col=col+2))



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

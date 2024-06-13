from Piece import Piece, Rook, Queen, Bishop, Pawn, Knight, King
import copy
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

def file_moves( board: list[list[Piece]], row, col, opposing_color):
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
def king_in_check( king_chk_color: str, board: list) -> bool:
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
    in_check = pawn_danger(board, row, col, opposing_color) or right_diagonal(board, row, col, opposing_color) or left_diagonal(board, row, col, opposing_color) or file_moves(board, row, col, opposing_color) or rank_moves(board, row, col, opposing_color) or knight_moves(board, row, col, opposing_color)
    return in_check


def simulate_drag_v2(board, prev_row, prev_col, move_row, move_col):
        tmp_board = copy.deepcopy(board)
        piece = tmp_board[prev_row][prev_col]
        tmp_board[prev_row][prev_col] = "--"
        tmp_board[move_row][move_col] = piece
        return tmp_board
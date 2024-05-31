# Size of board
WIDTH = HEIGHT = 512
# Dimensions of the board
DIMENSION = ROWS = COLS = 8
SQ_SIZE = HEIGHT // DIMENSION
import pygame as p
class Piece:
    def __init__(self, name, color):
        self.color:str = color
        self.name:str = name
        self.opponent:str = "white" if color == "black" else "black"

class Pawn(Piece):
    def __init__(self, name, color):
        super().__init__(name, color)
        self.has_moved = False
    
    def moved(self) -> None:
        self.has_moved = True
        
    def is_valid(self, board:list, row:int, col:int, moveRow:int, moveCol:int):
        moves = []
        is_blocked = False
        
        if self.has_moved == False:
            if self.color == "white":
                if row - 1 >= 0 and board[row-1][col] == "--": moves.append((row - 1, col))
                if row - 2 >= 0 and board[row-2][col] == "--" and board[row-1][col] == "--": moves.append((row - 2, col))
            ## if black pawn being moved 
            else:
                if row + 1 < 8 and board[row+1][col] == "--": moves.append((row + 1, col))
                if row + 2 < 8 and board[row+2][col] == "--" and board[row+1][col] == "--": moves.append((row + 2, col))
        else:
            if self.color == "white":
                if row - 1 >= 0 and board[row-1][col] == "--": moves.append((row - 1, col))
            else:
                if row + 1 >= 0 and board[row+1][col] == "--": moves.append((row + 1, col))
        
        
        if self.color == "white":
            ##check diagonal left piece
            if row - 1 >= 0 and col-1 >= 0:
                if board[row-1][col-1] != "--":
                    if board[row-1][col-1].color == self.opponent:
                        moves.append((row-1, col-1))
                    
            ##check diagonal right piece
            if row - 1 >= 0 and col+1 < 8:
                if board[row-1][col+1] != "--":
                    if board[row-1][col+1].color == self.opponent:
                        moves.append((row-1, col+1))
        ## if piece is black
        else:
            ##check diagonal left piece
            if row+1 <= 8 and col-1 >= 0:
                if board[row+1][col-1] != "--":
                    print(board[row+1][col-1])
                    if board[row+1][col-1].color == self.opponent:
                        moves.append((row+1, col-1))
                    
            ##check diagonal right piece
            if row+1 <= 8 and col+1 < 8:
                if board[row+1][col+1] != "--":
                    print(board[row+1][col-1])
                    if board[row+1][col+1].color == self.opponent:
                        moves.append((row+1, col+1))
        return (moveRow, moveCol) in moves
        
    
    
class Knight(Piece):
    def __init__(self, name, color):
        super().__init__(name, color)
        
    def validMoves(self, row, col):
        pass
class Bishop(Piece):
    def __init__(self, name, color):
        super().__init__(name, color)
    
    def left_diagonal(self, board, row, col) -> list:
        moves = []
        ## Top left diagonal
        for i in range(row-1, -1, -1):
            for j in range(col-1, -1, -1):
                if board[i][j] == "--":
                    moves.append((i, j))
                elif board[i][j].color == self.opponent:
                    moves.append((i, j))
                    break
                else:
                    break
            
        ## Bottom part of diagonal
        for i in range(row+1, 8,):
            for j in range(col+1, 8):
                if board[i][j] == "--":
                    moves.append((i, j))
                elif board[i][j].color == self.opponent:
                    moves.append((i, j))
                    break
                else:
                    break
        return moves
    
    def right_diagonal(self, board, row, col) -> list:
        moves = []
        ## Top right diagonal
        for i in range(row-1, -1, -1):
            for j in range(col+1, 8):
                if board[i][j] == "--":
                    moves.append((i, j))
                elif board[i][j].color == self.opponent:
                    moves.append((i, j))
                    break
                else:
                    break
            
        ## Bottom part of diagonal
        for i in range(row+1, 8,):
            for j in range(col-1, -1, -1):
                if board[i][j] == "--":
                    moves.append((i, j))
                elif board[i][j].color == self.opponent:
                    moves.append((i, j))
                    break
                else:
                    break
        return moves
    
    def is_valid(self, board:list, row:int, col:int, moveRow:int, moveCol:int, surface) -> bool:
        moves = []
        moves = self.left_diagonal(board=board, row=row, col=col)
        moves += self.right_diagonal(board=board, row=row, col=col)
        print(moves)
        for row, col in moves:
            rect = (col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            color = (255, 0, 0)
            p.draw.rect(surface, color, rect)
        return (moveRow, moveCol) in moves
class Rook(Piece):
    def __init__(self, name, color):
        super().__init__(name, color)
        
    def is_valid(self, board, row, col, moveRow, moveCol):
        moves = self.rank_moves(board, row, col)
        moves += self.file_moves(board, row, col)
        return (moveRow, moveCol) in moves
    
    def rank_moves(self, board, row, col):
        moves = []
        ## look at each move to the left of piece
        for i in range(col - 1, -1, -1):
            if board[row][i] == "--":
                moves.append((row, i))
            elif board[row][i].color == self.opponent:
                moves.append((row, i))
                break
            else:
                break
        ## look at each move to the right of piece
        for i in range(col + 1, 8):
            if board[row][i] == "--":
                moves.append((row, i))
            elif board[row][i].color == self.opponent:
                moves.append((row, i))
                break
            else:
                break
        return moves
    
    def file_moves(self, board, row, col):
        moves = []
        ## look at each move above a piece
        for i in range(row - 1, -1, -1):
            if board[i][col] == "--":
                moves.append((i, col))
            elif board[i][col].color == self.opponent:
                moves.append((i, col))
                break
            else:
                break
        ## look at each move to below a piece
        for i in range(row+1, 8):
            if board[i][col] == "--":
                moves.append((i, col))
            elif board[i][col].color == self.opponent:
                moves.append((i, col))
                break
            else:
                break
        return moves
    
class King(Piece):
    def __init__(self, name, color):
        super().__init__(name, color)
        
    def is_valid(self, board, row, col, moveRow, moveCol):
        moves = []
        ## look at rank above piece
        if row-1 >= 0:
            for j in range(col-1, col + 2):
                if j > 7:
                    break
                if j >= 0:
                    if board[row-1][j] == '--' or board[row-1][j].color == self.opponent:
                        moves.append((row-1, j))
        ## look at rank above piece
        if row+1 < 8:
            for j in range(col-1, col + 2):
                if j > 7:
                    break
                if j >= 0:
                    if board[row+1][j] == '--' or board[row+1][j].color == self.opponent:
                        moves.append((row+1, j))
        
        ## look at pieces to right/left
        if col-1 >= 0:
            if board[row][col-1] == '--' or board[row][col-1].color == self.opponent:
                moves.append((row, col-1))
        if col+1 < 8:
            if board[row][col+1] == '--' or board[row][col+1].color == self.opponent:
                moves.append((row, col+1))
        return (moveRow, moveCol) in moves
class Queen(Piece):
    def __init__(self, name, color):
        super().__init__(name, color)
        
    def validMoves(self, row, col):
        pass

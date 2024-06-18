from Piece import Piece, Pawn, Rook, Knight, King, Queen, Bishop
from ChessEngine import GameState
from bitboards.BitBoard import BitBoard
import copy
import pygame
WIDTH = HEIGHT = 512
# Dimensions of the board
DIMENSION = ROWS = COLS = 8
SQ_SIZE = HEIGHT // DIMENSION

class Dragger:
    def __init__(self):
        self.prevRow = self.prevCol = self.postRow = self.postCol = 0
        self.oldIdx = 0
        self.piece: Piece = None
        self.is_dragging = False
        self.mouseX = -100
        self.mouseY = -100

    def update_pos(self, board: list, x: int, y: int, game: GameState) -> None:
        if board[x][y] == '--':
            return
        if board[x][y].color == 'black' and game.white_to_move() == True or board[x][y].color == 'white' and game.white_to_move() == False:
            return
        self.piece = board[x][y]
        self.prevRow = x
        self.prevCol = y
        self.oldIdx = self.prevRow * 8 + self.prevCol
        self.is_dragging = True

    def update_mouse(self, pos) -> None:
        self.mouseX, self.mouseY = pos

    def update_blit(self, surface) -> None:
        piece = self.get_piece()
        img = pygame.image.load(piece.file)
        img_center = (self.mouseX, self.mouseY)
        surface.blit(img, img.get_rect(center=img_center))

    def illuminate_moves(self, surface, board) -> None:
        moves = self.piece.valid_moves(board, self.prevRow, self.prevCol)

        for move in moves:
            row, col = move.get_final()
            rect = (col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            color = (255,255,102)
            pygame.draw.rect(surface=surface, color=color, rect=rect)

    def illuminate_all_moves(self, surface, board, color):
        moves = []
        for i in range(8):
            for j in range(8):
                if board[i][j] != "--":
                    if board[i][j].color == color:
                        moves.extend(board[i][j].valid_moves(board, i, j))
        print(f"I, {color}, have {len(moves)} valid moves.")
        for move in moves:
            row, col = move.get_final()
            rect = (col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            color = (255,255,102)
            pygame.draw.rect(surface=surface, color=color, rect=rect)


    def drag2(self, bitboard: BitBoard, newIdx):
        bitboard.move_piece(self.oldIdx, newIdx)

    def drag(self, board: list[list[Piece]], x: int, y: int) -> list:
        print("I AM MOVING ONCE")
        self.postRow = x
        self.postCol = y
        self.is_dragging = False
        # if pawn, set moved to true
        if isinstance(self.piece, Pawn):
            self.piece.moved()
            # TODO: Refactor elsewhere
            # If pawn moved 2 spots, set en passant to true
            if abs(self.postRow - self.prevRow) == 2:
                self.piece.set_passant_active()
            else:
                self.piece.set_passant_inactive()
            # TODO: Now check if we are moving diagonally to an empty square.
            # if we are, remove the piece ether behind or in front of the move location
            # depending on current piece's color
            if board[self.postRow][self.postCol] == "--" and abs(self.postRow - self.prevRow) == 1 and abs(self.postCol - self.prevCol) == 1:
                print('EN PASSANTED2')
                if self.piece.color == "white":
                    board[self.postRow + 1][self.postCol] = "--"
                else:
                    board[self.postRow - 1][self.postCol] = "--"
        ## CASTLING LOGIC
        if isinstance(self.piece, King):
            print(";LKDSAFJ;SALKFJSA;LKFJSALKFJSDLKFAJSF;LSAKDJF")
            self.piece.has_moved = True
            if abs(self.postCol - self.prevCol == 2):
                ## if castling left
                if self.prevCol - self.postCol > 0:
                    ## move rook one space to the right of moved king
                    rook = board[self.postRow][0]
                    board[self.postRow][0] = "--"
                    board[self.postRow][self.postCol+1] = rook
                    rook.has_moved = True
                ## castling right
                else:
                    ## move rook one space to the left of moved king
                    rook = board[self.postRow][7]
                    board[self.postRow][7] = "--"
                    board[self.postRow][self.postCol-1] = rook
                    rook.has_moved = True
        board[self.prevRow][self.prevCol] = "--"
        board[self.postRow][self.postCol] = self.piece
        return board

    
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
        self.prevRow = self.prevCol = self.postRow = self.postCol = 0
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

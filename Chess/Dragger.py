from Piece import Piece, Pawn, Rook, Knight, King, Queen, Bishop
from ChessEngine import GameState
import copy


class Dragger:
    def __init__(self):
        self.prevRow = self.prevCol = self.postRow = self.postCol = 0
        self.piece = None
        self.is_dragging = False

    def update_pos(self, board: list, x: int, y: int, game: GameState) -> None:
        if board[x][y] == '--':
            return
        if board[x][y].color == 'black' and game.white_to_move() == True or board[x][y].color == 'white' and game.white_to_move() == False:
            return
        self.piece = board[x][y]
        self.prevRow = x
        self.prevCol = y
        self.is_dragging = True

    def drag(self, board: list, x: int, y: int) -> list:
        self.postRow = x
        self.postCol = y
        self.is_dragging = False
        # if pawn, set moved to true
        if isinstance(self.piece, Pawn):
            self.piece.moved()
            ##TODO: Refactor elsewhere
            # If pawn moved 2 spots, set en passant to true
            if abs(self.postRow - self.prevRow) == 2:
                self.piece.set_passant_active()
            else:
                self.piece.set_passant_inactive()
            ##TODO: Now check if we are moving diagonally to an empty square.
            ## if we are, remove the piece ether behind or in front of the move location
            ## depending on current piece's color
            if board[self.postRow][self.postCol] == "--" and abs(self.postRow - self.prevRow) == 1 and abs(self.postCol - self.prevCol) == 1:
                print('EN PASSANTED')
                if self.piece.color == "white":
                    board[self.postRow + 1][self.postCol] = "--"
                else:
                    board[self.postRow - 1][self.postCol] = "--"


        board[self.prevRow][self.prevCol] = "--"
        board[self.postRow][self.postCol] = self.piece
        return board

    def simulate_drag(self, board: list, x: int, y: int) -> list:
        tmp_board = copy.deepcopy(board)
        tmp_board[self.prevRow][self.prevCol] = "--"
        tmp_board[x][y] = self.piece
        return tmp_board
    
    def simulate_drag_v2(self, board, prev_row, prev_col, move_row, move_col):
        tmp_board = copy.deepcopy(board)
        piece = tmp_board[prev_row][prev_col]
        tmp_board[prev_row][prev_col] = "--"
        tmp_board[move_row][move_col] = piece
        return tmp_board
        
    def undrag(self):
        self.is_dragging = False
        self.prevRow = self.prevCol = self.postRow = self.postCol = 0
        self.piece = None

    def get_piece(self) -> Piece:
        return self.piece

    def get_moves(self) -> list:
        return None

    def get_moved_location(self) -> tuple:
        return (self.postRow, self.postCol)

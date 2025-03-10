from bitboards.BitBoard import BitBoard
from chessboard import Chessboard
import pygame, numpy as np
from move import Move
WIDTH = HEIGHT = 512
# Dimensions of the board
DIMENSION = ROWS = COLS = 8
SQ_SIZE = HEIGHT // DIMENSION

class GameState:

    def __init__(self, surface):
        self.board = Chessboard()
        self.surface = surface
        self.move_history: list[Move] = []


    """
    Returns square index from 0-63.
     0 bottom-left, 63 top-right
    """
    def coord_to_idx(self, posX: int, posY: int) -> tuple:
        x = posX // SQ_SIZE
        y = posY // SQ_SIZE
        # print(posX, posY)
        return (7 - y) * 8 + x

    def load(self, images: dict) -> None:
        for i in range(64):
            for key, board in self.board.get_piece_boards().items():
                if board.get_bit(i):
                    self.surface.blit(images[key], ((i % 8) * SQ_SIZE, (7 - (i // 8)) * SQ_SIZE))
                    # print(board.name)
                    # board.print()
                    # print()
                    break
    
    def show_bg(self):
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = (234, 235, 200)
                else:
                    color = (119, 154, 88)
                rect = (col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                pygame.draw.rect(self.surface, color, rect)

    def show_valid_moves(self, white_turn):
        if white_turn:
            pass
        else:
            pass
    
    def get_proper_board(self, idx) -> BitBoard:
        for key, board in self.board.get_piece_boards().items():
            if board.get_bit(idx) == 1:
                return board          
        return None
    
    def get_pseudolegal_moves(self, white_turn) -> list[Move]:
        moves = []
        moves.extend(self.board.get_bishop_moves(white_turn))
        moves.extend(self.board.get_rook_moves(white_turn))
        moves.extend(self.board.get_queen_moves(white_turn))
        moves.extend(self.board.get_pawn_moves(white_turn))
        moves.extend(self.board.get_knight_moves(white_turn))
        moves.extend(self.board.get_king_moves(white_turn))

        return moves

    def last_move_valid(self, white_moved_last) -> bool:
        prev_move = self.move_history[-1]
        
        # 1. is my king in check
        if white_moved_last:
            pass
        else:
            pass

        # 2. check if move is a castle
        pass

    def get_valid_moves(self, white_turn) -> list[Move]:
        """
        generates pseudolegal moves and tries each move to check validity
        """
        pseudo_moves: list[Move] = self.get_pseudolegal_moves(white_turn)
        legal_moves = []
        for move in pseudo_moves:
            from_idx = move.get_from_idx()
            to_idx = move.get_to_idx()
            bboard_to_move = self.get_proper_board(from_idx)
            self.move(piece=bboard_to_move, start=from_idx, end=to_idx)
            if self.last_move_valid(white_turn) == True:
                legal_moves.append(move)
            self.move(piece=bboard_to_move, start=from_idx, end=to_idx, undo=True)

        return legal_moves

    """
    Moves piece. returns true on success.
    """
    def move(self, piece, start, end, undo=False) -> bool:
        board_to_set: BitBoard = piece
        board_to_clear = self.get_proper_board(end)
        if not board_to_set or start == end: return False
        color = "white" if board_to_set.color == "white" else "black"
        if board_to_clear and (board_to_clear.color == color): return False
        
        if not undo:
            move_type = Move.get_move_type(board_to_set, board_to_clear, start, end)
            move = Move(start, end, move_type)
            white_turn = True if color == "white" else False
            board_to_set.move_piece(start, end)
            if board_to_clear:
                board_to_clear.clear_bit(end)
            self.move_history.append(move)
        else:
            board_to_set.move_piece(end, start)
            if board_to_clear:
                board_to_clear.set_bit(end)
            self.move_history.pop()
        return True
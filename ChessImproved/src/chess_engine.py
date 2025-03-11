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

    def last_move_valid(self, moved_piece, white_moved_last) -> bool:
        prev_move = self.move_history[-1]
        occupancy = self.board.get_occupancy_board()
        
        # 1. is my king in check
        all_attacks = self.board.get_all_attack_squares(occupancy, white_moved_last)
        king_bboard = self.board.bitboards["wK" if white_moved_last else "bK"].board
        if king_bboard & all_attacks > 0: return False # if king is on an attacked square move is invalid

        # 2. check if move is a castle
        castle_idx = 4 if white_moved_last else 60
        if prev_move.get_move_type() == Move.KING_CASTLE:
            RIGHT_ROOK = 7 if white_moved_last else 63
            # to do this we need to: 1. check if the 2 squares to the right of the king are occupied
            if self.board.get_queen_attacks(castle_idx, occupancy, not white_moved_last) & np.uint64(1 << RIGHT_ROOK) <= 0:
                return False # FALSE bc we can't see our right rook ( we treat our king as the enemy here so our rook isn't masked out)
            # 2. check if the 2 squares right of the king are under attack
            if (all_attacks & np.uint64(1 << castle_idx + 1) > 0) or (all_attacks & np.uint64(1 << castle_idx + 2)) > 0:
                return False # False as one of or both of these squares are under attack
            # 3. check if the king/right rook have been moved by searching through the move history
            for move in self.move_history:
                if move.get_from_idx() == castle_idx or move.get_from_idx() == RIGHT_ROOK:
                    return False

        if prev_move.get_move_type == Move.QUEEN_CASTLE:
            LEFT_ROOK = 0 if white_moved_last else 56
            # to do this we need to: 1. check if the 3 squares to the left of the king are occupied
            if self.board.get_queen_attacks(castle_idx, occupancy, not white_moved_last) & np.uint64(1 << LEFT_ROOK) <= 0:
                return False # FALSE bc we can't see our right rook ( we treat our king as the enemy here so our rook isn't masked out)
            # 2. ckeck if the 2 squares left of the king are under attack
            if (all_attacks & np.uint64(1 << castle_idx - 1) > 0) or (all_attacks & np.uint64(1 << castle_idx - 2)) > 0:
                return False # False as one of or both of these squares are under attack
            # 3. check if the king/left rook have been moved by searching through the move history
            for move in self.move_history:
                if move.get_from_idx() == castle_idx or move.get_from_idx() == LEFT_ROOK:
                    return False

        return True

    def get_valid_moves(self, white_turn) -> list[Move]:
        """
        generates pseudolegal moves and tries each move to check validity
        """
        pseudo_moves: list[Move] = self.get_pseudolegal_moves(white_turn)
        legal_moves = []
        for move in pseudo_moves:
            bboard_to_move = self.get_proper_board(move.get_from_idx())
            self.move(piece=bboard_to_move, move=move)
            if self.last_move_valid(bboard_to_move, white_turn) == True:
                legal_moves.append(move)
            self.move(piece=bboard_to_move, move=move, undo=True)

        return legal_moves

    """
    Moves piece. returns true on success.
    """
    def move(self, piece, move:Move, undo=False) -> bool:
        board_to_set: BitBoard = piece
        start = move.get_from_idx()
        end = move.get_to_idx()

        board_to_clear = self.get_proper_board(end)
        if not board_to_set or start == end: return False
        color = "white" if board_to_set.color == "white" else "black"
        if board_to_clear and (board_to_clear.color == color): return False
        
        if not undo:
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
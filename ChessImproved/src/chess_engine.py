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
        self.white_turn = True


    """
    Returns square index from 0-63.
     0 bottom-left, 63 top-right
    """
    def coord_to_idx(self, posX: int, posY: int) -> tuple:
        x = posX // SQ_SIZE
        y = posY // SQ_SIZE
        return (7 - y) * 8 + x
    
    def idx_to_coord(self, idx: int) -> tuple:
        x = idx % 8
        y = 7 - (idx // 8)
        posX = x
        posY = y
        return posX, posY

    def load(self, images: dict) -> None:
        for i in range(64):
            for key, board in self.board.get_piece_boards().items():
                if board.get_bit(i):
                    self.surface.blit(images[key], ((i % 8) * SQ_SIZE, (7 - (i // 8)) * SQ_SIZE))
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

    def show_valid_moves(self, from_idx, moves:list[Move]) -> None:
        for move in moves:
            if move.get_from_idx() == from_idx:
                idx = move.get_to_idx()
                rect = ((idx % 8) * SQ_SIZE, (7 - (idx // 8)) * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                color = (255,255,102)
                pygame.draw.rect(surface=self.surface, color=color, rect=rect)

    def show_promotion_options(self, color, IMAGES):
        """ Draws promotion choices centered above the board with proper spacing. """
        options = ["Q", "R", "B", "N"]
        option_size = 60  # Slightly larger squares for better visibility
        total_width = len(options) * option_size
        x_offset = (WIDTH - total_width) // 2  # Centering the options
        y_offset = 20 if color == "w" else HEIGHT - 80  # Offset from the top or bottom

        for i, piece in enumerate(options):
            rect = (x_offset + i * option_size, y_offset, option_size, option_size)
            pygame.draw.rect(self.surface, (200, 200, 200), rect, border_radius=5)  # Light gray with rounded corners
            self.surface.blit(IMAGES[f"{color}{piece}"], (x_offset + i * option_size + 5, y_offset + 5))  # Slight padding

    def get_promotion_choice(self, x, y, color):
        """ Detects which piece was selected for promotion based on the Y-coordinate. """
        # Adjusting the size based on scaling and positioning
        option_size = 60  # Same as in show_promotion_options
        total_width = 4 * option_size
        x_offset = (WIDTH - total_width) // 2  # Centering the options

        # Calculating the range for each piece based on the scaled size
        if x > x_offset and x < x_offset + option_size:
            return Move.QUEEN_PROMO
        elif x > x_offset + option_size and x < x_offset + 2 * option_size:
            return Move.ROOK_PROMO
        elif x > x_offset + 2 * option_size and x < x_offset + 3 * option_size:
            return Move.BISHOP_PROMO
        elif x > x_offset + 3 * option_size and x < x_offset + 4 * option_size:
            return Move.KNIGHT_PROMO

        return None  # Default if no valid area is clicked
        

    def replace_pawn(self, square, piece):
        """ Replaces the promoted pawn with the chosen piece. """
        color = "w" if square >= 56 else "b"
        if piece == Move.QUEEN_PROMO:
            piece = "Q"
        if piece == Move.ROOK_PROMO:
            piece = "R"
        if piece == Move.KNIGHT_PROMO:
            piece = "N"
        if piece == Move.BISHOP_PROMO:
            piece = "B"
        self.board.bitboards[f"{color}p"].clear_bit(square)
        self.board.bitboards[f"{color}{piece}"].set_bit(square)

    def current_turn(self):
        return "white" if self.white_turn else "black"

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
    
    def king_in_check(self, white_king):
        all_attacks = self.board.get_all_attack_squares(self.board.get_occupancy_board(), not white_king) # get enemy attacks
        king_bboard = self.board.bitboards["wK" if white_king else "bK"].board

        if king_bboard & all_attacks > 0: return True

    def last_move_valid(self, moved_piece, cleared_piece, white_moved_last) -> bool:
        prev_move = self.move_history[-1]
        occupancy = self.board.get_occupancy_board()

        # 1. is my king in check
        all_attacks = self.board.get_all_attack_squares(occupancy, not white_moved_last) # get enemy attacks
        king_bboard = self.board.bitboards["wK" if white_moved_last else "bK"].board

        if king_bboard & all_attacks > 0: return False
        

        if prev_move.get_flags() == Move.EP_CAPTURE:
            move_before_last = self.move_history[-2]
            if move_before_last.get_flags() != Move.DOUBLE_PAWN_PUSH:
                return False
            if abs(int(move_before_last.get_from_idx()) - int(prev_move.get_to_idx())) != 8:
                return False

        # 2. check if move is a castle
        castle_idx = 4 if white_moved_last else 60
        if prev_move.get_flags() == Move.KING_CASTLE:
            RIGHT_ROOK = 7 if white_moved_last else 63
            # 2. check if the 2 squares right of the king are under attack
            if (all_attacks & np.uint64(1 << castle_idx + 1) > 0) or (all_attacks & np.uint64(1 << castle_idx + 2)) > 0:
                return False # False as one of or both of these squares are under attack
            # 3. check if the king/right rook have been moved by searching through the move history
            for move in self.move_history:
                if move is not prev_move and (move.get_from_idx() == castle_idx or move.get_from_idx() == RIGHT_ROOK):
                    return False

        if prev_move.get_flags() == Move.QUEEN_CASTLE:
            LEFT_ROOK = 0 if white_moved_last else 56
            # 2. ckeck if the 2 squares left of the king are under attack
            if (all_attacks & np.uint64(1 << castle_idx - 1) > 0) or (all_attacks & np.uint64(1 << castle_idx - 2)) > 0:
                return False # False as one of or both of these squares are under attack
            # 3. check if the king/left rook have been moved by searching through the move history
            for move in self.move_history:
                if move is not prev_move and (move.get_from_idx() == castle_idx or move.get_from_idx() == LEFT_ROOK):
                    return False
        return True

    def get_valid_moves_by_color(self, white_turn):
        """
        generates pseudolegal moves and tries each move to check validity
        """
        pseudo_moves: list[Move] = self.get_pseudolegal_moves(white_turn)
        legal_moves = []
        for move in pseudo_moves:
            bboard_to_move = self.get_proper_board(move.get_from_idx())
            bboard_to_clear = self.get_proper_board(move.get_to_idx())
            self.move(board_to_move=bboard_to_move, board_to_clear=bboard_to_clear, move=move)
            if self.last_move_valid(bboard_to_move, bboard_to_clear, white_turn) == True:
                legal_moves.append(move)
            self.move(board_to_move=bboard_to_move, board_to_clear=bboard_to_clear, move=move, undo=True)

        return legal_moves

    def get_valid_moves(self) -> list[Move]:
        """
        generates pseudolegal moves and tries each move to check validity
        """
        pseudo_moves: list[Move] = self.get_pseudolegal_moves(self.white_turn)
        legal_moves = []
        for move in pseudo_moves:
            bboard_to_move = self.get_proper_board(move.get_from_idx())
            bboard_to_clear = self.get_proper_board(move.get_to_idx())
            self.move(board_to_move=bboard_to_move, board_to_clear=bboard_to_clear, move=move)
            if self.last_move_valid(bboard_to_move, bboard_to_clear, not self.white_turn) == True:
                legal_moves.append(move)
            self.move(board_to_move=bboard_to_move, board_to_clear=bboard_to_clear, move=move, undo=True)

        # print(f"there are {len(legal_moves)} for current board configuration")
        return legal_moves

    """
    Moves piece. returns true on success.
    """
    def move(self, board_to_move, board_to_clear, move:Move, undo=False) -> bool:
        board_to_set: BitBoard = board_to_move
        start = move.get_from_idx()
        end = move.get_to_idx()

        # if not board_to_set or start == end: return False
        color = "white" if board_to_set.color == "white" else "black"
        # if board_to_clear and (board_to_clear.color == color): return False
        white_turn = True if color == "white" else False
        if not undo:
            board_to_set.move_piece(start, end)
            if board_to_clear:
                board_to_clear.clear_bit(end)
            self.move_history.append(move)
            if move.get_flags() == Move.KING_CASTLE:
                self.board.bitboards["wR" if white_turn else "bR"].move_piece(7 if white_turn else 63, 5 if white_turn else 61)
            elif move.get_flags() == Move.QUEEN_CASTLE:
                self.board.bitboards["wR" if white_turn else "bR"].move_piece(0 if white_turn else 56, 3 if white_turn else 59)
            elif move.get_flags() == Move.EP_CAPTURE:
                self.board.bitboards["bp"].clear_bit(end - 8) if white_turn else self.board.bitboards["wp"].clear_bit(end + 8)

        else:
            board_to_set.move_piece(end, start)
            if board_to_clear:
                board_to_clear.set_bit(end)
            if move.get_flags() == Move.KING_CASTLE:
                self.board.bitboards["wR" if white_turn else "bR"].move_piece(5 if white_turn else 61, 7 if white_turn else 63)
            elif move.get_flags() == Move.QUEEN_CASTLE:
                pass
            elif move.get_flags() == Move.EP_CAPTURE:
                self.board.bitboards["bp"].set_bit(move.get_to_idx() - 8) if white_turn else self.board.bitboards["wp"].set_bit(move.get_to_idx() + 8)

            self.move_history.pop()
        self.white_turn = not self.white_turn
        return True
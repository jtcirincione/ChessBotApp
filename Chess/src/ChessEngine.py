"""
Responsible for storing all info about the current state of a chess game and validates moves. Keeps a move log.
"""
import numpy as np
from Piece import Piece, Pawn, Rook, Knight, King, Queen, Bishop
from Move import Move
from Move2 import Move2
from enums.MoveType import MoveType
import pygame, utils.check as check
from bitboards.BitBoard import BitBoard
from bitboards.BishopBoard import BishopBoard
from bitboards.KingBoard import KingBoard
from bitboards.KnightBoard import KnightBoard
from bitboards.PawnBoard import PawnBoard
from bitboards.RookBoard import RookBoard
from bitboards.QueenBoard import QueenBoard
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

        # self.white_pawn_board = PawnBoard("white")
        # self.white_rook_board = RookBoard("white")
        # self.white_queen_board = QueenBoard("white")
        # self.white_bishop_board = BishopBoard("white")
        # self.white_knight_board = KnightBoard("white")
        # self.white_king_board = KingBoard("white")
        
        # self.black_pawn_board = PawnBoard("black")
        # self.black_rook_board = RookBoard("black")
        # self.black_queen_board = QueenBoard("black")
        # self.black_bishop_board = BishopBoard("black")
        # self.black_knight_board = KnightBoard("black")
        # self.black_king_board = KingBoard("black")

        self.boards: dict[str, BitBoard]= {
            "wp": PawnBoard("white"),
            "wR": RookBoard("white"),
            "wQ": QueenBoard("white"),
            "wB": BishopBoard("white"),
            "wN": KnightBoard("white"),
            "wK": KingBoard("white"),
            
            "bp": PawnBoard("black"),
            "bR": RookBoard("black"),
            "bQ": QueenBoard("black"),
            "bB": BishopBoard("black"),
            "bN": KnightBoard("black"),
            "bK": KingBoard("black"),
        }
        
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
        self.history: list[Move2] = []

    def coord_to_idx(self, posX: int, posY: int) -> tuple:
        x = posX // SQ_SIZE
        y = posY // SQ_SIZE
        # print(posX, posY)
        return (x, y)
    
    def get_w_board(self):
        w_board = self.boards["wp"].board | self.boards["wR"].board | self.boards["wB"].board | self.boards["wN"].board | self.boards["wK"].board | self.boards["wQ"].board
        return w_board
    
    def get_b_board(self):
        b_board = self.boards["bp"].board | self.boards["bR"].board | self.boards["bB"].board | self.boards["bN"].board | self.boards["bK"].board | self.boards["bQ"].board
        return b_board
    

    def get_b_bitboard_object(self) -> list[BitBoard]:
        bboards = []
        bboards.append(self.boards["bp"])
        bboards.append(self.boards["bR"])
        bboards.append(self.boards["bN"])
        bboards.append(self.boards["bB"])
        bboards.append(self.boards["bQ"])
        bboards.append(self.boards["bK"])
        return bboards

    def get_w_bitboard_object(self) -> list[BitBoard]:
        bboards = []
        bboards.append(self.boards["wp"])
        bboards.append(self.boards["wR"])
        bboards.append(self.boards["wN"])
        bboards.append(self.boards["wB"])
        bboards.append(self.boards["wQ"])
        bboards.append(self.boards["wK"])
        return bboards


    def get_b_attack_squares(self) -> np.uint64:
        b_attacks = self.boards["bp"].valid_moves(self.get_b_board(), self.get_w_board(), self.history) | self.boards["bR"].valid_moves(self.get_b_board(), self.get_w_board(), self.history) | self.boards["bB"].valid_moves(self.get_b_board(), self.get_w_board(), self.history) | self.boards["bN"].valid_moves(self.get_b_board(), self.get_w_board(), self.history) | self.boards["bK"].valid_moves(self.get_b_board(), self.get_w_board(), self.history) | self.boards["bQ"].valid_moves(self.get_b_board(), self.get_w_board(), self.history)
        return b_attacks
    
    def get_w_attack_squares(self) -> np.uint64:
        w_attacks = self.boards["wp"].valid_moves(self.get_w_board(), self.get_b_board(), self.history) | self.boards["wR"].valid_moves(self.get_w_board(), self.get_b_board(), self.history) | self.boards["wB"].valid_moves(self.get_w_board(), self.get_b_board(), self.history) | self.boards["wN"].valid_moves(self.get_w_board(), self.get_b_board(), self.history) | self.boards["wK"].valid_moves(self.get_w_board(), self.get_b_board(), self.history) | self.boards["wQ"].valid_moves(self.get_w_board(), self.get_b_board(), self.history)
        return w_attacks
    
    def get_opponent_board(self):
        return self.get_b_board() if self.current_turn() == "white" else self.get_w_board()

    def get_current_player_board(self):
        return self.get_w_board() if self.current_turn() == "white" else self.get_b_board()

    def show_bg(self):
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = (234, 235, 200)
                else:
                    color = (119, 154, 88)
                rect = (col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                pygame.draw.rect(self.surface, color, rect)

    
    ## returns the bitboard type of piece at given index: idx
    def get_pieces_board(self, idx):
        for board in self.boards.values():
            if board.get_bit(idx) == 1:
                return board
        return None

    def load(self, images: dict) -> None:
        # for rank in range(8):
        #     for file in range(8):
        #         square = rank * 8 + file
        #         for key, board in self.boards.items():
        #             if board.get_bit(square) == 1:
        #                 self.surface.blit(images[key], (file * SQ_SIZE, rank * SQ_SIZE))
        for i in range(64):
            for key, board in self.boards.items():
                if board.get_bit(i):
                    self.surface.blit(images[key], ((i%8) * SQ_SIZE, (i//8) * SQ_SIZE))
                    break
    
    def get_proper_board(self, idx):
        for board in self.boards.values():
            if board.get_bit(idx) == 1:
                return board
            
        return np.uint64(0)

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


    # out of all of the valid moves, check if idx is on a set bit
    def is_valid_move(self, old_idx: int, new_idx: int) -> bool:
        for board in self.boards.values():
           if board.get_bit(old_idx) == 1:
               ## then we are looking at proper board
               return BitBoard.get_bit_on_board(new_idx, board.attacking_squares(old_idx, np.uint64(0), np.uint64(0)))
        return False
            
    ## FIXME: currently invalid castling isn't prevented. the king can move thru attacked squares
    def check_valid_castle(self, move: Move2, new_idx):
        move_type = move.get_move_type()
        old_idx = move.get_initial_idx()
        if self.current_turn() == "white":
            valid_castle = False
            if move_type == MoveType.CASTLE_LEFT:
                if not self.boards["wR"].left_rook_moved and self.boards["wR"].get_bit(56):
                    print('HI1')
                    valid_castle = True
            if move_type == MoveType.CASTLE_RIGHT:
                if not self.boards["wR"].right_rook_moved and self.boards["wR"].get_bit(63):
                    print('HI2')
                    valid_castle = True
        else:
            valid_castle = False
            if move_type == MoveType.CASTLE_LEFT:
                if not self.boards["bR"].left_rook_moved  and self.boards["bR"].get_bit(0):
                    ## TODO: SINCE ROOK HASN'T MOVED, MOVE THE ROOK DURING CASTLE one space to right of king
                    valid_castle = True
            if move_type == MoveType.CASTLE_RIGHT:
                if not self.boards["bR"].right_rook_moved  and self.boards["bR"].get_bit(7):
                    ## TODO: SINCE ROOK HASN'T MOVED, MOVE THE ROOK DURING CASTLE one space to left of king
                    valid_castle = True
        if not valid_castle:
            print("UNDO INVALID CASTLE")
            # self.get_proper_board(old_idx).moved = False
            return False
        return True


    def draw_promotions(self, piece: BitBoard, images: dict) -> None:
        if not isinstance(piece, PawnBoard):
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
    def promote(self, move_idx: int, men_row: int, men_col: int, color: str) -> bool:
        print(f"indices: ({men_row}, {men_col})")
        for key, val in self.promotions.items():
            if (men_row, men_col) in val:
                print(f"Selected item: {key}, {val}")
                if color == "black":
                    self.boards["bp"].clear_bit(move_idx)
                else:
                    self.boards["wp"].clear_bit(move_idx)
                if key == "Queen":
                    if color == "black":
                        self.boards["bQ"].set_bit(move_idx)
                    else:
                        self.boards["wQ"].set_bit(move_idx)
                elif key == "Knight":
                    if color == "black":
                        self.boards["bN"].set_bit(move_idx)
                    else:
                        self.boards["wN"].set_bit(move_idx)
                elif key == "Bishop":
                    if color == "black":
                        self.boards["bB"].set_bit(move_idx)
                    else:
                        self.boards["wB"].set_bit(move_idx)
                elif key == "Rook":
                    if color == "black":
                        self.boards["bR"].set_bit(move_idx)
                    else:
                        self.boards["wR"].set_bit(move_idx)

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
        

    # take in a board as a parameter instead of using self,
    # as we send a board copy simulating a move to check if
    # it exposes the king
    # def king_in_check(self, king_chk_color: str, board: list) -> bool:
    #     in_check = check.king_in_check(king_chk_color, board)
    #     if in_check:
    #         self.set_king_checked(king_chk_color)
    #     return in_check
    
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
    
    def in_checkmate(self, color):
        pseudos = []
        legals = []
        if color == "white":
            white_pieces = self.get_w_board()
            for i in range(64):
                if BitBoard.get_bit_on_board(i, white_pieces):
                    bboard = self.get_proper_board(i)
                    _, moves = bboard.attacking_squares(i, white_pieces, self.get_b_board(), self.history)
                    pseudos.extend(moves)
            if pseudos is not None:
                legals = self.get_legal_moves(pseudos, "white")
        else:
            black_pieces = self.get_b_board()
            for i in range(64):
                if BitBoard.get_bit_on_board(i, black_pieces):
                    bboard = self.get_proper_board(i)
                    _, moves = bboard.attacking_squares(i, black_pieces, self.get_w_board(), self.history)
                    pseudos.extend(moves)
            if pseudos is not None:
                legals = self.get_legal_moves(pseudos, "black")

        if len(legals) == 0: 
            print("mated")
            return True
        return False
    
    def undo_move(self, bitboard: BitBoard, move: Move2, board_to_set: BitBoard=np.uint64(0)):
        bitboard.set_bit(move.get_initial_idx())
        bitboard.clear_bit(move.get_final_idx())
        if board_to_set:
            board_to_set.set_bit(move.get_final_idx())
            if isinstance(board_to_set, KingBoard):
                board_to_set.moved = False


    def move(self, bitboard: BitBoard, move: Move2, board_to_clear: BitBoard=np.uint64(0)):
        ## dont use move_piece() to prevent setting king to moved in simulation
        bitboard.clear_bit(move.get_initial_idx())
        bitboard.set_bit(move.get_final_idx())
        if board_to_clear:
            board_to_clear.clear_bit(move.get_final_idx())


    def king_in_check(self, enemies, color) -> bool:
        in_check = np.uint64(0)
        if color == "white":
            in_check = enemies & self.boards["wK"].board
        else:
            in_check = enemies & self.boards["bK"].board
        return True if in_check != 0 else False

    def get_legal_moves(self, moves: list[Move2], color: str):
        # for i in range(len(moves)-1, -1, -1):
        #     move = moves[i]
        #     move_type = move.get_move_type()
        #     board_to_move = self.get_proper_board(move.get_initial_idx())
        #     # if move_type == MoveType.EN_PASSANT_CAPTURE:
        #     #     if self.current_turn() == "white":
        #     #         idx = new_idx + 8
        #     #         prop_board = self.get_proper_board(idx)
        #     #     else:
        #     #         idx = new_idx - 8
        #     #         prop_board = self.get_proper_board(idx)
        #     #     if prop_board != 0:
        #     #         prop_board.clear_bit(idx)
        #     if move_type == MoveType.CASTLE_LEFT or move_type == MoveType.CASTLE_RIGHT:
        #         if not self.check_valid_castle(move, move.get_final_idx()):
        #             # moves.remove(move)
        #             moves.pop(i)
        #     # Simulate a move
        #     board_to_clear = self.get_proper_board(move.get_final_idx())
        #     ##TODO: Investigate faster ways to do this. Generating attack squares for every possible move is slow
        #     self.move(board_to_move, move, board_to_clear)
        #     ## NOW CHECK IF KING IS IN CHECK
        #     # if color == "white":
        #     #     king_board = np.uint64(1) << np.uint64(63 - move.get_final_idx()) if isinstance(board_to_move, KingBoard) else self.boards["wK"].board
        #     # else:
        #     #     king_board = np.uint64(1) << np.uint64(63 - move.get_final_idx()) if isinstance(board_to_move, KingBoard) else self.boards["bK"].board
        #     # print(f"enemy attack squares:\n{BitBoard.print_board_2(enemies)}")
        #     ## if the king is on an enemy square
        #     # print(f"king location:\n:{BitBoard.print_board_2(king_board)}")
        #     enemies = self.get_w_attack_squares() if color == "black" else self.get_b_attack_squares()
        #     if self.king_in_check(enemies, color):
        #         moves.pop(i)
        #     self.undo_move(board_to_move, move, board_to_clear)


        for i in range(len(moves)-1, -1, -1):
            move = moves[i]
            move_type = move.get_move_type()
            # board_to_move = self.get_proper_board(boards, move.get_initial_idx())
            board_to_move = move.get_move_board()
            if self.get_proper_board(move.get_initial_idx()) == 0:
                print("ERRORERRORERROR")
                print(f"movidx: {move.get_initial_idx(), move.get_final_idx()}")
                print(f"Board status:\n:{BitBoard.print_board_2(self.get_w_board() | self.get_b_board())}")
            # print(f"move: {move.get_initial_idx()}, {move.get_final_idx()}")
            if move_type == MoveType.CASTLE_LEFT or move_type == MoveType.CASTLE_RIGHT:
                if not self.check_valid_castle(move, move.get_final_idx()):
                    moves.pop(i)
                    continue
            # Simulate a move
            board_to_clear = self.get_proper_board(move.get_final_idx())
            ##TODO: Investigate faster ways to do this. Generating attack squares for every possible move is slow
            self.move(board_to_move, move, board_to_clear)
            ## The only thing to do now is to check if the king is in check:
            if isinstance(move.get_move_board(), KingBoard):
                enemies = self.get_w_attack_squares() if color == "black" else self.get_b_attack_squares()
                if self.king_in_check(enemies, color):
                    moves.pop(i)
            else:
                ##The piece being moved isn't a king. the only way it could be in check is if it was pinned prior
                king_board: KingBoard = self.boards["wK"] if color == "white" else self.boards["bK"]
                idx = -1
                # for j in range(64):
                #      if king_board.get_bit(j):
                #         idx = j
                #         break
                idx = king_board.get_idx_of_king()
                # if idx < 0:
                #     print(f"move: {move.get_initial_idx()}, {move.get_final_idx()}")
                #     # print(f"moved board:\n{BitBoard.print_board_2(enemies)}")
                #     raise Exception("Unable to locate king")
                if color == "white":
                    enemy_squares = self.get_b_board()
                    my_squares = self.get_w_board()
                    enemy_bishops = self.boards["bB"].board
                    enemy_rooks = self.boards["bB"].board
                    enemy_queens = self.boards["bB"].board
                else:
                    enemy_squares = self.get_w_board()
                    my_squares = self.get_b_board()
                    enemy_bishops = self.boards["wB"].board
                    enemy_rooks = self.boards["wR"].board
                    enemy_queens = self.boards["wQ"].board
                king_vision_diagonals = king_board.get_d_anti_squares(idx, enemy_squares, my_squares)
                king_vision_h_v = king_board.get_h_v_squares(idx, enemy_squares, my_squares)
                if king_vision_diagonals & enemy_bishops != 0 or king_vision_diagonals & enemy_queens != 0:
                    # move puts king in check
                    moves.pop(i)
                elif king_vision_h_v & enemy_rooks != 0 or king_vision_h_v & enemy_queens != 0:
                    moves.pop(i)
                
            self.undo_move(board_to_move, move, board_to_clear)
        return moves

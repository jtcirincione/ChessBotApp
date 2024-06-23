from Dragger import Dragger
from ChessEngine import GameState
from Piece import Piece, Pawn, Rook, Bishop, Knight, Queen, King
from bitboards.BitBoard import BitBoard
from bitboards.BishopBoard import BishopBoard
from bitboards.PawnBoard import PawnBoard
from bitboards.KnightBoard import KnightBoard
from bitboards.RookBoard import RookBoard
from bitboards.QueenBoard import QueenBoard
from bitboards.KingBoard import KingBoard
import numpy as np
from Move import Move
from Move2 import Move2
from enums.MoveType import MoveType
import utils.check as check
import copy

class Robot:
    ## Simple Priority node that pushes higher value moves up
    class PriorityNode:
        def __init__(self, row, col, priority):
            self.row = row
            self.col = col
            self.priority = priority
            

        def compare_to(self, other):
            return other.priority - self.priority
        

    def __init__(self, color):
        self.color = color
        self.dragger = Dragger()
        self.nodes_visited = 0
        self.choosing = False
        # self.history = []

    def reset(self):
        self.nodes_visited = 0
        self.choosing = False


    def get_all_moves(self, board: list[list[Piece]], color):
        moves = []
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if board[row][col] == '--':
                    continue
                if board[row][col].color == color:
                    moves.extend(piece.valid_moves(board, row, col))
        return moves
    
    def opposite_color(self, color):
        return "black" if color == "white" else "white"

    def find_king(self, board: list[list[Piece]], color) -> tuple[King, int, int]:
        for i in range(8):
            for j in range(8):
                if isinstance(board[i][j], King):
                    if board[i][j].color == color:
                        return (board[i][j], i, j)
        raise Exception("Couldn't find king")
        return None
    
    def get_b_attack_squares(self, boards: dict[str, BitBoard], history) -> np.uint64:
        b_attacks = boards["bp"].valid_moves(self.get_b_board(boards), self.get_w_board(boards), history) | boards["bR"].valid_moves(self.get_b_board(boards), self.get_w_board(boards), history) | boards["bB"].valid_moves(self.get_b_board(boards), self.get_w_board(boards), history) | boards["bN"].valid_moves(self.get_b_board(boards), self.get_w_board(boards), history) | boards["bK"].valid_moves(self.get_b_board(boards), self.get_w_board(boards), history) | boards["bQ"].valid_moves(self.get_b_board(boards), self.get_w_board(boards), history)
        return b_attacks
    
    def get_w_attack_squares(self, boards: dict[str,BitBoard], history) -> np.uint64:
        w_attacks = boards["wp"].valid_moves(self.get_w_board(boards), self.get_b_board(boards), history) | boards["wR"].valid_moves(self.get_w_board(boards), self.get_b_board(boards), history) | boards["wB"].valid_moves(self.get_w_board(boards), self.get_b_board(boards), history) | boards["wN"].valid_moves(self.get_w_board(boards), self.get_b_board(boards), history) | boards["wK"].valid_moves(self.get_w_board(boards), self.get_b_board(boards), history) | boards["wQ"].valid_moves(self.get_w_board(boards), self.get_b_board(boards), history)
        return w_attacks
    
    def get_proper_board(self, boards: dict[str, BitBoard], idx) -> BitBoard | np.uint64:
        for board in boards.values():
            if board.get_bit(idx) == 1:
                return board
            
        return np.uint64(0)

    def move(self, bitboard: BitBoard, move: Move2, board_to_clear: BitBoard=np.uint64(0)):
        ## dont use move_piece() to prevent setting king to moved in simulation
        bitboard.clear_bit(move.get_initial_idx())
        bitboard.set_bit(move.get_final_idx())
        if board_to_clear:
            board_to_clear.clear_bit(move.get_final_idx())

    def handle_castle(self, boards: dict[str, BitBoard], move: Move2, color):
        move_type = move.get_move_type()
        if color == "white":
            if move_type == MoveType.CASTLE_LEFT:
                boards["wR"].move_piece(56, move.get_final_idx() + 1)
            if move_type == MoveType.CASTLE_RIGHT:
                boards["wR"].move_piece(63, move.get_final_idx() - 1)
        else:
            if move_type == MoveType.CASTLE_LEFT:
                boards["bR"].move_piece(0, move.get_final_idx() + 1)
            if move_type == MoveType.CASTLE_RIGHT:
                boards["bR"].move_piece(7, move.get_final_idx() - 1)

    def actually_move(self, boards, bitboard: BitBoard, move: Move2, color: str, board_to_clear: BitBoard=np.uint64(0)):
        bitboard.move_piece(move.get_initial_idx(), move.get_final_idx())
        if board_to_clear:
            board_to_clear.clear_bit(move.get_final_idx())
        move_type = move.get_move_type()
        new_idx = move.get_final_idx()
        if move_type == MoveType.EN_PASSANT_CAPTURE:
            if color == "white":
                idx = new_idx + 8
                prop_board = self.get_proper_board(boards, idx)
            else:
                idx = new_idx - 8
                prop_board = self.get_proper_board(boards, idx)
            if prop_board != 0:
                prop_board.clear_bit(idx)
        if move_type == MoveType.CASTLE_LEFT or move_type == MoveType.CASTLE_RIGHT:
            self.handle_castle(boards, move, color)
        if move_type == MoveType.PROMOTE:
            # print('PLEASE PRINT')
            promoting = True

    def king_in_check(self, boards, enemies, color) -> bool:
        in_check = np.uint64(0)
        if color == "white":
            in_check = enemies & boards["wK"].board
        else:
            in_check = enemies & boards["bK"].board
        return True if in_check != 0 else False
    
    ## FIXME: currently invalid castling isn't prevented. the king can move thru attacked squares
    def check_valid_castle(self, boards: dict[str, BitBoard], move: Move2, new_idx, color):
        move_type = move.get_move_type()
        old_idx = move.get_initial_idx()
        if color == "white":
            valid_castle = False
            if move_type == MoveType.CASTLE_LEFT:
                if not boards["wR"].left_rook_moved and boards["wR"].get_bit(56):
                    # print('HI1')
                    valid_castle = True
            if move_type == MoveType.CASTLE_RIGHT:
                if not boards["wR"].right_rook_moved and boards["wR"].get_bit(63):
                    # print('HI2')
                    valid_castle = True
        else:
            valid_castle = False
            if move_type == MoveType.CASTLE_LEFT:
                if not boards["bR"].left_rook_moved  and boards["bR"].get_bit(0):
                    ## TODO: SINCE ROOK HASN'T MOVED, MOVE THE ROOK DURING CASTLE one space to right of king
                    valid_castle = True
            if move_type == MoveType.CASTLE_RIGHT:
                if not boards["bR"].right_rook_moved  and boards["bR"].get_bit(7):
                    ## TODO: SINCE ROOK HASN'T MOVED, MOVE THE ROOK DURING CASTLE one space to left of king
                    valid_castle = True
        if not valid_castle:
            print("UNDO INVALID CASTLE")
            self.get_proper_board(boards, old_idx).moved = False
            return False
        return True

    def undo_move(self, bitboard: BitBoard, move: Move2, board_to_set: BitBoard=np.uint64(0)):
        bitboard.set_bit(move.get_initial_idx())
        bitboard.clear_bit(move.get_final_idx())
        if board_to_set:
            board_to_set.set_bit(move.get_final_idx())
            if isinstance(board_to_set, KingBoard):
                board_to_set.moved = False

    def get_legal_moves(self, boards: dict[str, BitBoard], moves: list[Move2], history, color: str):
        for i in range(len(moves)-1, -1, -1):
            move = moves[i]
            move_type = move.get_move_type()
            board_to_move = self.get_proper_board(boards, move.get_initial_idx())
            if board_to_move == 0:
                moves.pop(i)
                continue
            if move_type == MoveType.CASTLE_LEFT or move_type == MoveType.CASTLE_RIGHT:
                if not self.check_valid_castle(boards, move, move.get_final_idx(), color):
                    # moves.remove(move)
                    moves.pop(i)
            # Simulate a move
            board_to_clear = self.get_proper_board(boards, move.get_final_idx())
            ##TODO: Investigate faster ways to do this. Generating attack squares for every possible move is slow
            self.move(board_to_move, move, board_to_clear)
            
            enemies = self.get_w_attack_squares(boards, history) if color == "black" else self.get_b_attack_squares(boards, history)
            if self.king_in_check(boards, enemies, color):
                moves.pop(i)
            self.undo_move(board_to_move, move, board_to_clear)
        return moves
    
    def get_w_board(self, boards: dict[str, BitBoard]):
        w_board = boards["wp"].board | boards["wR"].board | boards["wB"].board | boards["wN"].board | boards["wK"].board | boards["wQ"].board
        return w_board
    
    def get_b_board(self, boards: dict[str, BitBoard]):
        b_board = boards["bp"].board | boards["bR"].board | boards["bB"].board | boards["bN"].board | boards["bK"].board | boards["bQ"].board
        return b_board
    
    def get_list_of_black_boards(self, game:GameState) -> list[BitBoard]:
        black_boards: list[BitBoard] = []
        for board in game.boards.values():
            if board.color == "black":
                black_boards.append(board)
        return black_boards
    
    def get_list_of_white_boards(self, game:GameState) -> list[BitBoard]:
        white_boards: list[BitBoard] = []
        for board in game.boards.values():
            if board.color == "white":
                white_boards.append(board)
        return white_boards
    
    def get_pseudo_moves(self, bitboard: BitBoard, idx, my_board, opp_board, move_history, board_to_clear: BitBoard=np.uint64):
        if not bitboard:
            return None
        _, moves = bitboard.attacking_squares(idx, my_board, opp_board, move_history)
        return moves
    
    def simulate_move(self, boards: dict[str, BitBoard], move: Move2, history: list[Move2]) -> tuple[dict[str, BitBoard], list[Move2]]:
        boards_copies = copy.deepcopy(boards)
        # print(f"copies: {boards_copies}")
        board_to_clear = self.get_proper_board(boards_copies, move.get_final_idx())
        board_to_move = self.get_proper_board(boards_copies, move.get_initial_idx())
        color = board_to_move.color
        self.actually_move(boards_copies, board_to_move, move, color, board_to_clear)
        # print(f"move: init:{move.get_initial_idx()} fin:{move.get_final_idx()}")
        # print(f"board to move:\n{BitBoard.print_board_2(board_to_move.board)}")
        historycpy = copy.deepcopy(history)
        historycpy.append(move)
        return (boards_copies, history)
    
    def is_terminal(self, moves, color, boards,  my_boards, enemy_boards, history) -> tuple[bool, list[Move2]]:
        # king, row, col = self.find_king(board, color)
        isTerminal = False
        if len(moves) == 0:
            isTerminal = True
        opp_color = self.opposite_color(color)
        # king, row, col = self.find_king(board, opp_color)
        pseudo_moves = []
        for i in range(64):
            if BitBoard.get_bit_on_board(i, enemy_boards):
                bitboard = self.get_proper_board(boards, i)
                pseudo_moves.extend(self.get_pseudo_moves(bitboard, i, enemy_boards, my_boards, history))
        opp_moves : list[Move2] = self.get_legal_moves(boards, pseudo_moves, history, color)
        if len(opp_moves) == 0:
            return True, 0
        return False, opp_moves

    def material(self, boards: list[list[Piece]], color) -> int:
        score = 0
        b_ct = 0
        w_ct = 0
        material_count = {
            PawnBoard: 1,
            KnightBoard: 3,
            BishopBoard: 3,
            RookBoard: 5,
            QueenBoard: 9,
            KingBoard: 0
        }
        for i in range(64):
            btype = self.get_proper_board(boards, i)
            if btype != 0:
                val = material_count[type(btype)]
                if btype.color != "black":
                    val *= -1
                if val > 0:
                    b_ct += 1
                elif val < 0:
                    w_ct += 1
                score += val
        # if score < 0:
            # print(f"black boar2d:\n {BitBoard.print_board_2(self.get_b_board(boards))}")
            # print(f"white boar2d:\n {BitBoard.print_board_2(self.get_w_board(boards))}")
        # print(f"black count: {b_ct}\nwhite count: {w_ct}")
        return score

    ## Add/sub points for player in check, add more for checkmate
    def winning(self, boards: dict[str, BitBoard], white_moves, black_moves, history, color) -> int:
        w_attackers = self.get_w_attack_squares(boards, history) 
        b_attackers = self.get_b_attack_squares(boards, history)
        opponent_color = self.opposite_color(color)
        score = 0
        if len(black_moves) == 0:
            return -10000
        if len(white_moves) == 0:
            return 10000
        
        ## if this move puts the opponent in check
        if self.king_in_check(boards, b_attackers, "white"):
            # print("I SHOULD USE THIS MOVE")
            score += 100
        elif self.king_in_check(boards, w_attackers, "black"):
            score -= 100
        return score
        

    def evaluate(self, boards: dict[str, BitBoard], white_moves: list[Move2], black_moves: list[Move2], history, color) -> int:
        score = 0
        score += self.material(boards, "black")
        score += self.winning(boards, white_moves, black_moves, history, "black")
        return score

    def minimax(self, boards:dict[str, BitBoard], isMax, depth, history: list[Move2]) -> tuple[Move2, int]:
    
        self.nodes_visited += 1
        if isMax == True:
            color = "black"
        else:
            color = "white"
        
        if color == 'white':
            my_boards = self.get_w_board(boards)
            enemy_boards = self.get_b_board(boards)
        else:
            my_boards = self.get_b_board(boards)
            enemy_boards = self.get_w_board(boards)
        # print(f"my_boards:\n{BitBoard.print_board_2(my_boards)}")
        # print(f"enemy_boards:\n{BitBoard.print_board_2(enemy_boards)}")
        pseudo_moves = []
        for i in range(64):
            if BitBoard.get_bit_on_board(i, my_boards):
                bitboard = self.get_proper_board(boards, i)
                pseudo_moves.extend(self.get_pseudo_moves(bitboard, i, my_boards, enemy_boards, history))
        moves : list[Move2] = self.get_legal_moves(boards, pseudo_moves, history, color)
        
        is_terminal, enemy_moves = self.is_terminal(moves, color, boards, my_boards, enemy_boards, history)
        white_moves = moves if color == "white" else enemy_moves
        black_moves = moves if color == "black" else enemy_moves
        if depth == 0 or is_terminal:
            return None, self.evaluate(boards, white_moves, black_moves, history, color)
        # print(color)
        best_move = None
        if isMax:
            max_eval = -float("inf")
            for move in moves:
                # print(f"initial move: {move.get_initial_idx()} finalidx: {move.get_final_idx()}")
                boards_copies, history_cpy = self.simulate_move(boards, move, history)
                # print(f"board after move:\n{BitBoard.print_board_2(self.get_b_board(boards_copies))}")
                _, current_eval = self.minimax(boards=boards_copies, isMax=False, depth=depth-1, history=history_cpy)
                if current_eval > max_eval:
                    max_eval = current_eval
                    best_move = move
            return best_move, max_eval
            
        else:
            min_eval = float("inf")
            for move in moves:
                boards_copies, history_cpy = self.simulate_move(boards, move, history)
                _, current_eval = self.minimax(boards=boards_copies, isMax=True, depth=depth-1, history=history_cpy)
                if current_eval < min_eval:
                    min_eval = current_eval
                    best_move = move
            return best_move, min_eval
    
        
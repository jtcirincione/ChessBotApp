from bitboards.BitBoard import BitBoard
from Move2 import Move2
import numpy as np
from enums.MoveType import MoveType

BLACK_2MOVE_ROW = np.uint64(0b0000000000000000000000001111111100000000000000000000000000000000)
WHITE_2MOVE_ROW = np.uint64(0b0000000000000000000000000000000011111111000000000000000000000000)
BLACK_PASSANT_ROW = np.uint64(0b0000000000000000111111110000000000000000000000000000000000000000)
WHITE_PASSANT_ROW = np.uint64(0b0000000000000000000000000000000000000000111111110000000000000000)
FILE_H_MASK = np.uint64(0b1111111011111110111111101111111011111110111111101111111011111110)
FILE_A_MASK = np.uint64(0b0111111101111111011111110111111101111111011111110111111101111111)
WHITE_PROMOTE_MASK = np.uint64(0xFF00000000000000)
BLACK_PROMOTE_MASK = np.uint64(0xFF)

class PawnBoard(BitBoard):
    def __init__(self, color):
        board = self.initialize_board(color)
        self.previous_board = board
        name = "bp" if color == "black" else "wp"
        super().__init__(color, board, name)
        self.en_passant_square = -1

    def initialize_board(self, color) -> int:
        if color == "white":
            return np.uint64(0b0000000000000000000000000000000000000000000000001111111100000000)
        return np.uint64(0b0000000011111111000000000000000000000000000000000000000000000000)
    
    def reset(self):
        self.board = self.initialize_board(self.color)
        

    def get_left_attacks(self, board, enemy_board):
        if self.color == "white":
            attacks = (board << np.uint64(9)) & FILE_H_MASK
        else:
            attacks = (board >> np.uint64(7)) & FILE_H_MASK
        return attacks & enemy_board
            

    def get_right_attacks(self, board, enemy_board):
        if self.color == "white":
            attacks = (board << np.uint64(7)) & FILE_A_MASK
        else:
            attacks = (board >> np.uint64(9)) & FILE_A_MASK
        return attacks & enemy_board

    def get_attacking_board(self, board, enemy_board: np.uint64):
        return self.get_left_attacks(board, enemy_board) | self.get_right_attacks(board, enemy_board)

    def move_piece(self, clrIdx, setIdx) -> None:
        if not (0 <= setIdx < 64) or not (0 <= clrIdx < 64):
            raise Exception("Square must be from 0 to 63")
        self.set_bit(setIdx)
        self.clear_bit(clrIdx)
        if abs(setIdx - clrIdx) == 16:
            self.en_passant_square = setIdx + 8 if self.color == "white" else setIdx - 8

    def valid_moves(self, my_color_board, enemy_board, move_history) -> np.uint64:
        board = self.board
        en_passant_board = np.uint64(0)
        moves = []


        ## En passant logic
        ## check most recent move and see if it is en passant
        if len(move_history) > 1:
            last_move = move_history[-1]
            ## if the last move that was made resulted in an en passant enabled
            if last_move.get_move_type() == MoveType.EN_PASSANT:
                if self.color == "white":
                    new_idx = last_move.get_final_idx() - 8
                if self.color == "black":
                    new_idx = last_move.get_final_idx() + 8
                ## set square that can be captured to an enemy square
                en_passant_board = self.get_single_piece_board(np.uint64(0xFFFFFFFFFFFFFFFF), new_idx)
                enemy_board |= en_passant_board
            # print(f"Enemy board:\n{BitBoard.print_board_2(enemy_board)}")


        if self.color == "white":
            one_move = np.uint64(board << np.uint64(8)) & ~my_color_board & ~enemy_board
            two_moves = np.uint64(WHITE_2MOVE_ROW & (one_move << np.uint64(8))) & ~my_color_board & ~enemy_board
            move_board = np.uint64(one_move | two_moves)
        if self.color == "black":
            one_move = board >> np.uint64(8) & ~my_color_board & ~enemy_board
            two_moves = np.uint64(BLACK_2MOVE_ROW & (one_move >> np.uint64(8))) & ~my_color_board & ~enemy_board
            move_board = one_move | two_moves
        # one_move
        attack_board = self.get_attacking_board(board, enemy_board) & ~my_color_board
        move_board = attack_board & ~en_passant_board
        if self.color == "white":
            promote_board = move_board & WHITE_PROMOTE_MASK
        if self.color == "black":
            promote_board = move_board & BLACK_PROMOTE_MASK

        # en_passant_board &= attack_board
        if en_passant_board & attack_board > 0:
            pass
            # moves.append(Move2(move_board, pieceIdx, new_idx, MoveType.EN_PASSANT_CAPTURE))

        return move_board | promote_board | one_move | two_moves
    
    def get_double_move(self, empty):
        if self.color == "white":
            two_moves = np.uint64(WHITE_2MOVE_ROW & (self.board << np.uint64(16))) & empty
        else:
            two_moves = np.uint64(BLACK_2MOVE_ROW & (self.board >> np.uint64(16))) & empty
        return two_moves

    def get_single_move(self, empty_squares):
        if self.color == "white":
            one_move = np.uint64(self.board << np.uint64(8)) & empty_squares
        else:
            one_move = self.board >> np.uint64(8) & empty_squares
        return one_move


    def generate_moves(self, empty: np.uint64, opponent_board: np.uint64, move_history: list[Move2]) -> list[Move2]:
        moves: list[Move2] = []
        captures_left = self.get_left_attacks(self.board, opponent_board)
        captures_right = self.get_right_attacks(self.board, opponent_board)
        en_passant_board = np.uint64(0)
        en_passant_left = np.uint64(0)
        en_passant_right = np.uint64(0)
        single_moves = self.get_single_move(empty_squares=empty)
        double_moves = self.get_double_move(empty)

        if len(move_history) > 1:
            last_move = move_history[-1]
            ## if the last move that was made resulted in an en passant enabled
            if last_move.get_move_type() == MoveType.DOUBLE:
                if self.color == "white":
                    new_idx = last_move.get_final_idx() - 8
                if self.color == "black":
                    new_idx = last_move.get_final_idx() + 8
                ## set square that can be captured to an enemy square
                en_passant_board = self.get_single_piece_board(np.uint64(0xFFFFFFFFFFFFFFFF), new_idx)
                en_passant_left = self.get_left_attacks(self.board, en_passant_board)
                en_passant_right = self.get_right_attacks(self.board, en_passant_board)
        
        if self.color == "white":
            # print(f"white double moves: {BitBoard.print_board_2(double_moves)}")
            promote_board = (single_moves | captures_right | captures_left) & WHITE_PROMOTE_MASK
            promote_right = np.uint64(0)
            promote_left = np.uint64(0)
            promote_north = np.uint64(0)
            if promote_board:
                promote_right = self.get_right_attacks(promote_board, opponent_board)
                promote_left = self.get_left_attacks(promote_board, opponent_board)
                promote_north = promote_board & ~(promote_right | promote_left)
            single_moves &= ~WHITE_PROMOTE_MASK
            captures_right &= ~WHITE_PROMOTE_MASK
            captures_left &= ~WHITE_PROMOTE_MASK
            while single_moves != 0:
                idx, single_moves = BitBoard.get_idx_of_lsb(single_moves)
                moves.append(Move2(self, idx + 8, idx, MoveType.QUIET))
            
            while double_moves != 0:
                idx, double_moves = BitBoard.get_idx_of_lsb(double_moves)
                # print(f"white double moves: {BitBoard.print_board_2(double_moves)}")
                moves.append(Move2(self, idx + 16, idx, MoveType.DOUBLE))
                
            while promote_right != 0:
                idx, promote_board = BitBoard.get_idx_of_lsb(promote_right)
                moves.append(Move2(self, idx + 7, idx, MoveType.PROMOTE))
            while promote_left != 0:
                idx, promote_board = BitBoard.get_idx_of_lsb(promote_left)
                moves.append(Move2(self, idx + 9, idx, MoveType.PROMOTE))
            while promote_north != 0:
                idx, promote_board = BitBoard.get_idx_of_lsb(promote_north)
                moves.append(Move2(self, idx + 8, idx, MoveType.PROMOTE))
                
            while en_passant_left != 0:
                idx, en_passant_left = BitBoard.get_idx_of_lsb(en_passant_left)
                moves.append(Move2(self, idx + 9, idx, MoveType.EN_PASSANT_CAPTURE))
                
            while en_passant_right != 0:
                idx, en_passant_right = BitBoard.get_idx_of_lsb(en_passant_right)
                moves.append(Move2(self, idx + 7, idx, MoveType.EN_PASSANT_CAPTURE))
                
            while captures_left != 0:
                idx, captures_left = BitBoard.get_idx_of_lsb(captures_left)
                moves.append(Move2(self, idx + 9, idx, MoveType.QUIET))
            
            while captures_right != 0:
                idx, captures_right = BitBoard.get_idx_of_lsb(captures_right)
                moves.append(Move2(self, idx + 7, idx, MoveType.QUIET))
            # for move in moves:
            #     if move.get_initial_idx() == 79:
            #         print(F"{move.get_move_type()}")
            #         print(F"board looks like: {BitBoard.print_board_2(move.get_move_board().board)}")
            # for i in range(64):
            #     if BitBoard.get_bit_on_board(i, single_moves):
            #         moves.append(Move2(self, i + 8, i, MoveType.QUIET))
            #     if BitBoard.get_bit_on_board(i, double_moves):
            #         moves.append(Move2(self, i + 16, i, MoveType.DOUBLE))
            #     if BitBoard.get_bit_on_board(i, promote_board):
            #         moves.append(Move2(self, i + 16, i, MoveType.PROMOTE))
            #     if BitBoard.get_bit_on_board(i, en_passant_left):
            #         moves.append(Move2(self, i + 9, i, MoveType.EN_PASSANT_CAPTURE))
            #     if BitBoard.get_bit_on_board(i, en_passant_right):
            #         moves.append(Move2(self, i + 7, i, MoveType.EN_PASSANT_CAPTURE))
            #     if BitBoard.get_bit_on_board(i, captures_left):
            #         moves.append(Move2(self, i + 9, i, MoveType.QUIET))
            #     if BitBoard.get_bit_on_board(i, captures_right):
            #         moves.append(Move2(self, i + 7, i, MoveType.QUIET))
        elif self.color == "black":
            promote_board = (single_moves | captures_right | captures_left) & BLACK_PROMOTE_MASK
            single_moves &= ~BLACK_PROMOTE_MASK
            captures_right &= ~BLACK_PROMOTE_MASK
            captures_left &= ~BLACK_PROMOTE_MASK
            promote_right = np.uint64(0)
            promote_left = np.uint64(0)
            promote_north = np.uint64(0)
            if promote_board:
                promote_right = self.get_right_attacks(promote_board, opponent_board)
                promote_left = self.get_left_attacks(promote_board, opponent_board)
                promote_north = promote_board & ~(promote_right | promote_left)
            # for i in range(64):
            #     if BitBoard.get_bit_on_board(i, single_moves):
            #         moves.append(Move2(self, i - 8, i, MoveType.QUIET))
            #     if BitBoard.get_bit_on_board(i, double_moves):
            #         moves.append(Move2(self, i - 16, i, MoveType.DOUBLE))
            #     if BitBoard.get_bit_on_board(i, promote_board):
            #         moves.append(Move2(self, i - 16, i, MoveType.PROMOTE))
            #     if BitBoard.get_bit_on_board(i, en_passant_left):
            #         moves.append(Move2(self, i - 7, i, MoveType.EN_PASSANT_CAPTURE))
            #     if BitBoard.get_bit_on_board(i, en_passant_right):
            #         moves.append(Move2(self, i - 9, i, MoveType.EN_PASSANT_CAPTURE))
            #     if BitBoard.get_bit_on_board(i, captures_left):
            #         moves.append(Move2(self, i - 7, i, MoveType.QUIET))
            #     if BitBoard.get_bit_on_board(i, captures_right):
            #         moves.append(Move2(self, i - 9, i, MoveType.QUIET))
            
            while single_moves != 0:
                idx, single_moves = BitBoard.get_idx_of_lsb(single_moves)
                moves.append(Move2(self, idx - 8, idx, MoveType.QUIET))
            
            while double_moves != 0:
                idx, double_moves = BitBoard.get_idx_of_lsb(double_moves)
                moves.append(Move2(self, idx - 16, idx, MoveType.DOUBLE))
                # print(f"double {self.color}move: {idx}")
                
            while promote_right != 0:
                idx, promote_board = BitBoard.get_idx_of_lsb(promote_right)
                moves.append(Move2(self, idx - 9, idx, MoveType.PROMOTE))
            while promote_left != 0:
                idx, promote_board = BitBoard.get_idx_of_lsb(promote_left)
                moves.append(Move2(self, idx - 7, idx, MoveType.PROMOTE))
            while promote_north != 0:
                idx, promote_board = BitBoard.get_idx_of_lsb(promote_north)
                moves.append(Move2(self, idx - 8, idx, MoveType.PROMOTE))
                
            while en_passant_left != 0:
                idx, en_passant_left = BitBoard.get_idx_of_lsb(en_passant_left)
                moves.append(Move2(self, idx - 7, idx, MoveType.EN_PASSANT_CAPTURE))
                
            while en_passant_right != 0:
                idx, en_passant_right = BitBoard.get_idx_of_lsb(en_passant_right)
                moves.append(Move2(self, idx - 9, idx, MoveType.EN_PASSANT_CAPTURE))
                
            while captures_left != 0:
                idx, captures_left = BitBoard.get_idx_of_lsb(captures_left)
                moves.append(Move2(self, idx - 7, idx, MoveType.QUIET))
            
            while captures_right != 0:
                idx, captures_right = BitBoard.get_idx_of_lsb(captures_right)
                moves.append(Move2(self, idx - 9, idx, MoveType.QUIET))
        
        return moves


    def attacking_squares(self, pieceIdx:int, my_color_board:np.uint64, enemy_board:np.uint64, move_history: list[Move2]) -> tuple[np.uint64, list[Move2]]:
        board = self.get_single_piece_board(self.board, pieceIdx)
        en_passant_board = np.uint64(0)
        moves = []




        if self.color == "white":
            one_move = np.uint64(board << np.uint64(8)) & ~my_color_board & ~enemy_board
            two_moves = np.uint64(WHITE_2MOVE_ROW & (one_move << np.uint64(8))) & ~my_color_board & ~enemy_board
            move_board = np.uint64(one_move | two_moves)
        if self.color == "black":
            one_move = board >> np.uint64(8) & ~my_color_board & ~enemy_board
            two_moves = np.uint64(BLACK_2MOVE_ROW & (one_move >> np.uint64(8))) & ~my_color_board & ~enemy_board
            move_board = one_move | two_moves
        # one_move
        ## En passant logic
        ## check most recent move and see if it is en passant
        if len(move_history) > 1:
            last_move = move_history[-1]
            ## if the last move that was made resulted in an en passant enabled
            if last_move.get_move_type() == MoveType.EN_PASSANT:
                if self.color == "white":
                    new_idx = last_move.get_final_idx() - 8
                if self.color == "black":
                    new_idx = last_move.get_final_idx() + 8
                ## set square that can be captured to an enemy square
                en_passant_board = self.get_single_piece_board(np.uint64(0xFFFFFFFFFFFFFFFF), new_idx)
                enemy_board |= en_passant_board
            # print(f"Enemy board:\n{BitBoard.print_board_2(enemy_board)}")
        attack_board = self.get_attacking_board(board, enemy_board) & ~my_color_board
        moves.extend(BitBoard.get_moves(self, one_move & ~BLACK_PROMOTE_MASK & ~WHITE_PROMOTE_MASK, pieceIdx))
        moves.extend(BitBoard.get_moves(self, two_moves & ~BLACK_PROMOTE_MASK & ~WHITE_PROMOTE_MASK, pieceIdx, MoveType.EN_PASSANT))
        moves.extend(BitBoard.get_moves(self, attack_board & ~en_passant_board & ~BLACK_PROMOTE_MASK & ~WHITE_PROMOTE_MASK, pieceIdx))
        move_board |= attack_board & ~en_passant_board
        if self.color == "white":
            promote_board = move_board & WHITE_PROMOTE_MASK
        if self.color == "black":
            promote_board = move_board & BLACK_PROMOTE_MASK
        if promote_board:
            moves.extend(BitBoard.get_moves(self, promote_board, pieceIdx, MoveType.PROMOTE))

        # en_passant_board &= attack_board
        if en_passant_board & attack_board > 0:
            moves.append(Move2(self, pieceIdx, new_idx, MoveType.EN_PASSANT_CAPTURE))

        return (move_board, moves)
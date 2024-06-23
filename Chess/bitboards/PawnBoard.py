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


    ##TODO: Add masking logic for moving up 2
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
    
    def attacking_squares(self, pieceIdx:int, my_color_board:np.uint64, enemy_board:np.uint64, move_history: list[Move2]) -> tuple[np.uint64, list[Move2]]:
        board = self.get_single_piece_board(self.board, pieceIdx)
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
        moves.extend(BitBoard.get_moves(self.board, one_move & ~BLACK_PROMOTE_MASK & ~WHITE_PROMOTE_MASK, pieceIdx))
        moves.extend(BitBoard.get_moves(self.board, two_moves & ~BLACK_PROMOTE_MASK & ~WHITE_PROMOTE_MASK, pieceIdx, MoveType.EN_PASSANT))
        moves.extend(BitBoard.get_moves(self.board, attack_board & ~en_passant_board & ~BLACK_PROMOTE_MASK & ~WHITE_PROMOTE_MASK, pieceIdx))
        move_board |= attack_board & ~en_passant_board
        if self.color == "white":
            promote_board = move_board & WHITE_PROMOTE_MASK
        if self.color == "black":
            promote_board = move_board & BLACK_PROMOTE_MASK
        if promote_board:
            moves.extend(BitBoard.get_moves(self.board, promote_board, pieceIdx, MoveType.PROMOTE))

        # en_passant_board &= attack_board
        if en_passant_board & attack_board > 0:
            moves.append(Move2(move_board, pieceIdx, new_idx, MoveType.EN_PASSANT_CAPTURE))

        return (move_board, moves)
from bitboards.BitBoard import BitBoard
from preload.moves import get_queen_attacks, get_rook_attacks, get_bishop_attacks, compute_pawn_attacks
import numpy as np
from move import Move
STARTING_POSITIONS = {
    "wp":  np.uint64(0b0000000000000000000000000000000000000000000000001111111100000000),
    "bp":  np.uint64(0b0000000011111111000000000000000000000000000000000000000000000000),
    "wN":  np.uint64(0b0000000000000000000000000000000000000000000000000000000001000010),  # B1, G1
    "bN":  np.uint64(0b0100001000000000000000000000000000000000000000000000000000000000),  # B8, G8
    "wB":  np.uint64(0b0000000000000000000000000000000000000000000000000000000000100100),  # C1, F1
    "bB":  np.uint64(0b0010010000000000000000000000000000000000000000000000000000000000),  # C8, F8
    "wR":  np.uint64(0b0000000000000000000000000000000000000000000000000000000010000001),  # A1, H1
    "bR":  np.uint64(0b1000000100000000000000000000000000000000000000000000000000000000),  # A8, H8
    "wQ":  np.uint64(0b0000000000000000000000000000000000000000000000000000000000010000),  # D1
    "bQ":  np.uint64(0b0001000000000000000000000000000000000000000000000000000000000000),  # D8
    "wK":  np.uint64(0b0000000000000000000000000000000000000000000000000000000000001000),  # E1
    "bK":  np.uint64(0b0000100000000000000000000000000000000000000000000000000000000000),  # E8
    }

NOT_AB_MASK = np.uint64(
    0b0011111100111111001111110011111100111111001111110011111100111111)
NOT_GH_MASK = np.uint64(
    0b1111110011111100111111001111110011111100111111001111110011111100)
NOT_A_MASK = np.uint64(
    0b0111111101111111011111110111111101111111011111110111111101111111)
NOT_B_MASK = np.uint64(
    0b1011111110111111101111111011111110111111101111111011111110111111)
NOT_G_MASK = np.uint64(
    0b1111110111111101111111011111110111111101111111011111110111111101)
NOT_H_MASK = np.uint64(
    0b1111111011111110111111101111111011111110111111101111111011111110)

DOUBLE_PUSH_WP_MASK = np.uint64(
    0b0000000000000000000000000000000011111111000000000000000000000000)

SINGLE_PUSH_WP_MASK = np.uint64(
    0b0000000000000000000000000000000000000000111111110000000000000000)

DOUBLE_PUSH_BP_MASK = np.uint64(
    0b0000000000000000000000001111111100000000000000000000000000000000)

SINGLE_PUSH_BP_MASK = np.uint64(
    0b0000000000000000111111110000000000000000000000000000000000000000)

"""
Starts from idx 0 at bottom right, goes up from right to left to 63 at top left
"""
class Chessboard:
    

    def __init__(self):
        self.bitboards = {
            key: BitBoard(val, key) for key, val in STARTING_POSITIONS.items()
        }

        self.KNIGHT_MOVES = [0] * 64

        self.KING_MOVES = [0] * 64
        self.WHITE_PAWN_ATTACKS, self.BLACK_PAWN_ATTACKS = compute_pawn_attacks()
        self.precompute_knights()
        self.precompute_kings()
        print("flkjdsalkdsfj: ")
        # BitBoard.static_print(BitBoard.generate_bishop_mask(24))
        # BitBoard.static_print(magics.get_queen_attacks(0, 0))

    def get_piece_boards(self) -> dict[str, BitBoard]:
        return {
            key: val for key, val in self.bitboards.items() if key != "white_pieces" and key != "black_pieces" and key != "occupied"
        }
    
    def get_color_board(self, is_white):
        occupancy = np.uint64(0)
        for p in self.bitboards:
            if "w" in p:  # Exclude self OR
                if is_white:
                    occupancy |= self.bitboards[p].board
            else:
                if not is_white:
                    occupancy |= self.bitboards[p].board
        return occupancy

    def get_occupancy_board(self):
        return self.get_color_board(True) | self.get_color_board(False)

    def precompute_knights(self):
        for i in range(64):
            self.KNIGHT_MOVES[i] = self.generate_knight_moves(i)
    
    def generate_knight_moves(self, idx):
        knight_move = np.uint64(0)
        board = np.uint64(0)
        BitBoard.static_set_bit(board, idx)
        moves = [
            6,  # top left move restrict from G and H
            15,  # top left move restrict from H
            10,  # top right move, # restrict from A and B
            17,  # top right move, # restrict from A
            -6,  # bottom right move # restrict from A and B
            -15,  # bottom right move # restrict from A
            -10,  # bottom left move # restrict from G and H
            -17  # bottom left move # restrict from H
        ]

        for move in moves:
            if move > 0:
                position = (board << np.uint64(move))
            else:
                position = (board >> np.uint64(-move))
            if move == 6 or move == -10:
                position &= NOT_GH_MASK
            if move == 15 or move == -17:
                position &= NOT_H_MASK
            if move == 10 or move == -6:
                position &= NOT_AB_MASK
            if move == -15 or move == 17:
                position &= NOT_A_MASK
            knight_move |= position

        return knight_move


    def precompute_kings(self):
        for i in range(64):
            self.KNIGHT_MOVES[i] = self.generate_king_moves(i)
    
    def generate_king_moves(self, idx):
        king_move = np.uint64(0)
        board = np.uint64(0)
        BitBoard.static_set_bit(board, idx)

        moves = [8, -8, 1, -1, 7, 9, -7, -9] 
        for move in moves:
            if move > 0:
                potential_move = (board << np.uint64(move))
            else:
                potential_move = (board >> np.uint64(-move))

            if move == -1 or move == -9 or move == 7: ## if piece is moving to the right
                potential_move &= NOT_A_MASK
            if move == 1 or move == 9 or move == -7: ## if piece is moving to the left
                potential_move &= NOT_H_MASK

            king_move |= potential_move
        return king_move

    def mask_pawn_attacks(self, white):
        attack_squares = np.uint64(0)
        if white:
            pawns = self.bitboards['wp'].board
            attack_squares |= (pawns << 9) & NOT_A_MASK ## right attack
            attack_squares |= (pawns << 7) & NOT_H_MASK ## left attack
            attack_squares &= ~self.get_color_board(is_white=True)
        else:
            pawns = self.bitboards['bp'].board
            attack_squares |= (pawns >> 7) & NOT_A_MASK ## right attack
            attack_squares |= (pawns >> 9) & NOT_H_MASK ## left attack
            attack_squares &= ~self.get_color_board(is_white=False)
        return attack_squares
    
    def get_pawn_attacks(self, idx, white):
        return self.WHITE_PAWN_ATTACKS[idx] if white else self.BLACK_PAWN_ATTACKS[idx]
    
    def get_pawn_single_pushes(self, idx, is_white):
        pawn  = np.uint64(np.uint64(1) << np.uint64(idx))
        return (pawn << 8) & SINGLE_PUSH_WP_MASK if is_white else (pawn >> 8) & SINGLE_PUSH_BP_MASK
    
    def get_pawn_double_pushes(self, idx, is_white):
        pawn = self.get_pawn_single_pushes(idx, is_white)
        return (pawn << 8) & DOUBLE_PUSH_WP_MASK if is_white else (pawn >> 8) & DOUBLE_PUSH_BP_MASK

    def get_bishop_attacks(self, idx, blockers, white_turn):
        return get_bishop_attacks(idx, blockers) & ~self.get_color_board(white_turn) # get attacks excluding captures on my colored pieces
    
    def get_rook_attacks(self, idx, blockers, white_turn):
        return get_rook_attacks(idx, blockers) & ~self.get_color_board(white_turn) # get attacks excluding captures on my colored pieces
    
    def get_queen_attacks(self, idx, blockers, white_turn):
        return get_queen_attacks(idx, blockers) & ~self.get_color_board(white_turn) # get attacks excluding captures on my colored pieces
    
    def get_pawn_moves(self, white_turn):
        #TODO: handle EP moves
        # EN PASSANT is possible IFF enemy pawn is behind (or in front of depending on the color) our pawn and on the file beside it,
        # and our attack square is empty
        moves = []
        occupancy = self.get_occupancy_board()
        enemy_pieces = self.get_color_board(not white_turn)

        # Pawns
        pawn_board = self.bitboards['wp' if white_turn else 'bp'].board
        while pawn_board:
            from_idx = BitBoard.bit_scan_forward(pawn_board)
            pawn_attacks = self.get_pawn_attacks(from_idx, white_turn) & enemy_pieces

            # GENERATE EP CAPTURES HERE

            pawn_single_pushes = self.get_pawn_single_pushes(from_idx, white_turn) & ~occupancy
            pawn_double_pushes = self.get_pawn_double_pushes(from_idx) & ~occupancy
            while pawn_attacks:
                to_idx = BitBoard.bit_scan_forward(pawn_attacks)
                if (to_idx >= 56):
                    # if we're on back rank
                    moves.append(Move(from_idx, to_idx, Move.ROOK_CAP_PROMO))
                    moves.append(Move(from_idx, to_idx, Move.BISHOP_CAP_PROMO))
                    moves.append(Move(from_idx, to_idx, Move.QUEEN_CAP_PROMO))
                    moves.append(Move(from_idx, to_idx, Move.KNIGHT_CAP_PROMO))
                else:
                    moves.append(Move(from_idx, to_idx, Move.CAPTURE))
                pawn_attacks &= pawn_attacks - 1
            while pawn_single_pushes:
                to_idx = BitBoard.bit_scan_forward(pawn_single_pushes)
                if (to_idx >= 56):
                    # if we're on back rank
                    moves.append(Move(from_idx, to_idx, Move.ROOK_PROMO))
                    moves.append(Move(from_idx, to_idx, Move.BISHOP_PROMO))
                    moves.append(Move(from_idx, to_idx, Move.QUEEN_PROMO))
                    moves.append(Move(from_idx, to_idx, Move.KNIGHT_PROMO))
                else:
                    moves.append(Move(from_idx, to_idx, Move.QUIET))
                pawn_single_pushes &= pawn_single_pushes - 1
            while pawn_double_pushes:
                to_idx = BitBoard.bit_scan_forward(pawn_double_pushes)
                moves.append(Move(from_idx, to_idx, Move.DOUBLE_PAWN_PUSH))
                pawn_double_pushes &= pawn_double_pushes - 1

            pawn_board &= pawn_board - 1
        return moves

    def get_bishop_moves(self, white_turn):
        bishop_board = self.bitboards['wB' if white_turn else 'bB']
        moves = []
        occupancy = self.get_occupancy_board()
        enemy_pieces = self.get_color_board(not white_turn)
        while bishop_board:
            from_idx = BitBoard.bit_scan_forward(bishop_board)
            bishop_attacks = self.get_bishop_attacks(from_idx, occupancy, white_turn)

            while bishop_attacks:
                to_idx = BitBoard.bit_scan_forward(bishop_attacks)
                if enemy_pieces & np.uint64(1 << to_idx):
                    # we on a capture
                    moves.append(Move(from_idx, to_idx, Move.CAPTURE))
                else:
                    moves.append(Move(from_idx, to_idx, Move.QUIET))
                bishop_attacks &= bishop_attacks - 1

            bishop_board &= bishop_board - 1
        return moves

    def get_rook_moves(self, white_turn):
        rook_board = self.bitboards['wR' if white_turn else 'bR']
        moves = []
        occupancy = self.get_occupancy_board()
        enemy_pieces = self.get_color_board(not white_turn)
        while rook_board:
            from_idx = BitBoard.bit_scan_forward(rook_board)
            rook_attacks = self.get_rook_attacks(from_idx, occupancy, white_turn)
            
            while rook_attacks:
                to_idx = BitBoard.bit_scan_forward(rook_attacks)
                if enemy_pieces & np.uint64(1 << to_idx):
                    # we on a capture
                    moves.append(Move(from_idx, to_idx, Move.CAPTURE))
                else:
                    moves.append(Move(from_idx, to_idx, Move.QUIET))
                rook_attacks &= rook_attacks - 1

            rook_board &= rook_board - 1
        return moves
    
    def get_queen_moves(self, white_turn):
        moves = []
        moves.extend(self.get_rook_moves(white_turn))
        moves.extend(self.get_bishop_moves(white_turn))
        return moves

    def get_knight_moves(self, white_turn):
        moves = []
        knight_board = self.bitboards['wN' if white_turn else 'bN']
        occupancy = self.get_occupancy_board()
        enemy_pieces = self.get_color_board(white_turn)

        while knight_board:
            from_idx = BitBoard.bit_scan_forward(knight_board)
            knight_captures = self.KNIGHT_MOVES[from_idx] & enemy_pieces
            knight_quiets = self.KNIGHT_MOVES[from_idx] & ~occupancy
            while knight_captures:
                to_idx = BitBoard.bit_scan_forward(knight_captures)
                moves.append(Move(from_idx, to_idx, Move.CAPTURE))
                knight_captures &= knight_captures - 1

            while knight_quiets:
                to_idx = BitBoard.bit_scan_forward(knight_quiets)
                moves.append(Move(from_idx, to_idx, Move.QUIET))
                knight_quiets &= knight_quiets - 1

            knight_board &= knight_board - 1
        return moves
    
    def get_king_moves(self, white_turn):
        king_board = self.bitboards['wK' if white_turn else 'bK']
        occupancy = self.get_occupancy_board()
        enemy_pieces = self.get_color_board(white_turn)
        moves = []


        from_idx = BitBoard.bit_scan_forward(king_board)
        king_quiets = self.KING_MOVES[from_idx] & ~occupancy
        king_captures = self.KING_MOVES[from_idx] & enemy_pieces

        while king_captures:
            to_idx = BitBoard.bit_scan_forward(king_captures)
            moves.append(Move(from_idx, to_idx, Move.CAPTURE))
            king_captures &= king_captures - 1

        while king_quiets:
            to_idx = BitBoard.bit_scan_forward(king_quiets)
            moves.append(Move(from_idx, to_idx, Move.QUIET))
            king_quiets &= king_quiets - 1

        return moves

        
        
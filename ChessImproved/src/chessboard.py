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
    "wQ":  np.uint64(0b0000000000000000000000000000000000000000000000000000000000001000),  # D1
    "bQ":  np.uint64(0b0000100000000000000000000000000000000000000000000000000000000000),  # D8
    "wK":  np.uint64(0b0000000000000000000000000000000000000000000000000000000000010000),  # E1
    "bK":  np.uint64(0b0001000000000000000000000000000000000000000000000000000000000000),  # E8
    }

NOT_GH_MASK = np.uint64(
    0b0011111100111111001111110011111100111111001111110011111100111111)
NOT_AB_MASK = np.uint64(
    0b1111110011111100111111001111110011111100111111001111110011111100)
NOT_H_MASK = np.uint64(
    0b0111111101111111011111110111111101111111011111110111111101111111)
NOT_G_MASK = np.uint64(
    0b1011111110111111101111111011111110111111101111111011111110111111)
NOT_B_MASK = np.uint64(
    0b1111110111111101111111011111110111111101111111011111110111111101)
NOT_A_MASK = np.uint64(
    0b1111111011111110111111101111111011111110111111101111111011111110)

DOUBLE_PUSH_WP_MASK = np.uint64(
    0b0000000000000000000000000000000011111111000000000000000000000000)

SINGLE_PUSH_WP_MASK = np.uint64(
    0b0000000011111111111111111111111111111111111111111111111111111111)

DOUBLE_PUSH_BP_MASK = np.uint64(
    0b0000000000000000000000001111111100000000000000000000000000000000)

SINGLE_PUSH_BP_MASK = np.uint64(
    0b1111111111111111111111111111111111111111111111111111111100000000)

"""
Starts from idx 0 at bottom right, goes up from right to left to 63 at top left
"""
class Chessboard:
    

    def __init__(self):
        self.bitboards = {
            key: BitBoard(val, key) for key, val in STARTING_POSITIONS.items()
        }

        self.KNIGHT_MOVES = self.precompute_knights()

        self.KING_MOVES = [0] * 64
        self.WHITE_PAWN_ATTACKS, self.BLACK_PAWN_ATTACKS = compute_pawn_attacks()
        
        self.precompute_kings()

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
        occupancy = np.uint64(0)
        for p in self.bitboards:
            occupancy |= self.bitboards[p].board
        return occupancy

    def precompute_knights(self):
        knight_moves = []
        for i in range(64):
            knight_moves.append(self.generate_knight_moves(i))
        return knight_moves
    
    def generate_knight_moves(self, idx):
        knight_move = np.uint64(0)
        board = BitBoard.static_set_bit(np.uint64(0), idx)
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
            self.KING_MOVES[i] = self.generate_king_moves(i)
    
    def generate_king_moves(self, idx):
        king_move = np.uint64(0)
        board = BitBoard.static_set_bit(np.uint64(0), idx)

        moves = [8, -8, 1, -1, 7, 9, -7, -9] 
        for move in moves:
            if move > 0:
                potential_move = (board << np.uint64(move))
            else:
                potential_move = (board >> np.uint64(-move))

            if move == -1 or move == -9 or move == 7: ## if piece is moving to the left
                potential_move &= NOT_H_MASK
            if move == 1 or move == 9 or move == -7: ## if piece is moving to the right
                potential_move &= NOT_A_MASK

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
    
    def get_pawn_ep_attacks(self, idx, is_white):
        pawn_ep_attacks = np.uint64(0)
        enemy_ep_potential_board = self.bitboards['bp'].board & DOUBLE_PUSH_BP_MASK if is_white else self.bitboards['wp'].board & DOUBLE_PUSH_WP_MASK
        if enemy_ep_potential_board & np.uint64(1 << (idx + 1)) > 0: # if pawn to the right on our ep row
            pawn_ep_attacks |= np.uint64(1 << (idx + 9)) if is_white else np.uint64(1 << (idx - 7))
        
        if enemy_ep_potential_board & np.uint64(1 << (idx - 1)) > 0: # if pawn to the left on our ep row
            pawn_ep_attacks |= np.uint64(1 << (idx + 7)) if is_white else np.uint64(1 << (idx - 9))
        return pawn_ep_attacks

    def get_pawn_single_pushes(self, idx, occupancy, is_white):
        pawn  = np.uint64(np.uint64(1) << np.uint64(idx))
        return ((pawn << 8) & SINGLE_PUSH_WP_MASK) & ~occupancy if is_white else ((pawn >> 8) & SINGLE_PUSH_BP_MASK) & ~occupancy
    
    def get_pawn_double_pushes(self, pawn_single_push, occupancy, is_white):
        return ((pawn_single_push << 8) & DOUBLE_PUSH_WP_MASK) & ~occupancy if is_white else ((pawn_single_push >> 8) & DOUBLE_PUSH_BP_MASK) & ~occupancy

    def get_bishop_attacks(self, idx, blockers, white_turn):
        attacks = get_bishop_attacks(idx, blockers)  # get attacks excluding captures on my colored pieces)

        return attacks & ~self.get_color_board(white_turn)
    
    def get_rook_attacks(self, idx, blockers, white_turn):
        attacks = get_rook_attacks(idx, blockers) & ~self.get_color_board(white_turn) # get attacks excluding captures on my colored pieces
        return attacks    
    
    def get_queen_attacks(self, idx, blockers, white_turn):
        attacks = get_queen_attacks(idx, blockers) & ~self.get_color_board(white_turn) # get attacks excluding captures on my colored pieces
        return attacks # get attacks excluding captures on my colored pieces
    
    def get_all_attack_squares(self, blockers, white_turn):
        attacks = np.uint64(0)
        bishop_board = self.bitboards['wB' if white_turn else 'bB'].board
        rook_board = self.bitboards['wR' if white_turn else 'bR'].board
        queen_board = self.bitboards['wQ' if white_turn else 'bQ'].board
        pawn_board = self.bitboards['wp' if white_turn else 'bp'].board
        knight_board = self.bitboards['wN' if white_turn else 'bN'].board
        king_board = self.bitboards['wK' if white_turn else 'bK'].board

        enemy_pieces = self.get_color_board(not white_turn)
        friendlies = self.get_color_board(white_turn)

        while bishop_board:
            idx = BitBoard.bit_scan_forward(bishop_board)
            attacks |= self.get_bishop_attacks(idx, blockers, white_turn)
            bishop_board &= bishop_board - 1
        while rook_board:
            idx = BitBoard.bit_scan_forward(rook_board)
            attacks |= self.get_rook_attacks(idx, blockers, white_turn)
            rook_board &= rook_board - 1
        while queen_board:
            idx = BitBoard.bit_scan_forward(queen_board)
            attacks |= self.get_queen_attacks(idx, blockers, white_turn)
            queen_board &= queen_board - 1
        while pawn_board:
            idx = BitBoard.bit_scan_forward(pawn_board)
            attacks |= self.get_pawn_attacks(idx, white_turn) & enemy_pieces
            pawn_board &= pawn_board - 1
        while knight_board:
            idx = BitBoard.bit_scan_forward(knight_board)
            attacks |= self.KNIGHT_MOVES[idx] & ~friendlies
            knight_board &= knight_board - 1
        while king_board:
            idx = BitBoard.bit_scan_forward(king_board)
            attacks |= self.KING_MOVES[idx] & ~friendlies
            king_board &= king_board - 1
        
        return attacks



    
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
            pawn_ep_attacks = self.get_pawn_ep_attacks(from_idx, white_turn)

            pawn_single_pushes = self.get_pawn_single_pushes(from_idx, occupancy, white_turn)

            pawn_double_pushes = self.get_pawn_double_pushes(pawn_single_pushes, occupancy, white_turn)
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
            while pawn_ep_attacks:
                to_idx = BitBoard.bit_scan_forward(pawn_ep_attacks)
                moves.append(Move(from_idx, to_idx, Move.EP_CAPTURE))
                pawn_ep_attacks &= pawn_ep_attacks - 1
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
        bishop_board = self.bitboards['wB' if white_turn else 'bB'].board
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
        rook_board = self.bitboards['wR' if white_turn else 'bR'].board
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
        queen_board = self.bitboards['wQ' if white_turn else 'bQ'].board
        moves = []
        occupancy = self.get_occupancy_board()
        enemy_pieces = self.get_color_board(not white_turn)
        while queen_board:
            from_idx = BitBoard.bit_scan_forward(queen_board)
            queen_attacks = self.get_queen_attacks(from_idx, occupancy, white_turn)
            
            while queen_attacks:
                to_idx = BitBoard.bit_scan_forward(queen_attacks)
                if enemy_pieces & np.uint64(1 << to_idx):
                    # we on a capture
                    moves.append(Move(from_idx, to_idx, Move.CAPTURE))
                else:
                    moves.append(Move(from_idx, to_idx, Move.QUIET))
                queen_attacks &= queen_attacks - 1

            queen_board &= queen_board - 1
        return moves

    def get_knight_moves(self, white_turn):
        moves = []
        knight_board = self.bitboards['wN' if white_turn else 'bN'].board
        occupancy = self.get_occupancy_board()
        enemy_pieces = self.get_color_board(not white_turn)

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
        king_board = self.bitboards['wK' if white_turn else 'bK'].board
        occupancy = self.get_occupancy_board()
        enemy_pieces = self.get_color_board(not white_turn)
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

        # castling
        castle_idx = 4 if white_turn else 60
        if BitBoard.bit_scan_forward(king_board) == castle_idx:
            # queen side castle
            to_idx = 2 if white_turn else 58
            if (1 << np.uint64(castle_idx - 1) & occupancy) == 0 and (1 << np.uint64(castle_idx - 2) & occupancy) == 0 and (1 << np.uint64(castle_idx - 3) & occupancy) == 0:
                moves.append(Move(from_idx, to_idx, Move.QUEEN_CASTLE))
            # king side castle
            to_idx = 6 if white_turn else 62
            if (1 << np.uint64(castle_idx + 1) & occupancy) == 0 and (1 << np.uint64(castle_idx + 2) & occupancy) == 0:
                moves.append(Move(from_idx, to_idx, Move.KING_CASTLE))

        return moves 

        
        
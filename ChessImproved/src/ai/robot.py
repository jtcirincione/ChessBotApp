from bitboards import BitBoard
from chess_engine import GameState

class Robot():
    def __init__(self, color):
        self.color = color
        self.choosing = False if color == "black" else True
        self.move_count = 0

    def is_terminal(self, moves):
        return True if len(moves) == 0 else False
    
    def material(self, game_state: GameState):
        PIECE_VALUES = {
            "p": 1,
            "N": 3,
            "B": 3,
            "R": 5,
            "Q": 9,
            "K": 100
        }
        ai_color = "w" if self.color == "white" else "b"
        score = 0
        for key, val in game_state.board.bitboards.items():
            num_pieces = bin(val.board).count("1")
            material_value = num_pieces * PIECE_VALUES[key[-1]]
            if not key.startswith(ai_color):
                material_value *= -1
            score += material_value
        
        return score
    
    def winning(self, game_state: GameState):
        score = 0
        if game_state.king_in_check(white_king=True):
            score += 100
            if len(game_state.get_valid_moves_by_color(True)) == 0:
                score += 10000
        if game_state.king_in_check(white_king=False):
            score -= 100
            if len(game_state.get_valid_moves_by_color(False)) == 0:
                score -= 10000

        return score



    def evaluate(self, game_state):
        score = self.material(game_state)
        score += self.winning(game_state)
        return score

    def minimax(self, game_state: GameState, isMax, depth, alpha, beta):
        if isMax == True:
            color = "black"
        else:
            color = "white"

        legal_moves = game_state.get_valid_moves()

        
        is_terminal = self.is_terminal(legal_moves)
        if depth == 0 or is_terminal:
            return None, self.evaluate(game_state)
        # print(color)
        best_move = None
        if isMax:
            max_eval = float("-inf")
            for move in legal_moves:
                self.move_count += 1
                # print(f"initial move: {move.get_initial_idx()} finalidx: {move.get_final_idx()}")
                # if not self.is_legal(boards, move, color):
                #     continue
                board_to_move = game_state.get_proper_board(move.get_from_idx())
                board_to_clear = game_state.get_proper_board(move.get_to_idx())
                game_state.move(board_to_move, board_to_clear, move)                
                # print(f"board after move:\n{BitBoard.print_board_2(self.get_b_board(boards_copies))}")
                _, current_eval = self.minimax(game_state, isMax=False, depth=depth-1, alpha=alpha, beta=beta)
                game_state.move(board_to_move, board_to_clear, move, undo=True)
                if current_eval > max_eval:
                    max_eval = current_eval
                    best_move = move
                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break
            return best_move, max_eval
            
        else:
            min_eval = float("inf")
            for move in legal_moves:
                self.move_count += 1
                # if not self.is_legal(boards, move, color):
                #     continue
                board_to_move = game_state.get_proper_board(move.get_from_idx())
                board_to_clear = game_state.get_proper_board(move.get_to_idx())
                game_state.move(board_to_move, board_to_clear, move)
                # print(f"board after move:\n{BitBoard.print_board_2(self.get_b_board(boards_copies))}")
                _, current_eval = self.minimax(game_state, isMax=False, depth=depth-1, alpha=alpha, beta=beta)
                game_state.move(board_to_move, board_to_clear, move, undo=True)
                if current_eval < min_eval:
                    min_eval = current_eval
                    best_move = move
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break
            return best_move, min_eval
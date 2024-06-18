from Dragger import Dragger
from ChessEngine import GameState
from Piece import Piece, Pawn, Rook, Bishop, Knight, Queen, King
from Move import Move
import utils.check as check

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
    
    def is_terminal(self, board, color) -> bool:
        # king, row, col = self.find_king(board, color)
        if not self.get_all_moves(board, color):
            return True
        opp_color = self.opposite_color(color)
        # king, row, col = self.find_king(board, opp_color)
        if not self.get_all_moves(board, opp_color):
            return True
        return False

    def material(self, board: list[list[Piece]], color) -> int:
        score = 0
        material_count = {
            Pawn: 1,
            Knight: 3,
            Bishop: 3,
            Rook: 5,
            Queen: 9,
            King: 0
        }
        for row in range(8):
            for col in range(8):
                if board[row][col] != '--':
                    val = material_count[type(board[row][col])]
                    if color != board[row][col].color:
                        val *= -1
                    score += val
                
        return score

    ## Add/sub points for player in check, add more for checkmate
    def winning(self, board, color) -> int:
        opponent_color = self.opposite_color(color)
        score = 0
        # for row in range(8):
        #     for col in range(8):
        #         piece = board[row][col]
        #         if piece != "--":
        #             ##FIXME: Shouldn't ever need to do color check because we should never be able to make a move that puts ourself in checkmate
        #             if isinstance(piece, King):
        #                 valid_moves = piece.valid_moves(board, row, col)
        #                 if valid_moves == 0 and check.king_in_check(color, board):
        #                     print("I HAVE BEEN MATED")
        #                     return 10000 if piece.color == "white" else -10000
        if not self.get_all_moves(board, "black"):
            return -10000
        if not self.get_all_moves(board, "white"):
            return 10000
        
        ## if this move puts the opponent in check
        if check.king_in_check("white", board):
            print("I SHOULD USE THIS MOVE")
            score += 100
        elif check.king_in_check("black", board):
            score -= 100
        return score
        

    def evaluate(self, board, color) -> int:
        score = 0
        score += self.material(board, "black")
        score += self.winning(board, "black")
        return score

    def minimax(self, board: list[list], isMax, depth) -> tuple[Move, int]:
        self.nodes_visited += 1
        if isMax == True:
            color = self.color
        else:
            color = "white" if self.color == "black" else "black"
        
        
        if depth == 0 or self.is_terminal(board, color):
            return None, self.evaluate(board, color)
        # print(color)
        moves : list[Move] = self.get_all_moves(board, color)
        best_move = None
        if isMax:
            max_eval = -float("inf")
            for move in moves:
                prev_row, prev_col = move.get_initial()
                move_row, move_col = move.get_final()
                bcopy = self.dragger.simulate_drag_v2(board, prev_row=prev_row, prev_col=prev_col, move_row=move_row, move_col=move_col)
                _, current_eval = self.minimax(board=bcopy, isMax=False, depth=depth-1)
                if current_eval > max_eval:
                    max_eval = current_eval
                    best_move = move
            return best_move, max_eval
            
        else:
            min_eval = float("inf")
            for move in moves:
                prev_row, prev_col = move.get_initial()
                move_row, move_col = move.get_final()
                bcopy = self.dragger.simulate_drag_v2(board, prev_row=prev_row, prev_col=prev_col, move_row=move_row, move_col=move_col)
                _, current_eval = self.minimax(board=bcopy, isMax=True, depth=depth-1)
                if current_eval < min_eval:
                    min_eval = current_eval
                    best_move = move
            return best_move, min_eval
    
        
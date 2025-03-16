import pygame as p, os
from chess_engine import GameState
from dragger import Dragger
from move import Move
from ai.robot import Robot

# Size of board
WIDTH = HEIGHT = 512

# menu size
MENU_WIDTH = MENU_HEIGHT = 200

# Play again button dimensions
BUTTON_HEIGHT = 25
BUTTON_WIDTH = 100
# Dimensions of the board
DIMENSION = ROWS = COLS = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK',
              'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', "bQ"]
    for piece in pieces:
        dir = os.path.join(os.path.dirname(__file__), "images", piece + ".png")
        IMAGES[piece] = p.image.load(dir)
    # add promotion pieces
    promotion_pieces = [('promotewQ', 'wQ'), ('promotewR', 'wR'), ('promotewB', 'wB'), ('promotewN', 'wN'),
                        ('promotebQ', 'bQ'), ('promotebR', 'bR'), ('promotebB', 'bB'), ('promotebN', 'bN')]
    for piece, name in promotion_pieces:
        dir = os.path.join(os.path.dirname(__file__), "images", name + ".png")
        IMAGES[piece] = p.image.load(dir)

p.init()
canvas = p.display.set_mode((WIDTH, HEIGHT))
exit = False
loadImages()
game = GameState(canvas)
dragger: Dragger = Dragger()
start_time = float("inf")
promoting = False
game_over = False
holding_r = False
ai_color = 'black'
white_turn = True
illuminate_white = illuminate_black = False
use_ai = True


def main():
    global exit, white_turn
    valid_moves = []
    promotion_color = None
    promotion_square = -1
    promoting = False
    if use_ai:
        robot = Robot("black")
    while not exit:
        game.show_bg()
        game.load(IMAGES)

        if game.current_turn() == robot.color:
            move, _ = robot.minimax(game, True, 3, float("-inf"), float("inf"))
            game.move(game.get_proper_board(move.get_from_idx()), game.get_proper_board(move.get_to_idx()), move)
            print(f"I looked at {robot.move_count} moves")
        
        if dragger.is_dragging:
            game.show_valid_moves(dragger.old_idx, valid_moves)
            dragger.update_mouse(p.mouse.get_pos())
            dragger.update_blit(game.surface)


        if promoting:
            # Draw options for promotion
            game.show_promotion_options(promotion_color, IMAGES)
            

        # check for mouse/key events
        for event in p.event.get():
            if event.type == p.QUIT:
                exit = True


            if event.type == p.MOUSEBUTTONDOWN:
                posX, posY = p.mouse.get_pos()
                
                if promoting:
                    selected_piece = game.get_promotion_choice(posX, posY, not game.white_turn) #confusing but we switched turns technically
                    if selected_piece:
                        # Replace pawn with chosen piece
                        game.replace_pawn(dragger.new_idx, selected_piece)
                        promoting = False
                    continue

                idx = game.coord_to_idx(posX, posY)
                board = game.get_proper_board(idx)
                if board and ((board.color == "white" and game.white_turn) or (board.color == "black" and not game.white_turn)):
                    dragger.update_pos(board, idx)
                    dragger.update_mouse(p.mouse.get_pos())
                    dragger.piece.set_bit(dragger.old_idx) #TEMPORARY
                    valid_moves = game.get_valid_moves()
                    if len(valid_moves) == None:
                        print("White wins" if game.white_turn else "Black wins")
                        exit = True
                    dragger.piece.clear_bit(dragger.old_idx) #TEMPORARY

            if event.type == p.MOUSEBUTTONUP:
                if dragger.is_dragging:
                    posX, posY = p.mouse.get_pos()
                    new_idx = game.coord_to_idx(posX, posY)
                    old_idx = dragger.get_old_idx()
                    dragger.piece.set_bit(dragger.old_idx) #TEMPORARY
                    board_to_clear = game.get_proper_board(new_idx)
                    move_success = False

                    if (dragger.piece.name == "wp" and new_idx >= 56) or (dragger.piece.name == "bp" and new_idx <= 7):
                        promoting = True  # Set the flag to indicate we need to promote
                        promotion_color = 'w' if game.white_turn else 'b'

                    for move in valid_moves:
                        if move.get_from_idx() == old_idx and move.get_to_idx() == new_idx:
                            # if promoting:
                                # if not selected_piece or (move.get_flags() != selected_piece and move.get_flags() != selected_piece + 4):
                                #     continue
                            move_success = game.move(dragger.piece, board_to_clear, move)
                            break
                    if move_success:
                        dragger.drag(new_idx)
                    else:
                        print('failed')
                        dragger.piece.set_bit(dragger.old_idx)
                        dragger.reset()


        p.display.update()

main()




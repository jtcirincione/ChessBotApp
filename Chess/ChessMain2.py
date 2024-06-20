"""
Deals with user input
"""

import pygame as p
import ChessEngine
from Dragger2 import Dragger2
from Piece import Pawn
import yaml
import copy, os
from ai.Robot import Robot
from bitboards.PawnBoard import PawnBoard
from bitboards.BitBoard import BitBoard

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
'''
Load images initializes a global dict of images.
'''

config_path = os.path.join(os.path.dirname(__file__), 'config', 'settings.yml')
with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

use_ai = config['game_settings']['robot']
if use_ai:
    robot = Robot('black')


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


def restart(game, dragger: Dragger2, robot=None):
    start_time = 0
    game.reset()
    dragger.undrag()
    if robot:
        robot.reset()


p.init()
canvas = p.display.set_mode((WIDTH, HEIGHT))
exit = False

loadImages()
game = ChessEngine.GameState(canvas)
dragger = Dragger2()
start_time = float("inf")
promoting = False
game_over = False
holding_r = False
ai_color = 'black'
illuminate_white = illuminate_black = False


# white_pawn_board = PawnBoard("white")
black_pawn_board = PawnBoard("black")

print(f"Black pawn board: \n")
black_pawn_board.print_board()


while not exit:
    game.show_bg()
    if dragger.is_dragging:
        dragger.illuminate_moves(game.surface, game.board)
        dragger.update_blit(game.surface)
    game.load(IMAGES)
    if promoting:
        game.draw_promotions(piece=dragger.get_piece(), images=IMAGES)
    # end game if king is check mate'd
    if game_over:
        exit = True
    # TODO: If I am checked and cannot escape check, quit (for now)
    # if game.king_in_check(game.current_turn, game.board):
    #     pass

    if illuminate_white:
        dragger.illuminate_all_moves(canvas, game.board, "white")
    if illuminate_black:
        dragger.illuminate_all_moves(canvas, game.board, "black")

    # Robot logic
    if use_ai and game.current_turn() == robot.color and robot.choosing == False:
        print("should print once")
        robot.choosing = True
        bcopy = copy.deepcopy(game.board)
        move, _ = robot.minimax(game.board, True, 2)
        if not move:
            print("GGILOSE")
        strtr, strtc = move.get_initial()
        finr, finc = move.get_final()
        # print(f"start idx: {strtr}, {strtc}")
        # print(f"end idx: {finr}, {finc}")
        row, col = move.get_final()
        strt_idx = strtr * 8 + strtc
        dragger.oldIdx = strt_idx
        dragger.piece = game.get_pieces_board(strt_idx)
        game.board = dragger.drag(game.board, row, col)
        print(f"number of moves evaluated: {robot.nodes_visited - 1}")
        robot.nodes_visited = 0
        game.finish_turn()
    for event in p.event.get():
        if event.type == p.QUIT:
            exit = True

        if game.iam_checked():
            if not game.has_valid_moves(game.board, dragger):
                print(f"{game.opponent()} wins!")
                exit = True


        if event.type == p.MOUSEBUTTONDOWN:
            posX, posY = p.mouse.get_pos()
            col, row = game.coord_to_idx(posX, posY)

            if promoting:
                move_row, move_col = dragger.get_moved_location()
                promoting = game.promote(move_row=move_row, move_col=move_col,
                                         men_row=row, men_col=col, color=dragger.get_piece().color)
                if use_ai:
                    robot.choosing = False
                game.finish_turn()
                continue
            if not dragger.is_dragging:
                dragger.update_pos(game.board, row, col, game)
                dragger.update_mouse(p.mouse.get_pos())
            else:
                pass
        # Releasing move
        elif event.type == p.MOUSEBUTTONUP:
            posX, posY = p.mouse.get_pos()
            col, row = game.coord_to_idx(posX, posY)
            if dragger.is_dragging:
                valid_move = game.is_valid_move(piece=dragger.get_piece(
                ), board=game.board, init_row=dragger.prevRow, init_col=dragger.prevCol, move_row=row, move_col=col, canvas=game.surface)
                if valid_move:
                    if isinstance(dragger.get_piece(), Pawn):
                        # check if promotion move
                        if dragger.get_piece().promote_row == row:
                            # check here as if this move puts current player's king in check
                            # if so, undrag and continue
                            board_copy = dragger.simulate_drag(
                                game.board, row, col)
                            if game.king_in_check(dragger.get_piece().color, board_copy):
                                dragger.undrag()
                                continue
                            promoting = True
                            game.board = dragger.drag(game.board, row, col)
                            game.draw_promotions(
                                piece=dragger.get_piece(), images=IMAGES)
                            continue
                    # check if this move puts current player's king in check
                    # if so, undrag
                    tmp_board = dragger.simulate_drag(game.board, row, col)
                    if game.king_in_check(game.current_turn(), tmp_board):
                        # Here, check if there are any legal moves to get out of check
                        valid_moves = game.has_valid_moves(game.board, dragger)
                        if not valid_moves:
                            print(f"HOLY! {game.current_turn()} WINS!")
                            exit = True
                        dragger.undrag()
                        continue
                    game.board = dragger.drag(game.board, row, col)
                    new_idx = row * 8 + col
                    old_idx = dragger.oldIdx
                    dragger.drag2(game.get_proper_board(old_idx), new_idx)
                    # check if this move we just made puts opponent in check.
                    # if so, set opponent king to checked
                    game.king_in_check(
                        dragger.get_piece().opponent, game.board)
                    game.finish_turn()
                    if use_ai:
                        robot.choosing = False
                    dragger.undrag()
                # undo move for invalid
                else:
                    if game.king_in_check(game.current_turn(), game.board):
                        # TODO: Here, check if there are any legal moves to get out of check
                        valid_moves = game.has_valid_moves(game.board, dragger)
                        if not valid_moves:
                            exit = True
                        dragger.undrag()
                        continue
                    dragger.undrag()
                    continue
        # Dragging motion
        elif event.type == p.MOUSEMOTION:
            if dragger.is_dragging:
                game.show_bg()
                dragger.illuminate_moves(game.surface, game.board)
                game.load(IMAGES)
                dragger.update_mouse(p.mouse.get_pos())
                dragger.update_blit(game.surface)
            pass
        elif event.type == p.KEYDOWN:
            if event.key == p.K_r:
                start_time = p.time.get_ticks()
            # Debug to check if moves are added properly:
            if event.key == p.K_i:
                illuminate_white = True
            if event.key == p.K_o:
                illuminate_black = True
        elif event.type == p.KEYUP:
            if event.key == p.K_r:
                if p.time.get_ticks() - start_time >= 2000:
                    if use_ai:
                        restart(game, dragger, robot)
                    else:
                        restart(game, dragger)
                else:
                    start_time = 0
            if event.key == p.K_i:
                illuminate_white = False
            if event.key == p.K_o:
                illuminate_black = False
        
    p.display.update()

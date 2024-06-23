"""
Deals with user input
"""

import pygame as p
import ChessEngine
from Dragger2 import Dragger2
from Piece import Pawn
import yaml
import copy
import os
from ai.Robot import Robot
from bitboards.PawnBoard import PawnBoard
from bitboards.BitBoard import BitBoard
from enums.MoveType import MoveType

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
dragger: Dragger2 = Dragger2()
start_time = float("inf")
promoting = False
game_over = False
holding_r = False
ai_color = 'black'
illuminate_white = illuminate_black = False



## TODO: implement promotion logic
def handle_promotion():
    pass


def main():
    global exit, start_time, promoting, game_over, holding_r, ai_color, illuminate_white, illuminate_black
    def handle_castle():
        if game.current_turn() == "white":
            valid_castle = False
            if move_type == MoveType.CASTLE_LEFT:
                if not game.boards["wR"].left_rook_moved and game.boards["wR"].get_bit(56):
                    print('HI1')
                    # TODO: SINCE ROOK HASN'T MOVED, MOVE THE ROOK DURING CASTLE one space to right of king
                    game.boards["wR"].move_piece(
                        56, move.get_final_idx() + 1)
                    valid_castle = True
            if move_type == MoveType.CASTLE_RIGHT:
                if not game.boards["wR"].right_rook_moved and game.boards["wR"].get_bit(63):
                    print('HI2')
                    # TODO: SINCE ROOK HASN'T MOVED, MOVE THE ROOK DURING CASTLE one space to left of king
                    game.boards["wR"].move_piece(
                        63, move.get_final_idx() - 1)
                    valid_castle = True
        else:
            valid_castle = False
            if move_type == MoveType.CASTLE_LEFT:
                if not game.boards["bR"].left_rook_moved  and game.boards["bR"].get_bit(0):
                    ## TODO: SINCE ROOK HASN'T MOVED, MOVE THE ROOK DURING CASTLE one space to right of king
                    game.boards["bR"].move_piece(0, move.get_final_idx() + 1)
                    valid_castle = True
            if move_type == MoveType.CASTLE_RIGHT:
                if not game.boards["bR"].right_rook_moved  and game.boards["bR"].get_bit(7):
                    ## TODO: SINCE ROOK HASN'T MOVED, MOVE THE ROOK DURING CASTLE one space to left of king
                    game.boards["bR"].move_piece(7, move.get_final_idx() - 1)
                    valid_castle = True
        if not valid_castle:
            print("UNDO INVALID CASTLE")
            game.get_proper_board(new_idx).moved = False
            dragger.undo_drag(game.get_proper_board(new_idx), move, board_to_clear)
            return False
        return True
    while not exit:
        game.show_bg()
        if dragger.is_dragging:
            # print(type(dragger.piece_board))
            dragger.illuminate_moves(game.surface, game.get_current_player_board(), game.get_opponent_board(), game.history, game)
            dragger.update_blit(game.surface)
        game.load(IMAGES)
        if promoting:
            game.draw_promotions(piece=dragger.get_piece(), images=IMAGES)
        # end game if king is check mate'd
        if game_over:
            exit = True

        # if illuminate_white:
        #     dragger.illuminate_all_moves(canvas, game.board, "white")
        # if illuminate_black:
        #     dragger.illuminate_all_moves(canvas, game.board, "black")

        # Robot logic
        if use_ai and game.current_turn() == robot.color and robot.choosing == False:
            print("should print once")
            robot.choosing = True
            bcopy = copy.deepcopy(game.boards)
            hcopy = copy.deepcopy(game.history)
            move, _ = robot.minimax(bcopy, True, 1, hcopy)
            if not move:
                print("GGILOSE")
            init_idx = move.get_initial_idx()
            fin_idx =  move.get_final_idx()
            # print(f"start idx: {strtr}, {strtc}")
            # print(f"end idx: {finr}, {finc}")
            dragger.oldIdx = init_idx
            dragger.newIdx = fin_idx
            dragger.drag2(game.get_proper_board(init_idx), move, game.get_proper_board(fin_idx))
            print(f"number of moves evaluated: {robot.nodes_visited - 1}")
            robot.nodes_visited = 0
            game.finish_turn()
        for event in p.event.get():
            if event.type == p.QUIT:
                exit = True


            if event.type == p.MOUSEBUTTONDOWN:
                posX, posY = p.mouse.get_pos()
                col, row = game.coord_to_idx(posX, posY)

                if promoting:
                    move_idx = dragger.get_moved_location()
                    print(f"MOVED LOCATION: {move_idx}")
                    promoting = game.promote(move_idx=move_idx, men_row=row, men_col=col, color=dragger.get_piece().color)
                    if use_ai:
                        robot.choosing = False
                    # game.finish_turn()
                    continue
                if not dragger.is_dragging:
                    board = game.get_proper_board(row * 8 + col)
                    dragger.update_pos(board, row*8+col, game)
                    dragger.update_mouse(p.mouse.get_pos())
                else:
                    pass
            # Releasing move
            elif event.type == p.MOUSEBUTTONUP:
                posX, posY = p.mouse.get_pos()
                col, row = game.coord_to_idx(posX, posY)
                new_idx = row * 8 + col
                if dragger.is_dragging:
                    if use_ai:
                        robot.choosing = False
                    old_idx = dragger.oldIdx
                    board_to_clear = game.get_proper_board(new_idx)
                    board_to_move = game.get_proper_board(old_idx)
                    moves = dragger.get_pseudo_moves(board_to_move, new_idx, game.get_current_player_board(), game.get_opponent_board(), game.history, board_to_clear)
                    legal_moves = game.get_legal_moves(moves, game.current_turn())
                    move = None
                    for mv in legal_moves:
                        if new_idx == mv.get_final_idx():
                            move = mv
                    if move is None:
                        dragger.undrag()
                        continue
                    dragger.drag2(game.get_proper_board(old_idx), move, board_to_clear)
                    move_type = move.get_move_type()
                    if move_type == MoveType.EN_PASSANT_CAPTURE:
                        if game.current_turn() == "white":
                            idx = new_idx + 8
                            prop_board = game.get_proper_board(idx)
                        else:
                            idx = new_idx - 8
                            prop_board = game.get_proper_board(idx)
                        if prop_board != 0:
                            prop_board.clear_bit(idx)
                    if move_type == MoveType.CASTLE_LEFT or move_type == MoveType.CASTLE_RIGHT:
                        if not handle_castle():
                            continue
                    if move_type == MoveType.PROMOTE:
                        print('PLEASE PRINT')
                        promoting = True
                    dragger.undrag()
                    game.history.append(move)
                    game.finish_turn()
                    if game.in_checkmate(game.current_turn()):
                        print(f"{game.opponent()} wins!")
                        exit = True
                    # undo move for invalid
            # Dragging motion
            elif event.type == p.MOUSEMOTION:
                if dragger.is_dragging:
                    game.show_bg()
                    dragger.illuminate_moves(game.surface, game.get_current_player_board(), game.get_opponent_board(), game.history, game)
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

main()
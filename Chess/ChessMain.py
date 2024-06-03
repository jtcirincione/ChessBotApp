"""
Deals with user input
"""

import pygame as p
import ChessEngine
from Dragger import Dragger
from Piece import Pawn

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


def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK',
              'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', "bQ"]
    for piece in pieces:
        IMAGES[piece] = p.image.load("images/" + piece + ".png")
    # add promotion pieces
    promotion_pieces = [('promotewQ', 'wQ'), ('promotewR', 'wR'), ('promotewB', 'wB'), ('promotewN', 'wN'),
                        ('promotebQ', 'bQ'), ('promotebR', 'bR'), ('promotebB', 'bB'), ('promotebN', 'bN')]
    for piece, name in promotion_pieces:
        IMAGES[piece] = p.image.load("images/" + name + ".png")

def restart(game, dragger):
    start_time = 0
    game.reset()
    dragger.undrag()
p.init()
canvas = p.display.set_mode((WIDTH, HEIGHT))
exit = False

loadImages()
game = ChessEngine.GameState(canvas)
dragger = Dragger()
start_time = float("inf")
promoting = False
game_over = False
holding_r = False
while not exit:
    game.show_bg()
    game.load(IMAGES)
    if promoting:
        game.draw_promotions(piece=dragger.get_piece(), images=IMAGES)
    # end game if king is check mate'd
    if game_over:
        exit = True
    ##TODO: If I am checked and cannot escape check, quit (for now)
    # if game.king_in_check(game.current_turn, game.board):
    #     pass
    for event in p.event.get():
        if event.type == p.QUIT:
            exit = True

        if game.iam_checked():
            if not game.has_valid_moves(game.board, dragger):
                print("woooo")

        if event.type == p.MOUSEBUTTONDOWN:
            posX, posY = p.mouse.get_pos()
            col, row = game.coord_to_idx(posX, posY)

            # TODO: if I am in check, restrict any moves but moves that put the king out of check
            if promoting and game.king_in_check(game.current_turn, game.board) == False:
                move_row, move_col = dragger.get_moved_location()
                promoting = game.promote(move_row=move_row, move_col=move_col,
                                         men_row=row, men_col=col, color=dragger.get_piece().color)
                # TODO: check if this promotion puts opponent king in check
                game.finish_turn()
                continue
            if not dragger.is_dragging:
                dragger.update_pos(game.board, row, col, game)
            else:
                valid_move = game.is_valid_move(piece=dragger.get_piece(
                ), board=game.board, init_row=dragger.prevRow, init_col=dragger.prevCol, move_row=row, move_col=col, canvas=game.surface)
                if valid_move:
                    if isinstance(dragger.get_piece(), Pawn):
                        # check if promotion move
                        if dragger.get_piece().promote_row == row:
                            print("PROMOTING")
                            # TODO: check here as well if this move puts current player's king in check
                            # if so, undrag and continue
                            board_copy = dragger.simulate_drag(
                                game.board, row, col)
                            if game.king_in_check(dragger.get_piece().color, board_copy):
                                pass
                            promoting = True
                            game.board = dragger.drag(game.board, row, col)
                            game.draw_promotions(
                                piece=dragger.get_piece(), images=IMAGES)
                            continue
                    # TODO: check if this move puts current player's king in check
                    # if so, undrag
                    tmp_board = dragger.simulate_drag(game.board, row, col)
                    if game.king_in_check(game.current_turn(), tmp_board):
                        ##TODO: Here, check if there are any legal moves to get out of check
                        valid_moves = game.has_valid_moves(game.board, dragger)
                        if not valid_moves:
                            print(f"HOLY! {game.current_turn} WINS!")
                            exit = True
                        dragger.undrag()
                        continue
                    game.board = dragger.drag(game.board, row, col)
                    # TODO: check if this move we just made puts opponent in check.
                    # if so, set opponent king to checked
                    game.king_in_check(dragger.get_piece().opponent, game.board)
                    game.finish_turn()
                    dragger.undrag()
                # undo move for invalid
                else:
                    if game.king_in_check(game.current_turn(), game.board):
                        ##TODO: Here, check if there are any legal moves to get out of check
                        valid_moves = game.has_valid_moves(game.board, dragger)
                        if not valid_moves:
                            exit = True
                        dragger.undrag()
                        continue
                    dragger.undrag()
                    continue

        elif event.type == p.KEYDOWN:
            if event.key == p.K_r:
                start_time = p.time.get_ticks()
        elif event.type == p.KEYUP:
            if event.key == p.K_r:
                if p.time.get_ticks() - start_time >= 2000:
                        restart(game, dragger)
                else:
                    start_time = 0

                
    p.display.update()

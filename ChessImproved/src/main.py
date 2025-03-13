import pygame as p, os
from chess_engine import GameState
from dragger import Dragger
from move import Move


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


def main():
    global exit, white_turn
    valid_moves = []
    while not exit:
        game.show_bg()
        game.load(IMAGES)
        
        if dragger.is_dragging:
            game.show_valid_moves(dragger.old_idx, valid_moves)
            dragger.update_mouse(p.mouse.get_pos())
            dragger.update_blit(game.surface)



        # check for mouse/key events
        for event in p.event.get():
            if event.type == p.QUIT:
                exit = True


            if event.type == p.MOUSEBUTTONDOWN:
                posX, posY = p.mouse.get_pos()
                idx = game.coord_to_idx(posX, posY)
                board = game.get_proper_board(idx)
                if board and ((board.color == "white" and white_turn) or (board.color == "black" and not white_turn)):
                    dragger.update_pos(board, idx)
                    dragger.update_mouse(p.mouse.get_pos())
                    dragger.piece.set_bit(dragger.old_idx) #TEMPORARY
                    valid_moves = game.get_valid_moves(white_turn)
                    dragger.piece.clear_bit(dragger.old_idx) #TEMPORARY

            if event.type == p.MOUSEBUTTONUP:
                if dragger.is_dragging:
                    posX, posY = p.mouse.get_pos()
                    new_idx = game.coord_to_idx(posX, posY)
                    old_idx = dragger.get_old_idx()
                    dragger.piece.set_bit(dragger.old_idx) #TEMPORARY
                    board_to_clear = game.get_proper_board(new_idx)
                    move_success = False

                    for move in valid_moves:
                        if move.get_from_idx() == old_idx and move.get_to_idx() == new_idx:
                            move_success = game.move(dragger.piece, board_to_clear, move, False)
                            break
                    if move_success:
                        dragger.drag(new_idx)
                        white_turn = not white_turn
                    else:
                        print('failed')
                        dragger.piece.set_bit(dragger.old_idx)
                        dragger.reset()


        p.display.update()

main()




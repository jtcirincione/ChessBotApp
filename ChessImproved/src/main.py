import pygame as p, os
from chess_engine import GameState
from dragger import Dragger


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
    global exit
    while not exit:
        game.show_bg()
        game.load(IMAGES)
        if dragger.dragging:
            game.show_valid_moves(white_turn)



        # check for mouse/key events
        for event in p.event.get():
            if event.type == p.QUIT:
                exit = True


            if event.type == p.MOUSEBUTTONDOWN:
                posX, posY = p.mouse.get_pos()
                idx = game.coord_to_idx(posX, posY)
                board = game.get_proper_board(idx, white_turn)
                dragger.update_pos(board, idx)
                dragger.update_mouse(p.mouse.get_pos())


        p.display.update()

main()




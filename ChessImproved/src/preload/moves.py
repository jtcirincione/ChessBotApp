import os
def generate_knight_moves():
    if os.path.exists(os.path.curdir.join("data/moves.pickle")):
        return
    
    
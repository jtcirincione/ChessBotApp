import os, numpy as np
def generate_knight_moves():
    if os.path.exists(os.path.curdir.join("data/moves.pickle")):
        return

"""
Generates a mask for rook at given index of empty board

used for magics
"""
def generate_rook_masks(idx):
    mask = np.uint64(0)
    rank = idx // 8
    file = idx % 8

    #vertical moves
    for i in range(rank + 1, 7): # Exclude board edges
         mask |= np.uint64(1) << (63 - (r * 8 + file))
    for r in range(rank - 1, 0, -1):  # Exclude board edges
        mask |= np.uint64(1) << (r * 8 + file)

    
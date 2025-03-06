import os, numpy as np
def generate_knight_moves():
    if os.path.exists(os.path.curdir.join("data/moves.pickle")):
        return

"""
Generates a mask for rook at given index of empty board

used for magics
"""
def generate_rook_mask(idx):
    mask = np.uint64(0)
    rank = idx // 8
    file = idx % 8

    #vertical moves
    for r in range(rank + 1, 7): # Exclude board edges
         mask |= np.uint64(1) << np.uint64(r * 8 + file)
    for r in range(rank - 1, 0, -1):  # Exclude board edges
        mask |= np.uint64(1) << np.uint64(r * 8 + file)

    #horizontal moves
    for f in range(file + 1, 7):
        mask |= np.uint64(1) << np.uint64(rank*8 + f)
    for f in range (file -1, 0, -1):
        mask |= np.uint64(1) << np.uint64(rank*8 + f)
    
    return mask

def generate_rook_masks():
    return [generate_rook_mask(idx) for idx in range(64)]


"""
Generates a mask for bishop at given index of empty board

used for magics
"""
def generate_bishop_mask(idx):
    mask = np.uint64(0)
    rank = idx // 8
    file = idx % 8
    # Diagonal (↗ and ↙)
    for i in range(1, 7):
        if rank + i < 7 and file + i < 7:
            mask |= np.uint64(1) << np.uint64((rank + i) * 8 + (file + i))
        if rank - i > 0 and file - i > 0:
            mask |= np.uint64(1) << np.uint64((rank - i) * 8 + (file - i))

    # Anti-diagonal (↖ and ↘)
    for i in range(1, 7):
        if rank + i < 7 and file - i > 0:
            mask |= np.uint64(1) << np.uint64((rank + i) * 8 + (file - i))
        if rank - i > 0 and file + i < 7:
            mask |= np.uint64(1) << np.uint64((rank - i) * 8 + (file + i))

    return mask

def generate_bishop_masks():
    return [generate_bishop_mask(idx) for idx in range(64)]



def generate_blocker_variations(mask: int):
    """Generates all possible blocker variations within the attack mask."""
    bits = [i for i in range(64) if (mask & np.uint64(1 << i)) != 0]
    num_bits = len(bits)
    blockers = []

    # Generate all subsets of blockers
    for i in range(2**num_bits):
        subset = np.uint64(0)
        for j in range(num_bits):
            if (i & (1 << j)) != 0:
                subset |= np.uint64(1) << np.uint64(bits[j])
        blockers.append(subset)
    
    return blockers


def compute_rook_attacks(square: int, blockers: int):
    """Computes actual attack set for a given blocker configuration."""
    attacks = 0

    rank = square // 8
    file = square % 8

    # Horizontal Moves
    for f in range(file + 1, 8):
        attacks |= (1 << np.uint64(rank * 8 + f))
        if blockers & (1 << np.uint64(rank * 8 + f)):  # Stop at blocker
            break
    for f in range(file - 1, -1, -1):
        attacks |= (np.uint64(1) << np.uint64(rank * 8 + f))
        if blockers & (np.uint64(1) << np.uint64(rank * 8 + f)):
            break

    # Vertical Moves
    for r in range(rank + 1, 8):
        attacks |= (np.uint64(1) << np.uint64(r * 8 + file))
        if blockers & (np.uint64(1) << np.uint64(r * 8 + file)):
            break
    for r in range(rank - 1, -1, -1):
        attacks |= (np.uint64(1) << np.uint64(r * 8 + file))
        if blockers & (np.uint64(1) << np.uint64(r * 8 + file)):
            break

    return attacks
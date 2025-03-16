import os, numpy as np, random, warnings, time, json

NOT_H_MASK = np.uint64(
    0b0111111101111111011111110111111101111111011111110111111101111111)
NOT_A_MASK = np.uint64(
    0b1111111011111110111111101111111011111110111111101111111011111110)

filename = "magics.json"

def static_get_bit(board, idx) -> int:
        if not (0 <= idx < 64):
            raise Exception("Square must be from 0 to 63")
        return (board >> np.uint64(idx)) & np.uint64(1)

def static_print(board):
        for rank in range(7, -1, -1):
            for file in range(0, 8):
                if not file:
                    print(rank + 1, end="  ")
                square = rank * 8 + file
                print(static_get_bit(board, idx=square), end=" ")
            print()
        
        print("\n   A B C D E F G H\n\n", end="")

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


ROOK_MASKS = generate_rook_masks()

BISHOP_MASKS = generate_bishop_masks()


def generate_blocker_variations(mask: int):
    """Generates all possible blocker variations within the attack mask."""
    bits = [i for i in range(64) if (mask & np.uint64(1 << i)) != 0]
    num_bits = len(bits)
    blockers = []
    # Generate all subsets of blockers
    for i in range(2**num_bits):
        subset = np.uint64(0)
        for j in range(num_bits):
            if (np.uint64(i) & (np.uint64(1) << np.uint64(j))) != 0:
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
        attacks |= (np.uint64(1) << np.uint64(rank * 8 + f))
        if blockers & (np.uint64(1) << np.uint64(rank * 8 + f)):  # Stop at blocker
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


def compute_bishop_attacks(square: int, blockers: int):
    """Computes actual attack set for a given blocker configuration."""
    attacks = 0
    rank = square // 8
    file = square % 8

    # Diagonal (↗ and ↙)
    for r in range(1, 8):
        if rank + r < 8 and file + r < 8:
            attacks |= (np.uint64(1) << np.uint64((rank + r) * 8 + (file + r)))
            if blockers & (np.uint64(1) << np.uint64((rank + r) * 8 + (file + r))):
                break
    for r in range(1, 8):
        if rank - r >= 0 and file - r >= 0:
            attacks |= (np.uint64(1) << np.uint64((rank - r) * 8 + (file - r)))
            if blockers & (np.uint64(1) << np.uint64((rank - r) * 8 + (file - r))):
                break

    # Anti-diagonal (↖ and ↘)
    for r in range(1, 8):
        if rank + r < 8 and file - r >= 0:
            attacks |= (np.uint64(1) << np.uint64((rank + r) * 8 + (file - r)))
            if blockers & (np.uint64(1) << np.uint64((rank + r) * 8 + (file - r))):
                break
    for r in range(1, 8):
        if rank - r >= 0 and file + r < 8:
            attacks |= (np.uint64(1) << np.uint64((rank - r) * 8 + (file + r)))
            if blockers & (np.uint64(1) << np.uint64((rank - r) * 8 + (file + r))):
                break

    return attacks


def compute_pawn_attacks():
    """
    Returns a tuple (white, black) of precomputed white and black pawn attacks
    white: array where idx is the square for white attack
    black: array where idx is the square for black attack
    """
    whites = []
    blacks = []
    for square in range(64):
        wattack_squares = np.uint64(0)
        battack_squares = np.uint64(0)
        pawn = np.uint64(np.uint64(1) << np.uint64(square))
        wattack_squares |= (pawn << 9) & NOT_A_MASK ## right attack
        wattack_squares |= (pawn << 7) & NOT_H_MASK ## left attack

        battack_squares |= (pawn >> 7) & NOT_A_MASK ## right attack
        battack_squares |= (pawn >> 9) & NOT_H_MASK ## left attack

        whites.append(wattack_squares)
        blacks.append(battack_squares)
    return whites, blacks


def find_magic_number(square, is_rook):
    """
    Finds a magic number for the given square for either rooks or bishops.
    """

    # Step 1: Generate mask for the piece
    mask = ROOK_MASKS[square] if is_rook else BISHOP_MASKS[square]
    print("finding magics")
    # Step 2: Generate all possible blocker variations
    blocker_variations = generate_blocker_variations(mask)
    print("done generating blockers")
    # Step 3: Compute all corresponding attack sets
    attack_sets = {}
    for blockers in blocker_variations:
        attack = compute_rook_attacks(square, blockers) if is_rook else compute_bishop_attacks(square, blockers)
        attack_sets[blockers] = attack

    print("done computing attacks")
    num_relevant_bits = bin(mask).count("1")  # Number of bits needed for unique indexing
    print(bin(mask))
    print(f"relevant bits: {num_relevant_bits}")

    start_time = time.process_time()
    # Step 4: Find a magic number by trial and error
    while True:
        magic = np.uint64(random.getrandbits(64) & random.getrandbits(64) & random.getrandbits(64))  # Random number with low bits cleared
        lookup_table = {}

        success = True
        for blockers in blocker_variations:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=RuntimeWarning)
                index = (blockers * magic) >> np.uint64(64 - num_relevant_bits)
            if index in lookup_table and lookup_table[index] != attack_sets[blockers]:
                collision_info = [(blockers, index)]
                success = False
                break
            lookup_table[index] = attack_sets[blockers]

        if success:
            end_time = time.process_time()
            print(f"magic found for idx: {square} in {end_time - start_time} seconds")
            return magic  # Found a working magic number

def generate_all_magics():
    rook_magics = [find_magic_number(square, is_rook=True) for square in range(64)]
    # rook_magics = [0]
    bishop_magics = [find_magic_number(square, is_rook=False) for square in range(64)]
    return rook_magics, bishop_magics

if not os.path.exists(os.path.join(os.curdir, "preload/data/magics.json")):
    rook_magics, bishop_magics = generate_all_magics()
    rook_magics_hex = [hex(magic) for magic in rook_magics]
    bishop_magics_hex = [hex(magic) for magic in bishop_magics]

    # Saving to JSON
    with open("preload/data/magics.json", 'w') as f:
        json.dump({
            "rook_magics": rook_magics_hex,
            "bishop_magics": bishop_magics_hex
        }, f, indent=4)
else:
    with open("preload/data/magics.json", 'r') as f:
        tables = json.load(f)

    # Convert hex strings back to np.uint64
    rook_magics = [np.uint64(int(magic, 16)) for magic in tables['rook_magics']]
    bishop_magics = [np.uint64(int(magic, 16)) for magic in tables['bishop_magics']]

rook_attack_table = {}
bishop_attack_table = {}



def generate_magic_lookup_table(is_rook):
    """
    Precomputes and stores all attack tables for rooks and bishops.
    """
    for square in range(64):
        if not is_rook and str(square) not in bishop_attack_table:
            bishop_attack_table[str(square)] = {}
        if is_rook and str(square) not in rook_attack_table:
            rook_attack_table[str(square)] = {}
        magic = rook_magics[square] if is_rook else bishop_magics[square]
        mask = ROOK_MASKS[square] if is_rook else BISHOP_MASKS[square]
        blocker_variations = generate_blocker_variations(mask)

        for blockers in blocker_variations:
            attack = compute_rook_attacks(square, blockers) if is_rook else compute_bishop_attacks(square, blockers)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=RuntimeWarning)
                index = (blockers * magic) >> np.uint64(64 - len(blocker_variations).bit_length())  # Magic hash
            if is_rook:
                rook_attack_table[str(square)][str(index)] = attack
            else:
                bishop_attack_table[str(square)][str(index)] = attack



def get_rook_attacks(square, blockers):
    """Retrieves rook attacks using magic bitboards."""
    magic = rook_magics[square]
    mask = ROOK_MASKS[square]
    relevant_blockers = np.uint64(blockers) & mask  # Only consider relevant blockers
    index = (relevant_blockers * magic) >> np.uint64(64 - len(rook_attack_table[str(square)]).bit_length())
    return rook_attack_table[str(square)][str(index)]

def get_bishop_attacks(square, blockers):
    """Retrieves bishop attacks using magic bitboards."""
    magic = bishop_magics[square]
    mask = BISHOP_MASKS[square]

    relevant_blockers = np.uint64(blockers) & mask  # Only consider relevant blockers
    index = (relevant_blockers * magic) >> np.uint64(64 - len(bishop_attack_table[str(square)]).bit_length())
    return bishop_attack_table[str(square)][str(index)]

def get_queen_attacks(square, blockers):
    diagonals = get_bishop_attacks(square, blockers)
    nsew = get_rook_attacks(square, blockers)
    return diagonals | nsew

generate_magic_lookup_table(False)
generate_magic_lookup_table(True)
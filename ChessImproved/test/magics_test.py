import pytest, numpy as np
import preload.moves as magics


def test_get_bishop_attacks():
    blockers = np.uint64(0b0000000011111111000000000000000000000000000000000000000000000000)
    att = magics.get_bishop_attacks(42, blockers)
    magics.static_print(blockers)
    magics.static_print(att)

    assert att==2

# def test_blocker_generation():
#     forty2_attack = np.uint64(0b0000000000001010000000000000101000010000001000000100000000000000)
#     magics.static_print(forty2_attack)
#     generate_blocker_variations(forty2_attack)
#     assert 2 == 3

# def generate_blocker_variations(mask: int):
#     """Generates all possible blocker variations within the attack mask."""
#     bits = [i for i in range(64) if (mask & np.uint64(1 << i)) != 0]
#     num_bits = len(bits)
#     blockers = []
#     # magics.static_print(mask)
#     # Generate all subsets of blockers
#     for i in range(2**num_bits):
#         subset = np.uint64(0)
#         for j in range(num_bits):
#             if (np.uint64(i) & (np.uint64(1) << np.uint64(j))) != 0:
#                 subset |= np.uint64(1) << np.uint64(bits[j])
#         magics.static_print(subset)
#         blockers.append(subset)
    
#     return blockers
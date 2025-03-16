import pytest, numpy as np
import preload.moves as magics


def test_get_bishop_attacks():
    blockers = np.uint64(0b0000000011111000000000000000000000000000000000000000000000000000)
    att = magics.get_rook_attacks(42, blockers)
    magics.static_print(blockers)
    magics.static_print(att)

    assert att==2
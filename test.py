import numpy as np
# def print_move(move):
#         print(f"encoded: {move}")
#         from_move = move & 0x3F
#         to_move = (move >> 6) & 0x3F
#         flag = move >> 12

#         print(f"decoded: \nfrom: {from_move}\nto: {to_move}\nflag: {flag}")

# def create_move(frum: np.uint, to, flags):
#         return (np.uint16(flags) << 12) | (np.uint16(to) << 6) | (np.uint16(frum))

# print_move(create_move(63,24,7))

def bit_scan_forward(bitboard: np.uint64) -> int:
    """Returns the index of the least significant bit (LSB) in the bitboard."""
    bitboard = int(bitboard)  # Convert to Python int to avoid overflow
    return (bitboard & -bitboard).bit_length() - 1

# Test with a bitboard where only one bit is set
bitboard = np.uint64(0b1001000)  # Binary: 0b1001000 (Decimal: 72)
print(bit_scan_forward(bitboard))  # Expected output: 3
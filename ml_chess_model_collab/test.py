import ast
import struct
import numpy as np

def fen_to_binary(fen):
    """
    Convert FEN string to 808-bit (101 byte) binary format.
    """
    # Initialize 101 bytes of zeros
    output = [0] * 101
    
    # Split FEN into its components
    parts = fen.split()
    if len(parts) != 6:
        raise ValueError("Invalid FEN string. Must contain 6 components.")
    
    board, active_color, castling, en_passant, halfmove, fullmove = parts
    
    print(board)
    print(active_color)
    print(castling)
    print(en_passant)
    print(halfmove)
    print(fullmove)

    # Updated piece mappings based on the example output
    piece_to_bits = {
        'r': 0x08,  # Black rook
        'n': 0x10,  # Black knight
        'b': 0x81,  # Black bishop
        'q': 0x24,  # Black queen
        'k': 0x42,  # Black king
        'p': 0xef,  # Black pawn
        'R': 0x08,  # White rook
        'N': 0x10,  # White knight
        'B': 0x81,  # White bishop
        'Q': 0x24,  # White queen
        'K': 0x42,  # White king
        'P': 0xcf,  # White pawn (different value than black pawn)
    }
    
    # Process board position
    square_index = 0
    for row in board.split('/'):
        for char in row:
            if char.isdigit():
                # Skip empty squares
                square_index += int(char) * 8  # Each square is 8 bytes
            else:
                # Place piece
                if square_index < len(output):
                    output[square_index] = piece_to_bits.get(char, 0)
                    # Special handling for second byte after piece
                    if char in ['P', 'p']:
                        output[square_index + 1] = 0x00
                    square_index += 8



    # Set metadata at the end (last 5 bytes)
    
    
    return bytes(output)

def bit_conversion(bytes_value):
  bin = np.frombuffer(bytes_value, dtype=np.uint8)
  bin = np.unpackbits(bin, axis=0).astype(np.single)
  return bin

# Example usage
fen_string = "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq d3 0 1"

binary_output = fen_to_binary(fen_string)
bited = bit_conversion(binary_output)

bytes = b'\x08\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x81\x00\x00\x00\x00\x00\x00\x00$\x00\x00\x00\x00\x00\x00\x00B\x00\x00\x00\x00\x00\x00\x00\x00\xef\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x81\x00\x00\x00\x00\x00\x00\x00$\x00\x00\x00\x00\x00\x00\x00B\x00\x00\x00\x00\x00\x00\xff\x00\x00\x00\x01\x13?'
bited2 = bit_conversion(bytes)

print(len(bited))
print(len(bited2))

print(bited == bited2)

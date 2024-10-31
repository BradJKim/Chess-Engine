import numpy as np


def fen_to_bitboard(fen):
    # Initialize bitboards
    bitboards = {
        'P': 0,  # White pawn
        'N': 0,  # White knight
        'B': 0,  # White bishop
        'R': 0,  # White rook
        'Q': 0,  # White queen
        'K': 0,  # White king
        'p': 0,  # Black pawn
        'n': 0,  # Black knight
        'b': 0,  # Black bishop
        'r': 0,  # Black rook
        'q': 0,  # Black queen
        'k': 0,  # Black king
    }

    # Split the FEN into components
    parts = fen.split()
    if len(parts) != 6:
        raise ValueError("Invalid FEN string. Must contain 6 components.")
    
    board, active_color, castling, en_passant, halfmove, fullmove = parts

    # Process the board position
    square_index = 0
    for char in board:
        if char == '/':
            continue
        if char.isdigit():
            square_index += int(char)  # Skip empty squares
        else:
            # Set the appropriate bit for the piece
            bitboards[char] |= (1 << (63 - square_index))
            square_index += 1

    # Prepare metadata
    metadata = 0
    # Color to move (1 bit)
    metadata |= (1 if active_color == 'b' else 0)  # 0 for White, 1 for Black
    # Castling rights (4 bits)
    if 'K' in castling:
        metadata |= 0x1  # White kingside
    if 'Q' in castling:
        metadata |= 0x2  # White queenside
    if 'k' in castling:
        metadata |= 0x4  # Black kingside
    if 'q' in castling:
        metadata |= 0x8  # Black queenside
    # En passant (6 bits)
    if en_passant != '-':
        file_num = ord(en_passant[0]) - ord('a')  # a=0, b=1, ...
        rank_num = 8 - int(en_passant[1])  # 8=0, 1=7, ...
        metadata |= (rank_num << 4) | file_num
    else:
        metadata |= 0x3F  # No en passant available
    # Halfmove (8 bits)
    metadata |= min(int(halfmove), 255) << 10
    # Fullmove (8 bits)
    metadata |= min(int(fullmove), 255) << 18

    # Combine the bitboards and metadata into bytes
    byte_array = bytearray()
    for piece in ['P', 'N', 'B', 'R', 'Q', 'K', 'p', 'n', 'b', 'r', 'q', 'k']:
        byte_array.extend(bitboards[piece].to_bytes(8, byteorder='big'))

    # Add metadata bytes
    byte_array.extend(metadata.to_bytes(5, byteorder='big'))  # 5 bytes for metadata

    return bytes(byte_array)

def bit_conversion(bytes_value):
  bin = np.frombuffer(bytes_value, dtype=np.uint8)
  bin = np.unpackbits(bin, axis=0).astype(np.single)
  return bin

# Example usage:
fen = "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 1"
bitboard_bytes = fen_to_bitboard(fen)
bits = bit_conversion(bitboard_bytes)
bytes = b'\x08\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x81\x00\x00\x00\x00\x00\x00\x00$\x00\x00\x00\x00\x00\x00\x00B\x00\x00\x00\x00\x00\x00\x00\x00\xef\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x81\x00\x00\x00\x00\x00\x00\x00$\x00\x00\x00\x00\x00\x00\x00B\x00\x00\x00\x00\x00\x00\xff\x00\x00\x00\x01\x13?'

print(bits == bit_conversion(bytes))

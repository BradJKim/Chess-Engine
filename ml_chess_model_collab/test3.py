def bitboard_to_fen(bitboards, metadata):
    # Initialize an empty board representation
    board = ['8'] * 8  # Start with 8 empty ranks
    
    # Build the board from the bitboards
    for piece, bitboard in bitboards.items():
        for square in range(64):
            if (bitboard >> (63 - square)) & 1:
                rank = square // 8
                file = square % 8
                
                # Update the board representation
                if board[rank] == '8':
                    board[rank] = ''  # Start building the rank
                board[rank] += piece  # Add the piece
                
                # If it’s a piece, check if there are any empty squares before it
                empty_count = (square % 8) - len(board[rank])
                if empty_count > 0:
                    board[rank] = str(empty_count) + board[rank]  # Count empty squares

    # Join the board ranks and reverse to match the FEN format
    board_fen = '/'.join(reversed(board))

    # Extract metadata
    # Active color (1 bit)
    active_color = 'w' if (metadata & 1) == 0 else 'b'
    
    # Castling rights (4 bits)
    castling = ''
    if (metadata >> 1) & 1:  # White kingside
        castling += 'K'
    if (metadata >> 2) & 1:  # White queenside
        castling += 'Q'
    if (metadata >> 3) & 1:  # Black kingside
        castling += 'k'
    if (metadata >> 4) & 1:  # Black queenside
        castling += 'q'

    # En passant (6 bits)
    en_passant = '-'
    ep_square = (metadata >> 5) & 0x3F  # Get the en passant bits
    if ep_square < 64:
        file = ep_square % 8
        rank = 8 - (ep_square // 8 + 1)  # Convert to rank (0-7)
        en_passant = f"{chr(file + ord('a'))}{rank + 1}"  # Convert to algebraic notation

    # Halfmove and fullmove (8 bits each)
    halfmove = (metadata >> 11) & 0xFF
    fullmove = (metadata >> 19) & 0xFF

    # Construct the final FEN string
    fen = f"{board_fen} {active_color} {castling if castling else '-'} {en_passant} {halfmove} {fullmove}"

    return fen


# Example bitboards and metadata
bitboards = {
    'P': 0x00FF000000000000,  # White pawns
    'N': 0x0000000000000042,  # White knights
    'B': 0x000000000000001C,  # White bishops
    'R': 0x0000000000000081,  # White rooks
    'Q': 0x0000000000000024,  # White queen
    'K': 0x0000000000000042,  # White king
    'p': 0xFF00000000000000,  # Black pawns
    'n': 0x0000000000000020,  # Black knights
    'b': 0x0000000000000010,  # Black bishops
    'r': 0x0000000000000080,  # Black rooks
    'q': 0x0000000000000000,  # Black queen
    'k': 0x0000000000000040,  # Black king
}

# Example metadata, assume:
# - White to move
# - Castling: KQkq
# - En passant: None
# - Halfmove: 0
# - Fullmove: 1
metadata = b'\x08\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x81\x00\x00\x00\x00\x00\x00\x00$\x00\x00\x00\x00\x00\x00\x00B\x00\x00\x00\x00\x00\x00\x00\x00\xef\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x81\x00\x00\x00\x00\x00\x00\x00$\x00\x00\x00\x00\x00\x00\x00B\x00\x00\x00\x00\x00\x00\xff\x00\x00\x00\x01\x13?'

# Convert back to FEN
fen_result = bitboard_to_fen(bitboards, metadata)
print(fen_result)

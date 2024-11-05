def fen_to_binary(fen):
    """
    Convert chess FEN notation to binary representation.

    Args:
        fen (str): FEN string in format like 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1'

    Returns:
        dict: Dictionary containing binary representations of different FEN components
    """
    # Split FEN into its components
    parts = fen.split()
    board_str, active_color, castling, en_passant, halfmove, fullmove = parts
    bin = []

    # Convert piece positions to binary
    piece_mapping = {
        'p': [0,0,0,0,0,1], 'P': [0,0,0,0,1,0],
        'n': [0,0,0,0,1,1], 'N': [0,0,0,1,0,0],
        'b': [0,0,0,1,0,1], 'B': [0,0,0,1,1,0],
        'r': [0,0,0,1,1,1], 'R': [0,0,1,0,0,0],
        'q': [0,0,1,0,0,1], 'Q': [0,0,1,0,1,0],
        'k': [0,0,1,0,1,1], 'K': [0,0,1,1,0,0],
        '.': [0,0,0,0,0,0]  # Empty square
    }

    # Process board position
    for c in board_str:
        if c.isdigit():
            bin.extend(piece_mapping['.'] * int(c))
        elif c != '/':
            bin.extend(piece_mapping[c])

    # Active color to binary (0 for white, 1 for black)
    if active_color == 'b':
      bin.append(1)
    else:
      bin.append(0)

    # Castling rights to binary
    if 'K' in castling:
      bin.append(1)
    else:
      bin.append(0)
    if 'Q' in castling:
      bin.append(1)
    else:
      bin.append(0)
    if 'k' in castling:
      bin.append(1)
    else:
      bin.append(0)
    if 'q' in castling:
      bin.append(1)
    else:
      bin.append(0)

    # En passant to binary
    if en_passant == '-':
        bin.extend([0] * 6)  # No en passant square
    else:
        file = ord(en_passant[0]) - ord('a')
        rank = 8 - int(en_passant[1])
        bin.extend([int(bit) for bit in format(file, '03b')])
        bin.extend([int(bit) for bit in format(rank, '03b')])

    return bin
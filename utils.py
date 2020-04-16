from checkertypes import Player, Square
from checkerboard import Jump, Move

__all__ = [
    'print_board',
    'print_move',
    'move_from_coords',
    'square_to_coords'
]

# By Kevin
_COLS = 'ABCDEFGH'

_PIECE_TO_CHAR = {
    None: ' . ',
    Player.black: ' x ',
    Player.white: ' o ',
}

_PLAYER_TO_NAME = {
    Player.black: 'Black',
    Player.white: 'White'
}

def print_board(board):
    for row in range(board.board_size, 0, -1):
        line = []
        for col in range(1, board.board_size + 1):
            piece = board.get(Square(row=row, col=col))
            if piece:
                piece = piece.player
            line.append(_PIECE_TO_CHAR[piece])
        print('%d %s' % (row, ''.join(line)))
    print('   ' + '  '.join(_COLS[:board.board_size]))

def print_move(player, move):
    if move.is_resign:
        move_str = ' resigns'
    else:
        jumps = move.jumps
        move_str = ' moves' + square_to_coords(jumps[0].sq_from)
        move_str += '->'.join(square_to_coords(jump.sq_to) for jump in jumps)
    return _PLAYER_TO_NAME[player] + move_str

def move_from_coords(coords):
    if coords == 'R':
        return Move.resign()

    coords = coords.split()
    assert len(coords) >= 2
    squares = []
    for pair in coords:
        row = int(pair[1:])
        col = _COLS.index(pair[0]) + 1
        squares.append(Square(row=row, col=col))

    jumps = []
    for sq_from, sq_to in zip(squares[:-1], squares[1:]):
        is_capture = (sq_from.row - sq_to.row) ** 2 == 4
        jumps.append(Jump(sq_from, sq_to, is_capture))

    return Move.play(jumps)

def square_to_coords(square):
    return _COLS[square.col - 1] + str(square.row)

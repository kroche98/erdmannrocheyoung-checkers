import importlib
import numpy as np
from checkerboard import __all__

class Encoder:
    def name(self):
        raise NotImplementedError()

    def encode(self, game_state):
        raise NotImplementedError()

    def encode_point(self, point):
        raise NotImplementedError()

    def decode_points(self):
        raise NotImplementedError()

    def decode_point_index(self, index):
        raise NotImplementedError()

    def num_points(self):
        raise NotImplementedError()

    def shape(self):
        raise NotImplementedError()

    def get_encoder_by_name(self, name, board_size = 8):
        if isinstance(board_size, int):
            board_size = (board_size, board_size)
        constructor = getattr(module, 'create')
        return constructor(board_size)

    class OnePlaneEncoder(Encoder):
        def __init__(self, board_size = 8):
            self.board_width, self.board_height = board_size
            self.num_planes = 1

        def name(self):
            return 'oneplane'

        def encode(self, game_state):
            board_matrix = np.zeros(self.shape())
            next_player = game_state.next_player
            for r in range(self.board_height):
                for c in range(self.board_width):
                    s = Square(row = r+1, col = c+1)
                    checker = game_state.board.get_checker(s)
                    if checker is None:
                        continue
                    if checker.color == next_player:
                        board_matrix[0, r, c] = 1
                    else:
                        board_matrix[0, r, c] = -1
            return board_matrix

        def encode_square(self, square):
            return self.board_width * (square.row - 1) + (square.col - 1)

        def decode_square_index(self, index):
            row = index // self.board_width
            col = index % self.board_width
            return Square(row = row + 1, col = col + 1)

        def num_squares(self):
            return self.board_width * self.board_height

        def shape(self):
            return self.num_planes, self.board_height, self.board_width
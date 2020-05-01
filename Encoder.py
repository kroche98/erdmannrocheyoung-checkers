import importlib
import numpy as np
from checkerboard import Board, GameState, Checker, Square
#By Kevin and Jude
class Encoder:
    def name(self):
        raise NotImplementedError()

    def encode(self, GameState):
        raise NotImplementedError()

    def encode_point(self, checker):
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
        board_size = (board_size, board_size)
        module = importlib.import_module('ErdmannRocheYoungProg3.py' + name)
        constructor = getattr(module, 'create')
        return constructor(board_size)

class OnePlaneEncoder(Encoder):
    def __init__(self, board_size = 8):
        self.board_width, self.board_height = board_size, board_size
        self.num_planes = 1

    def name(self):
        return 'oneplane'
    
    def encode(self, GameState):
        board_matrix = np.zeros(self.shape())
        next_player = GameState.next_player
        for r in range(self.board_height):
           for c in range(self.board_width):
                s = Square(row = r+1, col = c+1)
                checker = GameState.board.get(s)
                if checker is None:
                    continue
                if checker.player == next_player:
                    if checker.is_king:
                        board_matrix[0, r, c] = 2
                    else:
                        board_matrix[0, r, c] = 1
                else:
                    if checker.is_king:
                        board_matrix[0, r, c] = -2
                    else:
                        board_matrix[0, r, c] = -1
        return board_matrix

    def encode_square(self, square):
        return self.board_width * (square.row - 1) + (square.col - 1)

    def decode_square_index(self, index):
        row = index // 8
        col = index % 8
        return Square(row = row + 1, col = col + 1)

    def num_squares(self):
        return self.board_width * self.board_height

    def shape(self):
        return self.num_planes, self.board_height, self.board_width
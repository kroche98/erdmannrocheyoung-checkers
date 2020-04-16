import enum
from collections import namedtuple


__all__ = [
    'Player',
    'Square',
]

# By Patrick
class Player(enum.Enum):
    black = 1
    white = 2

    @property
    def other(self):
        return Player.white if self == Player.black else Player.black
# end Player class


# By Kevin
class Square(namedtuple('Square', 'row col')):
    def neighbors_above(self):
        return [
            Square(self.row + 1, self.col - 1),
            Square(self.row + 1, self.col + 1)
        ]

    def neighbors_below(self):
        return [
            Square(self.row - 1, self.col - 1),
            Square(self.row - 1, self.col + 1),
        ]

    def all_neighbors(self):
        return self.neighbors_above() + self.neighbors_below()

    def jump_neighbors_above(self):
        return [
            Square(self.row + 2, self.col - 2),
            Square(self.row + 2, self.col + 2)
        ]

    def jump_neighbors_below(self):
        return [
            Square(self.row - 2, self.col - 2),
            Square(self.row - 2, self.col + 2),
        ]

    def all_jump_neighbors(self):
        return self.jump_neighbors_above() + self.jump_neighbors_below()
    
    def __deepcopy__(self, memodict={}):
        # These are very immutable.
        return self
# end Square class

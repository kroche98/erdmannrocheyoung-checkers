# Patrick Erdmann, Kevin Roche, & Jude Young
# Project 3
# Artificial Intelligence
# Dr Ed Kovach

import enum


class Player(enum.Enum):
    black = 1
    red = 2

    @property
    def other(self):
        return Player.black if self == Player.red else Player.red

#Added by Jude
class King():
    def __init__(self, color, piece, kings):
        self.color = color
        self.piece = piece
        self.kings = kings
    
    def get_crowned_king(self, piece):
        if self.piece is not in kings
            kings.append(self.piece)
            return kings
    def add_king_moves(self, piece):
        assert(self.piece is in kings)
        self.add_backwards_capabilities(piece)
    def add_backwards_capabilities(self):

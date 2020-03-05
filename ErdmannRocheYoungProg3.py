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
    def __init__(self, color, checker, kings):
        self.color = color
        self.checker = checker
        self.kings = kings
    
    def get_crowned_king(self, checker):
        if self.checker is not in kings
            kings.append(self.checker)
            return kings
    def add_king_moves(self, checker):
        assert(self.checker is in kings)
        self.add_backwards_capabilities(checker)
    
    def add_backwards_capabilities(self, checker):

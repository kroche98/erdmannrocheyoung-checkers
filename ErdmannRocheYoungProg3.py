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

# Patrick Erdmann, Kevin Roche, & Jude Young
# Project 3
# Artificial Intelligence
# Dr Ed Kovach

import enum

#
class Player(enum.Enum):
    black = 1
    red = 2

    @property
    def other(self):
        return Player.black if self == Player.red else Player.red



#Move class largely by Jude
class Move():
    def __init__(self, left_right, checker, fowards_backwards):
        self.checker = checker
        self.fowards_backwards = fowards_backwards
        self.left_right = left_right
    
    def move_checker(self, checker, move_fowards_backwards, move_left_right):
        if move_fowards_backwards == 'backwards'
            assert (checker.is_king())
        if move_left_right == 'left':
            # assert that square is on board and not occupied
            if (move_fowards_backwards == 'fowards'):
                self.checker.row = checker.row + 1
            elif (move_fowards_backwards == 'backwards'):
                self.checker.row = checker.row - 1
            self.checker.col = checker.col - 1
        elif move_left_right == 'right':
            if (move_fowards_backwards == 'fowards'):
                self.checker.row = checker.row + 1
            elif (move_fowards_backwards == 'backwards'):
                self.checker.row = checker.row - 1
            self.checker.col = checker.col + 1
        elif (move_left_right == 'jump left'):
            if (move_fowards_backwards == 'fowards'):
                self.checker.row = checker.row + 2
            elif (move_fowards_backwards == 'backwards'):
                self.checker.row = checker.row -2
            self.checker.col = checker.col -2
        elif (move_left_right == 'jump right'):
            if (move_fowards_backwards == 'fowards'):
                self.checker.row = checker.row + 2
            elif (move_fowards_backwards == 'backwards'):
                self.checker.row == checker.row - 2
            self.checker.col == checker.col + 2
        
        self.checker.square = [self.checker.row, self.checker.col]
        return (self.checker.square)

#GameState class largely by Jude
class GameState():
    def __init__(self, board, next_player, move):
        self.board = board
        self.next_player = next_player
        self.last_move = move
    
    def apply_move(self, fowards_backwards, left_right):
        if move.is_play:
            next_board.move_checker(checker, fowards_backwards, left_right)
    def new_game(self):
        #new_game method
    def is_space_occupied(self, player, move):
        if move_checker(move.checker, move.fowards_backwards, move.left_right) is not null:
            return False
        else
            return True
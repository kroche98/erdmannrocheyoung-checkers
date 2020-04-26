from Bot import Bot
from checkertypes import Player, Square
from checkerboard import Jump, Move, GameState
from agents.dumb_checker_bot import DumbCheckerBot
import utils

class REY_Bot(Bot):
    def __init__(self, color, botFolder):
        # color = Player.black if color=="black" else Player.white
        self.game_state = GameState.new_game()
        self.agent = DumbCheckerBot()

    @staticmethod
    def square_to_str(square):
        return f"{square.col}x{square.row}"
    
    @staticmethod
    def str_to_square(string):
        col, row = string.split('x')
        return Square(col=int(col), row=int(row))

    @staticmethod
    def move_to_tuple(move):
        if move.is_resign:
            return "resign"
        start = REY_Bot.square_to_str(move.jumps[0].sq_from)
        rest = list(map(lambda j: REY_Bot.square_to_str(j.sq_to), move.jumps))
        return (start, rest)
    
    @staticmethod
    def tuple_to_move(tup):
        if tup=="resign":
            return Move.resign()
        start, rest = tup
        squares = [REY_Bot.str_to_square(start)]
        squares += list(map(lambda s: REY_Bot.str_to_square(s), rest))

        jumps = []
        for sq_from, sq_to in zip(squares[:-1], squares[1:]):
            is_capture = (sq_from.row - sq_to.row) ** 2 == 4
            jumps.append(Jump(sq_from, sq_to, is_capture))

        return Move.play(jumps)

    def makemove(self):
        move = self.agent.select_move(self.game_state)
        self.game_state = self.game_state.apply_move(move)
        return REY_Bot.move_to_tuple(move)

    def receiveMove(self, move):
        move = REY_Bot.tuple_to_move(move)
        if not self.game_state.is_valid_move(move.jumps):
            return False
        self.game_state = self.game_state.apply_move(move)
        return True
    
    def print_board(self):
        utils.print_board(self.game_state.board)

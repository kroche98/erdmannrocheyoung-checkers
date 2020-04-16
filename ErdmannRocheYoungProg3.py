# Patrick Erdmann, Kevin Roche, & Jude Young
# Project 3
# Artificial Intelligence
# Dr. Ed Kovach

import random

from checkertypes import Player
from checkerboard import Move, GameState
import utils

class Agent:
    def choose_move(self, game_state):
        pass

# by Patrick
class DumbCheckerBot(Agent):
    def choose_move(self, game_state):
        candidate_moves = game_state.legal_moves()
        if len(candidate_moves) == 0:
            return Move.resign()
        choice = random.randrange(0, len(candidate_moves))
        return Move.play(candidate_moves[choice])
# end DumbCheckerBot class

class HumanAgent(Agent):
    def choose_move(self, game_state):
        human_choice = input('-- ')
        return utils.move_from_coords(human_choice.strip())

def main():
    game = GameState.new_game()

    instructions = """To input a move, type the coordinates
    of the checker you want to move, followed by the coordinates
    of the square you want to move to. If your move involves
    multiple jumps, type all the squares you want to move to
    in succession.

    For example, the move 'C3 B4' would be a legal first move.
    The move 'D2 F4 D6' would be a move consisting of two jumps,
    which would be legal assuming that the jumps were legal.

    To resign, type 'R'
    """

    print(instructions)

    player_1 = DumbCheckerBot()
    player_2 = DumbCheckerBot()

    utils.print_board(game.board)
    
    while not game.winner():
        # print(chr(27) + "[2J")
        if game.next_player == Player.black:
            move = player_1.choose_move(game)
        else:
            move = player_2.choose_move(game)
        game = game.apply_move(move)
        # utils.print_move(game.next_player, move)
        utils.print_board(game.board)
    print(f"Game over! {game.winner()} wins")

if __name__ == '__main__':
    main()

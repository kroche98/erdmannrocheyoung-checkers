# Patrick Erdmann, Kevin Roche, & Jude Young
# Project 3
# Artificial Intelligence
# Dr. Ed Kovach

from checkertypes import Player
from checkerboard import GameState
import utils

from agents.dumb_checker_bot import DumbCheckerBot
from agents.monte_carlo_checker_bot import MonteCarloCheckerBot

def play_game(player_1, player_2):
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

    utils.print_board(game.board)
    
    while not game.winner():
        # print(chr(27) + "[2J")
        if game.next_player == Player.black:
            move = player_1.select_move(game)
        else:
            move = player_2.select_move(game)
        game = game.apply_move(move)
        # utils.print_move(game.next_player, move)
        utils.print_board(game.board)
    print(f"Game over! {game.winner()} wins")

def main():
    player_1 = DumbCheckerBot()
    player_2 = MonteCarloCheckerBot()

    play_game(player_1, player_2)

if __name__ == '__main__':
    main()

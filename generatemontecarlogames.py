import argparse
import numpy as np
from Encoder import OnePlaneEncoder
from checkerboard import GameState
from utils import print_board, print_move
from agents.monte_carlo_checker_bot import MonteCarloCheckerBot


def generate_game(rounds, max_moves, temperature):
    boards, moves = [], []

    encoder = OnePlaneEncoder()

    game = GameState.new_game()

    #bot = MonteCarloCheckerBot(rounds, temperature)
    bot = MonteCarloCheckerBot()

    num_moves = 0
    while not game.winner():
        print_board(game.board)
        move = bot.select_move(game)
        if move.is_play:
            boards.append(encoder.encode(game))

            move_one_hot = np.zeros(encoder.num_squares())
            move_one_hot[encoder.encode_square(move.jumps[0].sq_from)] = 1
            moves.append(move_one_hot)
        print_move(game.next_player, move)
        game = game.apply_move(move)
        num_moves += 1
        if num_moves > max_moves:
            break

    return np.array(boards), np.array(moves)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--board-size', '-b', type = int, default=8)
    parser.add_argument('--rounds', '-r', type = int, default = 1000)
    parser.add_argument('--temperature', '-t', type = float, default = 0.8)
    parser.add_argument('--max-moves', '-m', type = int, default = 10, help = 'Max moves per game.')
    parser.add_argument('--num-games', '-n', type = int, default = 2)
    parser.add_argument('--board-out', '-bo', type = str, default = "board_out.npy")
    parser.add_argument('--move-out', '-mo', type = str, default = "move_out.npy")

    args = parser.parse_args()
    xs = []
    ys = []

    for i in range(args.num_games):
        print('Generating game %d/%d...' % (i + 1, args.num_games))
        x, y = generate_game(args.rounds, args.max_moves, args.temperature)
        xs.append(x)
        ys.append(y)

    x = np.concatenate(xs)
    y = np.concatenate(ys)

    np.save(args.board_out, x)
    np.save(args.move_out, y)

if __name__ == '__main__':
    main()
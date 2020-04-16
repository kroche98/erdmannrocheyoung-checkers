from agents.agent import Agent
from checkerboard import Move
import random

# by Patrick
class DumbCheckerBot(Agent):
    def select_move(self, game_state):
        candidate_moves = game_state.legal_moves()
        if len(candidate_moves) == 0:
            return Move.resign()
        choice = random.randrange(0, len(candidate_moves))
        return Move.play(candidate_moves[choice])
# end DumbCheckerBot class

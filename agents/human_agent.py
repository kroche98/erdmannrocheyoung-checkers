from agents.agent import Agent
from utils import move_from_coords

# By Kevin
class HumanAgent(Agent):
    def select_move(self, game_state):
        human_choice = input('-- ')
        return move_from_coords(human_choice.strip())

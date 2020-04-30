import numpy as np
from Agents.agent import Agent
from Encoder import OnePlaneEncoder
from checkerboard import Move, GameState
from keras import Sequential

class DeepLearningAgent(Agent):
    #def __init__(self, model, encoder):
    def __init__(self, encoder):
        #self.model = model
        self.model = Sequential()
        self.encoder = encoder
    
    def predict(self, GameState):
        encoded_state = self.encoder.encode(GameState)
        input_tensor = np.array([encoded_state])
        return self.model.predict(input_tensor)[0]

    def select_move(self, GameState):
        #num_moves = self.encoder.board_width * self.encoder.board_height
        num_moves = 8 * 8
        move_probs = self.predict(GameState)

        move_probs = move_probs ** 3
        eps = 1e-6
        #Make sure move probabilities aren't stuck at 0 or 1
        move_probs = np.clip(move_probs, eps, 1-eps)
        move_probs = move_probs / np.sum(move_probs)

        candidates = np.arrange(num_moves)
        ranked_moves = np.random.choice(candidates, num_moves, replace = False, p = move_probs)
        #Pick the highest ranked move
        choice = max(ranked_moves)
        return Move.play(candidates[choice])
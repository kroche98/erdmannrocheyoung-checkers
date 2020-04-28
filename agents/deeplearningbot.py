import numpy as np
from Agents.agent import agent
from Encoder import OnePlaneEncoder
from checkerboard import Move, GameState

class DeepLearningAgent(Agent):
    def __init__(self, model, encoder):
        self.model = model
        self.encoder = encoder
    
    def predict(self, game_state):
        encoded_state = self.encoder.encode(game_state)
        input_tensor = np.array([encoded_state])
        return self.model.predict(input_tensor)[0]

    def select_move(self, game_state):
        num_moves = self.encoder.board_width * self.encoder.board_height
        move_probs = self.predict(game_state)

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
        '''
        for square_idx in ranked_moves:
            square_from = self.encoder.decode_square_index(square_idx)
            square_to = self.encoder.decode_square_index(square_idx)
            if game_state.is_valid_move(Move.play(square_from, square_to)
                return Move.play(
                    '''
from agents.agent import Agent
from agents.dumb_checker_bot import DumbCheckerBot
from checkerboard import Move, GameState
from copy import deepcopy

# by Kevin
class MonteCarloCheckerBot(Agent):    
    def select_move(self, game_state):
        candidate_moves = game_state.legal_moves()
        if len(candidate_moves) == 0:
            return Move.resign()
        scores = {}
        dummy_bot = DumbCheckerBot()
        for i, move in enumerate(candidate_moves):
            total_score = 0
            num_rollouts = 64
            rollout_depth = 4
            for _ in range(num_rollouts):
                temp_state = deepcopy(game_state)
                temp_state = temp_state.apply_move(Move.play(move))
                for _ in range(2 * rollout_depth - 1):
                    if temp_state.winner():
                        break
                    random_move = dummy_bot.select_move(temp_state)
                    temp_state = temp_state.apply_move(random_move)
                total_score += self.evaluate_position(temp_state, game_state.next_player)
            scores[i] = total_score / num_rollouts
        best_move, best_score = 0, scores[0]
        for move, score in scores.items():
            if score > best_score:
                best_move, best_score = move, score
        return Move.play(candidate_moves[best_move])
        
    def evaluate_position(self, game_state, player):
        """Give a score for the given player and game position
        A score of -18 indicates a loss, whereas a score of 18 indicates a win
        Otherwise the score is the material differential, where each
        regular checker counts for 1 point and each king counts for 1.5 points
        """
        winner = game_state.winner()
        if winner == player:
            score = 18
        elif winner == player.other:
            score = -18
        else:
            own_pieces = game_state.board.get_pieces(player)
            own_score = sum(map(lambda p: 1.5 if p[1].is_king else 1, own_pieces))
            opp_pieces = game_state.board.get_pieces(player.other)
            opp_score = sum(map(lambda p: 1.5 if p[1].is_king else 1, opp_pieces))
            score = own_score - opp_score
        return score
# end MonteCarloCheckerBot class

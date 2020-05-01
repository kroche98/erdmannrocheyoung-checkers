"""Competition checker bot
By Patrick Erdmann, Kevin Roche, & Jude Young

To use this file, put it in the same directory
as the API module, and import our bot using
from REY_Bot_onefile import REY_MonteCarloBot
"""

import enum
from collections import namedtuple
import copy
import random


# By Patrick
class Player(enum.Enum):
    black = 1
    white = 2

    @property
    def other(self):
        return Player.white if self == Player.black else Player.black
# end Player class


class utils:
    _COLS = 'ABCDEFGH'
    _PIECE_TO_CHAR = {
        None: '   ',
        (Player.black, True): ' B ',
        (Player.black, False): ' b ',
        (Player.white, True): ' R ',
        (Player.white, False): ' r '
    }

    @classmethod
    def board_repr(cls, board):
        lines = []
        for row in range(board.board_size, 0, -1):
            line = []
            for col in range(1, board.board_size + 1):
                if (row + col) % 2 == 1:
                    line.append('███')
                else:
                    piece = board.get(Square(row=row, col=col))
                    if piece:
                        piece = (piece.player, piece.is_king)
                    line.append(utils._PIECE_TO_CHAR[piece])
            lines.append('%d %s' % (row, ''.join(line)))
        lines.append('   ' + '  '.join(utils._COLS[:board.board_size]))
        return '\n'.join(lines)


# By Kevin
class Square(namedtuple('Square', 'row col')):
    def neighbors_above(self):
        return [
            Square(self.row + 1, self.col - 1),
            Square(self.row + 1, self.col + 1)
        ]

    def neighbors_below(self):
        return [
            Square(self.row - 1, self.col - 1),
            Square(self.row - 1, self.col + 1),
        ]

    def all_neighbors(self):
        return self.neighbors_above() + self.neighbors_below()

    def jump_neighbors_above(self):
        return [
            Square(self.row + 2, self.col - 2),
            Square(self.row + 2, self.col + 2)
        ]

    def jump_neighbors_below(self):
        return [
            Square(self.row - 2, self.col - 2),
            Square(self.row - 2, self.col + 2),
        ]

    def all_jump_neighbors(self):
        return self.jump_neighbors_above() + self.jump_neighbors_below()
    
    def __deepcopy__(self, memodict={}):
        # These are very immutable.
        return self
# end Square class


# Added by Kevin
class Checker:
    def __init__(self, player, is_king=False):
        self.player = player
        self.is_king = is_king

    def make_king(self):
        self.is_king = True
    
    def __deepcopy__(self, memodict={}):
        return Checker(self.player, self.is_king)
# end Checker class


class Board:
    def __init__(self, board_size=8):
        self.board_size = 8
        self._grid = {}

    def init_board(self):
        for row in range(1, self.board_size + 1):
            for col in range(1, self.board_size + 1):
                self._grid[Square(row, col)] = None
        black_squares = [
            (6, 2), (6, 4), (6, 6), (6, 8),
            (7, 1), (7, 3), (7, 5), (7, 7),
            (8, 2), (8, 4), (8, 6), (8, 8),
        ]
        white_squares = [
            (1, 1), (1, 3), (1, 5), (1, 7),
            (2, 2), (2, 4), (2, 6), (2, 8),
            (3, 1), (3, 3), (3, 5), (3, 7)
        ]
        for sq in black_squares:
            self._grid[Square(*sq)] = Checker(Player.black)
        for sq in white_squares:
            self._grid[Square(*sq)] = Checker(Player.white)

    def move_checker(self, square_from, square_to, is_capture):
        """Move a checker from one square to another
        Returns a boolean indicating whether the move resulted
        in the checker being crowned"""
        assert self.is_on_board(square_from)
        assert self.is_on_board(square_to)
        assert self._grid.get(square_from) is not None
        assert self._grid.get(square_to) is None

        checker = self._grid.get(square_from)

        self._grid[square_to] = checker
        self._grid[square_from] = None

        # If there's a capture, remove the captured piece
        if is_capture:
            captured_square = Square(
                (square_from.row + square_to.row) // 2,
                (square_from.col + square_to.col) // 2
            )
            self._grid[captured_square] = None

        # King the piece if appropriate
        move_crowns_checker = False
        if not checker.is_king:
            if checker.player == Player.white and square_to.row == self.board_size:
                checker.make_king()
                move_crowns_checker = True
            if checker.player == Player.black and square_to.row == 1:
                checker.make_king()
                move_crowns_checker = True
        
        return move_crowns_checker

    def is_on_board(self, square):
        return 1 <= square.row <= self.board_size and \
               1 <= square.col <= self.board_size

    def get(self, square):
        """Return the contents of a square on the board.

        Returns None if the square is empty, or a Checker if
        there is a checker on that square.
        """
        return self._grid.get(square)

    def get_pieces(self, player):
        """Return the pieces belonging to a player

        Returns a list containing all the checkers belonging
        to the player"""
        assert isinstance(player, Player)
        pieces = []
        for square, checker in self._grid.items():
            if checker == None:
                continue
            if checker.player == player:
                pieces.append((square, checker))
        return pieces

    def __deepcopy__(self, memodict={}):
        copied = Board(self.board_size)
        copied._grid = copy.deepcopy(self._grid)
        return copied
# end Board class


class Jump(namedtuple('Jump', 'sq_from sq_to is_capture')):
    pass


# By Kevin
class Move():
    """Any action a player can play on a turn.
    Either is_resign will be set, or jumps will be set."""

    def __init__(self, jumps=None, is_resign=False):
        assert (jumps is not None) ^ is_resign
        self.jumps = jumps
        self.is_play = (self.jumps is not None)
        self.is_resign = is_resign

    @classmethod
    def play(cls, jumps):
        return Move(jumps)

    @classmethod
    def resign(cls):
        return Move(is_resign=True)
# end Move class


# By Kevin and Jude
class GameState():
    def __init__(self, board, next_player, move):
        self.board = board
        self.next_player = next_player
        self.last_move = move

    @classmethod
    def new_game(cls):
        board = Board()
        board.init_board()
        return GameState(board, Player.black, None)

    def apply_move(self, move):
        if move.is_play:
            next_board = copy.deepcopy(self.board)
            for jump in move.jumps:
                next_board.move_checker(*jump)
        else:
            next_board = self.board
        return GameState(next_board, self.next_player.other, move)
 
    def is_jump_legal(self, jump):
        sq_from, sq_to, is_capture = jump

        # the starting square must be on the board
        if not self.board.is_on_board(sq_from):
            return False
        
        # the starting square must have a checker of the correct color
        checker = self.board.get(sq_from)
        if checker is None:
            return False
        if checker.player != self.next_player:
            return False
        
        # the destination square must be on the board
        if not self.board.is_on_board(sq_to):
            return False
        
        # the destination square must be unoccupied
        if self.board.get(sq_to) is not None:
            return False
        
        # Case 1: the move is not a capture
        if not is_capture:
            # the destination must be reachable from the starting square
            if checker.is_king:
                reachable_sqs = sq_from.all_neighbors()
            elif checker.player == Player.black:
                reachable_sqs = sq_from.neighbors_below()
            else:
                reachable_sqs = sq_from.neighbors_above()
            if sq_to not in reachable_sqs:
                return False
        
        # Case 2: the move is a capture
        else:
            # the destination must be reachable from the starting square
            if checker.is_king:
                reachable_sqs = sq_from.all_jump_neighbors()
            elif checker.player == Player.black:
                reachable_sqs = sq_from.jump_neighbors_below()
            else:
                reachable_sqs = sq_from.jump_neighbors_above()
            if sq_to not in reachable_sqs:
                return False
            
            # the square in between must have a checker of the opposing color
            sq_btwn = Square((sq_from.row + sq_to.row) // 2, (sq_from.col + sq_to.col) // 2)
            captured_checker = self.board.get(sq_btwn)
            if captured_checker is None:
                return False
            if captured_checker.player != self.next_player.other:
                return False

        # if we pass all these tests, then the jump is legal
        return True

    def is_valid_move(self, move):
        """Return a boolean indicating whether the given jump sequence is legal

        Assumes that move is an array of Jump objects"""

        # an empty sequence is invalid
        if len(move) == 0:
            return False

        # if there are multiple jumps in the sequence, they must all be captures
        if len(move) > 1:
            if set(map(lambda m: m.is_capture, move)) != {True}:
                return False
        
        jump = move[0]

        # Case 1: the move is not a capture
        if not jump.is_capture:
            # the jump must be legal
            if not self.is_jump_legal(jump):
                return False

            # it must not be possible to make a capture
            if self.is_capture_possible():
                return False
        
        # Case 2: the move involves a capture:
        else:
            temp_state = copy.deepcopy(self)
            checker_crowned = False
            current_square = jump.sq_from

            for jump in move:
                # if the checker has already been crowned on this turn,
                # no more jumps are allowed
                if checker_crowned:
                    return False
                
                # the jump must start from the square where
                # the last jump ended
                if current_square != jump.sq_from:
                    return False
                current_square = jump.sq_to

                # each jump must be legal
                if not temp_state.is_jump_legal(jump):
                    return False
                
                checker_crowned = temp_state.board.move_checker(*jump)
            
            # at the end, there must not be any valid captures remaining
            # unless we have just crowned the checker
            if temp_state.is_capture_possible(current_square) and not checker_crowned:
                return False
        
        # if we pass all these tests, then the move is valid
        return True

    def is_capture_possible(self, square=None):
        """Return a boolean indicating whether a capture is possible

        If square is not specified, it determines whether a capture is
        possible by any of the current player's checkers.
        Otherwise, it computes whether a capture is possible by the
        checker on the specified square. In this case, it assumes that
        the square contains a checker"""

        if square:
            piece = (square, self.board.get(square))
            pieces_to_check = [piece]
        else:
            pieces_to_check = self.board.get_pieces(self.next_player)
        
        for square, checker in pieces_to_check:
            if checker.is_king:
                reachable_sqs = square.all_jump_neighbors()
            elif checker.player == Player.black:
                reachable_sqs = square.jump_neighbors_below()
            else:
                reachable_sqs = square.jump_neighbors_above()
            
            for candidate_sq in reachable_sqs:
                jump = Jump(sq_from=square, sq_to=candidate_sq, is_capture=True)
                if self.is_jump_legal(jump):
                    return True
        
        # if we haven't found a possible capture by now, there are none
        return False
    
    # by Patrick and Kevin
    def legal_moves(self):
        candidate_moves = []

        for square, _ in self.board.get_pieces(self.next_player):
            # check for basic moves
            for neighbor in square.all_neighbors():
                jump = Jump(square, neighbor, is_capture=False)
                candidate_moves.append([jump])

            # check for captures
            candidate_captures = self._legal_captures(square)
            for candidate_move in candidate_captures:
                candidate_moves.append(candidate_move)
        
        return list(filter(lambda m: self.is_valid_move(m), candidate_moves))

    def _legal_captures(self, square):
        """Recursively find legal sequences of captures beginning at square"""
        candidate_moves = []

        for neighbor in square.all_jump_neighbors():
            jump = Jump(square, neighbor, is_capture=True)
            if self.is_jump_legal(jump):
                # if the capture is legal, add it as a possibility
                candidate_moves.append([jump])

                # now see if further captures are possible
                temp_state = copy.deepcopy(self)
                temp_state.board.move_checker(*jump)
                rest = temp_state._legal_captures(neighbor)
                for move in rest:
                    candidate_moves.append([jump] + move)

        return candidate_moves

    def winner(self):
        if self.last_move is None:
            return False
        if self.last_move.is_resign:
            return self.next_player
        if len(self.legal_moves()) == 0:
            return self.next_player.other
        return False
# end GameState class


class Agent:
    def select_move(self, game_state):
        raise NotImplementedError

#By Patrick
class DumbCheckerBot(Agent):
    def select_move(self, game_state):
        candidate_moves = game_state.legal_moves()
        if len(candidate_moves) == 0:
            return Move.resign()
        choice = random.randrange(0, len(candidate_moves))
        return Move.play(candidate_moves[choice])
# end DumbCheckerBot class

#By Kevin
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
                temp_state = copy.deepcopy(game_state)
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


class Bot:
    def __init__(self, color):
        self.color = color

    def make_move(self):
        raise NotImplementedError()

    def receive_move(self, move):
        raise NotImplementedError()

    def get_board_str(self):
        raise NotImplementedError()

    def undo_last_move(self):
        raise NotImplementedError()


class REY_Bot(Bot):
    def __init__(self, color, agent):
        # color = Player.black if color=="black" else Player.white
        self.game_state = GameState.new_game()
        self.temp_state = self.game_state
        self.agent = agent

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

    def make_move(self):
        # first apply the opponent's last move
        self.game_state = self.temp_state
        move = self.agent.select_move(self.game_state)
        self.temp_state = self.game_state.apply_move(move)
        return REY_Bot.move_to_tuple(move)
    
    def undo_last_move(self):
        # we haven't applied the move yet, so we'll just wait
        # until make_move gets called again
        pass

    def receive_move(self, move):
        # first apply our last move
        self.game_state = self.temp_state
        move = REY_Bot.tuple_to_move(move)
        if not self.game_state.is_valid_move(move.jumps):
            return False
        self.temp_state = self.game_state.apply_move(move)
        return True
    
    def get_board_str(self):
        # we return temp_state because game_state won't
        # be updated until 
        return utils.board_repr(self.temp_state.board)


class REY_MonteCarloBot(REY_Bot):
    def __init__(self, color):
        agent = MonteCarloCheckerBot()
        super().__init__(color, agent)
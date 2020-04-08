# Patrick Erdmann, Kevin Roche, & Jude Young
# Project 3
# Artificial Intelligence
# Dr. Ed Kovach


import random
import copy
import enum
from collections import namedtuple


# By Patrick
class Player(enum.Enum):
    red = 1
    white = 2

    @property
    def other(self):
        return Player.white if self == Player.red else Player.red
# end player class


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
        return self.neighbors_above() + self.neighbors_below()
# end square class


class IllegalMoveError(Exception):
    pass


# Added by Kevin
# Replaces King class
class Checker:
    def __init__(self, player, is_king=False):
        self.player = player
        self.is_king = is_king

    def make_king(self):
        self.is_king = True
# end checker class


class Board:
    def __init__(self, board_size=8):
        self.board_size = 8
        self._grid = {}

    def init_board(self):
        for row in range(1, self.board_size + 1):
            for col in range(1, self.board_size + 1):
                self._grid[Square(row, col)] = None
        red_squares = [
            (1, 1), (1, 3), (1, 5), (1, 7),
            (2, 2), (2, 4), (2, 6), (2, 8),
            (3, 1), (3, 3), (3, 5), (3, 7)
        ]
        white_squares = [
            (6, 2), (6, 4), (6, 6), (6, 8),
            (7, 1), (7, 3), (7, 5), (7, 7),
            (8, 2), (8, 4), (8, 6), (8, 8),
        ]
        for sq in red_squares:
            self._grid[Square(*sq)] = Checker(Player.red)
        for sq in white_squares:
            self._grid[Square(*sq)] = Checker(Player.white)

    def move_checker(self, square_from, square_to, is_jump):
        assert self.is_on_board(square_from)
        assert self.is_on_board(square_to)
        assert self._grid.get(square_from) is not None
        assert self._grid.get(square_to) is None

        checker = self._grid.get(square_from)

        self._grid[square_to] = checker
        self._grid[square_from] = None

        # If there's a capture, remove the captured piece
        if is_jump:
            captured_square = Square(
                (square_from.row + square_to.row) // 2,
                (square_from.col + square_to.col) // 2
            )
            self._grid[captured_square] = None

        # King the piece if appropriate
        if not checker.is_king:
            if checker.player == Player.red and square_to.row == self.board_size:
                checker.make_king()
            if checker.player == Player.white and square_to.row == 1:
                checker.make_king()

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
# end board class


class Move(namedtuple('Move', 'sq_from sq_to is_jump')):
    pass


# By Jude and Kevin
class Action():
    """Any action a player can play on a turn.
    Either is_resign will be set, or move will be set."""

    def __init__(self, moves=None, is_resign=False):
        assert (moves is not None) ^ is_resign
        self.moves = moves
        self.is_play = (self.moves is not None)
        self.is_resign = is_resign

    @classmethod
    def play(cls, moves):
        return Action(moves)

    @classmethod
    def resign(cls):
        return Action(is_resign=True)
# end action class


# By Jude and Kevin
class GameState():
    def __init__(self, board, next_player, move):
        self.board = board
        self.next_player = next_player
        self.last_move = move

    def apply_action(self, action):
        if action.is_play:
            next_board = copy.deepcopy(self.board)
            for move in action.moves:
                next_board.move_checker(*move)
        else:
            next_board = self.board
        return GameState(next_board, self.next_player.other, action)

    @classmethod
    def new_game(cls):
        board = Board()
        board.init_board()
        return GameState(board, Player.red, None)

    def is_valid_move(self, move_seq):
        """Return a boolean indicating whether the given move sequence is legal

        Assumes that move_seq is an array of Move objects"""

        # if there are multiple moves in the sequence, they must all be jumps
        if len(move_seq) > 1:
            if len(set(map(lambda m: m.is_jump, move_seq))) > 1:
                return False

        for sq_from, sq_to, is_jump in move_seq:
            # check that the first square in the move sequence
            # has a checker of the correct color
            if not self.board.is_on_board(sq_from):
                return False
            checker = self.board.get(sq_from)
            if checker is None:
                return False
            if checker.player != self.next_player:
                return False

            # check that the destination square is unoccupied
            if not self.board.is_on_board(sq_to):
                return False
            if self.board.get(sq_to) is not None:
                return False

            # if it is not a jump, check that the destination square is reachable
            if not is_jump:
                if checker.is_king:
                    reachable_sqs = sq_from.all_neighbors()
                elif checker.player == Player.red:
                    reachable_sqs = sq_from.neighbors_above()
                else:
                    reachable_sqs = sq_from.neighbors_below()
                if sq_to not in reachable_sqs:
                    return False

            # if it's a jump, check that the destination square
            # is reachable from the source square and that the jump is legal
            else:
                if (sq_from.row - sq_to.row) ** 2 + (sq_from.col - sq_to.col) ** 2 != 8:
                    return False
                sq_btwn = Square((sq_from.row + sq_to.row) // 2, (sq_from.col + sq_to.col) // 2)
                jumped_checker = self.board.get(sq_btwn)
                if jumped_checker is None:
                    return False
                if jumped_checker.player != self.next_player.other:
                    return False

        # finally, enforce the rule that all possible jumps must be taken
        temp_state = copy.deepcopy(self)
        for move in move_seq:
            if temp_state.is_jump_possible() and not move.is_jump:
                return False
        temp_state.board.move_checker(*move)
        if temp_state.is_jump_possible():
            return False

        return True

    def is_jump_possible(self):
        # TODO: there's code duplication between here and is_valid_move()
        for square, checker in self.board.get_pieces(self.next_player):
            if checker.is_king:
                reachable_sqs = square.all_jump_neighbors()
            elif checker.player == Player.red:
                reachable_sqs = square.jump_neighbors_above()
            else:
                reachable_sqs = square.jump_neighbors_below()
            for candidate_sq in reachable_sqs:
                if not self.board.is_on_board(candidate_sq):
                    continue
                if self.board.get(candidate_sq) is None:
                    sq_btwn = Square((square.row + candidate_sq.row) // 2, (square.col + candidate_sq.col) // 2)
                    jumped_checker = self.board.get(sq_btwn)
                    if jumped_checker is None:
                        continue
                    elif jumped_checker.player == self.next_player.other:
                        return True
        return False

    def is_over(self):
        if self.last_move is None:
            return False
        if self.last_move.is_resign:
            return True
        return False
        # return len(legal_moves) > 0

    def winner(self):
        # TODO
        pass
# end game_state class

"""
# TODO Some of this logic belongs in the is_valid() function
# By Jude
    def move_checker(self, checker, move_fowards_backwards, move_left_right):
        if move_fowards_backwards == 'backwards':
            assert (checker.is_king())
        if move_left_right == 'left':
            # assert that square is on board and not occupied
            if (move_fowards_backwards == 'fowards'):
                self.checker.row = checker.row + 1
            elif (move_fowards_backwards == 'backwards'):
                self.checker.row = checker.row - 1
            self.checker.col = checker.col - 1
        elif move_left_right == 'right':
            if (move_fowards_backwards == 'fowards'):
                self.checker.row = checker.row + 1
            elif (move_fowards_backwards == 'backwards'):
                self.checker.row = checker.row - 1
            self.checker.col = checker.col + 1
        elif (move_left_right == 'jump left'):
            if (move_fowards_backwards == 'fowards'):
                self.checker.row = checker.row + 2
            elif (move_fowards_backwards == 'backwards'):
                self.checker.row = checker.row -2
            self.checker.col = checker.col -2
        elif (move_left_right == 'jump right'):
            if (move_fowards_backwards == 'fowards'):
                self.checker.row = checker.row + 2
            elif (move_fowards_backwards == 'backwards'):
                self.checker.row == checker.row - 2
            self.checker.col == checker.col + 2

        self.checker.square = [self.checker.row, self.checker.col]
        return (self.checker.square)
"""


# by Patrick
class CheckerBot:
    def __init__(self):
        self.game = None
        self.moves = []
        self.single_jumps = []
        self.multi_jumps = []

    def print_moves(self):
        print("single move")
        for i in self.moves:
            print(i)
        print("Jumps")
        for j in self.single_jumps:
            print(j)

    def update_board(self, new_state):
        self.game = new_state

    def choose_move(self):
        
        if len(self.single_jumps) != 0:
            rand_move = random.randrange(0, len(self.single_jumps)-1)
            print("Robot picks move:")
            print(self.single_jumps[rand_move])
            return self.single_jumps[rand_move]

        if len(self.moves) != 0:
            rand_move = random.randrange(0, len(self.moves)-1)
            print("Robot picks move:")
            print(self.moves[rand_move])
            return self.moves[rand_move]

        else:
            print("No more moves")

    # by Patrick and Kevin
    def legal_moves(self):
        # TODO
        # basic idea: create a list of candidate move sequences
        # by looping through the player's pieces and seeing
        # what legal moves each one had
        # some cleverness is required to come up with the double jump moves
        # once you have candidate_moves you could just do
        # return list(filter(lambda m: self.is_valid(m), candidate_moves))
        # then for the bot, just call legal_moves and pick a random one
        for square, checker in self.game.board.get_pieces(self.game.next_player):
            # check for single moves
            for n in square.all_neighbors():
                new_move = [Move(square, n, False)]
                if self.game.is_valid_move(new_move):
                    self.moves.append(new_move)

            # check for jumps
            for j in square.all_jump_neighbors():
                new_jump = [Move(square, j, True)]
                print(new_jump)
                if self.game.is_valid_move(new_jump):
                    print("Jump avail")
                    print(new_jump)
                    self.single_jumps.append(new_jump)


# end checker bot class


# The Rest is by Kevin
COLS = 'ABCDEFGH'
PIECE_TO_CHAR = {
    None: ' . ',
    Player.red: ' x ',
    Player.white: ' o ',
}


def print_board(board):
    for row in range(board.board_size, 0, -1):
        line = []
        for col in range(1, board.board_size + 1):
            piece = board.get(Square(row=row, col=col))
            if piece:
                piece = piece.player
            line.append(PIECE_TO_CHAR[piece])
        print('%d %s' % (row, ''.join(line)))
    print('   ' + '  '.join(COLS[:board.board_size]))


"""
def print_move(player, move):
    if move.is_resign:
        move_str = 'resigns'
    else:
        move_str =  
"""


def move_from_coords(coords):
    if coords == 'R':
        return Action.resign()

    coords = coords.split()
    assert len(coords) >= 2
    squares = []
    for pair in coords:
        row = int(pair[1:])
        col = COLS.index(pair[0]) + 1
        squares.append(Square(row=row, col=col))

    moves = []
    for sq_from, sq_to in zip(squares[:-1], squares[1:]):
        is_jump = (sq_from.row - sq_to.row) ** 2 == 4
        moves.append(Move(sq_from, sq_to, is_jump))

    return moves


def square_to_chords(square):
    return COLS[square.col - 1] + str(square.row)


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
    robot = CheckerBot()

    while not game.is_over():
        # print(chr(27) + "[2J")
        print_board(game.board)
        if game.next_player == Player.red:
            human_choice = input('-- ')
            human_choice = move_from_coords(human_choice.strip())
            action = Action.play(human_choice)
        else:
            robot.update_board(game)
            robot.legal_moves()
            robot.print_moves()
            robot_choice = robot.choose_move()
            action = Action.play(robot_choice)
            print(action)
        # print_move(game.next_player, move)
        game = game.apply_action(action)


if __name__ == '__main__':
    main()

from checkertypes import Player, Square
import copy
from collections import namedtuple


__all__ = [
    'IllegalMoveError',
    'Checker',
    'Board',
    'Jump',
    'Move',
    'GameState'
]


class IllegalMoveError(Exception):
    pass


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

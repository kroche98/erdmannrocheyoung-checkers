#JMJ
#Agent.py
#An interface to work with the class competition.
#Programmed by Ben Campbell

"""
Board Conventions:

Ben and I discovered while trying to get our bots to play each other that we need a standard convention for numbering the board. We've decided on the following conventions:

1. The columns are numbered left to right from A to H.

2. The rows are numbered bottom to top from 1 to 8.

3. The black pieces are on the top of the board (rows 6-8), and the red pieces are on the bottom of the board (rows 1-3). The initial configuration is such that squares A1 and H8 have checkers, and squares A8 and H1 are empty.

For reference, the initial configuration should look like this (each 'b' is a black piece, and each 'r' is a red piece):

8 ███ b ███ b ███ b ███ b
7  b ███ b ███ b ███ b ███
6 ███ b ███ b ███ b ███ b
5    ███   ███   ███   ███
4 ███   ███   ███   ███  
3  r ███ r ███ r ███ r ███
2 ███ r ███ r ███ r ███ r
1  r ███ r ███ r ███ r ███
   A  B  C  D  E  F  G  H

When passing a move, the move should be stored in a tuple. The first element is the coordinates of the piece being moved. The second element is a list that contains the coordinates of the ending square, or the coordinates of all the steps in a multiple jump. Each coordinate should be a string of the form "AxB" where A is the x-coordinate (column) and B is the y-coordinate (row). For example, a move from E3 to D4 would be sent as ("5x3", ["4x4"]). A triple jump going from E3 to G5 to E7 to C5 would be sent as ("5x3", ["7x5", "5x7", "3x5"]).
"""

class Bot:

    def __init__(self, color):
        self.color = color

    def make_move(self):
        """
        Returns a tuple. The first is the coordinates for the piece that's moving.
        The second item is an array that contains the positions it
        ends up in or the steps in a multiple jump. All coordinates are in a string
        format "AxB" where A is the x coordinate and B is the Y coordinate.
        
        for a piece at (2,3) jumping to (4,5) and then (2,7)
            it should return ("2x3", ["4x5", "2x7"])
        """
        raise NotImplementedError()

    def receive_move(self, move):
        """
        Receives a move from the other bot and applies it to
        to its own gamestate. The move is in the same format that makemove sends in.

        If it receives an invalid move, it returns False.

        Else, it returns true.
        """
        raise NotImplementedError()

    def get_board_str(self):
        """
        returns a string representing the board. You can do this however you want,
        as long as it makes sense.
        """
        raise NotImplementedError()

    def undo_last_move(self):
        """
        called when the other bot returns false for recieve_move. This is sent to the
        bot who made the move, telling it to undo the last move it made. If the last move
        had several jumps, all of them are undone, so the board is in the same state it
        was in before the move was made.
        """
        raise NotImplementedError()

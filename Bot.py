#JMJ
#Agent.py
#An interface to work with the class competition.
#Programmed by Ben Campbell

class Bot:

    def __init__(self, color, botFolder):
        self.color = color

    def makemove(self):
        """
        Returns a tuple. The first is the piece that's moving
        The second item is an array that contains the posiitions it
        ends up in or the steps in a multiple jump.
        """
        raise NotImplementedError()

    def receiveMove(self, move):
        """
        Receives a move from the other bot and applies it to
        to its own gamestate.

        If it receives an invalid move, it returns False.

        Else, it returns true.
        """

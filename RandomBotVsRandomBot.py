# Note: before running, we need to download the opponent's bot
from BangsPepinCampbellRandomBot import RandomBot
from REY_Bot import REY_Bot
import os
import time

class Controller:

  def __init__(self, blackBot, redBot):
    self.redBot = redBot
    self.blackBot = blackBot

  def runGame(self):

    while True:
        blackMove = self.blackBot.makemove()
        print(f"black: {blackMove}")

        if blackMove == "resign":
            self.winner = self.redBot
            break

        self.redBot.receiveMove(blackMove)

        # os.system("cls")
        print(self.blackBot.board)
        self.redBot.print_board()
        time.sleep(0.1)

        redMove = self.redBot.makemove()
        print(F"red: {redMove}")

        if redMove == "resign":
            self.winner = self.blackBot
            break

        self.blackBot.receiveMove(redMove)

        # os.system("cls")
        print(self.blackBot.board)
        self.redBot.print_board()
        time.sleep(0.1)

    #print winner

def main():
    redBot = REY_Bot("red", None)
    blackBot = RandomBot("black", None)
    controller = Controller(blackBot, redBot)
    controller.runGame()

if __name__ == "__main__":
    main()
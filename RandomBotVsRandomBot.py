# from REY_Bot import REY_RandomBot
# from REY_Bot import REY_MonteCarloBot
from REY_Bot_onefile import REY_MonteCarloBot
import os
import time

class Controller:

    def __init__(self, black_bot, red_bot):
        self.red_bot = red_bot
        self.black_bot = black_bot
        self.winner = None

    def do_turn(self, mover, reciever):
        if self.winner != None:
            return
        
        move_is_valid = False

        while not move_is_valid:
            move = mover.make_move()

            if move == "resign":
                self.winner = reciever
                break

            move_is_valid = reciever.receive_move(move)
            if not move_is_valid:
                mover.undo_last_move()

        os.system("cls")
        print(self.black_bot.get_board_str())

    def run_game(self):
        print(self.black_bot.get_board_str())

        while self.winner == None:
            self.do_turn(self.black_bot, self.red_bot)
            self.do_turn(self.red_bot, self.black_bot)

        if self.winner == self.red_bot:
            print("Red wins!")
        else:
            print("Black wins!")

        input("Press a key to close")

def main():
    red_bot = REY_MonteCarloBot("red")
    black_bot = REY_MonteCarloBot("black")
    controller = Controller(black_bot, red_bot)
    controller.run_game()

if __name__ == "__main__":
    main()
Checkers Bot
CSC 410 Final Project
Patrick Erdmann, Kevin Roche, & Jude Young

----------

What's inside:

checkertypes.py : basic class definitions
checkerboard.py : checkers game structure and logic

agents/agent.py : Agent class
agents/deep_learning_bot.py : Agent which uses a neural network (not yet functional)
agents/dumb_checker_bot.py : Agent which selects random moves
agents/human_agent.py : Agent which prompts the user for a move
agents/monte_carlo_checker_bot : Agent which uses a Monte Carlo approach

ErdmannRocheYoungProg3.py : program to demonstrate functionality of agents

Bot.py : standard interface for competition
RandomBotVsRandomBot.py : API for competition

Encoder.py : encode a board for the neural network bot (WIP)
generatemontecarlogames.py : generate training data using the Monte Carlo bot (WIP)
networktrain.py : train the neural network (WIP)

REY_Bot.py : standard API driver for our bots
REY_Bot_onefile.py : a single file with everything necessary to play a game using the API

----------

To run a game, run ErdmannRocheYoungProg3.py. By changing player_1 and player_2 in the main function, different agents can be pitted against each other.

Currently the best bot is the MonteCarloCheckerBot. We've been working on a neural network bot, but it's not yet functional. Running generatemontecarlogames.py will generate training data and export it. Running networktrain.py will import the training data and train a model based on it, exporting this model for use by the bot. Unfortunately, the bot is not yet able to use this model to make predictions and select moves.

----------

Note that our internal representation uses Black and White. White is equivalent to Red.
import random
from textwrap import indent
import threading
import time
import numpy as np
from AlphaZero_version.chessEnvironment import ChessEnvironment
from AlphaZero_version.game import Game
from AlphaZero_version.agent import Agent
import argparse
import logging
logging.basicConfig(level=logging.INFO, format=" %(message)s")
logging.disable(logging.WARN)
import tensorflow as tf



class Main:
    def __init__(self, player: bool, local_predictions: bool = True, model_path: str = None):
        self.player = player
        self.opponent = Agent(local_predictions=local_predictions, model_path=model_path)

        if self.player:
            self.game = Game(ChessEnvironment(), self.opponent, self.opponent)
        else:
            self.game = Game(ChessEnvironment(), self.opponent, self.opponent)

        print("*" * 50)
        print(f"You play the {'white' if self.player else 'black'} pieces!")
        print("*" * 50)

        self.previous_moves = (None, None)

        thread = threading.Thread(target=self.play_game)
        thread.start()

    def play_game(self):
        self.game.reset()
        winner = None
        while winner is None:
            if self.player == self.game.turn:
                # self.get_player_move()
                # self.game.turn = not self.game.turn
                self.opponent_move()
            else:
                self.opponent_move()
                # self.GUI.make_move(self.game.environment.board.move_stack[-1])
            # check if the game is over
            if self.game.environment.board.is_game_over():
                # get the winner
                winner = Game.get_winner(self.game.environment.board.result(claim_draw=True))
                # show the winner but as string literal
                print("White wins" if winner == 1 else "Black wins" if winner == -1 else "Draw")

    # def get_player_move(self):
    #     while True:
    #         time.sleep(0.2)
    #         # break when the player has made a move
    #         try:
    #             if len(self.GUI.gameboard.board.move_stack) and not len(self.game.env.board.move_stack):
    #                 # player has made a move, but the move has not been added to the game yet
    #                 break
    #             if self.game.env.board.move_stack[-1] != self.GUI.gameboard.board.move_stack[-1]:
    #                 break
    #         except IndexError:
    #             continue
    #     self.game.env.board.push(self.GUI.gameboard.board.move_stack[-1])

    def opponent_move(self):
        self.previous_moves = self.game.play_move(stochastic=False, previous_moves=self.previous_moves,
                                                  save_moves=False)


if __name__ == "__main__":
    tf.debugging.set_log_device_placement(True)
    gpus = tf.config.list_logical_devices('GPU')
    print(gpus)
    # parser = argparse.ArgumentParser(description=__doc__)
    # parser.add_argument("--player", type=str, default=None, choices=('white', 'black'),
    #                     help="Whether to play as white or black. No argument means random.")
    # parser.add_argument('--local-predictions', action='store_true', help='Use local predictions instead of the server')
    # parser.add_argument("--model", type=str, default=None,
    #                     help="For local predictions: specify the path to the model to use.")
    # args = parser.parse_args()
    # args = vars(args)
    #
    # if args["local_predictions"]:
    #     if args["model"] is None:
    #         print("When using local predictions, specify the path to the model to use.")
    #         exit(1)
    #
    # model_path = args["model"]
    # local_predictions = args["local_predictions"]
    #
    # if args['player']:
    #     player = args['player'].lower().strip() == 'white'
    # else:
    #     player = np.random.choice([True, False])
    #
    # m = Main(False, True, model_path)
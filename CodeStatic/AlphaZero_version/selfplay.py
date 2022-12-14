#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import logging
from multiprocessing import Pool

import os
from random import choice, choices
from re import I
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import time
from AlphaZero_version.agent import Agent
from AlphaZero_version.chessEnvironment import ChessEnvironment
from AlphaZero_version.game import Game
from AlphaZero_version import config
import numpy as np
import chess
import pandas as pd

logging.basicConfig(level=logging.INFO, format=' %(message)s')


def setup(starting_position: str = chess.STARTING_FEN, local_predictions=False) -> Game:
    """
    Setup function to set up a game.
    This can be used in both the self-play and puzzle solving function
    """
    # set different random seeds for each process
    # number = int.from_bytes(socket.gethostname().encode(), 'little')
    # number *= os.getpid() if os.getpid() != 0 else 1
    # number *= int(time.time())
    # number %= 123456789

    # np.random.seed(number)
    # print(f"========== > Setup. Test Random number: {np.random.randint(0, 123456789)}")

    # create environment and game
    env = ChessEnvironment(fen=starting_position)

    # create agents
    model_path = os.path.join(config.MODEL_FOLDER, "model.h5")
    white = Agent(local_predictions, model_path, env.board.fen())
    black = Agent(local_predictions, model_path, env.board.fen())

    return Game(environment=env, white=white, black=black)


def self_play(local_predictions=True):
    """
    Continuously play games against itself
    """
    game = setup(local_predictions=local_predictions)

    # show_board = os.environ.get("SELFPLAY_SHOW_BOARD") == "true"

    # play games continuously
    # if show_board:
    #     gui = GUI(400, 400, game.env.board.turn)
    #     game.GUI = gui
    while True:
        # if show_board:
        #     game.GUI.gameboard.board.set_fen(game.env.board.fen())
            # game.GUI.draw()
        game.play_one_game(stochastic=True)


def puzzle_solver(puzzles, local_predictions=True):
    """
    Continuously solve puzzles
    """
    game = setup(local_predictions=local_predictions)

    # solve puzzles continuously
    while True:
        # shuffle pandas rows
        puzzles = puzzles.sample(frac=1).reset_index(drop=True)
        game.train_puzzles(puzzles)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run self-play or puzzle solver')
    parser.add_argument('--type', type=str, default='selfplay', choices=('selfplay', 'puzzles'),
                        help='selfplay or puzzles')
    parser.add_argument('--puzzle-file', type=str, default=None, help='File to load puzzles from (csv)')
    parser.add_argument('--puzzle-type', type=str, default='mateIn1',
                        help='Type of puzzles to solve. Make sure to set a puzzle move limit in config.py if necessary')
    parser.add_argument('--local-predictions', action='store_true', help='Use local predictions instead of the server')
    args = parser.parse_args()
    args = vars(args)

    if args['type'] == 'puzzles' and args['puzzle_file'] is None:
        raise argparse.ArgumentError('puzzle-file must be specified when type is puzzles')

    local_predictions = True
    # if args['local_predictions']:
    #     local_predictions = True
    # else:
    #     raise ValueError("Socket shuld not be applied")
    #     # wait until server is ready
    #     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    #     server = os.environ.get("SOCKET_HOST", "localhost")
    #     port = int(os.environ.get("SOCKET_PORT", 5000))
    #
    #     print("Checking if server is ready...")
    #     while s.connect_ex((server, port)) != 0:
    #         print(f"Waiting for server at {server}:{port}")
    #         time.sleep(1)
    #     print(f"Server is ready on {s.getsockname()}!")
    #     s.close()

    if args['type'] == 'selfplay':
        self_play(local_predictions)
    else:
        puzzles = Game.create_puzzle_set(filename=args['puzzle_file'], type=args['puzzle_type'])
        puzzle_solver(puzzles, local_predictions)
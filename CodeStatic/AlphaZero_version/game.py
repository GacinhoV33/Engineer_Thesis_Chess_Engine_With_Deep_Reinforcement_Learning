#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
from AlphaZero_version.chessEnvironment import ChessEnvironment
from AlphaZero_version.agent import Agent
from AlphaZero_version import utils
import logging
from AlphaZero_version import config
from chess.pgn import Game as ChessGame
from AlphaZero_version.edge import Edge
from AlphaZero_version.monteCarloSearchTree import MonteCarloSearchTree
import uuid
import pandas as pd
import numpy as np


class Game:
    def __init__(self, environment: ChessEnvironment, white: Agent, black: Agent):
        self.environment = environment
        self.white = white
        self.black = black
        self.memory = []

        self.reset()

    def reset(self):
        self.environment.reset()
        self.turn = self.environment.board.turn

    @staticmethod
    def get_winner(result: str) -> int:
        return 1 if result == '1-0' else -1 if result == '0-1' else 0

    @utils.time_function
    def play_one_game(self, stochastic: bool = True) -> int:
        self.reset()
        self.memory.append([])
        logging.info(f"\n {self.environment.board} \n")
        counter, previous_edges, full_game = 0, (None, None), True
        winner = 'None'
        while not self.environment.board.is_game_over():
            previous_edges = self.play_move(stochastic=stochastic, previous_moves=previous_edges)
            logging.info(f"\n{self.environment.board}")
            logging.info(f"Value according to white: {self.white.monteCarloSearchTree.root.value}")
            logging.info(f"Value according to black: {self.black.monteCarloSearchTree.root.value}")
            # if os.environ.get("SELFPLAY_SHOW_BOARD") == "true":
            #     self.GUI.gameboard.board.set_fen(self.env.board.fen())
            #     self.GUI.draw()
            counter += 1
            if counter > config.MAX_GAME_MOVES or self.environment.board.is_repetition(3):
                winner = ChessEnvironment.estimate_winner(self.environment.board)
                logging.info(f"Game Over by move limit. {config.MAX_GAME_MOVES}. Result: {winner}")
                full_game = False
                break
        if full_game:
            winner = Game.get_winner(self.environment.board.result())
            logging.info(f"Game over. Result: {winner}")

        for index, element in enumerate(self.memory[-1]):
            self.memory[-1][index] = (element[0], element[1], winner)

        game = ChessGame()
        # set starting position
        game.setup(self.environment.fen)
        # add moves
        node = game.add_variation(self.environment.board.move_stack[0])
        for move in self.environment.board.move_stack[1:]:
            node = node.add_variation(move)
        # print pgn
        logging.info(game)

        # save memory to file
        self.save_game(name="game", full_game=full_game)
        return winner

    def play_move(self, stochastic: bool = True, previous_moves: tuple = (None, None), save_moves: bool = True):
        current_player = self.white if self.turn else self.black
        if previous_moves[0] is None or previous_moves[1] is None:
            current_player.monteCarloSearchTree = MonteCarloSearchTree(current_player, state=self.environment.board.fen(), stochastic=stochastic)
        else:
            try:
                node = current_player.monteCarloSearchTree.root.get_edge(previous_moves[0].action).output_node
                node = node.get_edge(previous_moves[1].action).output_node
                current_player.monteCarloSearchTree.root = node
            except AttributeError:
                logging.warning("WARN: Node does not exist in tree, continuing with new tree...")
                current_player.mcts = MonteCarloSearchTree(current_player, state=self.environment.board.fen(), stochastic=stochastic)

        current_player.run_simulations(n=config.SIMULATIONS_PER_MOVE)

        moves = current_player.monteCarloSearchTree.root.edges
        if save_moves:
            self.save_to_memory(self.environment.board.fen(), moves)

        sum_move_visits = sum(edge.N for edge in moves)
        probs = [edge.N / sum_move_visits for edge in moves]

        if stochastic:
            best_move = np.random.choice(moves, p=probs)
        else:
            best_move = moves[np.argmax(probs)]

        logging.info(
            f"{'White' if self.turn else 'Black'} played  {self.environment.board.fullmove_number}. {best_move.action}")
        self.environment.step(best_move.action)

        self.turn = not self.turn

        return (previous_moves[1], best_move)

    def save_to_memory(self, state, moves):
        sum_move_visits = sum(edge.N for edge in moves)
        search_probabilities = {edge.action.uci() : edge.N / sum_move_visits for edge in moves}

        self.memory[-1].append((state, search_probabilities, None))

    def save_game(self, name: str = 'game', full_game: bool = False):
        game_id = f"{name}-{str(uuid.uuid4())[:8]}"
        if full_game:
            with open("full_games.txt", "a") as f:
                f.write(f"{game_id}.npy\n")
        np.save(os.path.join(config.MEMORY_DIR, game_id), self.memory[-1])
        logging.info(
            f"Game saved to {os.path.join(config.MEMORY_DIR, game_id)}.npy"
        )
        logging.info(f"Memory size: {len(self.memory)}")

    @utils.time_function
    def train_puzzles(self, puzzles: pd.DataFrame):
        """
        Create positions from puzzles (fen strings) and let the MCTS figure out how to solve them.
        The saved positions can be used to train the neural network.
        """
        logging.info(f"Training on {len(puzzles)} puzzles")
        for puzzle in puzzles.itertuples():
            self.environment.fen = puzzle.fen
            self.environment.reset()
            # play the first move
            moves = puzzle.moves.split(" ")
            self.environment.board.push_uci(moves.pop(0))
            logging.info(f"Puzzle to solve ({puzzle.rating} ELO): {self.env.fen}")
            logging.info(f"\n{self.environment.board}")
            logging.info(f"Correct solution: {moves} ({len(moves)} moves)")
            self.memory.append([])
            counter, previous_edges = 0, (None, None)
            while not self.environment.board.is_game_over():
                # deterministically choose the next move (we want no exploration here)
                previous_edges = self.play_move(stochastic=False, previous_moves=previous_edges)
                logging.info(f"\n{self.environment.board}")
                logging.info(f"Value according to white: {self.white.monteCarloSearchTree.root.value}")
                logging.info(f"Value according to black: {self.black.monteCarloSearchTree.root.value}")
                counter += 1
                if counter > config.MAX_PUZZLE_MOVES:
                    logging.warning("Puzzle could not be solved within the move limit")
                    break
            if not self.environment.board.is_game_over():
                continue
            logging.info(f"Puzzle complete. Ended after {counter} moves: {self.env.board.result()}")
            # save game result to memory for all games
            winner = Game.get_winner(self.env.board.result())
            for index, element in enumerate(self.memory[-1]):
                self.memory[-1][index] = (element[0], element[1], winner)

            game = ChessGame()
            # set starting position
            game.setup(self.environment.fen)
            # add moves
            node = game.add_variation(self.environment.board.move_stack[0])
            for move in self.environment.board.move_stack[1:]:
                logging.info(move)
                node = node.add_variation(move)
            # print pgn
            logging.info(game)

            # save memory to file
            self.save_game(name="puzzle")

    @staticmethod
    def create_puzzle_set(filename: str, type: str = "mateIn2") -> pd.DataFrame:
        """
        Load the puzzles from a csv file. The type of puzzle can be specified.
        Return the puzzles as a Pandas DataFrame.
        """
        start_time = time.time()
        puzzles: pd.DataFrame = pd.read_csv(filename, header=None)
        # drop unnecessary columns
        puzzles = puzzles.drop(columns=[0, 4, 5, 6, 8])
        # set column names
        puzzles.columns = ["fen", "moves", "rating", "type"]
        # only keep puzzles where type contains "mate"
        puzzles = puzzles[puzzles["type"].str.contains(type)]
        logging.info(f"Created puzzles in {time.time() - start_time} seconds")
        return puzzles
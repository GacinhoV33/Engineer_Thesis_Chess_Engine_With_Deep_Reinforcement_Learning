#!/usr/bin/python
# -*- coding: utf-8 -*-

from tensorflow.keras.models import Model
import chess
from network import create_init_positions, create_init_probabilities, create_init_position_eval, FEN_to_layers


class SelfPlay:
    def __init__(self, model: Model):
        self.model = model

    def playGames(self, starting_position: str = chess.STARTING_FEN, number_of_games: int = 10):
        positionData = create_init_positions()
        moveProbabilities = create_init_probabilities()
        positionEvalData = create_init_position_eval()

        board = chess.Board(fen=starting_position)

        while not board.is_game_over(claim_draw=True):
            positionData.append(board.fen())
            # moveProbabilities.append()
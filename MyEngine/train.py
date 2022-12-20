#!/usr/bin/python
# -*- coding: utf-8 -*-
from model import load_existing_model, NUMBER_OF_POSSIBLE_MOVES
import chess
from network import FEN_to_layers
import numpy as np

MODEL_NAME = 'basic_model'


def train(model_name: str = MODEL_NAME, number_of_games: int = 10, number_of_iterations: int = 10):
    model = load_existing_model(name=MODEL_NAME)

    for iteration in range(number_of_iterations):


        for game_number in range(number_of_games):


    sample_fen_position = chess.STARTING_FEN
    input_layers = FEN_to_layers(sample_fen_position)

    """Dummy DATA THERE -> REMOVE IT """
    x = np.array([input_layers, input_layers, input_layers, input_layers])
    y = [np.array([np.random.random_sample(size=(NUMBER_OF_POSSIBLE_MOVES, 1)), np.random.random_sample(size=(NUMBER_OF_POSSIBLE_MOVES, 1)),
               np.random.random_sample(size=(NUMBER_OF_POSSIBLE_MOVES, 1)), np.random.random_sample(size=(NUMBER_OF_POSSIBLE_MOVES, 1))]),
     np.array([0.1, 0.2, 0.1, -0.1])]
    print(y[0].shape, y[1].shape, x[0].shape)
    model.fit(x,
              y,
              epochs=10)
    print(input_layers.shape)
    policy_pred, value_pred = model.predict(np.array([input_layers]))

    print(f"Policy sorted, first 50: {policy_pred[:10]}")
    # model.predict()

train()

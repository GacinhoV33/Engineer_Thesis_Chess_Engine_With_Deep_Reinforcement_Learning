#!/usr/bin/python
# -*- coding: utf-8 -*-
from model import load_existing_model, NUMBER_OF_POSSIBLE_MOVES
import chess
from MoveMapping import map_valid_move
from network import FEN_to_layers
import numpy as np
from self_play import SelfPlay
from model import NUMBER_OF_CONSIDERED_POSITIONS
from tqdm import tqdm

MODEL_NAME = 'basic_model'
NUMBER_OF_EPOCHS_PER_GAME = 10


def prediction_to_moves(policy_prediction: np.array) -> str:
    raise NotImplementedError()


def train(model_name: str = MODEL_NAME, number_of_games: int = 10, number_of_iterations: int = 10):
    model = load_existing_model(name=model_name)
    self_play = SelfPlay(model=model)

    for iteration in range(number_of_iterations):
        """Initialize number of games data"""
        position_data_records = list()
        move_probabilities_data_records = list()
        position_evaluation_data_records = list()

        for game_number in range(number_of_games):
            position_data, moveProbabilitiesData, positionEvalData = self_play.playGame()
            # moveProbabilitiesData = np.zeros(shape=(73, 8, 8))
            position_data_records.append(position_data)
            moveProbabilitiesDataConverted = list()
            for i, record in enumerate(moveProbabilitiesData[NUMBER_OF_CONSIDERED_POSITIONS:]):
                moveProbabilities = np.zeros(shape=(73, 8, 8))
                for move, val, _, _ in record:
                    move, plane_index, col, row = map_valid_move(move, chess.Board(position_data[i]))
                    moveProbabilitiesData[plane_index][col][row] = val
                moveProbabilitiesDataConverted.append(moveProbabilities.reshape((NUMBER_OF_POSSIBLE_MOVES, 1)))

            move_probabilities_data_records.append(moveProbabilitiesDataConverted)
            position_evaluation_data_records.append(position_data_records)

            # if len(position_data) - 4 != len(moveProbabilitiesData):
            print(f"len of position: {len(position_data)}")
            print(f"len of posEvaldata: {len(positionEvalData)}")
            print(f"len of moveProbData: {len(moveProbabilitiesData)}")
                # raise ValueError("Different length of training set")
            data_length = len(position_data)
            x_train = [FEN_to_layers(position_data[i+NUMBER_OF_CONSIDERED_POSITIONS:i+NUMBER_OF_CONSIDERED_POSITIONS+NUMBER_OF_CONSIDERED_POSITIONS]) for i in range(data_length - NUMBER_OF_CONSIDERED_POSITIONS)] # -1 is last position where is no available moves
            y_train = [moveProbabilitiesData[NUMBER_OF_CONSIDERED_POSITIONS:], positionEvalData[NUMBER_OF_CONSIDERED_POSITIONS: -1]]


            """Mapping moves to format of network output :) """

            print(f"MoveProbData len: {len(moveProbabilitiesData[NUMBER_OF_CONSIDERED_POSITIONS:])} ")
            print(f"MoveEvalData len: {len(positionEvalData[NUMBER_OF_CONSIDERED_POSITIONS: -1])}")


            model.fit(x_train, y_train, epochs=NUMBER_OF_EPOCHS_PER_GAME)
            print(f"Training process, game: {game_number}")


    """ Save model there"""
    #TODO Implement
        # sample_fen_position = chess.STARTING_FEN
        # input_layers = FEN_to_layers(sample_fen_position)

    # """Dummy DATA THERE -> REMOVE IT """
    # input_layers = FEN_to_layers(chess.STARTING_FEN)
    # x = np.array([input_layers, input_layers, input_layers, input_layers])
    # y = [np.array([np.random.random_sample(size=(NUMBER_OF_POSSIBLE_MOVES, 1)), np.random.random_sample(size=(NUMBER_OF_POSSIBLE_MOVES, 1)),
    #            np.random.random_sample(size=(NUMBER_OF_POSSIBLE_MOVES, 1)), np.random.random_sample(size=(NUMBER_OF_POSSIBLE_MOVES, 1))]),
    #  np.array([0.1, 0.2, 0.1, -0.1])]
    # print(y[0].shape, y[1].shape, x[0].shape)
    # print(f"Training process, game: {game_number}")
    # model.fit(x,
    #           y,
    #           epochs=NUMBER_OF_EPOCHS_PER_GAME)
    # print(input_layers.shape)
    # policy_pred, value_pred = model.predict(np.array([input_layers]))
    #
    # print(f"Policy sorted, first 50: {policy_pred[:10]}")
    # model.predict()


train()
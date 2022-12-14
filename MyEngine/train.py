#!/usr/bin/python
# -*- coding: utf-8 -*-
from model import load_existing_model, NUMBER_OF_POSSIBLE_MOVES
import chess
from MoveMapping import map_valid_move
from network import FEN_to_layers
import numpy as np
from self_play import SelfPlay
from settings import NUMBER_OF_EPOCHS_PER_GAME, MODEL_NAME, NUMBER_OF_CONSIDERED_POSITIONS, \
    NUMBER_OF_GAMES_PER_ITERATION, NUMBER_OF_ITERATION_IN_TRAINING, N_MCTS_ITERATION, POLICY_SHAPE_3D, \
    NUMBER_OF_EPOCHS_PER_ITERATION
import sqlite3
import datetime
from time import time
from tqdm import tqdm
import matplotlib.pyplot as plt


def create_history_db():
    con = sqlite3.connect('./models/training_history.db')
    cur = con.cursor()
    cur.execute("""CREATE TABLE history(training_date text, 
                                        number_of_games INTEGER, 
                                        number_of_MCTS_simulations INTEGER, 
                                        n_of_draws INTEGER,
                                        n_of_white_wins INTEGER,
                                        n_of_black_wins INTEGER,
                                        games_not_ended INTEGER, 
                                        time_of_learning text)""")


def add_record(n_of_games: int, n_of_MCTS: int, n_of_draws: int, n_of_white_wins: int, n_of_black_wins: int, games_not_ended: int, time_of_learning: str) -> bool:
    try:
        now = datetime.datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        con = sqlite3.connect('./models/training_history.db')
        cur = con.cursor()
        cur.execute("""INSERT INTO history VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (dt_string, n_of_games, n_of_MCTS, n_of_draws, n_of_white_wins, n_of_black_wins, games_not_ended, time_of_learning))
        con.commit()
        con.close()
        return True
    except Exception as e:
        return False


def read_all():
    conn = sqlite3.connect('./models/training_history.db')
    c = conn.cursor()
    c.execute("""SELECT rowid,* from history
        """)
    for el in c.fetchall():
        print(el)
    conn.close()


def plot_results(loss, policy_loss, value_loss, game_number: int=0, n_epochs=20):
    epochs = [i for i in range(1, n_epochs+1)]
    plt.figure()
    plt.plot(epochs, loss, label='Loss')
    plt.plot(epochs, value_loss, label='Value head loss')
    plt.plot(epochs, policy_loss, label='Policy head loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Self-play game training history')
    plt.legend()
    plt.grid()
    plt.show()
    plt.savefig(f'Loss of game{game_number}')


def train(model_name: str = MODEL_NAME, number_of_games: int = 10, number_of_iterations: int = 10):
    model = load_existing_model(name=model_name)
    self_play = SelfPlay(model=model)

    time_start = time()
    black_wins = 0
    white_wins = 0
    draws = 0
    games_not_ended = 0
    for iteration in tqdm(range(number_of_iterations)):
        """Initialize number of games data"""
        position_data_records = list()
        move_probabilities_data_records = list()
        position_evaluation_data_records = list()
        x_general: np.array
        y_general: list = []
        for game_number in range(number_of_games):
            position_data, moveProbabilitiesData, positionEvalData = self_play.playGame()
            """Increasing data"""
            result = positionEvalData[-1]
            if 0.4 <= result:
                white_wins += 1
            elif -0.4 <= result <= 0.4:
                draws += 1
            elif result <= -0.4:
                black_wins += 1
            else:
                games_not_ended += 1

            moveProbabilitiesDataConverted = list()
            for i, record in enumerate(moveProbabilitiesData[NUMBER_OF_CONSIDERED_POSITIONS:]):
                moveProbabilities = np.zeros(shape=POLICY_SHAPE_3D)
                for move, val, _, _ in record:
                    move, plane_index, col, row = map_valid_move(move, chess.Board(position_data[i+NUMBER_OF_CONSIDERED_POSITIONS]))
                    moveProbabilities[plane_index][col][row] = val
                moveProbabilitiesDataConverted.append(moveProbabilities.reshape((NUMBER_OF_POSSIBLE_MOVES, 1)))

            """Adding records to n-games database"""
            move_probabilities_data_records.append(moveProbabilitiesDataConverted)
            position_evaluation_data_records.append(position_data_records)
            position_data_records.append(position_data)

            data_length = len(position_data)
            posEvalDataTrain = [np.array([evaluation]) for evaluation in positionEvalData[NUMBER_OF_CONSIDERED_POSITIONS:]]
            if game_number == 0:
                x_general = np.array([FEN_to_layers(position_data[NUMBER_OF_CONSIDERED_POSITIONS+i: NUMBER_OF_CONSIDERED_POSITIONS+i+NUMBER_OF_CONSIDERED_POSITIONS]) for i in range(data_length - NUMBER_OF_CONSIDERED_POSITIONS)])
                y_general = [np.array(moveProbabilitiesDataConverted), np.array(posEvalDataTrain)]
            else:
                x_new_game = np.array([FEN_to_layers(position_data[NUMBER_OF_CONSIDERED_POSITIONS+i: NUMBER_OF_CONSIDERED_POSITIONS+i+NUMBER_OF_CONSIDERED_POSITIONS]) for i in range(data_length - NUMBER_OF_CONSIDERED_POSITIONS)]) # -1 is last position where is no available moves
                x_last = x_general
                y_last = y_general
                x_general = np.append(x_last, x_new_game, axis=0)
                y_general = [np.append(y_last[0], np.array(moveProbabilitiesDataConverted), axis=0), np.append(y_last[1], np.array(posEvalDataTrain), axis=0)]

            print(f"Training process, game: {game_number+1}")
            # training_history = model.fit(x_train, y_train, epochs=NUMBER_OF_EPOCHS_PER_GAME)
            """Plotting history of training."""
            # data = training_history.history
            # loss = data['loss']
            # policy_loss = data['policy_head_loss']
            # value_loss = data['value_head_loss']
            # plot_results(loss, policy_loss, value_loss, game_number, NUMBER_OF_EPOCHS_PER_GAME)
            print(f"Saving model: iteration: {iteration + 1} - game: {game_number + 1}")
        training_history = model.fit(x_general, y_general, epochs=NUMBER_OF_EPOCHS_PER_ITERATION)
        data = training_history.history
        loss = data['loss']
        policy_loss = data['policy_head_loss']
        value_loss = data['value_head_loss']
        # plot_results(loss, policy_loss, value_loss, number_of_games, NUMBER_OF_EPOCHS_PER_GAME)
    model.save('./models/' + model_name + '.keras')
    time_end = time()
    time_of_training = time_end - time_start
    save_history_result = add_record(NUMBER_OF_GAMES_PER_ITERATION * NUMBER_OF_ITERATION_IN_TRAINING, N_MCTS_ITERATION,
                                     draws, white_wins, black_wins, games_not_ended, str(time_of_training))
    if save_history_result:
        print("Data of training added successfully!")
    else:
        print("Data of training didn't append successfully!!!")

    print("Training has ended")
    print(f"Black wins: {black_wins}")
    print(f"White wins: {white_wins}")
    print(f"Draws: {draws}")
    print(f"Without result:{games_not_ended}")
    print(f"Trainging last for: {time_of_training} seconds.")


if __name__ == "__main__":
    train(model_name='model_12_res', number_of_iterations=NUMBER_OF_ITERATION_IN_TRAINING, number_of_games=NUMBER_OF_GAMES_PER_ITERATION)
    read_all()
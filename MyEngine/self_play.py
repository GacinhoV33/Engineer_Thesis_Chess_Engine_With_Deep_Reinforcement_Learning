#!/usr/bin/python
# -*- coding: utf-8 -*-

from tensorflow.keras.models import Model
import chess
import numpy as np
from network import create_init_positions, create_init_probabilities
from MonteCarloTreeSearch import Edge, Node, MCTS
from model import load_existing_model
from settings import LIMIT_OF_MOVES_PER_GAME
import chess.engine


def stockfish_evaluation(board, time_limit=2.5):
    engine = chess.engine.SimpleEngine.popen_uci("./models/stockfish_15.1_win_x64_popcnt/stockfish-windows-2022-x86-64-modern.exe")
    result = engine.analyse(board, chess.engine.Limit(time=time_limit))
    engine.close()
    return result['score']


class SelfPlay:
    def __init__(self, model: Model):
        self.model = model

    def playGame(self, starting_position: str = chess.STARTING_FEN):
        positionData: list = create_init_positions()
        moveProbabilitiesData: list = create_init_probabilities()
        positionEvalData: list = list()

        """List 5 positions in fen format"""
        history: list = create_init_positions()
        board: chess.Board = chess.Board(fen=starting_position)
        stock_flag = False
        move_counter = 0
        while not board.is_game_over() and move_counter <= LIMIT_OF_MOVES_PER_GAME:
            move_counter += 1
            history.pop(0)
            positionData.append(board.fen()), history.append(board.fen())

            """Start MCTS"""
            rootEdge = Edge(None, None)
            rootNode = Node(board, rootEdge, history)
            mcts = MCTS(self.model)
            moveProbs = mcts.search(rootNode)
            moveProbsSorted = sorted(moveProbs, key= lambda x: x[1], reverse=True)
            probs = np.array([prob[1] for prob in moveProbsSorted])
            rand_idx = np.random.multinomial(1, probs)

            idx = np.where(rand_idx == 1)[0][0]
            nextMove = moveProbsSorted[idx]
            moveProbabilitiesData.append(moveProbsSorted)
            print(f"move {move_counter}: {nextMove[0]}")

            if move_counter % 50 == 0:
                stock_eval = stockfish_evaluation(board, 2)
                if stock_eval.is_mate():
                    move_counter += 1000
                    stock_flag = True
            if not stock_flag or move_counter == LIMIT_OF_MOVES_PER_GAME:
                board.push(nextMove[0])
        else:
            print(board)
            result = board.result()
            stock_eval = stockfish_evaluation(board, 2.5)
            if stock_eval.is_mate():
                stock_flag = True
                mate = stock_eval.pov(color=chess.WHITE)
                if str(mate)[1] == '+':
                    stock_eval = 1200
                elif str(mate)[1] == '-':
                    stock_eval = -1200
                else:
                    stock_eval = 0.0
            else:
                stock_eval = stock_eval.pov(color=chess.WHITE).cp
            print(f"Stock eval: {stock_eval}")
            for j in range(0, len(moveProbabilitiesData)):
                if stock_flag or result == '*':
                    positionEvalData.append(stock_eval / 1200)
                elif result == '1-0':
                    positionEvalData.append(1)
                elif result == '0-1':
                    positionEvalData.append(-1)
                elif result == '1/2-1/2':
                    positionEvalData.append(0)
            print(f"Len of data position: {len(positionEvalData)}, len of postion data: {len(positionData)}")
            return positionData, moveProbabilitiesData, positionEvalData


if __name__ == "__main__":
    selfPlay = SelfPlay(model=load_existing_model())
    game_data = selfPlay.playGame()
    position_data, moveProbabilitiesData, positionEvalData = game_data
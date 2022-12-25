#!/usr/bin/python
# -*- coding: utf-8 -*-

from tensorflow.keras.models import Model
import chess
import numpy as np
from model import NUMBER_OF_POSSIBLE_MOVES
from network import create_init_positions, create_init_probabilities, create_init_position_eval, FEN_to_layers
from MonteCarloTreeSearch import Edge, Node, MCTS
from model import load_existing_model


class SelfPlay:
    def __init__(self, model: Model):
        self.model = model

    def playGame(self, starting_position: str = chess.STARTING_FEN):
        positionData: list = create_init_positions()
        moveProbabilitiesData: list = [create_init_probabilities()]
        positionEvalData: list = [create_init_position_eval()]

        """List 5 positions in fen format"""
        history: list = create_init_positions()
        board: chess.Board = chess.Board(fen=starting_position)

        move_counter = 0
        while not board.is_game_over() and move_counter < 20: # claim_draw = True #TODO
            move_counter += 1
            history.pop(0)
            positionData.append(board.fen()), history.append(board.fen())

            """Start MCTS"""
            rootEdge = Edge(None, None)
            rootNode = Node(board, rootEdge, history)
            mcts = MCTS(self.model)
            moveProbs = mcts.search(rootNode)
            #TODO keep only legal moves
            #TODO Normalization of probability
            moveProbsSorted = sorted(moveProbs, key= lambda x: x[1], reverse=True)
            probs = np.array([prob[1] for prob in moveProbsSorted])
            rand_idx = np.random.multinomial(1, probs)

            idx = np.where(rand_idx == 1)[0][0]
            nextMove = moveProbsSorted[idx]
            print(move_counter)
            print(f'nextMove: {nextMove}')
            print(board)

            moveProbabilitiesData.append(moveProbsSorted)
            board.push(nextMove[0])

        else:
            result = board.outcome(claim_draw=True)
            for j in range(0, len(moveProbabilitiesData)):
                if result == chess.WHITE:
                    positionEvalData.append(1)
                elif result == chess.BLACK:
                    positionEvalData.append(-1)
                else:
                    positionEvalData.append(0)
            return positionData, moveProbabilitiesData, positionEvalData


if __name__ == "__main__":
    selfPlay = SelfPlay(model=load_existing_model())
    game_data = selfPlay.playGame()
    position_data, moveProbabilitiesData, positionEvalData = game_data

    x = 2

# 443 positions
# 439
# 885
#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from model import load_model

from MonteCarloTreeSearch import Edge, Node, MCTS
import chess
import time

if __name__ == "__main__":
    fen: str = 'r1bqk2r/pppp1ppp/2n2n2/2b1p1B1/4P3/2NP1N2/PPP2PPP/R2QKB1R b KQkq - 2 5'
    board: chess.Board = chess.Board(fen)

    N_OF_MCTS_SIMULATION: list = [i * 20 + 20 for i in range(50)]
    history: list = [
      'rnbqk1nr/pppp1ppp/8/2b1p3/4P3/2N2N2/PPPP1PPP/R1BQKB1R b KQkq - 3 3'
    , 'r1bqk1nr/pppp1ppp/2n5/2b1p3/4P3/2N2N2/PPPP1PPP/R1BQKB1R w KQkq - 4 4'
    , 'r1bqk1nr/pppp1ppp/2n5/2b1p3/4P3/2NP1N2/PPP2PPP/R1BQKB1R b KQkq - 0 4'
    , 'r1bqk2r/pppp1ppp/2n2n2/2b1p3/4P3/2NP1N2/PPP2PPP/R1BQKB1R w KQkq - 1 5'
    , 'r1bqk2r/pppp1ppp/2n2n2/2b1p1B1/4P3/2NP1N2/PPP2PPP/R2QKB1R b KQkq - 2 5'
    ]

    time_list = list()
    model = load_model('../models/' + 'model_12_res' + '.keras')

    for N_MCTS in N_OF_MCTS_SIMULATION:
        t_start = time.time()
        """ Find best move """
        rootEdge = Edge(None, None)
        rootNode = Node(board, rootEdge, history)
        mcts = MCTS(model, N_MCTS)
        moveProbs = mcts.search(rootNode)
        moveProbsSorted = sorted(moveProbs, key=lambda x: x[1], reverse=True)
        probs = np.array([prob[1] for prob in moveProbsSorted])
        rand_idx = np.random.multinomial(1, probs)
        idx = np.where(rand_idx == 1)[0][0]
        nextMove = moveProbsSorted[idx]

        t_end = time.time()
        time_of_simulation = t_end - t_start
        time_list.append(time_of_simulation)

    plt.figure(num=1)
    plt.plot(N_OF_MCTS_SIMULATION[1:], time_list[1:])
    plt.xlabel("Ilość symulacji MCTS")
    plt.ylabel("Czas (s)")
    plt.grid()
    plt.title("Czas znajdywania najlepszego ruchu w pozycji")
    plt.show()
    plt.savefig('MCTS_time')
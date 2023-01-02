#!/usr/bin/python
# -*- coding: utf-8 -*-
import chess
import stockfish
from stockfish import Stockfish
from MonteCarloTreeSearch import Edge, Node, MCTS
import numpy as np
from network import create_init_positions
from model import load_model

N_OF_GAMES_PER_LEVEL = 10

# model = load_model('../models/model_12_res.keras')
eng = Stockfish(r'C:\Users\gacek\Downloads\stockfish-11-win\stockfish-windows-2022-x86-64-avx2.exe')



def best_Reinf_move(board, history):
    history.pop(0)
    history.append(board.fen())
    rootEdge = Edge(None, None)
    rootNode = Node(board, rootEdge, history)
    mcts = MCTS(model)
    moveProbs = mcts.search(rootNode)
    moveProbsSorted = sorted(moveProbs, key=lambda x: x[1], reverse=True)
    probs = np.array([prob[1] for prob in moveProbsSorted])
    rand_idx = np.random.multinomial(1, probs)
    idx = np.where(rand_idx == 1)[0][0]
    nextMove = moveProbsSorted[idx]
    return nextMove


def getStockfishMove(board):
    engine.set_fen_position(board.fen())
    best_move = engine.get_best_move()
    print(best_move)
    return best_move


def playGame(level: int, stockfish_color: chess.Color) -> int:
    engine.set_skill_level(level)
    board: chess.Board = chess.Board(fen=chess.STARTING_FEN)
    history: list = create_init_positions()
    if stockfish_color == chess.WHITE:
        while board.is_game_over():
            """Stockfish start"""
            print(board)
            white_move = getStockfishMove(board)
            print(white_move)
            board.push_uci(white_move)
            history.pop(0)
            history.append(board.fen())
            """My Engine with black"""
            black_move = best_Reinf_move(board, history)
            board.push(black_move)
            print(board)
            print(f"move: {black_move}")

    elif stockfish_color == chess.BLACK:
        while board.is_game_over():
            """My engine starts with white"""
            white_move = best_Reinf_move(board, history)
            board.push(white_move)
            """Stockfish with Black"""
            black_move = getStockfishMove()
            board.push(black_move)
            history.pop(0)
            history.append(board.fen())

    if stockfish_color == chess.WHITE:
        if board.outcome() == 1.0:
            return -1
        elif board.outcome() == -1.0:
            return 1
        else:
            return 0
    elif stockfish_color == chess.BLACK:
        if board.outcome() == 1.0:
            return 1
        elif board.outcome() == -1.0:
            return -1
        else:
            return 0


def main():
    amatour_results: list = list()
    begginer_results: list = list()
    intermediate1_results: list = list()
    intermediate2_results: list = list()
    results = [amatour_results, begginer_results, intermediate1_results, intermediate2_results]

    for level, result in enumerate(results, 1):
        for i in range(N_OF_GAMES_PER_LEVEL):
            stockfish_color = chess.WHITE if i % 2 == 0 else chess.BLACK
            outcome = playGame(level=level, stockfish_color=stockfish_color)
            if outcome == 1:
                pass
            elif outcome == 0:
                pass
            elif outcome == -1.0:
                pass


def play_vs_stockfish(level: int):
    pass


if __name__ == "__main__":
    # main()
    # playGame(1, chess.WHITE)
    pass

#!/usr/bin/python
# -*- coding: utf-8 -*-
import chess
from stockfish import Stockfish, StockfishException
from MonteCarloTreeSearch import Edge, Node, MCTS
from network import create_init_positions
from model import load_model

N_OF_GAMES_PER_LEVEL = 2

options = {
    "Debug Log File": "",
    "Contempt": 0,
    "Min Split Depth": 0,
    "Threads": 1, # More threads will make the engine stronger, but should be kept at less than the number of logical processors on your computer.
    "Ponder": "false",
    "Hash": 16, # Default size is 16 MB. It's recommended that you increase this value, but keep it as some power of 2. E.g., if you're fine using 2 GB of RAM, set Hash to 2048 (11th power of 2).
    "MultiPV": 1,
    "Skill Level": 1,
    "Move Overhead": 5,
    "Minimum Thinking Time": 20,
    "Slow Mover": 100,
    "UCI_Chess960": "false",
    "UCI_LimitStrength": "false",
    "UCI_Elo": 200
}

engine = Stockfish(path="C:/Users/gacek/Desktop/VII_Semestr/Inzynierka/Repo/Engineer_Thesis_Chess_Engine_With_Deep_Reinforcement_Learning/MyEngine/models/stockfish_15.1_win_x64_popcnt/stockfish-windows-2022-x86-64-modern.exe", parameters=options)
engine.set_fen_position(chess.STARTING_FEN)
engine.set_depth(2)
model = load_model('../models/model_12_res.keras')


def best_Reinf_move(board, history):
    history.pop(0)
    history.append(board.fen())
    rootEdge = Edge(None, None)
    rootNode = Node(board, rootEdge, history)
    mcts = MCTS(model, 400)
    moveProbs = mcts.search(rootNode)
    moveProbsSorted = sorted(moveProbs, key=lambda x: x[1], reverse=True)
    nextMove = moveProbsSorted[0] # best Move according to probs
    return nextMove[0]


def getStockfishMove(board):
    engine.set_fen_position(board.fen())
    best_move = engine.get_best_move()
    return best_move


def playGame(level: int, stockfish_color: chess.Color) -> int:
    engine.set_skill_level(level)
    board: chess.Board = chess.Board(fen=chess.STARTING_FEN)
    history: list = create_init_positions()
    if stockfish_color == chess.WHITE:
        while not board.is_game_over():
            """Stockfish start"""
            print(board)
            white_move = getStockfishMove(board)
            print(f"White move: {white_move}")
            board.push_uci(white_move)
            history.pop(0)
            history.append(board.fen())
            """My Engine with black"""
            black_move = best_Reinf_move(board, history)
            board.push(black_move)
            print(board)
            print(f"Black move: {black_move}")

    elif stockfish_color == chess.BLACK:
        while not board.is_game_over():
            """My engine starts with white"""
            white_move = best_Reinf_move(board, history)
            board.push(white_move)
            """Stockfish with Black"""
            black_move = getStockfishMove(board)
            board.push_uci(black_move)
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
            print(f"Game: {i+1}. Outcome: {outcome}")

if __name__ == "__main__":
    main()
    # playGame(1, chess.WHITE)
    # pass

#!/usr/bin/python
# -*- coding: utf-8 -*-

import chess
import chess.engine
import chess.pgn
import numpy as np
from tensorflow.keras.models import load_model
from stockfish import Stockfish, StockfishException
from MonteCarloTreeSearch import Edge, Node, MCTS
# engine = chess.engine.SimpleEngine("./models/stoc")
# engine = chess.engine.SimpleEngine.popen_uci("./models/stockfish_15.1_win_x64_popcnt/stockfish-windows-2022-x86-64-modern.exe")
# engine.configure()
from network import create_init_positions

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
model = load_model('./models/model_12_res.keras')


def best_Reinf_move(board, history):
    history.pop(0)
    history.append(board.fen())
    rootEdge = Edge(None, None)
    rootNode = Node(board, rootEdge, history)
    mcts = MCTS(model, 400)
    moveProbs = mcts.search(rootNode)
    moveProbsSorted = sorted(moveProbs, key=lambda x: x[1], reverse=True)
    probs = np.array([prob[1] for prob in moveProbsSorted])
    rand_idx = np.random.multinomial(1, probs)
    # idx = np.where(rand_idx == 1)[0][0]
    nextMove = moveProbsSorted[0]
    return nextMove[0]


def getStockfishMove(board):
    engine.set_fen_position(board.fen())
    best_move = engine.get_best_move()
    # print(best_move)
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
            # result.append(outcome)
            print(outcome)
            # print(f"Level: {level} - Result: {result}")
            # if outcome == 1:
            #     result.append(outcome)
            # elif outcome == 0:
            #     pass
            # elif outcome == -1.0:
            #     pass


def play_vs_stockfish(level: int):
    pass


if __name__ == "__main__":
    main()
    # playGame(1, chess.WHITE)
    # pass


# def stockfish_evaluation(board, time_limit=2.5):
#     engine = chess.engine.SimpleEngine.popen_uci("./models/stockfish_15.1_win_x64_popcnt/stockfish-windows-2022-x86-64-modern.exe")
#     result = engine.analyse(board, chess.engine.Limit(time=time_limit))
#     engine.close()
#     return result['score']
#
# arr1 = np.ones((41, 75, 8, 8))
# arr2 = np.zeros((20, 75, 8, 8))
#
# arr3 = np.append(arr1, arr2, axis=0)
# print(arr3.shape)
# x = stockfish_evaluation(chess.Board(fen='rnbqkbnr/2pp1ppp/pp6/4p3/2B1P3/5Q2/PPPP1PPP/RNB1K1NR w KQkq - 0 4')).pov(color=chess.WHITE)
# print(str(x)[1:])
# print(int(-1)

# x1 = [[2], [4], [6], [7]]
# x2 = [[2], [4], [4], [3]]
#
# general = list()
# for el in x1:
#     general.append(el)
# # general.append([el for el in x1])
# print(general)
# mate_fen = 'rnbqkbnr/2pp1ppp/pp6/4p3/2B1P3/8/PPPP1QPP/RNB1K1NR w KQkq - 0 4'
# board = chess.Board(fen=mate_fen)
# x2 = board.result()
# print(board.is_checkmate())
# print(x2)
# #
# board.push(chess.Move.from_uci('a2a3'))
# board.push(chess.Move.from_uci('a7a6'))
# board.push(chess.Move.from_uci('a3a4'))
# board.push(chess.Move.from_uci('a6a5'))
# board.push(chess.Move.from_uci('a1a3'))
# board.push(chess.Move.from_uci('a8a6'))
#
# node = chess.pgn.Game.from_board(board)
# # print(node.headers['Result'])
# print(node.game().mainline())
# # board.push(chess.Move(chess.Square('a7'), chess.Square('a7')))
# with open('pgn/pgn.txt', 'w') as file:
#     file.write(str(node.game().mainline()))

# board.push(chess.Move('a7a6'))
# board = chess.Board(fen='')
# arr1 = np.ones((8, 8))
# arr2 = np.ones((8, 8))
#
# output = np.array([arr1, arr2])
# print(output.shape)
#
# board = chess.Board(fen=chess.STARTING_FEN)
# print(board.outcome())
#
#
# def stockfish_evaluation(board, time_limit=2.5):
#     engine = chess.engine.SimpleEngine.popen_uci("./models/stockfish_15.1_win_x64_popcnt/stockfish-windows-2022-x86-64-modern.exe")
#     result = engine.analyse(board, chess.engine.Limit(time=time_limit))
#     stock_eval = result['score']
#     print(stock_eval.pov(color=chess.WHITE).mate())
#     #     print("White mat")
#     # elif stock_eval.pov(color=chess.WHITE)[1] == '-':
#     #     print("Black mat")
#     if result['score'].is_mate():
#         print(result['score'].pov(color=chess.BLACK))
#         return 400
#
#     else:
#         return result['score'].pov(color=chess.WHITE).cp
#     return result['score']
#
# board = chess.Board(fen='r5rk/5p1p/5R2/4B3/8/8/7P/7K w')
# print(stockfish_evaluation(board))

#
# codes, i = {}, 0
# for nSquares in range(1,8):
#     for direction in ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]:
#         codes[(nSquares,direction)] = i
#         i += 1
# print(codes)
#
# for two in ["N","S"]:
#     for one in ["E","W"]:
#         codes[("knight", two, one)] , i = i , i + 1
# for two in ["E","W"]:
#     for one in ["N","S"]:
#         codes[("knight", two, one)] , i = i , i + 1
#
# for move in ["N","NW","NE"]:
#     for promote_to in ["Rook","Knight","Bishop"]:
#         codes[("underpromotion", move, promote_to)] , i = i , i + 1
# print(codes)
#
# policy = np.zeros((8,8,73))
# columns = { k:v for v,k in enumerate("abcdefgh")}
#
# e4policy = np.zeros((8,8,73))
# e4policy[ columns['e'] , 2 - 1 , codes[(2 , "N")]] = 1
# print(policy)
# NF3policy = np.zeros((8,8,73))
# NF3policy[ columns['g'], 1 - 1, codes[("knight", 'N', 'W')]] = 1
# #
# #
# #
# #
# #
# #
# # moves_dict = {}
# # letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
# # numbers = ['1', '2', '3', '4', '5', '6', '7', '8']
# # not_legal_moves_counter = 0
# # legal_moves_counter = 0
# #
# # possible_moves = [[] for _ in range(64)]
# # for i, letter in enumerate(letters):
# #     for j, number in enumerate(numbers):
# #         move = letter + number
# #         square = (i+1, j+1)
# #         # possible_moves = []
# #         # 'a4'
#         for m in range(8):
#             for n in range(8):
#                 if m == i and n != j:
#                     moves_dict[f'{move}'] = f'{letters[m]}{numbers[n]}'
#                     print(i*8 + j)
#                     possible_moves[i * 8 + j].append(f'{letters[m]}{numbers[n]}')
#                     legal_moves_counter += 1
#                 elif m != i and n == j:
#                     moves_dict[f'{move}'] = f'{letters[m]}{numbers[n]}'
#                     possible_moves[i * 8 + j].append(f'{letters[m]}{numbers[n]}')
#                     legal_moves_counter += 1
#                 elif abs(m - i) == abs(n - j) != 0:
#                     moves_dict[f'{move}'] = f'{letters[m]}{numbers[n]}'
#                     legal_moves_counter += 1
#                     possible_moves[i * 8 + j].append(f'{letters[m]}{numbers[n]}')
#                 else:
#                     not_legal_moves_counter += 1
#
#         #knight like moves
#         for m in range(8):
#             for n in range(8):
#                 if m + 2 == i and n + 1 == j and m >= n >= 0:
#                     moves_dict[f'{move}'] = f'{letters[m]}{numbers[n]}'
#                     legal_moves_counter += 1
#                     possible_moves[i * 8 + j].append(f'{letters[m]}{numbers[n]}')
#                 elif m + 2 == i and n - 1 == j and m >= n >= 0:
#                     moves_dict[f'{move}'] = f'{letters[m]}{numbers[n]}'
#                     legal_moves_counter += 1
#                     possible_moves[i * 8 + j].append(f'{letters[m]}{numbers[n]}')
#                 elif m - 2 == i and n - 1 == j and m >= n >= 0:
#                     moves_dict[f'{move}'] = f'{letters[m]}{numbers[n]}'
#                     legal_moves_counter += 1
#                     possible_moves[i * 8 + j].append(f'{letters[m]}{numbers[n]}')
#                 elif m - 2 == i and n + 1 == j and m >= n >= 0:
#                     moves_dict[f'{move}'] = f'{letters[m]}{numbers[n]}'
#                     legal_moves_counter += 1
#                     possible_moves[i * 8 + j].append(f'{letters[m]}{numbers[n]}')
#                 elif m + 1 == i and n + 2 == j and m >= n >= 0:
#                     moves_dict[f'{move}'] = f'{letters[m]}{numbers[n]}'
#                     legal_moves_counter += 1
#                     possible_moves[i * 8 + j].append(f'{letters[m]}{numbers[n]}')
#                 elif m + 1 == i and n - 2 == j and m >= n >= 0:
#                     moves_dict[f'{move}'] = f'{letters[m]}{numbers[n]}'
#                     legal_moves_counter += 1
#                     possible_moves[i * 8 + j].append(f'{letters[m]}{numbers[n]}')
#                 elif m - 1 == i and n - 2 == j and m >= n >= 0:
#                     moves_dict[f'{move}'] = f'{letters[m]}{numbers[n]}'
#                     legal_moves_counter += 1
#                     possible_moves[i * 8 + j].append(f'{letters[m]}{numbers[n]}')
#                 elif m - 1 == i and n + 2 == j and m >= n >= 0:
#                     moves_dict[f'{move}'] = f'{letters[m]}{numbers[n]}'
#                     legal_moves_counter += 1
#                     possible_moves[i * 8 + j].append(f'{letters[m]}{numbers[n]}')
#                 else:
#                     not_legal_moves_counter += 1
#
# print(f"legal_moves_counter: {legal_moves_counter}")
# print(f"not_legal_moves_counter: {not_legal_moves_counter}")
# print(moves_dict)
# print(f"size of list: {len(possible_moves)}")
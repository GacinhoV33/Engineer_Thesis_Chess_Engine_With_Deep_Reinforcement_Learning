#!/usr/bin/python
# -*- coding: utf-8 -*-

import chess
import chess.engine
import chess.pgn
import numpy as np
import random
import datetime


def stockfish_evaluation(board, time_limit=2.5):
    engine = chess.engine.SimpleEngine.popen_uci("./models/stockfish_15.1_win_x64_popcnt/stockfish-windows-2022-x86-64-modern.exe")
    result = engine.analyse(board, chess.engine.Limit(time=time_limit))
    engine.close()
    return result['score']

x = stockfish_evaluation(chess.Board(fen='rnbqkbnr/2pp1ppp/pp6/4p3/2B1P3/5Q2/PPPP1PPP/RNB1K1NR w KQkq - 0 4')).pov(color=chess.WHITE)
# print(str(x)[1:])
# print(int(-1)

mate_fen = 'rnbqkbnr/2pp1ppp/pp6/4p3/2B1P3/8/PPPP1QPP/RNB1K1NR w KQkq - 0 4'
board = chess.Board(fen=mate_fen)
x2 = board.outcome().result()
print(board.is_checkmate())
print(x2)
#
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
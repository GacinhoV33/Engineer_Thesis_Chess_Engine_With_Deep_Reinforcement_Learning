#!/usr/bin/python
# -*- coding: utf-8 -*-

import chess
import numpy as np
import random
# board = chess.Board(fen='')
# arr1 = np.ones((8, 8))
# arr2 = np.ones((8, 8))
#
# output = np.array([arr1, arr2])
# print(output.shape)
#
# board = chess.Board(fen=chess.STARTING_FEN)
# print(board.outcome())

print(random.choice([1, 2, 3, 4]))
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
#!/usr/bin/python
# -*- coding: utf-8 -*-
from model import NUMBER_OF_POSSIBLE_MOVES, INPUT_SHAPE, NUMBER_OF_CONSIDERED_POSITIONS

import chess
import numpy as np
from model import NUMBER_OF_POSSIBLE_MOVES

"""
Number of input layers:
-For each of 5 position:
    - 12 layers of Black&White Pieces
    - 2 layers for repetition
    - 
-For current position:
    - 4 layers of castling rights
    - 1 turn
    75 layers
"""
TOTAL_NUMBER_OF_LAYERS = 75
CHESSBOARD_X = 8
CHESSBOARD_Y = 8
startFen = chess.STARTING_FEN


def create_init_positions() -> list:
    return [startFen for _ in range(NUMBER_OF_CONSIDERED_POSITIONS)]

# TODO -> think there is it correct way of giving init data. Should init probabilities be 0 for none position.


def create_init_probabilities() -> np.array:
    return [np.zeros((NUMBER_OF_POSSIBLE_MOVES, 1)) for _ in range(NUMBER_OF_CONSIDERED_POSITIONS)]


def create_init_position_eval() -> np.array:
    return [np.zeros((NUMBER_OF_CONSIDERED_POSITIONS, 1)) for _ in range(NUMBER_OF_CONSIDERED_POSITIONS)]


def layers_of_one_position(fen: str) -> list:
    pass


def FEN_to_layers(fen_history: list) -> np.array:
    inputLayer = np.zeros((75, CHESSBOARD_X, CHESSBOARD_Y))
    for i, fen in enumerate(fen_history):
        board = chess.Board(fen=fen)
        """Layers that describe specific pieces on chessboard"""
        whiteKingLayer = np.zeros((CHESSBOARD_X, CHESSBOARD_Y), dtype=bool)
        whiteQueenLayer = np.zeros((CHESSBOARD_X, CHESSBOARD_Y), dtype=bool)
        whiteRooksLayer = np.zeros((CHESSBOARD_X, CHESSBOARD_Y), dtype=bool)
        whiteKnightsLayer = np.zeros((CHESSBOARD_X, CHESSBOARD_Y), dtype=bool)
        whiteBishopsLayer = np.zeros((CHESSBOARD_X, CHESSBOARD_Y), dtype=bool)
        whitePawnsLayer = np.zeros((CHESSBOARD_X, CHESSBOARD_Y), dtype=bool)
        # BLACK LAYERS
        blackKingLayer = np.zeros((CHESSBOARD_X, CHESSBOARD_Y), dtype=bool)
        blackQueenLayer = np.zeros((CHESSBOARD_X, CHESSBOARD_Y), dtype=bool)
        blackRooksLayer = np.zeros((CHESSBOARD_X, CHESSBOARD_Y), dtype=bool)
        blackKnightsLayer = np.zeros((CHESSBOARD_X, CHESSBOARD_Y), dtype=bool)
        blackBishopsLayer = np.zeros((CHESSBOARD_X, CHESSBOARD_Y), dtype=bool)
        blackPawnsLayer = np.zeros((CHESSBOARD_X, CHESSBOARD_Y), dtype=bool)

        """Iterating through every piece on chessboard and putting it on input network layer"""
        for key, value in board.piece_map().items():
            if value.piece_type == chess.PAWN:
                if value.color == chess.WHITE:
                    whitePawnsLayer[CHESSBOARD_X - 1 - int(key / 8)][key % 8] = True
                else:
                    blackPawnsLayer[CHESSBOARD_X - 1 - int(key / 8)][key % 8] = True
            elif value.piece_type == chess.KING:
                if value.color == chess.WHITE:
                    whiteKingLayer[CHESSBOARD_X - 1 - int(key / 8)][key % 8] = True
                else:
                    blackKingLayer[CHESSBOARD_X - 1 - int(key / 8)][key % 8] = True
            elif value.piece_type == chess.QUEEN:
                if value.color == chess.WHITE:
                    whiteQueenLayer[CHESSBOARD_X - 1 - int(key / 8)][key % 8] = True
                else:
                    blackQueenLayer[CHESSBOARD_X - 1 - int(key / 8)][key % 8] = True
            elif value.piece_type == chess.KNIGHT:
                if value.color == chess.WHITE:
                    whiteKnightsLayer[CHESSBOARD_X - 1 - int(key / 8)][key % 8] = True
                else:
                    blackKnightsLayer[CHESSBOARD_X - 1 - int(key / 8)][key % 8] = True
            elif value.piece_type == chess.ROOK:
                if value.color == chess.WHITE:
                    whiteRooksLayer[CHESSBOARD_X - 1 - int(key / 8)][key % 8] = True
                else:
                    blackRooksLayer[CHESSBOARD_X - 1 - int(key / 8)][key % 8] = True
            elif value.piece_type == chess.BISHOP:
                if value.color == chess.WHITE:
                    whiteBishopsLayer[CHESSBOARD_X - 1 - int(key / 8)][key % 8] = True
                else:
                    blackBishopsLayer[CHESSBOARD_X - 1 - int(key / 8)][key % 8] = True
            else:
                raise ValueError("Wrong piece type!")

            if board.is_repetition(count=1):
                firstRepetitionLayer = np.ones((CHESSBOARD_X, CHESSBOARD_Y), dtype=bool)
            else:
                firstRepetitionLayer = np.zeros((CHESSBOARD_X, CHESSBOARD_Y), dtype=bool)

            if board.is_repetition(count=2):
                secondRepetitionLayer = np.ones((CHESSBOARD_X, CHESSBOARD_Y), dtype=bool)
            else:
                secondRepetitionLayer = np.zeros((CHESSBOARD_X, CHESSBOARD_Y), dtype=bool)

            inputLayer[i * 14] = whiteKingLayer
            inputLayer[i * 14 +1] = whiteQueenLayer
            inputLayer[i * 14 +2] = whiteRooksLayer
            inputLayer[i * 14 +3] = whiteKnightsLayer
            inputLayer[i * 14 +4] = whiteBishopsLayer
            inputLayer[i * 14 +5] = whitePawnsLayer
            inputLayer[i * 14 +6] = blackKingLayer
            inputLayer[i * 14 +7] = blackQueenLayer
            inputLayer[i * 14 +8] = blackRooksLayer
            inputLayer[i * 14 +9] = blackKnightsLayer
            inputLayer[i * 14 +10] = blackBishopsLayer
            inputLayer[i * 14 +11] = blackPawnsLayer
            inputLayer[i * 14 +12] = firstRepetitionLayer
            inputLayer[i * 14 +13] = secondRepetitionLayer

    """Layer that describes which player is to make move"""
    board = chess.Board(fen=fen_history[-1])
    if board.turn == chess.WHITE:
        turnLayer = np.ones((CHESSBOARD_X, CHESSBOARD_Y), dtype=bool)
    elif board.turn == chess.BLACK:
        turnLayer = np.zeros((CHESSBOARD_X, CHESSBOARD_Y), dtype=bool)
    else:
        raise ValueError("Turn is not chosen! ")

    """Layers that describe castle rights"""
    if bool(board.castling_rights & chess.BB_A1):
        castleA1Layer = np.ones((CHESSBOARD_X, CHESSBOARD_Y), dtype=bool)
    else:
        castleA1Layer = np.zeros((CHESSBOARD_X, CHESSBOARD_Y), dtype=bool)
    if bool(board.castling_rights & chess.BB_A8):
        castleA8Layer = np.ones((CHESSBOARD_X, CHESSBOARD_Y), dtype=bool)
    else:
        castleA8Layer = np.zeros((CHESSBOARD_X, CHESSBOARD_Y), dtype=bool)
    if bool(board.castling_rights & chess.BB_H1):
        castleH1Layer = np.ones((CHESSBOARD_X, CHESSBOARD_Y), dtype=bool)
    else:
        castleH1Layer = np.zeros((CHESSBOARD_X, CHESSBOARD_Y), dtype=bool)
    if bool(board.castling_rights & chess.BB_H8):
        castleH8Layer = np.ones((CHESSBOARD_X, CHESSBOARD_Y), dtype=bool)
    else:
        castleH8Layer = np.zeros((CHESSBOARD_X, CHESSBOARD_Y), dtype=bool)

    inputLayer[70] = castleA1Layer
    inputLayer[71] = castleA8Layer
    inputLayer[72] = castleH1Layer
    inputLayer[73] = castleH8Layer
    inputLayer[74] = turnLayer
    return inputLayer
    # return np.array([turnLayer,
    #                  whiteKingLayer, whiteQueenLayer, whiteRooksLayer, whiteBishopsLayer, whiteKnightsLayer, whitePawnsLayer,
    #                  blackKingLayer, blackQueenLayer, blackRooksLayer, blackBishopsLayer, blackKnightsLayer, blackPawnsLayer,
    #                  castleA1Layer, castleA8Layer, castleH1Layer, castleH8Layer,
    #                  firstRepetitionLayer, secondRepetitionLayer
    #                  ])

    # counter plane -> not needed
    # progress plane -> ?not needed?

# FEN_to_layers(startFen)


def encode_moves_to_input(moves: list) -> np.array:
    move_probabilities = np.zeros(shape=(1, NUMBER_OF_POSSIBLE_MOVES))

    """
    Ex. from a1 to a8
    """


    return


def decode_output_to_moves(moves_probabilities: np.array) -> list:
    for move_probability in moves_probabilities:
        if move_probability != 0:
            pass
    return


# # print(create_init_positions()[0].shape)
#
# h = FEN_to_layers([startFen for _ in range(5)])
# print(h.shape)

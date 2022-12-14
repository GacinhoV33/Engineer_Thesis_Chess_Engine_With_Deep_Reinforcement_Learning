#!/usr/bin/python
# -*- coding: utf-8 -*-

from AlphaZero_version import config
import chess
from chess import Move
import numpy as np

import logging

logging.basicConfig(level=logging.INFO, format=' %(message)s')


class ChessEnvironment:
    def __init__(self, fen: str = chess.STARTING_FEN):
        self.fen = fen
        self.reset()

    def reset(self):
        self.board = chess.Board(self.fen)


    @staticmethod
    def state_to_input(fen: str) -> np.ndarray(config.INPUT_SHAPE):
        board = chess.Board(fen)

        is_white_turn = np.ones((8, 8)) if board.turn else np.zeros((8, 8))
        castling = np.asarray([
            np.ones((8, 8)) if board.has_queenside_castling_rights(
                chess.WHITE) else np.zeros((8, 8)),
            np.ones((8, 8)) if board.has_kingside_castling_rights(
                chess.WHITE) else np.zeros((8, 8)),
            np.ones((8, 8)) if board.has_queenside_castling_rights(
                chess.BLACK) else np.zeros((8, 8)),
            np.ones((8, 8)) if board.has_kingside_castling_rights(
                chess.BLACK) else np.zeros((8, 8)),
        ])

        repetition_counter = np.ones((8, 8)) if board.can_claim_fifty_moves() else np.zeros((8, 8))
        arrays = []
        for color in chess.COLORS:

            for piece_type in chess.PIECE_TYPES:
                array = np.zeros((8, 8))
                for index in list(board.pieces(piece_type, color)):
                    array[7 - int(index/8)][index % 8] = True
                arrays.append(array)
        arrays = np.asarray(arrays)

        en_passant = np.zeros((8, 8))
        if board.has_legal_en_passant():
            en_passant[7 - int(board.ep_square / 8)][board.ep_square % 8] = True

        r = np.array([is_white_turn, *castling,
                      repetition_counter, *arrays, en_passant]).reshape((1, *config.INPUT_SHAPE))
        # memory management
        del board
        return r.astype(bool)

    @staticmethod
    def estimate_winner(board: chess.Board) -> int:
        """
        Estimate the winner of the current node.
        Pawn = 1, Bishop = 3, Rook = 5, Queen = 9
        Positive score = white wins, negative score = black wins
        """
        score = 0
        piece_scores = {
            chess.PAWN: 1,
            chess.KNIGHT: 3.28,
            chess.BISHOP: 3.33,
            chess.ROOK: 5.1,
            chess.QUEEN: 8.88,
            chess.KING: 2.55 # TODO 1 instead 2.55
        }
        for piece in board.piece_map().values():
            if piece.color == chess.WHITE:
                score += piece_scores[piece.piece_type]
            else:
                score -= piece_scores[piece.piece_type]
        if np.abs(score) > 5:
            if score > 0:
                logging.debug("White wins (estimated)")
                return 0.25
            else:
                logging.debug("Black wins (estimated)")
                return -0.25
        else:
            logging.debug("Draw")
            return 0

    @staticmethod
    def get_piece_amount(board: chess.Board) -> int:
        return len(board.piece_map().values())

    def __str__(self):
        return str(chess.Board(self.board))

    def step(self, action: Move):
        self.board.push(action)
        return self.board
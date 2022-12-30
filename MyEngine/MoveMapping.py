#!/usr/bin/python
# -*- coding: utf-8 -*-

import chess
from enum import Enum
from typing import Tuple
from chess import PieceType
import numpy as np
# import threading
import concurrent.futures

class QueenLikeDirection(Enum):
    """Enum types that represents 8 directions that may be chosen to make queen-like move, mentioned in alphazero papers"""
    NORTHWEST = 0
    NORTH = 1
    NORTHEAST = 2
    EAST = 3
    SOUTHEAST = 4
    SOUTH = 5
    SOUTHWEST = 6
    WEST = 7


class KnightMove(Enum):
    """ 8 possible knight moves possible to make by superPiece. """
    NORTH_LEFT = 0  # diff == -15
    NORTH_RIGHT = 1  # diff == -17
    EAST_UP = 2  # diff == -6
    EAST_DOWN = 3  # diff == 10
    SOUTH_RIGHT = 4  # diff == 15
    SOUTH_LEFT = 5  # diff == 17
    WEST_DOWN = 6  # diff == 6
    WEST_UP = 7  # diff == -10


class UnderPromotion(Enum):
    """Underpromotion for pieces other than Knight or Queen"""
    KNIGHT = 0
    BISHOP = 1
    ROOK = 2


class Mapping:
    """
    The mapper is a dictionary of moves.

    * the index is the type of move
    * the value is the plane's index, or an array of plane indices (for distance)
    """
    # knight moves from north_left to west_up (clockwise)
    knight_mappings = [-15, -17, -6, 10, 15, 17, 6, -10]

    def get_index(self, piece_type: PieceType, direction: Enum, distance: int = 1) -> int:
        if piece_type == PieceType.KNIGHT:
            return 56 + KnightMove(direction).value
        else:
            return QueenLikeDirection(direction) * 8 + distance

    @staticmethod
    def get_underpromotion_move(piece_type: PieceType, from_square: int, to_square: int) -> Tuple[UnderPromotion, int]:
        piece_type = UnderPromotion(piece_type - 2)
        diff = from_square - to_square
        if to_square < 8:
            # black promotes (1st rank)
            direction = diff - 8
        elif to_square > 55:
            # white promotes (8th rank)
            direction = diff + 8
        return (piece_type, direction)

    @staticmethod
    def get_knight_move(from_square: int, to_square: int) -> KnightMove:
        return KnightMove(Mapping.knight_mappings.index(from_square - to_square))

    @staticmethod
    def get_queenlike_move(from_square: int, to_square: int) -> Tuple[QueenLikeDirection, int]:
        diff = from_square - to_square
        if diff % 8 == 0:
            # north and south
            if diff > 0:
                direction = QueenLikeDirection.SOUTH
            else:
                direction = QueenLikeDirection.NORTH
            distance = int(diff / 8)
        elif diff % 9 == 0:
            # southwest and northeast
            if diff > 0:
                direction = QueenLikeDirection.SOUTHWEST
            else:
                direction = QueenLikeDirection.NORTHEAST
            distance = np.abs(int(diff / 8))
        elif from_square // 8 == to_square // 8:
            # east and west
            if diff > 0:
                direction = QueenLikeDirection.WEST
            else:
                direction = QueenLikeDirection.EAST
            distance = np.abs(diff)
        elif diff % 7 == 0:
            if diff > 0:
                direction = QueenLikeDirection.SOUTHEAST
            else:
                direction = QueenLikeDirection.NORTHWEST
            distance = np.abs(int(diff / 8)) + 1
        else:
            raise Exception("Invalid queen-like move")
        return (direction, distance)

    mapper = {
        # queens
        QueenLikeDirection.NORTHWEST: [0, 1, 2, 3, 4, 5, 6],
        QueenLikeDirection.NORTH: [7, 8, 9, 10, 11, 12, 13],
        QueenLikeDirection.NORTHEAST: [14, 15, 16, 17, 18, 19, 20],
        QueenLikeDirection.EAST: [21, 22, 23, 24, 25, 26, 27],
        QueenLikeDirection.SOUTHEAST: [28, 29, 30, 31, 32, 33, 34],
        QueenLikeDirection.SOUTH: [35, 36, 37, 38, 39, 40, 41],
        QueenLikeDirection.SOUTHWEST: [42, 43, 44, 45, 46, 47, 48],
        QueenLikeDirection.WEST: [49, 50, 51, 52, 53, 54, 55],
        # knights
        KnightMove.NORTH_LEFT: 56,
        KnightMove.NORTH_RIGHT: 57,
        KnightMove.EAST_UP: 58,
        KnightMove.EAST_DOWN: 59,
        KnightMove.SOUTH_RIGHT: 60,
        KnightMove.SOUTH_LEFT: 61,
        KnightMove.WEST_DOWN: 62,
        KnightMove.WEST_UP: 63,
        # underpromotions
        UnderPromotion.KNIGHT: [64, 65, 66],
        UnderPromotion.BISHOP: [67, 68, 69],
        UnderPromotion.ROOK: [70, 71, 72]
    }


def map_valid_move(move: chess.Move, board: chess.Board) -> list:
    from_square = move.from_square
    to_square = move.to_square
    piece = board.piece_at(from_square)
    direction = None
    if piece is None:
        raise Exception(f"No piece found on {from_square}")
    if move.promotion and move.promotion != chess.QUEEN:
        piece_type, direction = Mapping.get_underpromotion_move(
            move.promotion, from_square, to_square)
        plane_index = Mapping.mapper[piece_type][1 - direction]
    else:
        # find the correct plane based on from_square and move_square
        if piece.piece_type == chess.KNIGHT:
            # get direction
            direction = Mapping.get_knight_move(from_square, to_square)
            plane_index = Mapping.mapper[direction]
        else:
            # get direction of queen-type move
            direction, distance = Mapping.get_queenlike_move(
                from_square, to_square)
            plane_index = Mapping.mapper[direction][np.abs(distance) - 1]
        # create a mask with only valid moves
    row = from_square % 8
    col = 7 - (from_square // 8)
    return (move, plane_index, row, col)


def map_probabilities_to_moves(move_probabilities: np.array, board: chess.Board):
    move_probabilities = move_probabilities.reshape((73, 8, 8))
    actions = {}
    valid_moves = board.generate_legal_moves()
    outputs = list()
    while True:
        try:
            move = next(valid_moves)
        except StopIteration:
            break
        outputs.append(map_valid_move(move, board))

    for move, plane_index, col, row in outputs:
        actions[move.uci()] = move_probabilities[plane_index][col][row] + np.random.random()/1000
    return actions

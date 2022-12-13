#!/usr/bin/python
# -*- coding: utf-8 -*-
import chess
from random import random

"""This class implements MinMax algorithm with alpha-beta pruning to chess game. It's simple version. """
class MinMax:
    def __init__(self, board, max_depth=4, color=chess.WHITE):
        self.board = board
        self.maxDepth = max_depth
        self.color = color

    def getBestMove(self):
        return self.engine(None, 1)

    def evalFunc(self):
        """Simple function for chess position evaluation"""
        compt = 0
        for i in range(64):
            compt += self.squareResPoints(chess.SQUARES[i])
        compt += self.mateOpportunity() + self.openning() + 0.001 * random()
        return compt

    def mateOpportunity(self):
        """This function checks whether position is a check mate. If yes it gives very big reward for MinMax algorithm"""
        if self.board.legal_moves.count() == 0:
            if self.board.turn == self.color:
                return -999
            else:
                return 999
        else:
            return 0

    def openning(self):
        if self.board.fullmove_number < 10:
            if self.board.turn == self.color:
                return 1/30 * self.board.legal_moves.count()
            else:
                return -1/30 * self.board.legal_moves.count()
        else:
            return 0

    def squareResPoints(self, square):
        """This functions return approximate value of specific piece according to Han's Berliner's system value."""
        pieceValue = 0
        if self.board.piece_type_at(square) == chess.PAWN:
            pieceValue = 1
        elif self.board.piece_type_at(square) == chess.ROOK:
            pieceValue = 5.1
        elif self.board.piece_type_at(square) == chess.KNIGHT:
            pieceValue = 3.2
        elif self.board.piece_type_at(square) == chess.KING:
            pieceValue = 1
        elif self.board.piece_type_at(square) == chess.QUEEN:
            pieceValue = 8.8
        elif self.board.piece_type_at(square) == chess.BISHOP:
            pieceValue = 3.33
        if self.board.color_at(square) != self.color:
            return -pieceValue
        else:
            return pieceValue

    def engine(self, candicate, depth):
        if depth == self.maxDepth or self.board.legal_moves.count() == 0:
            return self.evalFunc()
        else:
            #get list of legal moves of the current position
            moveList = list(self.board.legal_moves)
            #initialise newCandidate
            newCandidate = None
            if depth % 2 != 0:
                newCandidate = float("-inf")
            else:
                newCandidate = float("inf")
            for i in moveList:
                self.board.push(i)

                # get the value of move i
                value = self.engine(newCandidate, depth+1)
                #if maximizing(engine's turn)
                if value > newCandidate and depth % 2 != 0:
                    if depth == 1:
                        move = i
                    newCandidate = value

                #if minimizing humans turn
                elif value < newCandidate and depth % 2 == 0:
                    newCandidate = value

                #alpha-beta pruning cuts
                #if previous move was made by the engine
                if candicate is not None and value < candicate and depth % 2 == 0:
                    self.board.pop() # removing last move from the board
                    break
                # if previous move was made by the human
                elif candicate is not None and value > candicate and depth % 2 != 0:
                    self.board.pop()  # removing last move from the board
                    break

                self.board.pop()

            if depth > 1:
                return newCandidate
            else:
                return move
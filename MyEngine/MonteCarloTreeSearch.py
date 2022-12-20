#!/usr/bin/python
# -*- coding: utf-8 -*-
from tensorflow.keras.models import Model
import copy
from network import FEN_to_layers

class Edge:
    def __init__(self, move, parentNode):
        self.parentNode = parentNode
        self.move = move
        self.N = 0
        self.W = 0
        self.Q = 0
        self.P = 0


class Node:
    def __init__(self, board, parentEdge):
        self.board = board
        self.parentEdge = parentEdge
        self.childEdgeNode = []

    def expand(self, model: Model):
        moves = self.board.legal_moves()
        for move in moves:
            childBoard = copy.deepcopy(self.board)
            childBoard.push(move)
            childEdge = Edge(move, self)
            childNode = Node(childBoard, childEdge)
            self.childEdgeNode.append((childEdge, childNode))

        """Network prediction"""
        pred_value = model.predict(FEN_to_layers(self.board.fen()))
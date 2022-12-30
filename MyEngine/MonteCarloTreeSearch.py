#!/usr/bin/python
# -*- coding: utf-8 -*-
import math

import chess
# from tensorflow.keras.models import Model
import copy

from MoveMapping import map_probabilities_to_moves
from network import FEN_to_layers
import random
from settings import N_MCTS_ITERATION


class Edge:
    def __init__(self, move, parentNode):
        self.parentNode = parentNode
        self.move = move
        self.N = 0
        self.W = 0
        self.Q = 0
        self.P = 0


class Node:
    def __init__(self, board, parentEdge, history, is_it_root: bool = True):
        self.board = board
        self.parentEdge = parentEdge
        self.childEdgeNode = []
        self.history = history
        if not is_it_root:
            self.history.pop(0)
            self.history.append(board.fen())

    def expand(self, model):
        """Legal moves in position -> Think about not taking all moves to cut the computional complexity"""
        for move in self.board.legal_moves:
            childBoard = copy.deepcopy(self.board)
            childBoard.push(move)
            childEdge = Edge(move, self)
            childNode = Node(childBoard, childEdge, history=self.history, is_it_root=False)
            self.childEdgeNode.append((childEdge, childNode))

        """Network prediction"""
        input_to_network = [FEN_to_layers(self.history).reshape(1, 75, 8, 8)]
        policy_prediction, value_prediction = model.predict(input_to_network)
        actions = map_probabilities_to_moves(policy_prediction, self.board)
        probability_sum = 0.0

        """Take the prediction from network, find legal moves and corresponding probability values. Return list."""
        for edge, _ in self.childEdgeNode:
            edge.P = actions[edge.move.uci()]
            probability_sum += edge.P

        for edge, _ in self.childEdgeNode:
            edge.P /= probability_sum

        return value_prediction

    def isLeaf(self):
        return self.childEdgeNode == []


class MCTS:
    def __init__(self, model):
        self.model = model
        self.rootNode = None
        self.tau = 1 # the temperature -> best keep it on 1 or 1.2
        self.c_puct = 3 # bigger value -> higher exploration

    def uctValue(self, edge, parentN):
        return self.c_puct * edge.P * (math.sqrt(parentN)/(1+edge.N))

    def select(self, node):
        if node.isLeaf():
            return node
        else:
            maxUctChild = None
            maxUctValue = -10000000
            for edge, child_node in node.childEdgeNode:
                uctVal = self.uctValue(edge, edge.parentNode.parentEdge.N)
                val = edge.Q
                if edge.parentNode.board.turn == chess.BLACK:
                    val = -edge.Q
                uctValChild = val + uctVal
                if uctValChild > maxUctValue:
                    maxUctChild = child_node
                    maxUctValue = uctValChild
            allBestChilds = []
            for edge, child_node in node.childEdgeNode:
                uctVal = self.uctValue(edge, edge.parentNode.parentEdge.N)
                val = edge.Q
                if edge.parentNode.board.turn == chess.BLACK:
                    val = -edge.Q
                uctValChild = val + uctVal
                if uctValChild == maxUctValue:
                    allBestChilds.append(child_node)

            if maxUctChild is None:
                return self.select(random.choice(allBestChilds))
            else:
                if len(allBestChilds) > 1:
                    return self.select(random.choice(allBestChilds))
                else:
                    return self.select(maxUctChild)

    def expandAndEvaluate(self, node):
        outcome = node.board.outcome()
        if outcome is None:
            v = node.expand(self.model)
            self.backpropagate(v, node.parentEdge)
        else:
            v = 0.0
            if outcome == chess.WHITE:
                v = 1.0
            elif outcome == chess.BLACK:
                v = -1.0
            self.backpropagate(v, node.parentEdge)

    def backpropagate(self, v, edge):
        edge.N += 1
        edge.W = edge.W + v
        edge.Q = edge.W / edge.N
        if edge.parentNode is not None:
            if edge.parentNode.parentEdge is not None:
                self.backpropagate(v, edge.parentNode.parentEdge)

    def search(self, rootNode):
        self.rootNode = rootNode
        _ = self.rootNode.expand(self.model)
        for i in range(N_MCTS_ITERATION):
            selected_node = self.select(rootNode)
            self.expandAndEvaluate(selected_node)
        N_sum = 0
        moveProbs = []

        for edge, _ in rootNode.childEdgeNode:
            N_sum += edge.N
        for edge, node in rootNode.childEdgeNode:
            prob = (edge.N ** (1/ self.tau)) / (N_sum**(1 / self.tau))
            moveProbs.append((edge.move, prob, edge.N, edge.Q))
        return moveProbs


#!/usr/bin/python
# -*- coding: utf-8 -*-

import chess
from tensorflow.keras.models import load_model
from flask import Flask
from flask_restful import Resource, Api, reqparse
from MonteCarloTreeSearch import Edge, Node, MCTS, N_MCTS_ITERATION
from flask_cors import CORS
import numpy as np

from network import FEN_to_layers

model = load_model('./models/model_12_res.keras')


class BestMove(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('positions', required=True)
        args = parser.parse_args()
        data = args['positions']
        positions = data.split(';')
        best_move = best_reinf_move(positions)
        print(f"Done: {best_move}")
        return {'bestMove': f'{best_move}'}, 200


class PositionEvaluation(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('positions')
        args = parser.parse_args()
        data = args['positions'].split(';')
        input_to_network = [FEN_to_layers(data).reshape(1, 75, 8, 8)]
        _, evaluation = model.predict(input_to_network)
        return {'evaluation': f'{evaluation[0][0]}'}, 200


def best_reinf_move(history):
    board = chess.Board(fen=history[-1])
    rootEdge = Edge(None, None)
    rootNode = Node(board, rootEdge, history)
    mcts = MCTS(model, 200)
    moveProbs = mcts.search(rootNode)
    moveProbsSorted = sorted(moveProbs, key=lambda x: x[3], reverse=True)
    nextMove = moveProbsSorted[0] # best Move according to probs
    return nextMove[0]


def server():
    app = Flask(__name__)
    CORS(app)
    api = Api(app)
    api.add_resource(BestMove, '/best_move')
    api.add_resource(PositionEvaluation, '/pos_eval')
    app.run()

"""Test string - http://127.0.0.1:5000/best_move?positions={%22positions%22:%20[%228/8/8/4p1K1/2k1P3/8/8/8%20b%20-%20-%200%201%22,%20%224k2r/6r1/8/8/8/8/3R4/R3K3%20w%20Qk%20-%200%201%22,%20%228/5k2/3p4/1p1Pp2p/pP2Pp1P/P4P1K/8/8%20b%20-%20-%2090%2032%22,%20%228/5k2/3p4/1p1Pp2p/pP2Pp1P/P4P1K/8/8%20b%20-%20-%2099%2050%22,%20%228/5k2/3p4/1p1Pp2p/pP2Pp1P/P4P1K/8/8%20b%20-%20-%2099%2050%22]}"""

if __name__ == '__main__':
    server()
    # bestMove([])
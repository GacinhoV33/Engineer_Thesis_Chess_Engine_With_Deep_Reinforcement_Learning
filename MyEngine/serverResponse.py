#!/usr/bin/python
# -*- coding: utf-8 -*-

import chess
# import tensorflow as tf
from tensorflow.keras.models import load_model
from flask import Flask
from flask_restful import Resource, Api, reqparse
import json
from MonteCarloTreeSearch import Edge, Node, MCTS, N_MCTS_ITERATION
from flask_cors import CORS

model = load_model('./models/model_12_res.keras')

class BestMove(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('positions', required=True)
        args = parser.parse_args()

        data = args['positions']
        data_converted = json.loads(data)
        positions = data_converted['positions']
        best_move = best_Reinf_move(positions)
        print("Im in")
        return {'bestMove': f'{best_move}'}, 200


def best_Reinf_move(history):
    board = chess.Board(fen=history[-1])
    rootEdge = Edge(None, None)
    rootNode = Node(board, rootEdge, history)
    mcts = MCTS(model, 400)
    moveProbs = mcts.search(rootNode)
    moveProbsSorted = sorted(moveProbs, key=lambda x: x[1], reverse=True)
    nextMove = moveProbsSorted[0] # best Move according to probs
    return nextMove[0]


def server():
    app = Flask(__name__)
    CORS(app)
    api = Api(app)
    api.add_resource(BestMove, '/best_move')
    # app.r
    app.run()

"""Test string - http://127.0.0.1:5000/best_move?positions={%22positions%22:%20[%228/8/8/4p1K1/2k1P3/8/8/8%20b%20-%20-%200%201%22,%20%224k2r/6r1/8/8/8/8/3R4/R3K3%20w%20Qk%20-%200%201%22,%20%228/5k2/3p4/1p1Pp2p/pP2Pp1P/P4P1K/8/8%20b%20-%20-%2090%2032%22,%20%228/5k2/3p4/1p1Pp2p/pP2Pp1P/P4P1K/8/8%20b%20-%20-%2099%2050%22,%20%228/5k2/3p4/1p1Pp2p/pP2Pp1P/P4P1K/8/8%20b%20-%20-%2099%2050%22]}"""

if __name__ == '__main__':
    server()
    # bestMove([])
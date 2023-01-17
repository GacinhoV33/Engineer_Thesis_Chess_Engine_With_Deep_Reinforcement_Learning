#!/usr/bin/python
# -*- coding: utf-8 -*-

import chess
from tensorflow.keras.models import load_model
from flask import Flask
from flask_restful import Resource, Api, reqparse
from MonteCarloTreeSearch import Edge, Node, MCTS, N_MCTS_ITERATION
from flask_cors import CORS

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

if __name__ == '__main__':
    server()

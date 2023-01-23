#!/usr/bin/python
# -*- coding: utf-8 -*-

import chess
from tensorflow.keras.models import load_model
from flask import Flask
from flask_restful import Resource, Api, reqparse
from MonteCarloTreeSearch import Edge, Node, MCTS, N_MCTS_ITERATION
from flask_cors import CORS
from simpleMinMaxEngine import MinMaxEngine

from network import FEN_to_layers

model = load_model('./models/model_12_res.keras')


class BestMove(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('positions', required=True)
        parser.add_argument('engine', required=True)
        parser.add_argument('depth', required=True)
        args = parser.parse_args()
        positions_data, engine_type, depth = args['positions'], args['engine'], int(args['depth'])
        positions = positions_data.split(';')
        if engine_type == 'AlphaZero':
            best_move = best_reinf_move(positions)
        else:
            current_position = positions[-1]
            board = chess.Board(fen=current_position)
            engine = MinMaxEngine(board, depth + 1, board.turn)
            best_move = engine.getBestMove()
        return {'bestMove': f'{best_move}'}, 200


class PositionEvaluation(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('positions')
        parser.add_argument('engine', required=True)
        parser.add_argument('depth', required=True)
        args = parser.parse_args()
        positions_data, engine_type, depth = args['positions'], args['engine'], int(args['depth'])
        data = args['positions'].split(';')
        if engine_type == 'AlphaZero':
            input_to_network = [FEN_to_layers(data).reshape(1, 75, 8, 8)]
            _, evaluation = model.predict(input_to_network)
            ret_eval = evaluation[0][0]
        else:
            engine = MinMaxEngine(chess.Board(fen=data[-1]), 2, chess.WHITE)
            evaluation = engine.evalFunc() / 20
            ret_eval = min([abs(evaluation), 1])
            ret_eval = -ret_eval if evaluation < 0 else ret_eval
        return {'evaluation': f'{ret_eval}'}, 200


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

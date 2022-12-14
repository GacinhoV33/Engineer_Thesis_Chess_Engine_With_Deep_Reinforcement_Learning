#!/usr/bin/python
# -*- coding: utf-8 -*-
import chess
import chess.pgn
import tqdm
import numpy as np
import logging
import threading
from graphviz import Digraph
from AlphaZero_version.edge import Edge
import AlphaZero_version.config as config
from AlphaZero_version.mapper import Mapping
from AlphaZero_version.node import Node
from AlphaZero_version.chessEnvironment import ChessEnvironment


class MonteCarloSearchTree:
    def __init__(self, agent, state: str = chess.STARTING_FEN, stochastic: bool = False):
        self.root = Node(state=state)
        self.game_path = list()
        self.current_board: chess.Board = None

        self.agent = agent
        self.stochastic = stochastic
        # self.outputs = list()

    def run_simulations(self, n: int) -> None:
        for _ in tqdm.tqdm(range(n)):
            self.game_path = list()
            leaf = self.select_child(self.root)
            leaf.N += 1
            leaf = self.expand(leaf)
            leaf = self.backpropagate(leaf, leaf.value)

    def select_child(self, node: Node) -> Node:

        while not node.is_leaf():
            if not len(node.edges):
                return node
            noise = [1 for _ in range(len(node.edges))]
            if self.stochastic and node == self.root:
                noise = np.random.dirichlet([config.DIRICHLET_NOISE]  * len(node.edges))
            best_edge = None
            best_score = -np.inf
            for i,edge in enumerate(node.edges):
                if edge.upper_confidence_bound(noise[i]) > best_score:
                    best_score = edge.upper_confidence_bound(noise[i])
                    best_edge = edge
            if best_edge is None:
                raise Exception("Edge not found! ")

            node = best_edge.output_node
            self.game_path.append(best_edge)
        return node

    def map_valid_move(self, move: chess.Move) -> None:
        logging.debug("Filtering valid moves... ")
        from_square = move.from_square
        to_square = move.to_square
        plane_index: int = None
        piece = self.current_board.piece_at(from_square)
        direction = None
        if piece is None:
            raise Exception(f"No piece at {from_square}")

        if move.promotion and move.promotion != chess.QUEEN:
            piece_type, direction = Mapping.get_underpromotion_move(move.promotion, from_square, to_square)
            plane_index = Mapping.mapper[piece_type][1 - direction]
        else:
            if piece.piece_type == chess.KNIGHT:
                direction = Mapping.get_knight_move(from_square, to_square)
                plane_index = Mapping.mapper[direction]
            else:
                direction, distance = Mapping.get_queenlike_move(from_square, to_square)
                plane_index = Mapping.mapper[direction][np.abs(distance) - 1]
        row = from_square % 8
        col = 7 - (from_square // 8)
        self.outputs.append((move, plane_index, row, col ))

    def probabilities_to_actions(self, probabilities: np.ndarray, board: str) -> dict:
        probabilities = probabilities.reshape(config.amount_of_planes, config.n, config.n)
        actions = {}

        self.current_board = chess.Board(board)
        valid_moves = self.current_board.generate_legal_moves()
        self.outputs = list()
        threads = []
        while True:
            try:
                move = next(valid_moves)
            except StopIteration:
                break

            thread = threading.Thread(target=self.map_valid_move, args=(move,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        for move, plane_index, col, row in self.outputs:
            actions[move.uci()] = probabilities[plane_index][col][row]

        return actions

    def expand(self, leaf: Node) -> Node:
        logging.debug("Expanding... ")
        board = chess.Board(leaf.state)

        possible_actions = list(board.generate_legal_moves())

        if not len(possible_actions):
            assert board.is_game_over(), "Game is not over, but there are no possible moves"
            outcome = board.outcome(claim_draw=True)
            if outcome is None:
                leaf.value = 0
            else:
                leaf.value = 1 if outcome.winner == chess.WHITE else -1
            return leaf
        input_state = ChessEnvironment.state_to_input(leaf.state)
        prediction, value = self.agent.predict(input_state)

        actions = self.probabilities_to_actions(prediction, leaf.state)

        logging.debug(f"Model predictions: {prediction}")
        logging.debug(f"Value of state: {value}")

        leaf.value = value

        for action in possible_actions:
            new_state = leaf.step(action)
            leaf.add_child(Node(new_state), action, actions[action.uci()])
        return leaf

    def backpropagate(self, end_node: Node, value: float):
        logging.debug("Backpropagating... ")
        for edge in self.game_path:
            edge.input_node.N += 1
            edge.N += 1
            edge.W += value
        return end_node

    def plot_node(self, dot: Digraph, node: Node):
        dot.node(f"{node.state}", "N")
        for edge in node.edges:
            dot.edge(str(edge.input_node.state), str(edge.output_node.state), label=edge.action.uci())
            dot = self.plot_node(dot, edge.output_node)

        return dot

    def plot_tree(self, save_path: str = "tests/mcts_tree.gv") -> None:
        logging.debug("Plotting Tree... ")
        dot = Digraph(comment='Chess MCTS')
        logging.info(f"# of nodes in tree: {len(self.root.get_all_children())}")
        dot = self.plot_node(dot, self.root)
        dot.save(save_path)

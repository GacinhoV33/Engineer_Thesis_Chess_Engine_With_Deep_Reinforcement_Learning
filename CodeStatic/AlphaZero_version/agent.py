#!/usr/bin/python
# -*- coding: utf-8 -*-
# !/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import chess
import logging
from tensorflow.keras.models import Model
import time
from AlphaZero_version.monteCarloSearchTree import MonteCarloSearchTree
from AlphaZero_version import config

# Need to implement -> MCTS, RLModelBuilder


class Agent:
    def __init__(self, local_predictions: bool = False, model_path=None, state=chess.STARTING_FEN):
        # if local_predictions and model_path is not None:
        if local_predictions: #CHANGED!
            logging.info("Using local predictions")
            from tensorflow.python.ops.numpy_ops import np_config
            from tensorflow.keras.models import load_model
            # self.model = load_model(model_path)
            self.model = load_model('./models/my_model.h5')
            self.local_predictions = True
            np_config.enable_numpy_behavior()
        else:
            print("Server version - not implemented!")
            self.local_predictions = False

        self.monteCarloSearchTree = MonteCarloSearchTree(self, state=state)

    def build_model(self, ) -> Model:
        # model_builder = RLModelBuilder(config.INPUT_SHAPE, config.OUTPUT_SHAPE)
        # model = model_builder.build_model()
        # return model
        pass

    def run_simulations(self, n: int = 1):
        self.monteCarloSearchTree.run_simulations(n)

    def save_model(self, timestamped: bool = False):
        if timestamped:
            self.model.save(f"{config.MODEL_FOLDER}/model-{time.time()}.h5")
        else:
            self.model.save(f"{config.MODEL_FOLDER}/model.h5")

    def predict(self, data):
        if self.local_predictions:
            from AlphaZero_version.local_prediction import predict_local
            prediction, value = predict_local(self.model, data)
            return prediction.numpy(), value[0][0]
        else:
            # not implemented
            pass

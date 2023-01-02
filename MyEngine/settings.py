#!/usr/bin/python
# -*- coding: utf-8 -*-
import screeninfo

"""MCTS Values"""
N_MCTS_ITERATION = 200
LIMIT_OF_MOVES_PER_GAME = 200

"""Reinforcment Learning values"""
NUMBER_OF_GAMES_PER_ITERATION = 1
NUMBER_OF_ITERATION_IN_TRAINING = 5
NUMBER_OF_EPOCHS_PER_GAME = 20
MODEL_NAME = 'model_12_res'

TOTAL_NUMBER_OF_LAYERS = 75


NUMBER_OF_CONSIDERED_POSITIONS = 5
NUMBER_OF_POSSIBLE_MOVES = 4672
INPUT_SHAPE = (75, 8, 8)
POLICY_SHAPE = (NUMBER_OF_CONSIDERED_POSITIONS, 1)

POLICY_SHAPE_3D = (73, 8, 8)


"""Game settings"""
monitor_width = screeninfo.get_monitors()[0].width
monitor_height = screeninfo.get_monitors()[0].height


width = monitor_width/1.92
height = monitor_height/1.08
pos_width = (monitor_width - width) // 2
pos_height = (monitor_height - height) // 2

svg_x = 150
svg_y = 0


num_2_letter = {
    -1: "none",
    0 : "none",
    1 : "a",
    2 : "b",
    3 : "c",
    4 : "d",
    5 : "e",
    6 : "f",
    7 : "g",
    8 : "h",
    9 : "none",
    10: "none",
}

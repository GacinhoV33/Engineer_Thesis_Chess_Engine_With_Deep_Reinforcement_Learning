#!/usr/bin/python
# -*- coding: utf-8 -*-

import chess
import numpy as np

# board = chess.Board(fen='')
arr1 = np.ones((8, 8))
arr2 = np.ones((8, 8))

output = np.array([arr1, arr2])
print(output.shape)
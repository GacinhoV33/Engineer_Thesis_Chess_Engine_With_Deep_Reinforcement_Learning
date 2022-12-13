#!/usr/bin/python
# -*- coding: utf-8 -*-


class Move:
    def __init__(self, piece, start_field, end_field, color='white'):
        self.start_field = start_field
        self.piece = piece
        self.end_field = end_field
        self.color = color

    def pgn_notation(self, ):

        return None

class Environtment:
    def __init__(self):
        pass

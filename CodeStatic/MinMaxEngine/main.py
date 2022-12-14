#!/usr/bin/python
# -*- coding: utf-8 -*-
import chess
import chess.svg
import chess.pgn
from MinMaxEngine.MinMax import MinMax
from PyQt5.QtCore import QMutex, QTimer
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QLabel, QPushButton
from settings import width, height, pos_height, pos_width, svg_x, svg_y
from helpers import num_2_letter
from PyQt5 import QtTest
from random import choice, random
import datetime


class MainWindow(QWidget):
    def __init__(self, record_pgn=True):
        super().__init__()
        self.isFirstClick = True
        self.isWhite = True
        self.firstField = None
        #General settings in Window
        self.setGeometry(pos_width, pos_height, 150 + width, height)
        self._mutex = QMutex()

        self.widgetSvg = QSvgWidget(parent=self)
        self.widgetSvg.setGeometry(svg_x, svg_y, width, height)
        self.chessboard = chess.Board()

        self.chessboardSvg = chess.svg.board(self.chessboard).encode("UTF-8")
        self.widgetSvg.load(self.chessboardSvg)

        # Input panel
        self.moveInput = QLineEdit(self)
        self.moveInput.move(5, 20)
        self.moveInput.returnPressed.connect(self.makeMove)

        self.moveLabel = QLabel(self)
        self.moveLabel.move(5, 2)
        self.moveLabel.setText('Insert move there:')

        self.currentColorLabel = QLabel(self)
        self.currentColorLabel.move(5, 100)
        self.currentColorLabel.setText('Move to make:')
        self.currentColor = QLabel(self)
        self.currentColor.move(5, 120)
        self.currentColor.setText("White" if self.isWhite else "Black")
        self.record_pgn = record_pgn

        # Move Button
        moveButton = QPushButton("Move", self)
        moveButton.clicked.connect(self.makeMove) #ignore error
        moveButton.move(5, 40)

        # Move Button
        # writePGNButton = QPushButton("Write PGN", self)
        # writePGNButton.clicked.connect(self.writePGNButton)  # ignore error
        # writePGNButton.move(5, 70)

    def _updateBoard(self):
        self.chessboardSvg = chess.svg.board(self.chessboard).encode("UTF-8")
        self.widgetSvg.load(self.chessboardSvg)
        self.currentColor.setText("White" if self.isWhite else "Black")
        self.moveInput.setText('')

    def mousePressEvent(self, event):
        x, y = event.pos().x(), event.pos().y()
        if 190 < x < 1110 and 40 < y < 960:
            field = self.calcPole((x, y))
            if field:
                if self.isFirstClick:
                    if field in self.getAllPiecesPosition("white" if self.isWhite else "black"):
                        self.isFirstClick = False
                        self.firstField = field
                else:
                    move = chess.Move.from_uci(self.firstField + field)
                    if move in self.chessboard.legal_moves:
                        self.isFirstClick = True
                        self.isWhite = not self.isWhite
                        self.makeMove(move)

                    else:
                        self.isFirstClick = True
                        print("Illegal move")

    def playEngineMove(self, max_depth, color):
        engine = MinMax(self.chessboard, max_depth, color)
        best_move = engine.getBestMove()
        print("BEST MOVE: ", best_move)
        self.chessboard.push(best_move)
        self.isWhite = not self.isWhite
        self._updateBoard()

    def makeMove(self, move=None):
        user_input = self.moveInput.text()
        if not move:
            move = chess.Move.from_uci(user_input)
        if move in self.chessboard.legal_moves:
            self.chessboard.push(move)
            self._updateBoard()
        else:
            print("Illegal")

    def calcPole(self, position: tuple):
        x, y = position
        x_0, y_0 = x - 188, y - 40
        field = (int(x_0 // 115 + 1), int(y_0 // 115 + 1))
        if field[0] != "none" and field[1] not in [-1, 0, 9]:
            return f'{num_2_letter[field[0]]}{8 + 1 - field[1]}'
        else:
            return None

    def getAllPiecesPosition(self, col="white"):
        fields = []
        color = True if col == "white" else False

        for i in range(1, 7):
            for piece_number in self.chessboard.pieces(i, color):
                field_x = int(piece_number) % 8
                field_y = piece_number // 8
                fields.append(f'{num_2_letter[field_x + 1]}{field_y + 1}')

        return fields

    def play_engine_vs_engine(self):
        i = 0
        while not self.chessboard.is_checkmate():
            i += 1
            print(f'Move {i}')
            QtTest.QTest.qWait(200)
            self.playEngineMove(max_depth=5, color=chess.WHITE)
            QtTest.QTest.qWait(200)
            self.playEngineMove(max_depth=5, color=chess.BLACK)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    window.play_engine_vs_engine()
    app.exec()
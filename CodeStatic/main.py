import chess
import chess.svg
from PyQt5.QtCore import QMutex

from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QLabel, QPushButton
from settings import width, height, pos_height, pos_width, svg_x, svg_y
from helpers import num_2_letter


class MainWindow(QWidget):
    def __init__(self):
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
        self.moveInput.returnPressed.connect(self.clickMoveButtonMethod)

        self.moveLabel = QLabel(self)
        self.moveLabel.move(5, 2)
        self.moveLabel.setText('Insert move there:')

        # Move Button
        moveButton = QPushButton("Move", self)
        moveButton.clicked.connect(self.clickMoveButtonMethod) #ignore error
        moveButton.move(5, 40)

    def clickMoveButtonMethod(self, move=None):
        user_input = self.moveInput.text()
        if not move:
            move = chess.Move.from_uci(user_input) # check from square
        if move in self.chessboard.legal_moves:
            self.chessboard.push(move)
            self._updateBoard()
        else:
            print("Illegal")

    def _updateBoard(self):
        self.chessboardSvg = chess.svg.board(self.chessboard).encode("UTF-8")
        self.widgetSvg.load(self.chessboardSvg)
        self.moveInput.setText('')
        # if self.chessboard.legal_moves

    def mousePressEvent(self, event):
        x, y = event.pos().x(), event.pos().y()
        if 190 < x < 1110 and 40 < y < 960:
            print("On Board")
        field = self.calcPole((x, y))
        print(field)
        if field:
            if self.isFirstClick:
                if field in self.getAllPiecesPosition("white" if self.isWhite else "black"):
                    self.isFirstClick = False
                    self.firstField = field
            else:
                print(self.firstField + field)
                move = chess.Move.from_uci(self.firstField + field)
                if move in self.chessboard.legal_moves:
                    print("I'm in")
                    self.clickMoveButtonMethod(move)
                    self.isFirstClick = True
                    self.isWhite = not self.isWhite

    def calcPole(self, position: tuple):
        x, y = position
        x_0, y_0 = x - 188, y - 40
        # x_1 = 920/8 = 115
        field = (int(x_0 // 115 + 1), int(y_0 // 115 + 1))
        print(field)
        if field[0] != "none" and field[1] not in [-1, 0, 9]:
            return f'{num_2_letter[field[0]]}{8 +1 - field[1]}'
        else:
            return None

    def getAllPiecesPosition(self, col="white"):
        fields = []
        color = True if col == "white" else False

        for i in range(1, 7):
            for piece_number in self.chessboard.pieces(i, color):
                field_x = int(piece_number) % 8
                field_y = piece_number // 8
                fields.append(f'{num_2_letter[field_x+1]}{field_y+1}')

        return fields


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
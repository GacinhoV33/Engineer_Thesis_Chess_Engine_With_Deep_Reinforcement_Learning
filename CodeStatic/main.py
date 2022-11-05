import chess
import chess.svg

from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QLabel, QPushButton
from settings import width, height, pos_height, pos_width


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        #General settings in Window
        self.setGeometry(pos_width, pos_height, 150 + width, height)

        self.widgetSvg = QSvgWidget(parent=self)
        self.widgetSvg.setGeometry(150, 0, width, height)

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

    def clickMoveButtonMethod(self):
        user_input = self.moveInput.text()
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
        print(event.pos())
        #TODO logic behing mousle clicking


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
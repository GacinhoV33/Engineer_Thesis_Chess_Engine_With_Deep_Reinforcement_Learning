import chess
import chess.svg
import chess.pgn

from PyQt5.QtCore import QMutex
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QLabel, QPushButton

from network import create_init_positions
from settings import width, height, pos_height, pos_width, svg_x, svg_y, num_2_letter
from PyQt5 import QtTest
from random import choice, random

from MonteCarloTreeSearch import Edge, Node, MCTS
import numpy as np
from model import load_existing_model


class MainWindow(QWidget):
    def __init__(self, record_pgn=True):
        super().__init__()
        self.isFirstClick = True
        self.isWhite = True
        self.firstField = None
        self.mode = None
        #General settings in Window
        self.setGeometry(pos_width, pos_height, 150 + width, height)
        self._mutex = QMutex()
        self.model = load_existing_model('model_12_res')

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

        self.currentColorLabel = QLabel(self)
        self.currentColorLabel.move(5, 100)
        self.currentColorLabel.setText('Move to make:')
        self.currentColor = QLabel(self)
        self.currentColor.move(5, 120)
        self.currentColor.setText("White" if self.isWhite else "Black")
        self.record_pgn = record_pgn
        self.history: list = create_init_positions()
        # Move Button
        moveButton = QPushButton("Move", self)
        moveButton.clicked.connect(self.clickMoveButtonMethod) #ignore error
        moveButton.move(5, 40)

        # Write PGN
        writePGNButton = QPushButton("Write PGN", self)
        writePGNButton.clicked.connect(self.save_pgn)  # ignore error
        writePGNButton.move(5, 240)

        # Human-Human Button
        HumanHumanButton = QPushButton("Human vs Human", self)
        HumanHumanButton.clicked.connect(self.setHumanVsHuman)  # ignore error
        HumanHumanButton.move(5, 150)

        # Human-Engine Button
        HumanEngineButton = QPushButton("Human vs Engine", self)
        HumanEngineButton.clicked.connect(self.setHumanVsEngine)  # ignore error
        HumanEngineButton.move(5, 180)

        # Engine-Engine Button
        EngineEngineButton = QPushButton("Engine vs Engine", self)
        EngineEngineButton.clicked.connect(self.play_engine_vs_engine)  # ignore error
        EngineEngineButton.move(5, 210)

    def setHumanVsHuman(self):
        self.mode = "HumanVsHuman"

    def setHumanVsEngine(self):
        self.mode = "HumanVsEngine"
        print(self.mode)

    def playEngineMove(self, maxDepth, color, engine_type: str='minmax'):
        if engine_type == 'minmax':
            engine = MinMaxEngine(self.chessboard, maxDepth, color)
            best_move = engine.getBestMove()
        elif engine_type == 'Reinf':
            engine = 0
            best_move = 'a2a3'
            pass
        else:
            raise ValueError('Wrong engine name!')

        print("BEST MOVE: ", best_move)
        self.chessboard.push(best_move)
        self.isWhite = not self.isWhite
        self._updateBoard()

    def clickMoveButtonMethod(self, move=None):
        print(self.chessboard.fen())
        user_input = self.moveInput.text()
        if not move:
            move = chess.Move.from_uci(user_input) # check from square
        if move in self.chessboard.legal_moves:
            self.chessboard.push(move)
            print(self.chessboard.result() == '*')
            self.save_pgn()
            self._updateBoard()
            if self.isWhite:
                self.history.pop(0)
                self.history.append(self.chessboard.fen())
        if not self.isWhite and self.mode == 'HumanVsEngine':
           self.playReinf_move()

    def save_pgn(self):
        node = chess.pgn.Game.from_board(self.chessboard)
        with open(f'pgn/last_pgn.txt', 'w') as file:
            file.write(str(node.game().mainline()))
            file.write('Result: ' + str(node.headers['Result']))
        print("PGN of game saved.")

    def playReinf_move(self):
        black_move = self.best_Reinf_move(self.chessboard)[0]
        self.isWhite = not self.isWhite
        self.clickMoveButtonMethod(black_move)

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
                        self.clickMoveButtonMethod(move)

                    else:
                        self.isFirstClick = True
                        print("Illegal move")

    def calcPole(self, position: tuple):
        x, y = position
        x_0, y_0 = x - 188, y - 40
        field = (int(x_0 // 115 + 1), int(y_0 // 115 + 1))
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

    def play_game(self, random_game=True):
        if random_game:
            for i in range(100):
                move = choice(list(self.chessboard.legal_moves))
                self.clickMoveButtonMethod(move)
                QtTest.QTest.qWait(500)

    def best_Reinf_move(self, board):
        self.history.pop(0)
        self.history.append(board.fen())
        rootEdge = Edge(None, None)
        rootNode = Node(board, rootEdge, self.history)
        mcts = MCTS(self.model)
        moveProbs = mcts.search(rootNode)
        moveProbsSorted = sorted(moveProbs, key=lambda x: x[1], reverse=True)
        probs = np.array([prob[1] for prob in moveProbsSorted])
        rand_idx = np.random.multinomial(1, probs)
        idx = np.where(rand_idx == 1)[0][0]
        nextMove = moveProbsSorted[idx]
        return nextMove

    def play_engine_vs_engine(self):
        i = 0

        while not self.chessboard.is_game_over():
            i+= 1
            QtTest.QTest.qWait(1000)
            white_move = self.best_Reinf_move(self.chessboard)[0]
            self.clickMoveButtonMethod(white_move)
            QtTest.QTest.qWait(1000)
            black_move = self.best_Reinf_move(self.chessboard)[0]
            self.clickMoveButtonMethod(black_move)
            print(f"Move: {i}")
        self.save_pgn()


class MinMaxEngine:
    def __init__(self, board, maxDepth, color):
        self.board = board
        self.maxDepth = maxDepth
        self.color = color

    def getBestMove(self):
        return self.minmax_engine(None, 1)

    def evalFunc(self):
        compt = 0
        for i in range(64):
            compt += self.squareResPoints(chess.SQUARES[i])
        compt += self.mateOpportunity() + self.openning() + 0.001 * random()
        return compt

    def mateOpportunity(self):
        if self.board.legal_moves.count() == 0:
            if self.board.turn == self.color:
                return -999
            else:
                return 999
        else:
            return 0

    def openning(self):
        if self.board.fullmove_number < 10:
            if self.board.turn == self.color:
                return 1/30 * self.board.legal_moves.count()
            else:
                return -1/30 * self.board.legal_moves.count()
        else:
            return 0

    #takes a square as input and returns the corresponding han's Berliner's system value of it's resident
    def squareResPoints(self, square):
        pieceValue = 0
        if self.board.piece_type_at(square) == chess.PAWN:
            pieceValue = 1
        elif self.board.piece_type_at(square) == chess.ROOK:
            pieceValue = 5.1
        elif self.board.piece_type_at(square) == chess.KNIGHT:
            pieceValue = 3.2
        elif self.board.piece_type_at(square) == chess.KING:
            pieceValue = 1
        elif self.board.piece_type_at(square) == chess.QUEEN:
            pieceValue = 8.8
        elif self.board.piece_type_at(square) == chess.BISHOP:
            pieceValue = 3.33
        if self.board.color_at(square) != self.color:
            return -pieceValue
        else:
            return pieceValue

    def minmax_engine(self, candicate, depth):
        if depth == self.maxDepth or self.board.legal_moves.count() == 0:
            return self.evalFunc()
        else:
            #get list of legal moves of the current position
            moveList = list(self.board.legal_moves)
            #initialise newCandidate
            newCandidate = None
            if depth % 2 != 0:
                newCandidate = float("-inf")
            else:
                newCandidate = float("inf")
            for i in moveList:
                self.board.push(i)
                # get the value of move i
                value = self.minmax_engine(newCandidate, depth+1)
                #if maximizing(engine's turn)
                if value > newCandidate and depth % 2 != 0:
                    if depth == 1:
                        move = i
                    newCandidate = value

                #if minimizing humans turn
                elif value < newCandidate and depth % 2 == 0:
                    newCandidate = value

                #alpha-beta pruning cuts
                #if previous move was made by the engine
                if candicate is not None and value < candicate and depth % 2 == 0:
                    self.board.pop() # removing last move from the board
                    break
                # if previous move was made by the human
                elif candicate is not None and value > candicate and depth % 2 != 0:
                    self.board.pop()  # removing last move from the board
                    break

                self.board.pop()

            if depth > 1:
                return newCandidate
            else:
                return move


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
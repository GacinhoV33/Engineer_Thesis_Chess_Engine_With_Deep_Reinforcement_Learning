import chess
import chess.svg
import chess.pgn

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
        self.init_pgn()

        # Move Button
        moveButton = QPushButton("Move", self)
        moveButton.clicked.connect(self.clickMoveButtonMethod) #ignore error
        moveButton.move(5, 40)

        # Move Button
        writePGNButton = QPushButton("Write PGN", self)
        writePGNButton.clicked.connect(self.writePGNButton)  # ignore error
        writePGNButton.move(5, 70)

    def writePGNButton(self):
        pass
        # print(self.game_pgn)
        # with open(f'pgn/Game - {datetime.date}', 'w') as file:
        #     file.write(self.game_pgn)

    def playEngineMove(self, maxDepth, color):
        engine = Engine(self.chessboard, maxDepth, color)
        best_move = engine.getBestMove()
        print("BEST MOVE: ", best_move)
        self.chessboard.push(best_move)
        self.isWhite = not self.isWhite
        self._updateBoard()

    def clickMoveButtonMethod(self, move=None):
        user_input = self.moveInput.text()
        if not move:
            move = chess.Move.from_uci(user_input) # check from square
        if move in self.chessboard.legal_moves:
            self.chessboard.push(move)
            self._updateBoard()
            # if self.record_pgn:
            #     print(self.game_pgn.eval())
            #     self.game_pgn.add_variation(move)
            # print(list(self.chessboard.legal_moves))
            if not self.isWhite:
                self.playEngineMove(4, chess.BLACK)
        else:
            print("Illegal")

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

    def translate_move(self, move, color: str = "white"):
        if move == "O-O":
            if color == "white":
                move_trans = "e1f1"
            else:
                move_trans = "e8f8"
        elif move == "O-O-O":
            if color == "white":
                move_trans = "e1c1"
            else:
                move_trans = 'e8c8'

    def play_game(self, random_game=True):
        if random_game:
            # while not self.chessboard.is_checkmate():
            for i in range(100):
                # async def make_move(self):
                #     print("im in")
                #     await asyncio.sleep(1)
                move = choice(list(self.chessboard.legal_moves))
                self.clickMoveButtonMethod(move)
                QtTest.QTest.qWait(500)
                # print(self.chessboard.kings)
                # print("in")
                # timer = QTimer()
                # timer.timeout.connect(update)
                # timer.setInterval(1000 / fps)
                # timer.start()
                # QTimer()

    def play_engine_vs_engine(self):
        i = 0
        # QtTest.QTest.qWait(200)
        while not self.chessboard.is_checkmate():
            i += 1
            print(f'Move {i}')
            QtTest.QTest.qWait(200)
            self.playEngineMove(maxDepth=4, color=chess.WHITE)
            QtTest.QTest.qWait(200)
            self.playEngineMove(maxDepth=4, color=chess.BLACK)

    def init_pgn(self, event="random_game"):
        self.game_pgn = chess.pgn.Game()
        self.game_pgn.headers["Event"] = event

        # if is_this_init:
        #     self.game_pgn = chess.pgn.Game()
        #     self.game_pgn.headers["Event"] = event
        #     self.game_moves = []
        # else:
        #     self.


class Engine:
    def __init__(self, board, maxDepth, color):
        self.board = board
        self.maxDepth = maxDepth
        self.color = color

    def getBestMove(self):
        return self.engine(None, 1)

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

    def engine(self, candicate, depth):
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
                # play the move i
                # print(i)
                self.board.push(i)

                # get the value of move i
                value = self.engine(newCandidate, depth+1)
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

#
# class Play:
#     def __init__(self, board=chess.Board):
#         self.board = board
#
#     def playHumanMove(self):
#         try:
#             print(self.board.legal_moves)
#             play = input("Your move: ")
#             if play == "undo":
#                 self.board.pop()
#                 self.board.pop()
#                 self.playHumanMove()
#                 return
#             self.board.push_san(play)
#         except:
#             self.playHumanMove()
#
#     def playEngineMove(self, maxDepth, color):
#         engine = Engine(self.board, maxDepth, color)
#         self.board.push(move=engine.getBestMove())
#
#     def startGame(self):
#         color=None
#         while color != 'b' and color != 'w':
#             color = input('Color: ')
#         maxDepth = None
#         while not isinstance(maxDepth, int):
#             maxDepth = int(input("Choose depth"))
#         if color == 'b':
#             while not self.board.is_checkmate():
#                 print('Engine is thinking... ')
#                 self.playEngineMove(maxDepth, chess.WHITE)
#                 print(self.board)
#                 self.playHumanMove()
#                 print(self.board)
#             print(self.board)
#             print(self.board.outcome())
#
#         elif color == 'w':
#             while not self.board.is_checkmate():
#                 print(self.board)
#                 self.playHumanMove()
#                 print(self.board)
#                 print("The engine is thinking... ")
#                 self.playEngineMove(maxDepth, chess.BLACK)
#             print(self.board)
#             print(self.board.outcome())
#         self.board.reset()
#         self.startGame()
class Play:
    def __init__(self, board=chess.Board):
        self.board = board

    def playHumanMove(self, move):
        try:
            # print(self.board.legal_moves)
            # play = input("Your move: ")
            # if play == "undo":
                # self.board.pop()
                # self.board.pop()
                # self.playHumanMove()
                # return
            self.board.push_san(move)
        except:
            self.playHumanMove()

    def playEngineMove(self, maxDepth, color):
        engine = Engine(self.board, maxDepth, color)
        self.board.push(move=engine.getBestMove())

    def startGame(self):
        color=None
        while color != 'b' and color != 'w':
            color = input('Color: ')
        maxDepth = None
        while not isinstance(maxDepth, int):
            maxDepth = int(input("Choose depth"))
        if color == 'b':
            while not self.board.is_checkmate():
                print('Engine is thinking... ')
                self.playEngineMove(maxDepth, chess.WHITE)
                # print(self.board)
                self.playHumanMove()
                # print(self.board)
            # print(self.board)
            # print(self.board.outcome())

        elif color == 'w':
            while not self.board.is_checkmate():
                # print(self.board)
                self.playHumanMove()
                # print(self.board)
                # print("The engine is thinking... ")
                self.playEngineMove(maxDepth, chess.BLACK)
            # print(self.board)
            # print(self.board.outcome())
        self.board.reset()
        self.startGame()


def Game_check():
    newBoard = chess.Board()
    game = Play(newBoard)
    bruh = game.startGame()

if __name__ == "__main__":
    # Game_check()
    app = QApplication([])
    window = MainWindow()
    # window.play_game(random_game=False)
    window.show()
    window.play_engine_vs_engine()

    # window.play_game()
    app.exec()
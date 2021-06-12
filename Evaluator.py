import numpy as np

class Evaluator(object):

    def __init__(self, type, matrix=None):
        self.type = type
        self.weights = matrix

    def heuristicValue(self):
        if self.type <= 4:
            return self.heuristicWeights
        elif self.type == 5:
            return self.logistello
        elif self.type == 6:
            return self.logistello2

    def setWeights(self):
        if self.type == 1:
            self.weights = [[100, -20, 10, 7, 7, 10, -20, 100],
                       [-20, -50, -4, -4, -4, -4, -50, -20],
                       [10, -4, -2, -2, -2, -2, -4, 10],
                       [7, -4, -2, 1, 1, -2, -4, 7],
                       [7, -4, -2, 1, 1, -2, -4, 7],
                       [10, -4, -2, -2, -2, -2, -4, 10],
                       [-20, -50, -4, -4, -4, -4, -50, -20],
                       [100, -20, 10, 7, 7, 10, -20, 100]]

        elif self.type == 2:
            self.weights = [[120, -20, 20, 5, 5, 20, -20, 120],
                       [-20, -40, -5, -5, -5, -5, -40, -20],
                       [20, -5, 15, 3, 3, 15, -5, 20],
                       [5, -5, 3, 3, 3, 3, -5, 5],
                       [5, -5, 3, 3, 3, 3, -5, 5],
                       [20, -5, 15, 3, 3, 15, -5, 20],
                       [-20, -40, -5, -5, -5, -5, -40, -20],
                       [120, -20, 20, 5, 5, 20, -20, 120]]
        elif self.type == 3:
            self.weights = [[80, -26, 24, -1, -5, 28, -18, 76],
                           [-23, -39, -18, -9, -6, -8, -39, -1],
                           [46, -16, 4, 1, -3, 6, -20, 52],
                           [-13, -5, 2, -1, 4, 3, -12, -2],
                           [-5, -6, 1, -2, -3, 0, -9, -5],
                           [48, -13, 12, 5, 0, 5, -24, 41],
                           [-27, -53, -11, -1, -11, -16, -58, -15],
                           [87, -25, 27, -1, 5, 36, -3, 100]]
        elif self.type == 4: # Pesos sacados en algoritmo genetico
            """self.weights = [[136, -18, 20, 20, 5, 33, -39, 108],
                            [-20, -31, -4, -23, 13, 9, -42, -19],
                            [5, -5, 16, -5, 3, 17, 8, 31],
                            [5, -22, 3, -1, -2, 11, -5, -5],
                            [0, -5, -11, 3, 3, 5, -5, 5],
                            [23, -16, 15, 3, 12, 27, -7, 14],
                            [-24, -40, -5, -5, -15, -19, -21, -26],
                            [123, -20, 32, 25, -13, 20, -7, 120]]"""

            self.weights = [[122, -8, 14, 0, 20, 22, -13, 100],
                            [-1, -54, 12, 13, 14, 12, -21, -39],
                            [36, 3, 24, -13, 2, 11, -22, 1],
                            [14, -3, 19, 20, -12, 22, 3, 10],
                            [19, 13, 7, 6, 20, 7, 15, 20],
                            [38, -16, 30, 8, 21, 34, -7, 9],
                            [-2, -45, 9, -20, -6, 5, -24, -36],
                            [105, -8, 39, -6, 12, 14, -15, 111]]


    # Obtiene el valor heuristico
    def heuristicWeights(self, color, newGame):
        score = 0
        if self.weights == None:
            self.setWeights()

        # Si te permite ganar, puntuación máxima
        if newGame.isEnd():
            white, black = newGame.countColors()
            if color == black and color > white:
                return 1000000
            elif color == white and color > black:
                return 1000000

        newboard = newGame.getBoard()
        for i in range(8):
            for j in range(8):
                if newboard[i][j] == color:
                    score += self.weights[i][j]
                elif newboard[i][j] == self.getOpponentColor(color):
                    score += -(self.weights[i][j])
        return score

    def logistello(self,color, game):
        white, black = game.countColors()
        if color == 2:
            return max(0, (black-13)/4)
        else:
            return max(0, (white-13)/4)

    def logistello2(self,color, game):
        return max(0, (self.stableCoins(game.getBoard(), color) - 13) / 4)


    def stableCoins(self, board, color):
        stable = np.zeros((8, 8))
        count = 0

        for i in range(8):
            for j in range(8):
                if ((i, j) == (0, 0) or (0, 7) or (7, 0) or (7, 7)) and board[i][j] == color:
                    count += 1
                else:
                    if self.adhere(board, stable, color, i, j):
                        stable[i][j] = 1
                        count += 1

        for i in reversed(range(8)):
            for j in reversed(range(8)):
                if stable[i][j] == 1 and board[i][j] == color:
                    count += 1
                else:
                    if self.adhere(board, stable, color, i, j):
                        stable[i][j] = 1
                        count += 1
        return count

    def adhere(self, board, stable, color, i, j):
        if board[i][j] != color:
            return False
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (1, -1), (-1, 1), (1, 1)]
        for direction in directions:
            if i + direction[0] <= 7 and i + direction[0] >= 0 and j + direction[1] <= 7 and j + direction[1] >= 0:
                if stable[i + direction[0]][j + direction[1]] == 1:
                    return True
        return False

    def getOpponentColor(self, color):
        if color == 1:
            return 2
        else:
            return 1



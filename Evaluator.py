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
            self.weights [[102, -32, 11, 0, 1, 17, -22, 111],
                    [-23, -57, 4, -12, -5, 1, -46, -38],
                    [-1, -5, -8, -10, 1, -4, -2, 9],
                    [-10, -1, -10, -9, -9, -15, 12, 0],
                    [24, -9, -14, 4, -7, -2, 8, -4],
                    [9, -10, -1, -5, 3, 5, 2, 4],
                    [-22, -75, 1, 13, -26, -4, -55, -7],
                    [105, -13, 1, 16, 11, 12, -16, 97]]

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



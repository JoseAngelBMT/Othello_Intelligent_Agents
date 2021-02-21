import GameRules as gm
import numpy as np
from random import randint


class RandomAgent():

    def __init__(self,color):
        self.color = color

    # Un movimiento aleatorio de los movimientos legales
    def getAction(self, game):
        moves = game.getMoves(self.color)
        random_number = randint(0, len(moves)) - 1
        return moves[random_number]

class RulesAgent():

    def __init__(self, color):
        self.color = color

    # Movimiento que minimiza el numero de movimientos del oponente o si encuentra una esquina se queda con ella
    def getAction(self, game):
        moves = game.getMoves(self.color)
        min = 64
        betterMoves = []
        for move in moves:
            # Si el movimiento es una esquina lo selecciona
            if self.isCorner(move):
                return move

            numberMoves = len(game.getOpponentMove(move[0], move[1], self.opponentColor()))
            if numberMoves <= min:
                betterMoves.append(move)
                min = numberMoves

        # Dentro de todos los movimientos minimos se elige aleatoriamente para que las partidas no sean iguales
        random_number = randint(0, len(betterMoves)) - 1
        return betterMoves[random_number]


    def isCorner(self,move):
        if move == (0, 0) or move == (0, 7) or move == (7, 0) or move == (0, 7):
            return True
        return False

    def opponentColor(self):
        if self.color == 1:
            return 2
        elif self.color == 2:
            return 1

class RulesAledoAgent():

    def __init__(self,color):
        self.color = color
        self.weights = [[10,0,7,7,7,7,0,10],
                        [0, 0,3,3,3,3,0, 0],
                        [7, 3,4,4,4,4,3, 7],
                        [7, 3,4,4,4,4,3, 7],
                        [7, 3,4,4,4,4,3, 7],
                        [7, 3,4,4,4,4,3, 7],
                        [0, 0,3,3,3,3,0, 0],
                        [10,0,7,7,7,7,0,10]]

    def getAction(self,game):
        self.updateWeights(game.getBoard())
        max = 0
        moves = game.getMoves(self.color)
        betterMoves = []
        for move in moves:
            weight = self.weights[move[0]][move[1]]
            if max <= weight:
                max = weight
                betterMoves.append(move)

        random_number = randint(0, len(betterMoves)) - 1
        return betterMoves[random_number]


    def updateWeights(self,board):
        """Casilla del perimetro de modo que entre una de las esquinas de ese lado y la casilla que ocupamos, todas las casillas (incluida la
        esquina) sea de nuestro color.Estas casillas ya no las puede conseguir el adversario"""
        self.blockPerimeter(board, 0, 0)
        self.blockPerimeter(board, 0, 7)
        self.blockPerimeter(board, 7, 0)
        self.blockPerimeter(board, 7, 7)

        """Casilla del perimetro que tras ser ocupada quede adyacente a dos casillas del perimetro del adversario"""
        """Casilla del perimetro que tras ser ocupada no quede adyacente a ninguna casilla del perimetro del adversario, salvo las casillas
                adyacentes a las esquinas. Notar que si queda adyacente a una unica casilla del perimetro del adversario, este puede revertir el color
                a su favor"""
        self.middlePerimeter(board)
        self.printBoard()


    def middlePerimeter(self,board):
        perimeter = [board[0][:],board[7][:],board[0:,0],board[0:,7]]
        opponentColor = 1
        if self.color == 1:
            opponentColor = 2
        else:
            opponentColor = 1

        for i in range(4):
            for j in range(8):
                des = j + 2
                desless = j - 2
                if des < 8:
                    """if desless >= 0:
                        if perimeter[i][desless] == 0 and perimeter[i][j-1] == 0 and perimeter[i][j] == opponentColor:
                            if i == 0:
                                self.weights[i][j-1] = 2
                            elif i == 1:
                                self.weights[7][j-1] = 2
                            elif i == 2:
                                self.weights[j-1][0] = 2
                            else:
                                self.weights[j-1][7] = 2
                        if perimeter[i][j] == opponentColor and perimeter[i][j+1] == 0 and perimeter[i][des] == 0:
                            if i == 0:
                                self.weights[i][j+1] = 2
                            elif i == 1:
                                self.weights[7][j+1] = 2
                            elif i == 2:
                                self.weights[j+1][0] = 2
                            else:
                                self.weights[j+1][7] = 2"""
                    if perimeter[i][j] == opponentColor and perimeter[i][j+1] == 0 and perimeter[i][des] == opponentColor:
                        if i == 0:
                            self.weights[i][j+1] = 8
                        elif i == 1:
                            self.weights[7][j+1] = 8
                        elif i == 2:
                            self.weights[j+1][0] = 8
                        else:
                            self.weights[j+1][7] = 8

    def blockPerimeter(self,board, i, j):
        directions = [(0,1), (1,0), (0, -1), (-1, 0)]
        if board[i][j] == self.color:
            for dir in directions:
                x = i + dir[0]
                y = j + dir[1]
                while self.inBoard(x,y) and board[x][y] == self.color:
                    x += dir[0]
                    y += dir[1]
                if self.inBoard(x,y) and board[x][y] == 0:
                    self.weights[x][y] = 9

    def printBoard(self):
        for row in self.weights:
            print(row)
        print("\n")

    def inBoard(self,i,j):
        if i >= 0 and i < 8 and j >= 0 and j < 8:
            return True
        return False


class MinMaxAgent():

    def __init__(self,color):
        self.color = color
        self.heuristic = 0

    def getAction(self, game):
        pass

    """
    def alphabeta(self,depth, alpha, beta):

        if depth == 0:
            return self.heuristic

        if player == MAX:
            for son in subtree:
                alpha = max(alpha, self.alphabeta(depth-1, alpha, beta))
                if beta <= alpha:
                    break
            return alpha

        if player == MIN:
            for son in subtree:
                beta = min(beta, self.alphabeta(depth-1, alpha, beta))
                if beta <= alpha:
                    break
            return beta"""



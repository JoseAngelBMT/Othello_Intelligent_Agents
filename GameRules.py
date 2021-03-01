import numpy as np
import copy
import random

class Othello:

    #Inicializacion del tablero
    def __init__(self):
        # Matriz -> 0 vacio, 1 Blanco, 2 Negro
        self.board = np.zeros((8, 8)) # Estado del juego
        self.board[3, 3] = 1
        self.board[3, 4] = 2
        self.board[4, 3] = 2
        self.board[4, 4] = 1

        self.directions = [(0,-1),(0,1),(-1,0),(1,0),(-1,-1),(1,-1),(-1,1),(1,1)] #ARRIBA, ABAJO, IZQ, DER, ARR-IZQ,ARR-DER, AB-IZQ, AR-DER

    #Obtener el valor de una celda del tablero
    def getValue(self,i,j):
        return self.board[i][j]

    #Obtener la matriz del tablero
    def getBoard(self):
        return self.board

    #Obtiene todos los movimientos validos para un color
    def getMoves(self,color):
        moves = []

        for i in range(8):
            for j in range(8):
                if self.getValue(i,j) == color:
                    moves = moves + self.validMoves(i,j,color)
        return moves

    #Devuelve los movimientos validos para una ficha de un color
    def validMoves(self,i,j,color):
        if color == 1:
            opponent = 2
        else:
            opponent = 1

        moves = []
        for (d1,d2) in self.directions:
            (x,y) = self.validPosition(i,j,d1,d2,opponent)
            if x != None:
                moves.append((x,y))
        return moves

    # Dada una posicion comprueba si esta dentro del tablero
    def inBoard(self,i,j):
        if (i in range(8) and j in range(8)):
            return True
        return False

    # Devuelve una posicion valida para una ficha en una direccion
    def validPosition(self,i,j,d1,d2,opponent):
        x = i + d1
        y = j + d2
        # Al avanzar en la direccion se comprueba que seguimos en el tablero y la ficha es del color del oponente
        if self.inBoard(x,y) and self.getValue(x,y) == opponent:
            x += d1
            y += d2
            # Mientras encontremos mas fichas del oponente continuamos
            while self.inBoard(x,y) and self.getValue(x,y) == opponent:
                x += d1
                y += d2
                # Si se encuentra un hueco vacio, entonces esa posicion sera valida
            if self.inBoard(x,y) and self.getValue(x,y) == 0:
                return(x,y)
        return (None,None)

    # Realiza el movimiento
    def doMove(self,color, i,j):
        if (i,j) in self.getMoves(color):
            self.board[i][j] = color
            # Voltea las fichas de distinto color en direccion a una ficha del color actual
            for (d1,d2) in self.directions:
                self.flipCoin(color,i,j,d1,d2)

    # Voltea las fichas al colocar una nueva
    def flipCoin(self,color,i,j,d1,d2):

        if color == 1:
            opponent = 2
        else:
            opponent = 1

        coinsFlip = []  # Posicion de las fichas que se voltearan
        x = i + d1
        y = j + d2

        if self.inBoard(x,y) and self.getValue(x,y) == opponent:
            coinsFlip = coinsFlip + [(x, y)]
            x += d1
            y += d2
            while self.inBoard(x,y) and self.getValue(x,y) == opponent:
                coinsFlip = coinsFlip + [(x, y)]
                x += d1
                y += d2
            if self.inBoard(x,y) and self.getValue(x,y) == color:
                for p in coinsFlip:
                    self.board[p[0]][p[1]] = color


    # Devuelve el numero de fichas de cada color del tablero
    def countColors(self):
        white, black = 0,0
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 1:
                    white += 1
                elif self.board[i][j] == 2:
                    black += 1
        return white, black

    # Comprueba si la partida ha terminado
    def isEnd(self):
        # Si no hay mas fichas que poner
        white, black = self.countColors()
        if (white + black) == 64:
            return True

        # No hay mas movimientos validos
        if self.getMoves(1) == [] and self.getMoves(2) == []:
            return True

        return False

    def setBoard(self,board):
        self.board = board

    # Dado un movimiento, devuelve la lista de movimientos legales del oponente
    def getOpponentMove(self,i,j,opponentColor):
        game = copy.deepcopy(self)
        color = self.getOpponentColor(opponentColor)
        game.doMove(color,i,j)
        return game.getMoves(opponentColor)

    # Devuelve todos los estados para un movimiento
    def getNextStates(self,color):
        moves = self.getMoves(color)
        states = []
        for move in moves:
            game = copy.deepcopy(self)
            game.doMove(color, move[0], move[1])
            states.append(game)
        states = self.sortStates(color, states)
        return states


    def getOpponentColor(self,color):
        if color == 1:
            return 2
        else:
            return 1

    # Obtiene el valor heuristico
    def getHeuristic(self,color,newGame):
        score = 0
        weights = [[100, -20, 10,  7,  7, 10, -20, 100],
                   [-20, -50, -4, -4, -4, -4, -50, -20],
                   [10,   -4, -2, -2, -2, -2,  -4, 10],
                   [7,    -4, -2,  1,  1, -2,  -4, 7],
                   [7,    -4, -2,  1,  1, -2,  -4, 7],
                   [10,   -4, -2, -2, -2, -2,  -4, 10],
                   [-20, -50, -4, -4, -4, -4, -50, -20],
                   [100, -20, 10,  7,  7, 10, -20, 100]]

        # Si el oponente no tiene ningun movimiento, el estado es muy bueno
        if len(newGame.getMoves(self.getOpponentColor(color))) == 0:
            return 100000000

        newboard = newGame.getBoard()
        for i in range(8):
            for j in range(8):
                if newboard[i][j] == color:
                    score += weights[i][j]
                elif newboard[i][j] == self.getOpponentColor(color):
                    score += -(weights[i][j])

        return score

    #Ordena los diferentes estados pasados por parametr, segun una heuristica dada
    def sortStates(self,color, states):
        scoreList = {}
        for i in states:
            score = self.getHeuristic(color, i)
            scoreList[i] = score
        scoreList = dict(sorted(scoreList.items(),reverse=True, key=lambda item: item[1]))
        return list(scoreList.keys())


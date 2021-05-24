from random import randint
import copy
import time
import Node

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

            numberMoves = len(game.getOpponentMove(move[0], move[1], game.getOpponentColor(self.color)))
            if numberMoves <= min:
                betterMoves.append(move)
                min = numberMoves

        # Dentro de todos los movimientos minimos se elige aleatoriamente para que las partidas no sean iguales
        random_number = randint(0, len(betterMoves)) - 1
        return betterMoves[random_number]

    # Comprueba si la posicion esta en una esquina del tablero
    def isCorner(self,move):
        if move == (0, 0) or move == (0, 7) or move == (7, 0) or move == (0, 7):
            return True
        return False


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
        self.moves = None

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

        self.moves = betterMoves
        random_number = randint(0, len(betterMoves)) - 1
        return betterMoves[random_number]

    # Actualiza la matriz de pesos
    def updateWeights(self,board):
        self.blockPerimeter(board, 0, 0)
        self.blockPerimeter(board, 0, 7)
        self.blockPerimeter(board, 7, 0)
        self.blockPerimeter(board, 7, 7)
        self.middlePerimeter(board)

    # Si una posicion se encuentra en el perimetro y no tiene al lado ninguna ficha de oponente, es una posicion buena
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
                if des < 8:
                    # Si una posicion del perimetro es cogida por el oponente, las posiciones de al lado son peores. Viendo los resultados, los empeora (NO SE HA ANADIDO)
                    if perimeter[i][j] == opponentColor and perimeter[i][j+1] == 0 and perimeter[i][des] == opponentColor:
                        if i == 0:
                            self.weights[i][j+1] = 8
                        elif i == 1:
                            self.weights[7][j+1] = 8
                        elif i == 2:
                            self.weights[j+1][0] = 8
                        else:
                            self.weights[j+1][7] = 8

    # Si a partir de una esquina, en las direcciones del perimetro hay fichas de nuestro mismo color, la siguiente posicion vacia sera muy buena
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

    # Comprueba si la posicion esta dentro de la matriz
    def inBoard(self,i,j):
        if i >= 0 and i < 8 and j >= 0 and j < 8:
            return True
        return False

    def getMoves(self):
        return self.moves


class AlphaBetaAgent():
    nodes = 0
    def __init__(self,color ,depth ,evaluator):
        self.color = color
        self.heuristic = 0
        self.evaluator = evaluator
        self.initialDepth = depth

        self.nodes = 0


    def getAction(self, game):
        board = self.bestMove(game, self.initialDepth)
        return board.getLastMove()

    def bestMove(self, game, depth):
        bestMove = None
        alpha = float('inf')
        beta = float('-inf')
        score = float('-inf')
        for child in game.getNextStates(self.color, self.evaluator.heuristicValue()):
            self.nodes += 1
            if bestMove == None:
                bestMove = copy.copy(child)
            newScore = self.alphabeta(child, depth - 1, alpha, beta, False)
            if score < newScore:
                score = newScore
                bestMove = copy.copy(child)
        return bestMove

    def alphabeta(self, game, depth, alpha, beta, actualPlayer):

        if depth == 0:
            function = self.evaluator.heuristicValue()
            return function(self.color,game)

        opponent = game.getOpponentColor(self.color)

        if actualPlayer:
            newScore = float('-inf')
            for child in game.getNextStates(self.color,self.evaluator.heuristicValue()):
                self.nodes +=1
                score = self.alphabeta(child, depth - 1,alpha, beta, False)
                if score > newScore:
                    newScore = score
                    beta = newScore
                if beta <= alpha:
                    break
            return beta

        else:
            newScore = float('inf')
            for child in game.getNextStates(opponent,self.evaluator.heuristicValue()):
                self.nodes += 1
                score = self.alphabeta(child, depth - 1, alpha, beta, True)
                if score < newScore:
                    newScore = score
                    alpha = newScore
                if beta <= alpha:
                    break
            return alpha

    def getNodesandDepth(self):
        return (self.nodes, self.initialDepth)

class MinimaxAgent():

    def __init__(self,color, depth, evaluator):
        self.color = color
        self.heuristic = 0
        self.evaluator = evaluator
        self.initialDepth = depth

        self.nodes = 0

    def getAction(self, game):
        board = self.bestMove(game,self.initialDepth)
        return board.getLastMove()

    def bestMove(self,game,depth):
        bestMove = None
        score = float('-inf')
        for child in game.getNextStates(self.color, None):
            self.nodes += 1
            newScore = self.minimax(child,depth-1,False)
            if score < newScore:
                score = newScore
                bestMove = copy.copy(child)
        return bestMove

    def minimax(self,game,depth,actualPlayer):

        if depth == 0:
            function = self.evaluator.heuristicValue()
            return function(self.color,game)

        opponent = game.getOpponentColor(self.color)

        if actualPlayer:
            newScore = float('-inf')
            for child in game.getNextStates(self.color, None):
                self.nodes += 1
                score = self.minimax(child, depth - 1, False)
                if score > newScore:
                    newScore = score
            return newScore

        else:
            newScore = float('inf')
            for child in game.getNextStates(opponent, None):
                self.nodes += 1
                score = self.minimax(child, depth - 1, True)
                if score < newScore:
                    newScore = score
            return newScore

    def getNodesandDepth(self):
        return (self.nodes, self.initialDepth)

# Union de los dos agentes de reglas anteriores
class UnionRulesAgent():

    def __init__(self, color):
        self.color = color
        self.weights = [[10, 0, 7, 7, 7, 7, 0, 10],
                        [0, 0, 3, 3, 3, 3, 0, 0],
                        [7, 3, 4, 4, 4, 4, 3, 7],
                        [7, 3, 4, 4, 4, 4, 3, 7],
                        [7, 3, 4, 4, 4, 4, 3, 7],
                        [7, 3, 4, 4, 4, 4, 3, 7],
                        [0, 0, 3, 3, 3, 3, 0, 0],
                        [10, 0, 7, 7, 7, 7, 0, 10]]
        self.agentRules = RulesAgent(self.color)
        self.agentAledoRules = RulesAledoAgent(self.color)


    def getAction(self,game):
        self.agentAledoRules.getAction(game)
        betterMoves = self.agentAledoRules.getMoves()
        minimizeMoves = []
        min = float('inf')
        for move in betterMoves:
            numberMoves = len(game.getOpponentMove(move[0], move[1], game.getOpponentColor(self.color)))
            if numberMoves <= min:
                minimizeMoves.append(move)
                min = numberMoves
        random_number = randint(0, len(minimizeMoves)) - 1
        return minimizeMoves[random_number]

# Agente no heuristico
class MonteCarloAgent():

    def __init__(self, color, evaluator):
        self.color = color
        self.root = None
        self.turn = self.color
        self.evaluator = evaluator

    def getAction(self,game):
        root = Node.Node(game,self.color)
        for i in range(100):
            node = root.select()
            self.turn = node.getTurn()
            result = self.simulate(node.getGame())
            node.backpropagate(result)
        betterNode = root.bestChild()
        child = betterNode.getGame()
        return child.getLastMove()

    # Simula la partida actual y devuelve el ganador o si es empate
    def simulate(self,game):
        gameSimulate = copy.deepcopy(game)
        turn = self.turn
        black = RandomAgent(2)
        white = RandomAgent(1)
        while True:
            moves = gameSimulate.getMoves(turn)
            if moves != []:
                (x, y) = (-1, -1)
                if turn == 2:
                    (x, y) = black.getAction(gameSimulate)
                else:
                    (x, y) = white.getAction(gameSimulate)
                gameSimulate.doMove(turn, x, y)
            if turn == 1:
                turn = 2
            else:
                turn = 1
            if gameSimulate.isEnd():
                break;
        result = gameSimulate.getWinner
        if result == 1 and self.color == 1:
            return 1
        elif result == 2 and self.color == 2:
            return 1
        else:
            return -1



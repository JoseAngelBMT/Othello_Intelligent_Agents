from random import randint
import copy
import time
import Node
import time
import multiprocessing as mp

class RandomAgent():

    def __init__(self,color):
        self.color = color

    # Un movimiento aleatorio de los movimientos legales
    def getAction(self, game):
        moves = game.getMoves(self.color)
        if moves == []:
            return (None, None)
        random_number = randint(0, len(moves) -1)
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
        random_number = randint(0, len(betterMoves) - 1)

        return betterMoves[random_number]

    # Comprueba si la posicion esta en una esquina del tablero
    def isCorner(self,move):
        if move == (0, 0) or move == (0, 7) or move == (7, 0) or move == (0, 7):
            return True
        return False


class RulesPriorityAgent():

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
        random_number = randint(0, len(betterMoves) - 1)
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
    def __init__(self,color ,depth ,evaluator):
        self.color = color
        self.heuristic = 0
        self.evaluator = evaluator
        self.initialDepth = depth

        self.nodes = 0
        self.timeMove = 0
        self.moves = 0


    def getAction(self, game):
        start_time = time.time()
        board = self.bestMove(game, self.initialDepth)
        final_time = time.time() - start_time
        self.timeMove += final_time
        self.moves += 1
        return board.getLastMove()

    def bestMove(self, game, depth):
        bestMove = None
        alpha = float('inf')
        beta = float('-inf')
        newScore = float('-inf')
        for child in game.getNextStates(self.color, self.evaluator.heuristicValue()):
            self.nodes += 1
            if bestMove == None:
                bestMove = copy.copy(child)
            score = self.alphabeta(child, depth - 1, alpha, beta, False)
            if score > newScore:
                newScore = score
                alpha = newScore
                bestMove = copy.copy(child)
            if beta <= alpha:
                break;
        return bestMove

    def alphabeta(self, game, depth, alpha, beta, actualPlayer):

        if depth == 0 or game.isEnd():
            function = self.evaluator.heuristicValue()
            return function(self.color,game)

        opponent = game.getOpponentColor(self.color)

        if actualPlayer:
            newScore = float('-inf')
            for child in game.getNextStates(self.color,self.evaluator.heuristicValue()):
                self.nodes += 1
                score = self.alphabeta(child, depth - 1,alpha, beta, False)
                if score > newScore:
                    newScore = score
                    alpha = newScore
                if beta <= alpha:
                    break
            return alpha

        else:
            newScore = float('inf')
            for child in game.getNextStates(opponent,self.evaluator.heuristicValue()):
                self.nodes += 1
                score = self.alphabeta(child, depth - 1, alpha, beta, True)
                if score < newScore:
                    newScore = score
                    beta = newScore
                if beta <= alpha:
                    break
            return beta

    def getNodesandDepth(self):
        return (self.nodes, self.initialDepth)

    def getTimeandMoves(self):
        return (self.timeMove/self.moves, self.moves)

class MinimaxAgent():
    def __init__(self,color, depth, evaluator):
        self.color = color
        self.heuristic = 0
        self.evaluator = evaluator
        self.initialDepth = depth

        self.nodes = 0
        self.timeMove = 0
        self.moves = 0

    def getAction(self, game):

        start_time = time.time()
        board = self.bestMove(game,self.initialDepth)
        final_time = time.time() - start_time
        self.timeMove += final_time
        self.moves += 1

        return board.getLastMove()


    def bestMove(self,game,depth):
        bestMove = None
        newScore = float('-inf')
        for child in game.getNextStates(self.color, self.evaluator.heuristicValue()):
            if bestMove == None:
                bestMove = copy.copy(child)
            self.nodes += 1
            score = self.minimax(child,depth-1,False)
            if score > newScore:
                newScore = score
                bestMove = copy.copy(child)
        return bestMove

    def minimax(self,game,depth,actualPlayer):

        if depth == 0:
            function = self.evaluator.heuristicValue()
            return function(self.color,game)

        opponent = game.getOpponentColor(self.color)

        if actualPlayer:
            newScore = float('-inf')
            for child in game.getNextStates(self.color, self.evaluator.heuristicValue()):
                self.nodes += 1
                score = self.minimax(child, depth - 1, False)
                if score > newScore:
                    newScore = score
            return newScore

        else:
            newScore = float('inf')
            for child in game.getNextStates(opponent, self.evaluator.heuristicValue()):
                self.nodes += 1
                score = self.minimax(child, depth - 1, True)
                if score < newScore:
                    newScore = score
            return newScore

    def getNodesandDepth(self):
        return (self.nodes, self.initialDepth)

    def getTimeandMoves(self):
        return (self.timeMove/self.moves, self.moves)

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
        self.agentAledoRules = RulesPriorityAgent(self.color)


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

    def __init__(self, color, iterations):
        self.color = color
        self.root = None
        self.turn = self.color
        self.iterations = int(iterations)

        self.nodes = 0
        self.timeMove = 0
        self.moves = 0

    def getAction(self,game):
        start_time = time.time()
        root = Node.Node(copy.deepcopy(game),self.color)
        #timeCondition = time.time()
        #timeFinish = time.time() - timeCondition
        #while (time.time() - timeCondition) <= self.iterations:
        for i in range(self.iterations):
            node = self.select(root)
            result = self.simulate(node.getGame(), node.getTurn())
            node.backpropagate(result)

        bestChild = root.bestChild()
        child = bestChild.getGame()

        final_time = time.time() - start_time
        self.timeMove += final_time
        self.moves +=1
        self.nodes += root.getNodes()

        return child.getLastMove()

    def select(self, node):
        while not node.isLeaf():
            if not node.isExpanded():
                return node.expand()
            else:
                node = node.bestChild()
        return node


    # Simula la partida actual y devuelve el ganador o si es empate
    def simulate(self, game, turn):
        gameTurn = turn
        gameSimulate = copy.deepcopy(game)
        black = RandomAgent(2)
        white = RandomAgent(1)
        while not gameSimulate.isEnd():
            if gameTurn == 2:
                (x, y) = black.getAction(gameSimulate)
            else:
                (x, y) = white.getAction(gameSimulate)
            if x != None:
                gameSimulate.doMove(gameTurn, x, y)
            gameTurn = self.changeTurn(gameTurn)

        result = gameSimulate.getWinner()
        if result == 1 and self.color == 1:
            return 1
        elif result == 2 and self.color == 2:
            return 1
        else:
            return -1

    def getNodesandDepth(self):
        return (self.nodes, self.iterations)

    def getTimeandMoves(self):
        return (self.timeMove/self.moves, self.moves)

    def changeTurn(self,color):
        if color == 1:
            return 2
        else:
            return 1


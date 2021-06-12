import numpy as np
import copy
from random import randint
import random as rd
import Evaluator as ev
import Agent as ag
import time
import GameRules as gm
import pandas as pd
from collections import Counter
import ast

class Genetic():

    def __init__(self,poblation,range):
        self.weights = [[120, -20, 20, 5, 5, 20, -20, 120],
                     [-20, -40, -5, -5, -5, -5, -40, -20],
                     [20, -5, 15, 3, 3, 15, -5, 20],
                     [5, -5, 3, 3, 3, 3, -5, 5],
                     [5, -5, 3, 3, 3, 3, -5, 5],
                     [20, -5, 15, 3, 3, 15, -5, 20],
                     [-20, -40, -5, -5, -5, -5, -40, -20],
                     [120, -20, 20, 5, 5, 20, -20, 120]]
        """self.weights = [[100, -20, 10, 7, 7, 10, -20, 100],
                   [-20, -50, -4, -4, -4, -4, -50, -20],
                   [10, -4, -2, -2, -2, -2, -4, 10],
                   [7, -4, -2, 1, 1, -2, -4, 7],
                   [7, -4, -2, 1, 1, -2, -4, 7],
                   [10, -4, -2, -2, -2, -2, -4, 10],
                   [-20, -50, -4, -4, -4, -4, -50, -20],
                   [100, -20, 10, 7, 7, 10, -20, 100]]"""
        self.npoblation = poblation
        self.range = range
        self.actualPoblation = None
        self.threshold = 64/4

        self.parents = None
        self.childs = None
        self.better = None
        self.bestScore = -200
        self.count = 0

    # Inicia la poblacion desde la matriz inicial
    def initPoblation(self):

        individuals = []
        individuals.append(copy.deepcopy(self.weights))
        for i in range(self.npoblation -1):
            matrix = self.randomMatrix()
            individuals.append(copy.deepcopy(matrix))

        self.actualPoblation = individuals

    # Crea matrices con numeros aleatorios dentro de un rango
    def randomMatrix(self):
        matrix = copy.deepcopy(self.weights)
        for i in range(8):
            for j in range(8):
                value = matrix[i][j]
                matrix[i][j] = randint(value-self.range, value+self.range)

        return matrix


    def coupleDiffer(self, ind1, ind2):
        n = 0

        differentPositions = []
        for i in range(8):
            for j in range(8):
                v1 = ind1[i][j]
                v2 = ind2[i][j]
                if v1 != v2:
                    n += 1
                    differentPositions.append((i,j))
        return n, differentPositions

    def modifyMatrix(self,matrix):
        for i in range(8):
            for j in range(8):
                random = randint(0,100)
                if random < 10:
                    matrix[i][j] = randint(matrix[i][j]-self.range, matrix[i][j]+self.range)
        return matrix

    # FUNCIONES ALGORITMO GENETICO CHC
    def selection(self):
        childs = []
        individuals = copy.deepcopy(self.actualPoblation)
        self.parents = copy.deepcopy(individuals)
        random_list = self.randomList(len(individuals))

        for (ind1, ind2) in random_list:
            differ, positions = self.coupleDiffer(individuals[ind1],individuals[ind2])
            if(differ/2 > self.threshold):
                descendant1, descendant2 = self.uniformCrossoverHUX(individuals[ind1],individuals[ind2], positions)
                childs.append(descendant1)
                childs.append(descendant2)

        self.childs = copy.deepcopy(childs)

    def uniformCrossover(self, matrix1, matrix2):
        child1 = copy.deepcopy(matrix1)
        child2 = copy.deepcopy(matrix2)
        for i in range(8):
            for j in range(8):
                random = randint(0, 1)
                if random == 0:
                    value1 = matrix1[i][j]
                    value2 = matrix2[i][j]
                    child1[i][j] = value2
                    child2[i][j] = value1

        return child1, child2

    def uniformCrossoverHUX(self, matrix1, matrix2, positions):
        child1 = copy.deepcopy(matrix1)
        child2 = copy.deepcopy(matrix2)
        numberExchanges = int(len(positions)/2)
        rd.shuffle(positions) # Ordena aleatoriamente las posiciones con valores diferentes entre los padres
        """for x, y in positions:
            child1[x][y] = matrix2[x][y]
            child2[x][y] = matrix1[x][y]"""
        for k in range(numberExchanges):
            (i, j) = positions[k]
            child1[i][j] = matrix2[i][j]
            child2[i][j] = matrix1[i][j]

        return child1, child2

    def elitism(self):
        if(len(self.childs) == 0):
            self.actualPoblation = self.parents
            return True, self.bestScore

        print("LONGITUD PADRES E HIJOS: ",len(self.parents),len(self.childs))
        individuals = self.parents + self.childs
        scores = {}
        i=0
        for individual in individuals:
            print(i, end=" ")
            score = self.getFitness(individual)
            ind = str(individual)
            scores[ind] = score
            i+=1
        print("\n")
        scoreList = dict(sorted(scores.items(),reverse=True, key=lambda item: item[1]))
        l = list(scoreList.keys())
        best = []
        i=0
        for ind in l:
            if i >= self.npoblation:
                break
            ind = ast.literal_eval(ind)
            best.append(ind)
            i +=1

        if(self.duplicates(best)):
            print("HAY DUPLICADOS")


        self.actualPoblation = copy.deepcopy(best)
        scores = list(scoreList.values())
        maxScore = scores[0]
        if self.bestScore < maxScore:
            self.bestScore = maxScore
            self.better = best[0]
            self.count = 0
        elif self.bestScore == maxScore:
            self.count +=1

        """if self.count == 10:
            self.threshold -=1
            print("Desciende el umbral por estancamiento: ",self.threshold)
            self.count = 0"""
        
        if Counter(map(id,self.parents)) == Counter(map(id,best)):
            return True, maxScore
        return False, maxScore

    # 35% modificacion del mejor individuo
    def rebootPoblation(self):
        individuals = []
        best = self.better
        individuals.append(copy.deepcopy(best))
        
        for i in range(self.npoblation - 1):
            matrix = self.modifyBest(best)
            individuals.append(copy.deepcopy(matrix))

        self.actualPoblation = individuals

    def modifyBest(self,matrix):
        newMatrix = copy.deepcopy(matrix)
        for i in range(8):
            for j in range(8):
                nRandom = randint(1,100)
                if(nRandom <= 35):
                    value = newMatrix[i][j]
                    newMatrix[i][j] = randint(value-self.range, value+self.range)
        return newMatrix

    def simulateGame(self,agent1, agent2):
        game = gm.Othello()
        agentW = agent1
        agentB = agent2
        turn = 2
        while True:
            moves = game.getMoves(turn)
            if moves != []:
                (x, y) = (-1, -1)
                if turn == 2:
                    (x, y) = agentB.getAction(game)
                else:
                    (x, y) = agentW.getAction(game)
                game.doMove(turn, x, y)
            if turn == 1:
                turn = 2
            else:
                turn = 1
            if game.isEnd():
                break
        return game.getWinner(), game

    # Elabora las partidas entre dos matrices
    def resultSimulate(self,matrix1,matrix2):
        ev1_1 = ev.Evaluator(1, matrix1)
        ev2_1 = ev.Evaluator(1, matrix2)
        ag1_1 = ag.AlphaBetaAgent(1, 4, ev1_1)     # ind1 -> Blanco
        ag2_1 = ag.AlphaBetaAgent(2, 4, ev2_1)     # ind2 -> Negro
        simulate1 = self.simulateGame(ag1_1, ag2_1)
        a1w, a2b, d1 = 0,0,0
        if(simulate1 == 2):
            a2b +=1
        elif(simulate1 == 1):
            a1w +=1
        else:
            d1 +=1

        ev1_2 = ev.Evaluator(1, matrix1)
        ev2_2 = ev.Evaluator(1, matrix2)
        ag1_2 = ag.AlphaBetaAgent(2, 4, ev1_2)     # ind1 -> Negro
        ag2_2 = ag.AlphaBetaAgent(1, 4, ev2_2)     # ind2 -> Blanco
        simulate2 = self.simulateGame(ag2_2, ag1_2)
        a2w, a1b, d2 = 0, 0, 0
        if (simulate2 == 2):
            a1b += 1
        elif (simulate2 == 1):
            a2w += 1
        else:
            d2 += 1

        a1 = a1w + a1b
        a2 = a2w + a2b
        d = d1 + d2
        if a1 > a2:
            return matrix1,1
        elif a2 > a1:
            return matrix2,2
        else:
            random = randint(0,1)
            if random == 0:
                return matrix1,-1
            else:
                return matrix2,-2

    def randomList(self,n):
        random_list = []
        while len(random_list) < n:
            random = randint(0, n - 1)
            if random not in random_list:
                random_list.append(random)
        return [(random_list[i],random_list[i+1]) for i in range(0,len(random_list),2)]


    def getFitness(self,matrix):
        ev1_1 = ev.Evaluator(1,matrix)
        ev2_1 = ev.Evaluator(2)
        ag1_1 = ag.AlphaBetaAgent(1,2,ev1_1)
        ag2_1 = ag.AlphaBetaAgent(2,2,ev2_1)
        result1, game1 = self.simulateGame(ag1_1, ag2_1)
        
        white, black = game1.countColors()

        if black == 0:
            fitness1 = 64
        elif white == 0:
            fitness1 = -64
        else:
            fitness1 = white - black



        ev1_2 = ev.Evaluator(1, matrix)
        ev2_2 = ev.Evaluator(2)
        ag2_2 = ag.AlphaBetaAgent(1, 2, ev2_2)
        ag1_2 = ag.AlphaBetaAgent(2, 2, ev1_2)
        result2, game2 = self.simulateGame(ag2_2,ag1_2)

        white, black = game2.countColors()

        if black == 0:
            fitness2 = -64
        elif white == 0:
            fitness2 = 64
        else:
            fitness2 = black - white

        fitness = (fitness1 + fitness2)
        return fitness

    def corners(self,game, color):
        board = game.getBoard()
        corners = 0
        if board[0][0] == color:
            corners += 1
        if board[0][7] == color:
            corners += 1
        if board[7][0] == color:
            corners += 1
        if board[7][7] == color:
            corners += 1
        return corners


    def matrixExtremumValues(self, matrix):
        min, max = 0, 0
        for i in range(8):
            for j in range(8):
                value = matrix[i][j]
                if value > 0:
                    max += value
                elif value < 0:
                    min += value
        return max, min

    def duplicates(self,lista):
        nuevaLista = []
        for elem in lista:
            if elem in nuevaLista:
                return True
            else:
                nuevaLista.append(elem)
        return False

    def printMatrix(self,matrix):
        for i in range(8):
                print(matrix[i])

    def getPoblation(self):
        return self.actualPoblation

    def getThreshold(self):
        return self.threshold;

    def setThreshold(self, value):
        self.threshold = value



class Main():
    
    start_time = time.time()
    genetic = Genetic(10,20)
    genetic.initPoblation()
    condition = False
    same = False
    i = 0
    scores = np.array([])
    while(not condition):
        same = False
        print("Iteracion: ",i+1)
        genetic.selection()
        isEqual, score = genetic.elitism()
        print("Score: " ,score)
        scores = np.append(scores, score)
        if(score > 82):
            matrix = genetic.better
            condition = True

        if(isEqual): #Misma poblacion
            genetic.threshold -=1
            print("Desciende el umbral: ",genetic.threshold)
            same = True
        if(genetic.threshold <= 0):
            print("Reinicio de poblacion")
            genetic.rebootPoblation()
            genetic.threshold = 16
        i+=1
        

    print("Calculando el mejor individuo")
    genetic.printMatrix(matrix)
    print(scores)
    time = (time.time() - start_time)
    min, seg = divmod(time, 60)
    print("Tiempo de ejecucion: ", int(min), ":", int(seg), " min \n")

    file = open("AGCHC.txt", "a")
    text = "\n"+str(matrix) + "\n" + "Total Time: " + str(time)+"\nScores: "+str(scores)+"\n\n"
    file.write(text)
    file.close()








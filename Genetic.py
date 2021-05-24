import numpy as np
import copy
from random import randint
import Simulation as sim
import Evaluator as ev
import Agent as ag
import time
import GameRules as gm

class Genetic():

    def __init__(self,poblation,range):
        self.weights = [[100, -20, 10, 7, 7, 10, -20, 100],
                   [-20, -50, -4, -4, -4, -4, -50, -20],
                   [10, -4, -2, -2, -2, -2, -4, 10],
                   [7, -4, -2, 1, 1, -2, -4, 7],
                   [7, -4, -2, 1, 1, -2, -4, 7],
                   [10, -4, -2, -2, -2, -2, -4, 10],
                   [-20, -50, -4, -4, -4, -4, -50, -20],
                   [100, -20, 10, 7, 7, 10, -20, 100]]
        self.npoblation = poblation
        self.range = range
        self.actualPoblation = None
        self.threshold = 64/4

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
        matrix = copy.copy(self.weights)
        for i in range(8):
            for j in range(8):
                matrix[i][j] = randint(matrix[i][j]-self.range, matrix[i][j]+self.range)
        return matrix

    # Selecciona los mejores descendientes haciendo un torneo entre ellos
    def selection(self):
        bestIndividuals = []
        individuals = self.actualPoblation

        random_list = self.randomList(len(individuals))

        for (ind1, ind2) in random_list:
            print("Simulacion partida entre ",ind1, "y", ind2)
            result, number = self.resultSimulate(individuals[ind1],individuals[ind2])
            bestIndividuals.append(result)

        newPoblation = self.crossover(bestIndividuals)
        self.actualPoblation = newPoblation

    def coupleDiffer(self,ind1, ind2):
        i = 0
        for i in range(8):
            for j in range(8):
                v1 = self.actualPoblation[ind1]
                v2 = self.actualPoblation[ind2]
                if v1 == v2:
                    i += 1
        return i


    def crossover(self,individuals):
        poblation = []
        numberCross = 0
        random_list = self.randomList(len(individuals))
        for (ind1, ind2) in random_list:
            differ = self.coupleDiffer(ind1,ind2)
            if(differ != self.threshold):
                descendant1, descendant2 = self.uniformCrossoverHUX(individuals[ind1],individuals[ind2])
                poblation.append(descendant1)
                poblation.append(descendant2)
            else:
                numberCross +=1
                poblation.append(ind1)
                poblation.append(ind2)
        if(numberCross == self.npoblation / 2):
            self.threshold -=1
        newpoblation = poblation + individuals

        return newpoblation

    def modifyMatrix(self,matrix):
        for i in range(8):
            for j in range(8):
                random = randint(0,100)
                if random < 10:
                    matrix[i][j] = randint(matrix[i][j]-self.range, matrix[i][j]+self.range)
        return matrix

    def uniformCrossover(self,matrix1,matrix2):
        child1 = copy.copy(matrix1)
        child2 = copy.copy(matrix2)
        for i in range(8):
            for j in range(8):
                random = randint(0,1)
                if random == 0:
                    value1 = matrix1[i][j]
                    value2 = matrix2[i][j]
                    child1[i][j] = value2
                    child2[i][j] = value1

        return child1, child2

    def uniformCrossoverHUX(self, matrix1, matrix2):
        child1 = copy.copy(matrix1)
        child2 = copy.copy(matrix2)
        for i in range(8):
            for j in range(8):
                random = 1
                if (matrix1[i][j] == matrix2[i][j]):
                    random = 0
                if random == 1:
                    value1 = matrix1[i][j]
                    value2 = matrix2[i][j]
                    child1[i][j] = value2
                    child2[i][j] = value1

        return child1, child2

    # 35% modificacion del mejor individuo
    def rebootPoblation(self):
        individuals = []
        best = self.getBetterIndividual()
        individuals.append(copy.deepcopy(best))
        
        for i in range(self.npoblation - 1):
            matrix = self.modifyBest()
            individuals.append(copy.deepcopy(matrix))

        self.actualPoblation = individuals

    def modifyBest(self,matrix):
        newMatrix = copy.copy(matrix)
        for i in range(8):
            for j in range(8):
                nRandom = randint(1,100)
                if(nRandom > 35):
                    newMatrix[i][j] = randint(newMatrix[i][j]-self.range, newMatrix[i][j]+self.range)
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
                break;
        return game.getWinner()

    # Elabora las partidas entre dos matrices
    def resultSimulate(self,matrix1,matrix2):
        ev1_1 = ev.Evaluator(1, matrix1)
        ev2_1 = ev.Evaluator(1, matrix2)
        ag1_1 = ag.AlphaBetaAgent(1, ev1_1)     # ind1 -> Blanco
        ag2_1 = ag.AlphaBetaAgent(2, ev2_1)     # ind2 -> Negro
        simulate1 = self.simulateGame(ag1_1, ag2_1)
        a1w, a2b, d1 = 0,0,0
        if(simulate1 == 2):
            a2b +=1
            print("Gana blanco")
        elif(simulate1 == 1):
            a1w +=1
            print("Gana negro")
        else:
            d1 +=1

        ev1_2 = ev.Evaluator(1, matrix1)
        ev2_2 = ev.Evaluator(1, matrix2)
        ag1_2 = ag.AlphaBetaAgent(2, ev1_2)     # ind1 -> Negro
        ag2_2 = ag.AlphaBetaAgent(1, ev2_2)     # ind2 -> Blanco
        simulate2 = self.simulateGame(ag2_2, ag1_2)
        a2w, a1b, d2 = 0, 0, 0
        if (simulate2 == 2):
            print("Gana blanco")
            a1b += 1
        elif (simulate2 == 1):
            print("Gana negro")
            a2w += 1
        else:
            d2 += 1

        a1 = a1w + a1b
        a2 = a2w + a2b
        print(a1, a2)
        d = d1 + d2
        if a1 > a2:
            print("Gana 1")
            return matrix1,1
        elif a2 > a1:
            print("Gana 2")
            return matrix2,2
        else:
            print("Empate")
            random = randint(0,1)
            if random == 0:
                return matrix1,0
            else:
                return matrix2,0

    def randomList(self,n):
        random_list = []
        while len(random_list) < n:
            random = randint(0, n - 1)
            if random not in random_list:
                random_list.append(random)
        return [(random_list[i],random_list[i+1]) for i in range(0,len(random_list),2)]

    def getBetterIndividual(self):
        result = np.zeros(len(self.actualPoblation))
        for i in range(len(self.actualPoblation)):
            print(result)
            for j in range(len(self.actualPoblation)):
                j = i+j
                if i != j and j < len(self.actualPoblation):
                    print("Partida entre ",i,"y",j)
                    matrix, match = self.resultSimulate(self.actualPoblation[i], self.actualPoblation[j])
                    if match == 1:
                        result[i] += 1
                    elif match == 2:
                        result[j] += 1

        index = 0
        max = -1
        for i in range(len(result)):
            if result[i] > max:
                index = i
                max = result[i]
        return self.actualPoblation[index]

    def printMatrix(self,matrix):
        for i in range(8):
                print(matrix[i])

    def getPoblation(self):
        return self.actualPoblation

    def getThreshold(self):
        return self.threshold;


class Main():
    start_time = time.time()
    genetic = Genetic(8,20)
    genetic.initPoblation()
    for i in range(2):
        print("Iteracion: ",i)
        genetic.selection()
        if(genetic.getThreshold() < 0):
            genetic.rebootPoblation()

    print("Calculando el mejor individuo")
    matrix = genetic.getBetterIndividual()
    genetic.printMatrix(matrix)

    time = (time.time() - start_time)
    min, seg = divmod(time, 60)
    print("Tiempo de ejecucion: ", int(min), ":", int(seg), " min \n")








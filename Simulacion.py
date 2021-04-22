import Agent as ag
import GameRules as gm
import Evaluator as ev
import pandas as pd
import time


class Simulation():
    def __init__(self,agent1,agent2,nGames):
        self.agent1 = agent1
        self.agent2 = agent2
        self.nGames = nGames

        self.df = None
        #self.readCSV()




    def game(self):
        game = gm.Othello()
        agentW = self.agent1
        agentB = self.agent2
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

    def simulate(self):
        len = self.nGames
        agente1, agente2, empates = 0, 0, 0
        start_time = time.time()
        for i in range(len):
            print("Partida: ", i + 1, "/", len)
            if i < len / 2:
                 # HAY QUE CAMBIAR EL COLOR PARA LA OTRA MITAD DE SIMULACIONES
                value = self.game()
                if value == 1:
                    agente2 += 1
                elif value == 2:
                    agente1 += 1
                else:
                    empates += 1
            if i >= len / 2:
                self.agent1 = agent2
                self.agent2 = agent1
                value = self.game()
                if value == 2:
                    agente1 += 1
                elif value == 1:
                    agente2 += 1
                else:
                    empates += 1

        time = (time.time() - start_time)
        min, seg = divmod(time, 60)
        print("Tiempo de ejecucion: ", int(min), ":", int(seg), " min \n")

        print("TASA AGENTE1: ", round((agente1 / len) * 100, 2))
        print("TASA AGENTE2: ", round((agente2 / len) * 100, 2))
        print("TASA EMPATES: ", round((empates / len) * 100, 2))

    # Funciones de pandas para crear una base de datos de resultados
    def createCSV(self):
        df = pd.DataFrame(columns =["White", "Black", "Games", "Win", "Draw", "Lose", "Time", "Heuristic_White",
                                         "Heuristic_Black"])
        print(df)
        df.to_csv("./othello.csv")

    def readCSV(self):
        self.df = pd.read_csv("othello.csv")
        print(self.df.head(5))


class MainSimulate():

    simulate = Simulation(10)
    simulate.simulate(ag.AlphaBetaAgent())

import Agent as ag
import GameRules as gm
import Evaluator as ev
import pandas as pd
import time
import copy

class Simulation():
    def __init__(self,agent1,agent2,nGames,ev1 = "", ev2 = ""):
        self.agent1 = agent1 # Agente blanco
        self.agent2 = agent2 # Agente negro
        self.nGames = nGames

        self.ev1 = ev1
        self.ev2 = ev2
        self.nameW = agent1.__class__.__name__[:-5] # Quitar 'Agent' del string
        self.nameB = agent2.__class__.__name__[:-5]

        self.df = None
        self.readCSV()
        self.simulate()

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
        winner = game.getWinner()
        return winner

    def simulate(self):
        len = self.nGames
        agentW, agentB, empates = 0, 0, 0
        totalTime = 0
        nodesw, nodesb, depthw, depthb = 0, 0, 0, 0
        for i in range(len):
            start_time = time.time()
            value = self.game()
            final_time = (time.time() - start_time)
            if value == 1:
                agentW += 1
            elif value == 2:
                agentB += 1
            else:
                empates += 1
            totalTime += final_time


        self.insertRow(self.nameW + str(self.ev1), self.nameB + str(self.ev2), agentW, agentB, empates, totalTime)
        self.df.to_csv("./othello.csv")
        return agentW, agentB, empates

    # Funciones de pandas para crear una base de datos de resultados
    def readCSV(self):
        try:
            self.df = pd.read_csv("othello.csv", index_col=0)
        except:
            self.df = pd.DataFrame(columns=["White", "Black", "Win","Lose","Draw", "Time", "NodesW", "NodesB", "DepthW", "DepthB","MovesW","MovesB","TimeMoveW","TimeMoveB"])
            self.df.to_csv("./othello.csv", index_label= "Index")
        print(self.df.head)
    def insertRow(self,agent1, agent2, win, lose, draw, time):

        nodesw, nodesb, depthw, depthb, movesw, movesb, timeMovew, timeMoveb = None, None, None, None, None, None, None, None
        if self.nameW.startswith("AlphaBeta") or self.nameW.startswith("Minimax") or self.nameW.startswith("Monte"):
            nodesw, depthw = self.agent1.getNodesandDepth()
            timeMovew, movesw = self.agent1.getTimeandMoves()

        if self.nameB.startswith("AlphaBeta") or self.nameB.startswith("Minimax") or self.nameB.startswith("Monte"):
            nodesb, depthb = self.agent2.getNodesandDepth()
            timeMoveb, movesb = self.agent2.getTimeandMoves()

        df2 = pd.DataFrame([[agent1, agent2, win, lose, draw, time, nodesw, nodesb, depthw, depthb, movesw, movesb, timeMovew, timeMoveb]], columns=list(self.df))
        self.df = self.df.append(df2, ignore_index=True)


def simulateRulesandRandom(number_simulations):
    # White vs Black
    # Random vs Rules
    ag1_1 = ag.RandomAgent(1)
    ag2_1 = ag.RulesAgent(2)
    sim = Simulation(ag1_1, ag2_1, number_simulations)

    # Rules vs Random
    ag1_2 = ag.RulesAgent(1)
    ag2_2 = ag.RandomAgent(2)
    sim = Simulation(ag1_2, ag2_2, number_simulations)

    # Rules vs RulesAledo
    ag1_3 = ag.RulesAgent(1)
    ag2_3 = ag.RulesPriorityAgent(2)
    sim = Simulation(ag1_3, ag2_3, number_simulations)

    # RulesAledo vs Rules
    ag1_4 = ag.RulesPriorityAgent(1)
    ag2_4 = ag.RulesAgent(2)
    sim = Simulation(ag1_4, ag2_4, number_simulations)

    # RulesAledo vs RulesUnion
    ag1_5 = ag.RulesAgent(1)
    ag2_5 = ag.UnionRulesAgent(2)
    sim = Simulation(ag1_5, ag2_5, number_simulations)

    # RulesUnion vs RulesAledo
    ag1_6 = ag.UnionRulesAgent(1)
    ag2_6 = ag.RulesAgent(2)
    sim = Simulation(ag1_6, ag2_6, number_simulations)

def simulateEvaluator():
    # Alfabeta vs alfabeta variando evaluator
    for i in range(1, 7):
        for j in range(1, 7):
            if i != j:
                sim = Simulation(ag.AlphaBetaAgent(1, 4, ev.Evaluator(i)), ag.AlphaBetaAgent(2, 4, ev.Evaluator(j)), 1, i, j)

# Mejores evaluadores son 1 y 3, depth
def simulateBestAlphaModifyDepth(evaluator):
    ev1 = ev.Evaluator(evaluator)
    ev2 = ev.Evaluator(evaluator)
    # Deterministas
    #Alfabeta vs minimax
    for i in range(1,3):
        ag1 = ag.MinimaxAgent(1,i,ev1)
        ag2 = ag.MinimaxAgent(1,4,ev2)
        sim = Simulation(ag1, ag2, 1, evaluator, evaluator)

def simulateAlpha():
    ev1 = ev.Evaluator(1)
    ev2 = ev.Evaluator(1)

    """#Alfabeta vs Union
    ag1 = ag.AlphaBetaAgent(1,4,ev1)
    ag2 = ag.UnionRulesAgent(2)
    sim = Simulation(ag1, ag2, 250, 1)

    # Union vs Alfabeta
    ag1 = ag.UnionRulesAgent(1)
    ag2 = ag.AlphaBetaAgent(2,4,ev1)
    sim = Simulation(ag1, ag2, 250, None, 1)"""

    # Determinista
    # Alfabeta vs Minimax
    ag1 = ag.AlphaBetaAgent(1,4,ev1)
    ag2 = ag.MinimaxAgent(2,4,ev2)
    sim = Simulation(ag1, ag2, 1, 1, 1)

    # Minimax vs Alfabeta
    ag1 = ag.MinimaxAgent(1, 4, ev2)
    ag2 = ag.AlphabetaAgent(2, 4, ev1)
    sim = Simulation(ag1, ag2, 1, 1, 1)

    #Alfabeta vs MCTS
    ag1 = ag.AlphaBetaAgent(1, 4, ev1)
    ag2 = ag.MonteCarloAgent(2, None)
    sim = Simulation(ag1, ag2, 250, 1)

    # MCTS vs Alfabeta
    ag1 = ag.MonteCarloAgent(1,None)
    ag2 = ag.AlphaBetaAgent(2, 4, ev1)
    sim = Simulation(ag1, ag2, 250, None, 1)

def simulateDepthAB():
    ev1 = ev.Evaluator(1)
    ev2 = ev.Evaluator(1)

    for i in range(13):
        sim = Simulation(ag.AlphaBetaAgent(1, i, ev1), ag.AlphaBetaAgent(2, 4, ev2), 1, "", 1)

        sim = Simulation(ag.AlphaBetaAgent(1, 4, ev2), ag.AlphaBetaAgent(2, i, ev1), 1, 1, "")

def simulateDepthM():
    ev1 = ev.Evaluator(1)
    ev2 = ev.Evaluator(1)

    for i in range(1,9):
        sim = Simulation(ag.MinimaxAgent(1, i, ev1), ag.AlphaBetaAgent(2, 4, ev2), 1, "", 1)

        sim = Simulation(ag.AlphaBetaAgent(1, 4, ev2), ag.MinimaxAgent(2, i, ev1), 1, 1, "")

def simulateMCTS():
    Simulation(ag.MonteCarloAgent(1, 10), ag.UnionRulesAgent(2), 50)

    Simulation(ag.UnionRulesAgent(1), ag.MonteCarloAgent(2, 10), 50)

    for i in range(20,80,20):
        Simulation(ag.MonteCarloAgent(1, i), ag.UnionRulesAgent(2), 50)

        Simulation(ag.UnionRulesAgent(1), ag.MonteCarloAgent(2, i), 50)
        
def tiempoMCTS():
    Simulation(ag.MonteCarloAgent(1, 0.47), ag.UnionRulesAgent(2), 50)

    Simulation(ag.UnionRulesAgent(1), ag.MonteCarloAgent(2, 0.47), 50)

    Simulation(ag.MonteCarloAgent(1, 0.93), ag.UnionRulesAgent(2), 50)

    Simulation(ag.UnionRulesAgent(1), ag.MonteCarloAgent(2, 0.93), 50)

    Simulation(ag.MonteCarloAgent(1, 1.89), ag.UnionRulesAgent(2), 50)

    Simulation(ag.UnionRulesAgent(1), ag.MonteCarloAgent(2, 1.89), 50)

    Simulation(ag.MonteCarloAgent(1, 3.06), ag.UnionRulesAgent(2), 50)

    Simulation(ag.UnionRulesAgent(1), ag.MonteCarloAgent(2, 3.06), 50)

    

class Main():
    tiempoMCTS()
import GameRules as gm
import Agent as ag
import numpy as np
import pandas as pd



def printBoard(board):
    for row in board:
        print(row)

game = gm.Othello()
agente = ag.RulesAledoAgent(2)


board = game.getBoard()

board = [[1, 1, 1, 1, 1, 1, 1, 1],
         [0, 0, 0, 0, 0, 1, 1, 1],
         [0, 0, 0, 0, 0, 0, 1, 1],
         [0, 0, 0, 0, 0, 0, 0, 1],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 1, 1],
         [0, 0, 0, 0, 0, 1, 1, 1],
         [0, 0, 0, 0, 1, 1, 1, 1]]
game.setBoard(board)



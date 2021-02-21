import numpy as np
import GameRules as gr
import Agent as ag

game = gr.Othello()
board = game.getBoard()

board[0][3] = 1
game.setBoard(board)

agente = ag.RulesAledoAgent(2)
move = agente.getAction(game)


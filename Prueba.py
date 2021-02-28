import GameRules as gm
import Agent as ag

game = gm.Othello()
agente = ag.RulesAledoAgent(2)

board = game.getBoard()
board[0][7] = 2
board[1][7] = 2
board[7][7] = 2
board[7][6] = 2
game.setBoard(board)
print(board)
agente.getAction(game)

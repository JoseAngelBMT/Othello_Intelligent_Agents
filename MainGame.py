import Interface
import Agent as ag
import GameRules as gr
import pygame as pg
import time
import Evaluator as ev


class Game():
    def __init__(self):

        self.nmoves = 1
        # Menu para elegir a los jugadores
        self.menu = Interface.Menu()
        self.playerBlack, self.playerWhite = self.menu.returnPlayers()
        self.evaluator1 = ev.Evaluator(1)
        self.evaluator2 = ev.Evaluator(1)

        self.selectPlayers()

        self.board = Interface.Board()

        # Crea el juego
        self.game = gr.Othello()
        self.startGame()


    # Crea el tipo de los dos jugadores
    def selectPlayers(self):
        if self.playerBlack == 2:
            self.agentBlack = ag.RandomAgent(2)
        elif self.playerBlack == 3:
            self.agentBlack = ag.RulesAgent(2)
        elif self.playerBlack == 4:
            self.agentBlack = ag.RulesPriorityAgent(2)
        elif self.playerBlack == 5:
            self.agentBlack = ag.UnionRulesAgent(2)
        elif self.playerBlack == 6:
            self.agentBlack = ag.AlphaBetaAgent(2, 4, self.evaluator1)
        elif self.playerBlack == 7:
            self.agentBlack = ag.MinimaxAgent(2, 5, self.evaluator1)
        elif self.playerBlack == 8:
            self.agentBlack = ag.MonteCarloAgent(2, 60)

        if self.playerWhite == 2:
            self.agentWhite = ag.RandomAgent(1)
        elif self.playerWhite == 3:
            self.agentWhite = ag.RulesPriorityAgent(1)
        elif self.playerWhite == 4:
            self.agentWhite = ag.RulesPriorityAgent(1)
        elif self.playerWhite == 5:
            self.agentWhite = ag.RulesPriorityAgent(1)
        elif self.playerWhite == 6:
            self.agentWhite = ag.AlphaBetaAgent(1, 4, self.evaluator2)
        elif self.playerWhite == 7:
            self.agentWhite = ag.MinimaxAgent(1, 5, self.evaluator2)
        elif self.playerWhite == 8:
            self.agentWhite = ag.MonteCarloAgent(1, 60)


    # Devuelve la posicion segun el tipo de jugador
    def getPosition(self,turn):
        if turn == 1:
            if self.playerWhite == 1:
                return self.board.getPositionMouse()
            else:
                return self.agentWhite.getAction(self.game)
        else:
            if self.playerBlack == 1:
                return self.board.getPositionMouse()
            else:
                return self.agentBlack.getAction(self.game)

    # Bucle principal que actualiza el juego y la interfaz
    def startGame(self):
        turn = 2
        actualBoard = self.game.getBoard()
        (x,y) = (-1,-1)

        while True:
            pg.event.pump() # Permite que la ventana no se quede colgada cuando no es necesario controlar eventos de teclado y raton
            # Interfaz
            self.board.printBoard()
            self.board.visualizeGrid(actualBoard)
            self.board.printMovement(self.game.getMoves(turn))
            self.board.printActualCoin(x,y)
            nWhites, nBlacks = self.game.countColors()
            self.board.printScoreboard(nBlacks,nWhites)

            # Comprueba si el juego termina
            if self.game.isEnd():
                break

            # Realiza el turno
            (x,y) = self.doTurn(turn)

            actualBoard = self.game.getBoard()
            # Cambia el turno
            if turn == 1:
                turn = 2
            else:
                turn = 1

            pg.display.flip()

        self.getWinner()
        time.sleep(3)
        pg.quit()
        Game()


    # Realiza un turno completo para el jugador
    def doTurn(self,turn):
        moves = self.game.getMoves(turn)
        if moves == []:
            return (-1,-1)
        validMove = False
        while not validMove:
            (x, y) = self.getPosition(turn)
            print(self.nmoves,"-> Turno: ", turn, " Movimiento: ",(x+1,y+1))
            self.nmoves +=1
            if (x, y) in moves:
                validMove = True
            else:
                print("Posicion incorrecta, intentalo con otra")

        self.game.doMove(turn, x, y)
        return (x,y)

    def getWinner(self):
        white, black = self.game.countColors()
        if white > black:
            self.board.printWinner('GANA EL JUGADOR BLANCO')
        elif white < black:
            self.board.printWinner('GANA EL JUGADOR NEGRO')
        else:
            self.board.printWinner('EMPATE')

        if self.agentBlack.__class__.__name__ == "AlphaBetaAgent" or self.agentBlack.__class__.__name__  == "MinimaxAgent":
            print("Negro Nodes: ",self.agentBlack.getNodesandDepth())
        if self.agentWhite.__class__.__name__ == "AlphaBetaAgent" or self.agentWhite.__class__.__name__  == "MinimaxAgent":
            print("Blanco Nodes: ",self.agentWhite.getNodesandDepth())

class Main():
    game = Game()
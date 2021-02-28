import pygame as pg
import pygame_menu as pgmenu
import os

class Board():

    def __init__(self):
        # Colores
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (53, 101, 77)  # Color del tablero

        pg.init()
        self.dimScreen = [1000, 680]
        self.dimBoard = [680, 680]
        self.screen = pg.display.set_mode(self.dimScreen)
        pg.display.set_caption("Othello")

        self.clock = pg.time.Clock()
        self.clock.tick(24)
        self.width = int(self.dimBoard[0] / 8)
        self.heigth = int(self.dimBoard[1] / 8)

    # Dibuja las lineas del tablero
    def printLines(self):
        for i in range(7):
            x = int((self.dimBoard[0] * (i + 1)) / 8)
            pg.draw.line(self.screen, self.BLACK, (x, 0), (x, self.dimBoard[0]), 1)
            pg.draw.line(self.screen, self.BLACK, (0, x), (self.dimBoard[1], x), 1)
        pg.draw.line(self.screen, self.BLACK, (self.dimBoard[0], 0), (self.dimBoard[0], self.dimBoard[1]), 1)
        pg.display.update()

    # Crea la ficha dentro del tablero
    def createCoin(self, x, y, color):
        pg.draw.circle(self.screen, color, (int(x), int(y)), 40)

    # Crea la ficha vacia para ver los movimientos disponibles
    def createEmptyCoin(self,x, y, color):
        pg.draw.circle(self.screen, color, (int(x), int(y)), 40, 1)

    # Dibuja el tablero
    def visualizeGrid(self, matrix):
        for row in range(len(matrix)):
            for column in range(len(matrix)):
                y = (row + 1) * self.width - 42.5
                x = (column + 1) * self.heigth - 42.5
                if matrix[row,column] == 1:
                    self.createCoin(x, y, self.WHITE)
                elif matrix[row,column] == 2:
                    self.createCoin(x, y, self.BLACK)
        pg.display.update()

    # Dibuja los movimientos legales
    def printMovement(self,moves):
        if moves == []:
            return None
        for i in moves:
            y = (i[0] + 1) * self.width - 42.5
            x = (i[1] + 1) * self.heigth - 42.5
            self.createEmptyCoin(x, y, self.BLACK)
        pg.display.update()

    # Inicia el tablero vacio
    def printBoard(self):
        self.screen.fill(self.GREEN)
        self.printLines()

    #Devuelve la posicion del raton como coordenadas en la matriz
    def getPositionMouse(self):
        pos = (None, None)
        while pos[0] == None:
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONUP:
                    pos = pg.mouse.get_pos()
        y = int(pos[0] / (self.dimBoard[0] / 8))
        x = int(pos[1] / (self.dimBoard[1] / 8))
        return (x, y)

    # Dibuja un punto rojo para indicar cual es la ficha mas reciente puesta
    def printActualCoin(self,i,j):
        y = (i + 1) * self.width - 42.5
        x = (j + 1) * self.heigth - 42.5
        pg.draw.circle(self.screen, (255,0,0), (int(x), int(y)), 5)
        pg.display.update()

    # Dibujar el numero de fichas en cada momento
    def printScoreboard(self,nBlacks,nWhites):
        font = pg.font.SysFont('Arial', 25)
        pg.draw.circle(self.screen, self.BLACK, (840, 200), 40)
        self.screen.blit(font.render(str(nBlacks), True, self.BLACK), (840, 250))
        pg.draw.circle(self.screen, self.WHITE, (840, 400), 40)
        self.screen.blit(font.render(str(nWhites), True, self.BLACK), (840, 450))
        pg.display.update()

    def printWinner(self,winner):
        font = pg.font.SysFont('Arial', 50)
        self.screen.blit(font.render(str(winner), True, (0, 0, 255)), (200, 340))
        pg.display.update()

class Menu():

    def __init__(self):
        pg.init()
        self.pBlack = 1 # Por defecto jugador humano
        self.pWhite = 1
        self.printMenu()

    # Dibuja el menu y las opciones
    def printMenu(self):
        menuScreen = [500, 500]
        os.environ['SDL_VIDEO_CENTERED'] = '1' # Poner las ventanas en medio de la pantalla
        self.screen = pg.display.set_mode(menuScreen)
        pg.display.set_caption("Othello")

        self.clock = pg.time.Clock()
        self.clock.tick(24)
        self.menu = pgmenu.Menu(500, 500, 'Othello',
                                theme=pgmenu.themes.THEME_GREEN)

        self.menu.add_selector('Jugador Negras :', [['Persona', 1], ['Aleatorio', 2], ['Reglas', 3], ['ReglasAledo',4], ['Minimax', 5]], onchange=self.playerBlack)
        self.menu.add_selector('Jugador Blancas :', [['Persona', 1], ['Aleatorio', 2],['Reglas', 3],['ReglasAledo',4], ['Minimax', 5]], onchange=self.playerWhite)
        self.menu.add_button('Jugar', self.startGame)
        self.menu.add_button('Salir', pgmenu.events.EXIT)
        self.menu.mainloop(self.screen)

    def playerBlack(self,value, player):
        self.pBlack = player

    def playerWhite(self, value, player):
        self.pWhite = player

    def startGame(self):
        self.menu.disable()
        self.menu.reset(1)

    def returnPlayers(self):
        return (self.pBlack,self.pWhite)








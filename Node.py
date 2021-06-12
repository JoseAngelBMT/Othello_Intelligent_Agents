import math
import random
import copy


class Node():
    totalVisits = 0
    def __init__(self,game, turn,parent = None):
        self.game = game
        self.parent = parent
        self.turn = turn
        self.children = set()       # DICT[move, NODE]

        self.visits = 0
        self.value = 0              # Resultados de las partidas
        self.nextStates = self.game.getNextStates(self.turn, None)
        self.nStates = len(self.nextStates)


    def isExpanded(self):
        return len(self.children) == self.nStates

    def bestChild(self):

        best = None
        score = -1000000
        i = 0
        for child in self.children:
            newScore = (child.value/child.visits) + (1) * math.sqrt(math.log(self.visits)/child.visits)
            #print("Hijo",i,":"," Visitas:",child.visits, " Resultados:", child.value, "Score: ",newScore)
            if score < newScore:
                score = newScore
                best = child
            #i += 1
        return best

    def expand(self):
        for child in self.nextStates:
            newChild = Node(copy.deepcopy(child), self.changeColor(self.turn),self)
            if newChild is not self.children:
                self.children.add(newChild)
                del self.nextStates[0]
            return newChild

    def backpropagate(self,result):
        self.value += result
        self.visits += 1
        Node.totalVisits += 1
        if not self.parent is None:
            self.parent.backpropagate(result)

    def UCT(self):
        return (self.value/self.visits) + (1) * math.sqrt(math.log(self.parent.visits)/self.visits)

    def isLeaf(self):
        return len(self.game.getMoves(self.turn)) == 0 or self.isEnd()

    def getGame(self):
        return self.game

    def getTurn(self):
        return self.turn

    def getNodes(self):
        return Node.totalVisits

    def isEnd(self):
        return self.game.isEnd()

    def addChild(self, child):
        self.children.add(child)

    def changeColor(self, color):
        if color == 1:
            return 2
        else:
            return 1
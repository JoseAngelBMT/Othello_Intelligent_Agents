import math
import random
import copy


class Node():
    totalVisits = 0
    def __init__(self,game, turn,parent = None):
        self.game = game
        self.parent = parent
        self.turn = turn
        self.children = set()  # DICT[move, NODE]

        self.visits = 0
        self.value = 0


    def isExpanded(self):
        return len(self.children) == len(self.game.getNextStates(self.turn, None))

    def bestChild(self):
        return max(self.children, key=lambda node: node.UCB())

    def select(self):
        while not self.isExpanded():
            return self.expand()
        if self.isExpanded():
            node = self.bestChild()
        return node

    def expand(self):
        for child in self.game.getNextStates(self.turn, None):
            newChild = Node(child, self.game.getOpponentColor(self.turn),self)
            if newChild is not self.children:
                self.children.add(newChild)
            return newChild

    def backpropagate(self,result):
        self.value += result
        self.visits += 1
        Node.totalVisits += 1
        if not self.parent is None:
            self.parent.backpropagate(result)

    def UCB(self):
        return self.value + math.sqrt(2*math.log(Node.totalVisits, math.e)/self.visits)

    def getGame(self):
        return self.game

    def getTurn(self):
        return self.turn
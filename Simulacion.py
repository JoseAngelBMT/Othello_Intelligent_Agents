import Agent as ag
import GameRules as gm
import time

def game(agentBla,agentWhi):
    game = gm.Othello()
    agentB = agentBla
    agentW = agentWhi
    turn = 2
    while True:
        moves = game.getMoves(turn)
        if moves != []:
            (x, y) = (-1,-1)
            if turn == 2:
                (x, y) = agentB.getAction(game)
            else:
                (x, y) = agentW.getAction(game)
            game.doMove(turn,x,y)
        if turn == 1:
            turn = 2
        else:
            turn = 1
        if game.isEnd():
            break;
    w,b = game.countColors()
    if w > b:
        #print("Gana blanco: "," Blanco: ",w," Negro: ",b)
        return 0
    elif w < b:
        #print("Gana negro"," Blanco: ",w," Negro: ",b)
        return 1
    else:
        return 2


len = 100
agente1, agente2, empates = 0,0,0
start_time = time.time()
for i in range(len):
    if i <  len/2:
        agentB = ag.MiniMaxAgent(2)
        agentW = ag.RulesAgent(1)
        value = game(agentB, agentW)
        if value == 0:
            agente2 += 1
        elif value == 1:
            agente1 += 1
        else:
            empates += 1
    if i >= len/2:
        agentW = ag.MiniMaxAgent(1)
        agentB = ag.RulesAgent(2)
        value = game(agentB, agentW)
        if value == 0:
            agente1 += 1
        elif value == 1:
            agente2 += 1
        else:
            empates += 1

print("Tiempo de ejecucion: ",(time.time() - start_time),"\n")

print("TASA AGENTE1: ", (agente1/len)*100)
print("TASA AGENTE2: ", (agente2/len)*100)
print("TASA EMPATES: ", (empates/len)*100)

import GameRules as gm

game = gm.Othello()
print(game.getBoard(),"\n\n\n")
boards = game.getnextStates(2)
for board in boards:
    print(board)
# Design of intelligent agents based on heuristics and evolutionary computation to play Othello

To test the graphical interface and compete against the intelligent agents, by executing the file "MainGame.py", the menu for the selection of the players and their corresponding colour will be opened.

By default, the evaluator for the Alfa-Beta agent will be the first weight matrix (value 1) commented in the memory, for the modification of the evaluator it is necessary to modify in the constructor the integer associated to the "Evaluator" class.
For the MCTS agent, the default number of iterations is 60. It can be modified in the "selectPlayers" function.
The file "Agent.py" contains the classes of all the implemented intelligent agents.

The file "Genetic.py" allows the execution of the genetic algorithm.

The results obtained for the memory realisation can be found in "AGCHC.txt". Resulting in the weight matrix, the evolution of the fitness and the execution time.
The file "Simulation.py", allows the creation of games and saving the results in "othello.csv".

"othello.csv" contains all the results obtained from the different studies of the project.

_______________________________________________________________________________________________________________________________________________________________________

Para probar la interfaz gráfica y competir contra los agentes inteligentes, mediante la ejecución del fichero "MainGame.py",
se abrirá el  menú para la selección de los jugadores y su color correspondiente.

1. Por defecto el evaluador para el agente Alfa-Beta será la primera matriz de pesos (valor 1) comentada en la memoria, para la modificación del evaluador es necesario modificar en el
el constructor el entero asociado a la clase "Evaluator".
2. Para el agente MCTS, el número de iteraciones por defecto son 60. Se puede modificar en la función "selectPlayers".

El fichero "Agent.py" contiene las clases de todos los agentes inteligentes implementados.

El fichero "Genetic.py" permite la ejecución del algoritmo genético.
1. Los resultados obtenidos para la realización de la memoria se encuentran en "AGCHC.txt". Dando como resultado la matriz de pesos, la evolución del fitness y el tiempo de ejecución

El fichero "Simulation.py", permite la creación de partidas y guardar los resultados en "othello.csv"
1. "othello.csv" contiene todos los resultados obtenidos de los diferentes estudios del proyecto.

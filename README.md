# TFGOthello
TFG Othello Agentes inteligentes

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

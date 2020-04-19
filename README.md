# Halma-Game-Playing-Agent
This is a programming assignment done for the CSCI 561 - Artificial Intelligence class.

The code in the game.py file is a fully functional game playing agent for the halma game (similar to checkers).

This agent defeated 75% of the class(750 students). Results: http://ilab.usc.edu/halma/HW2bis/

The objective is to defeat the agent designed by the professor.

The code implements a **min max tree algorithm with alpha beta pruining**.
A list of valid moves is generated and the best move is played minimizing the chances of the opponent to win. 

Th game uses the standard rules of the Halma game to decide who wins. 
Input.txt has the following information about the game
1) Game Mode(Single/Game)
1) Total Game time
2) Player's Turn
3) Current Board state

Sample:

SINGLE

WHITE

100.0

WWWWW...........

WWWWW...........

WWW.............

WWW.W...........

WW..............

................ 

................

................ 

................ 

................ 

................ 

..........B...BB 

.............BBB 

.............BBB 

...........BBBBB 

...........BBBBB 

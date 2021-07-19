# Gomoku-AI
(MinMax/player.py)  
This algorithm was a coursework for my AI module in university. It is designed to play freestyle Gomoku against an AI opponent as part of the Gomoku platform provided by my lecturer. The algorithm has two main components, a heuristic that scores the value of owning any single square, and a predictive algorithm that is a heavily modified version of a MinMax algorithm.  
  
The platform uses an 11x11 board, and players must match 5 pieces in a row to win. If a player tries to claim a square that is already claimed or is not on the board, they will lose by disqualification. If the board is filled without a winner, the game will be a draw.

### Selfish Heuristic
- The selfish heuristic assigns a score to a single root square. This score is the immediate benefit to the given player of taking that square and does not consider any benefit from blocking the opponent.
- It considers the state of 32 squares around the root square, those being all the squares that could possibly be part of the same line as the root square.
- If taking the root square would result in an immediate win, it is assigned the highest possible score.
- If taking the root square would guarantee a win next turn (set up two winning moves such that the opponent can only block one), it is assigned a very high score.
- Otherwise, the AI will assign scores based on 3 factors with descending significance. The number of claimed squares in all the lines it could help complete, the number of claimed squares it will be in continuous lines with, and the number of claimed or available squares in all the lines it could help complete.  
To simplify, it will prioritise setting up as many lines as possible that are as long as possible, then it will prioritise filling lines from the middle, then claiming squares where there is the most room to build new lines.

### MinMax Implementation
- The AI implements a modified MinMax algorithm and uses alpha beta pruning.
- The algorithm will assign scores to each possible move as a combination of the benefit to the given player and the harm to the opponent player (both using the selfish heuristic)
- It will then select a number of apparently best moves from the possible moves.
- If any of those apparently best moves is a winning move or required to prevent the opponent from winning, it will be returned as the actual best move.
- If any of those apparently best moves can be ruled out of being actual best moves, they will be ignored. Moves can be ruled out by alpha beta pruning where the score of the best possible move in a scenario is considered the score of that scenario.
- For each remaining move, the algorithm will generate the result of that move and then recurse, finding the other player's best move in each scenario.
- This recursion will halt if it goes beyond its maximum depth, or if the AI is almost out of time to decide its move.
- If no winning or required move has been found, then the initial moves will be scored based on their predicted outcomes (as far ahead as the algorithm has considered) and the one with the best outcome will be returned as the actual best move.

### Development Environment
- ubuntu 20.04
- Python 3.8.5

### Credit for the Included Gomoku Platform Files
(gomoku.py, gomokuAgent.py, misc.py)
Gomoku Platform (single game)
Version 0.5

Xiuyi Fan, Matt Bastiman, Edward Wall, Joe Panes  
Swansea University  
Feb 2020

# Gomoku-AI
(MinMax/player.py)

### How it Works


### Selfish Heuristic
- The selfish heuristic assigns a score to a single root square. This score is the immidiate benefit to the given player of taking that square, and does not consider any benefit from blocking the opponent.
- It considers the state of 32 squares around the root square, those being all of the squares that could possibly be part of the same line as the root square.
- If taking the root square would result in an immidiate win, it is assigned the highest possible score.
- If taking the root square would guarantee a win next turn (set up two winning moves such that the opponent can only block one), it is assigned a very high score.
- Otherwise, the AI will assign scores based on 3 factors with descending significance. The number of claimed squares in all the lines it could help complete, the number of claimed squares it will be in continuous lines with, and the number of claimed or available squares in all the lines it could help complete.  
To simplify, it will prioritise setting up as many lines as possible that are as long as possible, then it will prioritise filling lines from the middle, then filling squares where there is the most room to build new lines.

### MinMax Implementation
- The AI implements a modified MinMax algorithm and uses alpha beta pruning.
- The algorithm will assign scores to each possible move as a combination of the benefit to the given player and the harm to the opponent player (using the selfish heuristic)
- It will then select a number of apparently best moves from the possible moves.
- If any of those apparently best moves is a winning move, it will be returned as the actual best move.
- If any of those apparently best moves can be ruled out of being actual best moves, they will be ignored. Moves can be ruled out by alpha beta pruning where the score of the best possible move in a scenario is considered the score of that scenario.
- For each remaining move, the algorithm will generate the result of that move and then recurse, finding the other player's best move in each scenario.
- This recursion will halt if goes beyond its maximum depth, or if the AI is almost out of time to decide its move.
- If no winning outcome has been found, then the intial moves will be scored based on their predicted outcomes (as far ahead as the algorithm has considered) and the one with the best outcome will be returned as the actual best move.

### Credit for the Included Gomoku Platform Files
(gomoku.py, gomokuAgent.py, misc.py)

Gomoku Platform (single game)
Version 0.5

Xiuyi Fan, Matt Bastiman, Edward Wall, Joe Panes  
Swansea University  
Feb 2020

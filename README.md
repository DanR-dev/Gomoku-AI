# Gomoku-AI
(MinMax/player.py)

### How it Works


### Selfish Heuristic
- The selfish heuristic assigns a score to a single root square. This score is the immidiate benefit to the given player of taking that square, and does not consider any benefit from blocking the opponent.
- It considers the state of 32 squares around it, those being all of the squares that could possibly be part of the same line as the root square.
- If taking the root square would result in an immidiate win, it is assigned the highest possible score.
- If taking the root square would guarantee a win next turn (set up two winning moves such that the opponent can only block one), it is assigned a very high score.
- Otherwise, the AI will assign scores based on 3 factors with descending significance. The number of claimed squares in all the lines it could help complete, the number of claimed squares it will be in continuous lines with, and the number of claimed or available squares in all the lines it could help complete.  
To simplify, it will prioritise setting up as many lines as possible that are as long as possible, then it will prioritise filling lines from the middle, then filling squares where there is the most room to start new lines.

### MinMax Implementation

### Credit for the Included Gomoku Platform Files
(gomoku.py, gomokuAgent.py, misc.py)

Gomoku Platform (single game)
Version 0.5

Xiuyi Fan, Matt Bastiman, Edward Wall, Joe Panes  
Swansea University  
Feb 2020

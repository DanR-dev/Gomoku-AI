from misc import legalMove
from gomokuAgent import GomokuAgent
import time

class Player(GomokuAgent):
    N_MOVES_CONSIDER = 24; # how many moves with most immidiate gain to consider for each player turn
    N_MOVES_PREDICT = 4; # how many turns ahead to predict outcomes when choosing a move (alternating between self and opponent)
    TIME_LIMIT = 4.8; # how much time to allow recursive function to continue before returning a move

    moveStart = 0; # what time the programs turn started
    outOfTime = False; # whether or not the program has run out of time

    VERY_BIG_INT = 1000000;
    RANGE11 = list(range(11)); # for use in loops across a board (list/tuple access is faster than range access)
    DIAMETERS = [ # the relative positions of squares relevant to a root square, aranged as such:  [i][j][k]  i for diagonal-down, vertical, diagonal-up, horizontal.
        [                                                                                                  #  j for 1st direction in line, 2nd direction in line.
            [(-1, -1),(-2, -2),(-3, -3),(-4, -4)],                                                         #  k for closest, 2nd closest, 3rd closest, 4th closest.
            [(1, 1),(2, 2),(3, 3),(4, 4)]
        ],                                                                                   # access order:
        [                                                                                                  #  04 -- -- --  12  -- -- -- 20
            [(0, -1),(0, -2),(0, -3),(0, -4)],                                                             #  -- 03 -- --  11  -- -- 19 --
            [(0, 1),(0, 2),(0, 3),(0, 4)]                                                                  #  -- -- 02 --  10  -- 18 -- --
        ],                                                                                                 #  -- -- -- 01  09  17 -- -- --
        [                                                                                                  #  32 31 30 29 ROOT 25 26 27 28
            [(1, -1),(2, -2),(3, -3),(4, -4)],                                                             #  -- -- -- 21  13  05 -- -- --
            [(-1, 1),(-2, 2),(-3, 3),(-4, 4)]                                                              #  -- -- 22 --  14  -- 06 -- --
        ],                                                                                                 #  -- 23 -- --  15  -- -- 07 --
        [                                                                                                  #  24 -- -- --  16  -- -- -- 08
            [(1, 0),(2, 0),(3, 0),(4, 0)],
            [(-1, 0),(-2, 0),(-3, 0),(-4, 0)]
        ]
    ];

    # pick best move for given board
    def move(self, board):
        self.outOfTime = False; #       <- Note the starting time
        self.moveStart = time.time(); # <-
        if(board[5][5] == 0): #  <- Take center square if not already taken
            bestMove = (5, 5); # <-
        else: # otherwise, calculate the best move available
            bestMove = self.minMaxRecursive(board, self.ID, self.N_MOVES_CONSIDER, self.N_MOVES_PREDICT);
        return (bestMove[0], bestMove[1]);

    # calculate the benefit to the given player of claiming the given square of the given board (ignores all harm to opponent)
    # returns 12722 if immidiate win
    # returns 6361 if win next turn
    # returns 0 -> 6360 if no guaranteed win
    # returns None if illegal move
    def selfishHeuristic(self, board, rootX, rootY, playerID):
        if(board[rootX][rootY] == 0): # quick check if the move is legal
            score = 0; # how beneficial this move is to the given player
            lineOf4 = False; # whether the given player has a line of 3 out of 5 that this root square would extend to a line of 4 out of 5
            winIn2 = False;
            for diameter in self.DIAMETERS:
                completedLine = 0; # number of continuous peices of the given player that extend through this root square for this diameter
                partialLine = 0; # number of peices of the given player that are in this diameter and not cut off from the root square by an opponents' peice
                availableLine = 0; # number of (peices of the given player or empty squares) that are in this diameter and not cut off by an opponents' peice
                open4 = 0; # number of open ends in current diameter where current diameter must have a line of 3 that passes through the root square
                for radius in diameter:
                    lineBroken = False; # whether the current radius has reached an unclaimed square
                    for square in radius:
                        trueX = rootX + square[0]; # true X position of current square on the given board
                        trueY = rootY + square[1]; # true Y position of current square on the given board
                        if (trueX >= 0 and trueX < 11 and trueY >= 0 and trueY < 11): # check that current square is on the board
                            occupier = board[trueX][trueY]; # square currently being looked at in relation to root square
                            # RAW HEURISTIC SCORING:
                            if (occupier == -playerID): # <- if current square is claimed by opponent, all squares in current radius past it are irrelevant to the root square
                                break; #                  <-
                            elif(occupier == 0): # if current square is unclaimed, it and squares past it are only relevant to the root square for setting up future moves
                                if(completedLine >= 3): # <- if claiming the root square would create a line of 4 open at both ends, opponent cannot prevent win on next turn
                                    open4 += 1; #         <-
                                    if(open4 == 2): #     <-
                                        break; #          <-
                                availableLine += 1;
                                lineBroken = True;
                            elif(lineBroken == False): # every square so far in current radius and current square has been claimed by the given player
                                completedLine += 1;
                                partialLine += 1;
                                availableLine += 1;
                            else: # current square is claimed by given player but not in an unbroken line from root square
                                partialLine += 1;
                                availableLine += 1;
                # WEIGHTED HEURISTIC SCORING:
                if(completedLine >= 4):
                    return 12722; # if claiming root square is a winning move
                elif(open4 == 2):
                    winIn2 = True; # if win in 2 moves (complete a line of 4 open at both ends)
                elif(availableLine >= 4): # if line of 5 is possible in this diameter
                    if(lineOf4 and completedLine >= 3):
                        winIn2 = True; # if win in 2 moves (complete 2 lines of 4 with at least 1 open end each)
                    elif(completedLine >= 3):
                        lineOf4 = True;
                    score += partialLine * 265; # fill longest line first       : most significant factor (0, 265 ... 6360)
                    score += completedLine * 33; # fill lines from the middle   : mid significant factor (0, 33 ... 264)
                    score += availableLine; # fill where most options for lines : least significant factor (4, 5 ... 32)
            if(winIn2 == True):
                return 6361;
            return score;
        else:
            return None;

    # recursively calculate the best probable outcome of possible moves for the given board and return the best move
    # assuming opponent is trying to force a draw (after much AB testing, this seems to work best)
    # assuming opponent uses the same algorithm
    # assuming its the given player's turn
    # accounting for the given number of best moves per turn
    # accounting for the given number of turns (shared between given player and opponent)
    # using min-max algorithm
    # using alpha-beta pruning
    # using the calculated benefit of claiming any given square as the primary heuristic (not a board-wide heuristic. again, seems to work best)
    # halting recursive calls if out of time
    # returns the single best move possible (as far as parameters allow it to check)
    #         best move is returned as a list [y, x, score], where score is the best predicted outcome
    # returns [] if no moves are possible
    def minMaxRecursive(self, board, playerID, nMoves, nRecursions, alpha=-VERY_BIG_INT, beta=VERY_BIG_INT):
        selfishScoreboard = self.selfishScoreboard(board, playerID); # heuristic scores for possible moves of given player if ignoring opponent
        selflessScoreboard = self.selfishScoreboard(board, -playerID); # heuristic scores for possible moves of opponent if ignoring given player (blocking scores for given player)
        rootBoard = self.addBoards(selfishScoreboard, selflessScoreboard); # combined scores for given player to build lines and/or block opponent
        bestMoves = self.bestMoves(rootBoard, nMoves); # list of best moves for given player according to the rootBoard (limited to nMoves)
        nBestMoves = len(bestMoves); # true number of best moves found (smaller than nMoves if fewer legal moves available)
        iBestMoves = list(range(nBestMoves)); # indexes of best moves
        if(nBestMoves == 0): # <- if no available moves
            return []; #       <-
        if(self.outOfTime): #      <- if outOfTime is True, immidiately return best known move
            return bestMoves[0]; # <-
        if(time.time() - self.moveStart > self.TIME_LIMIT): # <- if out of time for first time, set outOfTime to True and immidiately return best known move
            self.outOfTime = True; #                          <-
            return bestMoves[0]; #                            <-
        if(nRecursions == 0 or bestMoves[0][2] >= 12722): # <- if depth limit reached or winning move found
            return bestMoves[0]; #                          <-
        # MAXIMISING
        if(playerID == self.ID):
            outcome = -self.VERY_BIG_INT;
            for i in iBestMoves:
                if(board[bestMoves[i][0]][bestMoves[i][1]] == 0): # quick check that move is legal
                    bestNextMove = self.minMaxRecursive( #             <- recursive call
                        self.tryMove(board, bestMoves[i], playerID), # <- for each apparently good move, predict the best move for the opponent given the resulting board
                        -playerID, #                                   <-
                        nMoves, #                                      <-
                        nRecursions - 1, #                             <-
                        alpha, #                                       <-
                        beta, #                                        <-
                    ); #                                               <-
                    if(len(bestNextMove) != 0): # if there is a valid next move
                        if(bestNextMove[2] > outcome):
                            outcome = bestNextMove[2];
                        if(outcome > alpha):
                            alpha = outcome;
                        if(alpha >= beta):
                            break; # tree cut-off due to beta pruning
                        bestMoves[i][2] = outcome;
            for move in bestMoves: #             <- place best move (opponent has worst options) at front
                if(move[2] < bestMoves[0][2]): # <-
                    bestMoves[0] = move; #       <-
        # MINIMISING
        else:
            outcome = self.VERY_BIG_INT;
            for i in iBestMoves:
                if(board[bestMoves[i][0]][bestMoves[i][1]] == 0): # quick check that move is legal
                    bestNextMove = self.minMaxRecursive( #             <- recursive call
                        self.tryMove(board, bestMoves[i], playerID), # <- for each apparently good move, predict the best move for the opponent given the resulting board
                        -playerID, #                                   <-
                        nMoves, #                                      <-
                        nRecursions - 1, #                             <-
                        alpha, #                                       <-
                        beta, #                                        <-
                    ); #                                               <-
                    if(len(bestNextMove) != 0): # if there is a valid next move
                        if(bestNextMove[2] < outcome):
                            outcome = bestNextMove[2];
                        if(outcome < beta):
                            beta = outcome;
                        if(alpha >= beta):
                            break; # tree cut-off due to alpha pruning
                        bestMoves[i][2] = outcome;
            for move in bestMoves: #             <- place best move (opponent has worst options) at front
                if(move[2] > bestMoves[0][2]): # <-
                    bestMoves[0] = move; #       <-
        return bestMoves[0];

#_____________________________________________________________convenience functions_____________________________________________________________

    # generate a scoreboard using the selfish heuristic for the given board for the given player's turn
    # return an 11x11 board with each square replaced with heuristic score of claiming that square
    # illegal moves are scored as None
    def selfishScoreboard(self, board, playerID):
        scoreBoard = [];
        for i in self.RANGE11:
            row = [];
            for j in self.RANGE11:
                row += [self.selfishHeuristic(board, i, j, playerID)];
            scoreBoard += [row];
        return scoreBoard;

    # find the given number of best moves for the given scoreboard
    # returns list of given number of best moves with single best move first (others un-ordered)
    #         each move is returned as a list [y, x, score]
    # returns [] if no moves available
    def bestMoves(self, scoreBoard, nMax):
        bestMoves = [];
        nBestMoves = 0;
        for i in self.RANGE11:
            for j in self.RANGE11:
                if(nBestMoves < nMax): #                           <- fill best moves list up to given number of best moves with first moves found
                    if(scoreBoard[j][i] != None): #                <-
                        bestMoves += [[j, i, scoreBoard[j][i]]]; # <-
                        nBestMoves += 1; #                         <-
                else: #                                        <- once best moves list contains given number of moves
                    minConsidered = bestMoves[0][2]; #         <- find the index and score of worst move in the current list of best moves
                    iMinConsidered = 0; #                      <-
                    for k in range(1, nBestMoves): #           <-
                        if(bestMoves[k][2] < minConsidered): # <-
                            minConsidered = bestMoves[k][2]; # <-
                            iMinConsidered = k; #              <-
                    if(scoreBoard[j][i] != None): #                                 <- if this move is better than the worst move in best moves list
                        if(scoreBoard[j][i] > minConsidered): #                     <- then replace worst move with this move in best moves list
                            bestMoves[iMinConsidered] = [j, i, scoreBoard[j][i]]; # <-
        if(nBestMoves > 0): # quick check that there is at least 1 possible move
            for i in range(1, nBestMoves): #             <- move the single best move in the best moves list to the front of the list
                if(bestMoves[i][2] > bestMoves[0][2]): # <-
                    temp = bestMoves[0]; #               <-
                    bestMoves[0] = bestMoves[i]; #       <-
                    bestMoves[i] = temp; #               <-
            return bestMoves;
        else:
            return [];

    # produce the result of the given player making the given move on the given board
    # return resultant board
    def tryMove(self, board, pos, playerID):
        newBoard = self.copyBoard(board);
        newBoard[pos[0]][pos[1]] = playerID;
        return newBoard;

    # add the contents of 2 scoreboards, applying the given weight to the second board given
    # returns the resultant scoreboard
    def addBoards(self, scoreBoard1, scoreBoard2):
        newScoreBoard = [];
        for i in self.RANGE11:
            row = [];
            for j in self.RANGE11:
                if(scoreBoard1[i][j] == None or scoreBoard2[i][j] == None):
                    row += [None];
                else:
                    row += [scoreBoard1[i][j] + scoreBoard2[i][j]];
            newScoreBoard += [row];
        return newScoreBoard;

    # produce a deep copy of the given board
    # returns a copy of original board
    def copyBoard(self, board):
        newBoard = [];
        for i in self.RANGE11:
            row = [];
            for j in self.RANGE11:
                row += [board[i][j]];
            newBoard += [row];
        return newBoard;

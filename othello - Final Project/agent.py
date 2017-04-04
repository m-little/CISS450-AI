'''
Author: Mike Little
Othelo AI agent using the minmax algorithm with alpha-beta pruning.
'''
"""
Agent clases

def get_action(self,
               game_id=None,   # Unique ID of game. Right now this is None.
               player=None,    # Either 'O' or '@'
               state=None,     # 2d array
               timeleft=0)     # time left in seconds
"""

from othello import *
import inspect
 
# Board is weighted to impart basic strategy on the AI agent, such as taking corners

weights = [[75, -25, 25, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,  25, -25, 75],
                        [-25, -50, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5,  -5, -50, -25],
                        [25, -5, 15, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,  15, -5, 25],
                        [5, -5, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,  4, -5, 5],
                        [5, -5, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,  4, -5, 5],
                        [5, -5, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,  4, -5, 5],
                        [5, -5, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,  4, -5, 5],
                        [5, -5, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,  4, -5, 5],
                        [5, -5, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,  4, -5, 5],
                        [5, -5, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,  4, -5, 5],
                        [5, -5, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,  4, -5, 5],
                        [5, -5, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,  4, -5, 5],
                        [5, -5, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,  4, -5, 5],
                        [25, -5, 15, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,  15, -5, 25],
                        [-25, -50, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5,  -5, -50, -25],
                        [75, -25, 25, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,  25, -25, 75]]

MAX = 0
for row in weights:
    for x in row:
        MAX += x
MIN = -MAX

beta = 0
for row in weights:
    for v in row:
        beta += v
alpha = -beta

# prints the char used by the opponent
def opponent(player):
    ret = '@'
    if player == '@':
        ret = 'O'

    return ret


def score_weight(player, state):
    total_score = 0
    opp = opponent(player)
    for x,row in enumerate(state):
        #print x, ': ',
        for y,space in enumerate(row):
            #print j,
            if space == player:
                total_score += weights[x][y]
                #total_score += 1
            elif space == opp:
                total_score -= weights[x][y]
                #total_score -= 1

    #print total_score        
    return total_score

class Agent:
    def __init__(self):
        pass
    def get_action(self,
                   game_id=None,
                   state=None,
                   timeleft=0):
        raise NotImplemented

# ai agent that picks a random move
class RandomAgent(Agent):
    def get_action(self,
                   game_id=None,
                   player=None,
                   state=None,
                   timeleft=0):
        oboard = OthelloBoard(board=state)
        options = oboard.expand(player)
        #print player
        if len(options) > 0:

            return random.choice(options)[1]
        else: # This should not happen
            return "pass"

def alphabeta(player, state, alpha, beta, depth):
    if depth == 0:
        return score_weight(player, state), None

    board = OthelloBoard(board = state)
    options = board.expand(player)

    if len(options) <= 0:
        return score_weight(player, state), None

    mv = None
    for option in options:
        new_state, tmp = option
        if alpha >= beta:
            break
        val = -alphabeta(opponent(player), new_state, -beta, -alpha, depth-1)[0]
        #print val
        if val > alpha or mv == None:
            alpha = val
            mv = tmp
    return alpha, mv

# ai agent that uses minmax with alpa-beta pruning
class AIAgent(Agent):
    def __init__(self):
        Agent.__init__(self)


    def get_action(self,
                   game_id=None,
                   player=None,
                   state=None,
                   timeleft=0):


        oboard = OthelloBoard(board=state)
        options = oboard.expand(player)
        o = options[0]
        #print o[1]
        #exit()
        s,rc = o
        beta = 0
        for row in weights:
            for v in row:
                beta += v

        alpha = -beta
        #print alpha, beta
        
        if len(options) > 0:
            return alphabeta(player, state, MIN, MAX, 4)[1]


        else: # This should not happen
            print "here"
            return "pass"

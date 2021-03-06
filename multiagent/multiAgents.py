# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        INF = 999999
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        capsules = successorGameState.getCapsules()
        ghosts = successorGameState.getGhostPositions()

        ghostDistance = INF
        for gLoc in ghosts:
            newGhostDistance = manhattanDistance(gLoc, newPos)
            if newGhostDistance < ghostDistance:
                ghostDistance = newGhostDistance
        if ghostDistance == INF:
            ghostDistance = 0
        elif ghostDistance > 4:
            ghostDistance = 4

        food_distance = INF
        for food in newFood.asList():
            new_dist = manhattanDistance(food, newPos)
            if new_dist < food_distance:
                food_distance = new_dist

        if food_distance == INF:
            food_distance = 0


        score = 2 * successorGameState.getScore() + ghostDistance - food_distance
        return score


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        depth = self.depth
        return self.max_value(gameState, depth)

    def min_value(self, state, agentIndex, depth):
        v = 99999
        if state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        numAgents = state.getNumAgents()
        for action in state.getLegalActions(agentIndex):
            successor = state.generateSuccessor(agentIndex, action)
            if agentIndex + 1 >= numAgents:
                v = min(v, self.max_value(successor, depth - 1))
            else:
                v = min(v, self.min_value(successor, agentIndex + 1, depth))
        return v

    def max_value(self, state, depth):
        v = -99999
        if state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        if depth <= 0:
            v = self.evaluationFunction(state)
            return v
        else:
            for action in state.getLegalActions(0):
                successor = state.generateSuccessor(0, action)
                tempV = self.min_value(successor, 1, depth)
                if depth == self.depth:
                    if max(v, tempV) == tempV:
                        v = tempV
                        returnAction = action
                else:
                    v = max(v, tempV)
        if depth == self.depth:
            return returnAction
        else:
            return v


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        depth = self.depth
        Alpha = -99999
        Beta = 99999
        return self.max_value(gameState,depth, Alpha, Beta)
        util.raiseNotDefined()

    def max_value(self,state,depth,Alpha,Beta):
        v = -99999
        if state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        if depth <= 0:
            v = self.evaluationFunction(state)
            return v
        else:
            for action in state.getLegalActions(0):
                successor = state.generateSuccessor(0,action)
                tempV = self.min_value(successor,1,depth,Alpha,Beta)
                if depth == self.depth:
                    if max(v,tempV) == tempV:
                        v = tempV
                        returnAction = action
                        if v > Beta: 
                            return returnAction
                        Alpha = max(Alpha,v)
                else:
                    v = max(v,tempV)
                    if v > Beta: 
                        return v
                    Alpha = max(Alpha,v)
        if depth == self.depth:
            return returnAction
        else:
            return v

    def min_value(self, state, agentIndex,depth,Alpha,Beta):
        v = 99999
        if state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        numAgents = state.getNumAgents()
        for action in state.getLegalActions(agentIndex):
            successor = state.generateSuccessor(agentIndex,action)
            if agentIndex + 1 >= numAgents:
                v = min(v,self.max_value(successor,depth-1,Alpha,Beta))
            else:
                v = min(v,self.min_value(successor, agentIndex + 1,depth,Alpha,Beta))
            if v < Alpha: 
                return v
            Beta = min(Beta,v)
        return v

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        depth = self.depth
        return self.max_value(gameState,depth)

    def max_value(self, state, depth):
        v = -99999
        if state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        if depth <= 0:
            v = self.evaluationFunction(state)
            return v
        else:
            for action in state.getLegalActions(0):
                successor = state.generateSuccessor(0, action)
                tempV = self.exp_value(successor, 1, depth)
                if depth == self.depth:
                    if max(v, tempV) == tempV:
                        v = tempV
                        returnAction = action
                else:
                    v = max(v, tempV)
        if depth == self.depth:
            return returnAction
        else:
            return v

    def exp_value(self,state,agentIndex,depth):
        v = 0
        if state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        numAgents = state.getNumAgents()
        numsuccessors = len(state.getLegalActions(agentIndex))
        p = 1/numsuccessors
        for action in state.getLegalActions(agentIndex):
            successor = state.generateSuccessor(agentIndex,action)
            if agentIndex + 1 >= numAgents:
                v += p * self.max_value(successor,depth-1)
            else:
                v += p * self.exp_value(successor, agentIndex + 1,depth)
        return v


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    depth = 2
    score = max_value(currentGameState,depth)
    newFood = currentGameState.getFood()
    food_distance = 999999
    for food in newFood.asList():
        new_dist = manhattanDistance(food, currentGameState.getPacmanPosition())
        if new_dist < food_distance:
            food_distance = new_dist

    if food_distance == 999999:
        food_distance = 0
    return score - food_distance + currentGameState.getScore()


def max_value(state, depth):
    v = -99999
    if state.isWin() or state.isLose():
        return state.getScore()
    if depth <= 0:
        v = state.getScore()
        return v
    else:
        for action in state.getLegalActions(0):
            successor = state.generateSuccessor(0, action)
            tempV = exp_value(successor, 1, depth)
            v = max(v, tempV)
    return v

def exp_value(state,agentIndex,depth):
    v = 0
    if state.isWin() or state.isLose():
        return state.getScore()
    numAgents = state.getNumAgents()
    numsuccessors = len(state.getLegalActions(agentIndex))
    p = 1/numsuccessors
    for action in state.getLegalActions(agentIndex):
        successor = state.generateSuccessor(agentIndex,action)
        if agentIndex + 1 >= numAgents:
            v += p * max_value(successor,depth-1)
        else:
            v += p * exp_value(successor, agentIndex + 1,depth)
    return v



# Abbreviation
better = betterEvaluationFunction

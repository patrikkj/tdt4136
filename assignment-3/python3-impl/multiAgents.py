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


class MinimaxNode:
    '''
    Object representing one node in the search tree.
    Used in both Minimax and Minimax w/AlphaBeta-pruning.
    '''

    def __init__(self, state, action=None, agent_index=0, successors=None, utility=None, alpha=None, beta=None):
        self.state = state
        self.action = action # Holds the action taken to get to this node
        self.agent_index = agent_index
        self.successors = successors if successors else []
        self.utility = utility
        self.alpha = alpha
        self.beta = beta

    @staticmethod
    def create_minimax_node(state, action, agent_index):
        return MinimaxNode(
            state=state,
            action=action,
            agent_index=agent_index
        )
    
    @staticmethod
    def create_alphabeta_node(state, action, agent_index, alpha, beta):
        return MinimaxNode(
            state=state,
            action=action,
            agent_index=agent_index,
            alpha=alpha,
            beta=beta
        )

    def __str__(self):
        if self.alpha and self.beta:
            return "Agent {}: [utility={}, α={}, β={}]".format(
                self.agent_index,
                self.utility,
                self.alpha,
                self.beta
            )
        else:
            return f"Agent {self.agent_index}: [utility={self.utility}]"


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
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

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
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    @staticmethod
    def minimax_multiagent(node, successor_gen, utility_func, depth, num_adversaries=1):
        """
        DOCS
        """
        # Base case
        if depth == 0 or node.state.isWin() or node.state.isLose():
            node.utility = utility_func(node.state)
            return node

        # Calculate agent index and depth for immediate successors
        next_agent = (node.agent_index + 1) % (num_adversaries + 1)
        next_depth = depth - 1 if (next_agent == 0) else depth

        # First, determine the objective at current level;
        # max if agent is PacMan, min otherwise
        _min_or_max = max if (node.agent_index == 0) else min

        # Generate successor nodes
        for state, action in successor_gen(node.state, node.agent_index):
            v = MinimaxNode.create_minimax_node(state, action, next_agent)
            node.successors.append(v)
            
            # Evaluate successor
            MinimaxAgent.minimax_multiagent(v, successor_gen, utility_func, next_depth, num_adversaries)

        # Find best successor, inherit utility from the selected node
        best_successor = _min_or_max(node.successors, key=lambda successor: successor.utility)
        node.utility = best_successor.utility
        return best_successor


    @staticmethod
    def successor_gen(state, agent_index):
        actions = state.getLegalActions(agent_index)
        yield from ((state.generateSuccessor(agent_index, action), action) for action in actions)

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
        """
        current_node = MinimaxNode(gameState)
        optimal_node = MinimaxAgent.minimax_multiagent(
            node=current_node, 
            successor_gen=self.successor_gen, 
            utility_func=lambda state: state.getScore(), 
            depth=self.depth, 
            num_adversaries=gameState.getNumAgents() - 1 
        )
        return optimal_node.action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    @staticmethod
    def alphabeta_multiagent(node, successor_gen, utility_func, depth, num_adversaries=1):
        """
        DOCS
        """
        # Base case
        if depth == 0 or node.state.isWin() or node.state.isLose():
            node.utility = utility_func(node.state)
            return node

        # Calculate agent index and depth for immediate successors
        next_agent = (node.agent_index + 1) % (num_adversaries + 1)
        next_depth = depth - 1 if (next_agent == 0) else depth

        # Determine the objective at current level;
        # max if agent is PacMan, min otherwise
        _min_or_max = max if (node.agent_index == 0) else min

        # Generate successor nodes
        for state, action in successor_gen(node.state, node.agent_index):
            v = MinimaxNode.create_alphabeta_node(state, action, next_agent, node.alpha, node.beta)
            node.successors.append(v)
            
            # Evaluate successor
            AlphaBetaAgent.alphabeta_multiagent(v, successor_gen, utility_func, next_depth, num_adversaries)
            
            # Check if current subtree can be pruned
            if _min_or_max == max:
                if v.utility > node.beta: # actually >=
                    node.utility = v.utility
                    return v
                node.alpha = max(node.alpha, v.utility)
            else:
                if v.utility < node.alpha: # actually <=
                    node.utility = v.utility
                    return v
                node.beta = min(node.beta, v.utility)

        # Find best successor, inherit utility from the selected node
        best_successor = _min_or_max(node.successors, key=lambda successor: successor.utility)
        node.utility = best_successor.utility
        return best_successor


    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        current_node = MinimaxNode(gameState, alpha=-float('inf'), beta=float('inf'))
        optimal_node = AlphaBetaAgent.alphabeta_multiagent(
            node=current_node,
            successor_gen=MinimaxAgent.successor_gen, 
            utility_func=lambda state: state.getScore(),
            depth=self.depth,
            num_adversaries=gameState.getNumAgents() -1 
        )
        return optimal_node.action


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
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction


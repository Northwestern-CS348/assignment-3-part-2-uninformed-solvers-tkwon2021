
from solver import *
from collections import deque

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here

        # This checks if the very first game state is a win condition; not 
        # necessary otherwise.
    

        self.visited[self.currentState] = True
        
        if self.gm.isWon():
            return True
        
        

        # Getting all list of movables (aka children)
        movables = self.gm.getMovables()

        # If list is empty, then reverse the current state
        if movables == False:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            self.solveOneStep()

        # Otherwise, traverse through the list and set the parent and child states
        else:
            for child in movables:
                self.gm.makeMove(child)
                childGameState = GameState(self.gm.getGameState(), self.currentState.depth+1, child)
                childGameState.parent = self.currentState
                self.currentState.children.append(childGameState)
                self.gm.reverseMove(child)

        # For first child that hasn't been visited, go into it and check if 
        # it's the winning child; return True if it is, false otherwise.
        for x in self.currentState.children:
            if x not in self.visited:
                self.visited[self.currentState] = True
                self.gm.makeMove(x.requiredMovable)
                self.currentState = x
                if self.gm.isWon():
                    return True
                else:
                    return False
        
        return True


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.orderedStates = []

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here

        # This checks if the very first game state is a win condition; not 
        # necessary otherwise.
        self.visited[self.currentState] = True
        if self.gm.isWon():
            return True

        # Getting all list of movables (aka children)
        movables = self.gm.getMovables()
            
       
        # Otherwise, traverse through the list and set the parent and child states
        if movables:
            for child in movables:
                self.gm.makeMove(child)
                childGameState = GameState(self.gm.getGameState(), self.currentState.depth+1, child)
                childGameState.parent = self.currentState
                self.orderedStates.append(childGameState)
                self.currentState.children.append(childGameState)
                self.gm.reverseMove(child)

        # Make the first node the current node
        for x in range(self.currentState.depth):
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.setCurrentState(self.currentState.parent)

        # Pop the first state
        nextState = self.orderedStates.pop(0)

        # Make sure the popped state hasn't already been visited
        while nextState in self.visited:
            nextState = self.orderedStates.pop(0)
        movesForNextState = []

        # Create list of moves that need to be made to get to the
        # next state in orderedStates
        for y in range(nextState.depth):
            movesForNextState.append(nextState.requiredMovable)
            nextState = nextState.parent

        # Traverses down the tree (making moves) towards the state that was popped
        for z in reversed(movesForNextState):
            self.gm.makeMove(z)
            newCurrentState = self.gm.getGameState()
            for child in self.currentState.children:
                if newCurrentState == child.state:
                    self.setCurrentState(child)
                    self.visited[child] = True

        self.visited[self.currentState] = True

        if self.gm.isWon():
            return True
        return False

    # Helper function that sets state
    def setCurrentState(self, state):
        self.currentState = state


    
from collections import deque

class EightPuzzle:
    """
    This class is an implementation of the classic 8-puzzle game, including methods for finding the blank tile, making moves, getting possible moves, and solving the puzzle using a breadth-first search algorithm.
    """

    def __init__(self, initial_state):
        """
        Initializing the initial state of Eight Puzzle Game, stores in attribute self.initial_state.
        And set the goal state of this game, stores in self.goal_state. In this case, set the size as 3*3
        :param initial_state: a 3*3 size list of Integer, stores the initial state
        """
        self.initial_state = initial_state
        self.goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def find_blank(self, state):
        """
        Find the blank position of current state, which is the 0 element.
        :param state: a 3*3 size list of Integer, stores the current state.
        :return i, j: two Integers, represent the coordinate of the blank block.
        """
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    return (i, j)
        return (2, 2)  # Should not reach here

    def move(self, state, direction):
        """
        Find the blank block, then makes the board moves forward the given direction.
        :param state: a 3*3 size list of Integer, stores the state before moving.
        :param direction: str, only has 4 direction 'up', 'down', 'left', 'right'
        :return new_state: a 3*3 size list of Integer, stores the state after moving.
        """
        i, j = self.find_blank(state)
        new_state = [row[:] for row in state]
        if direction == 'up':
            new_state[i][j], new_state[i-1][j] = new_state[i-1][j], new_state[i][j]
        elif direction == 'down':
            new_state[i][j], new_state[i+1][j] = new_state[i+1][j], new_state[i][j]
        elif direction == 'left':
            new_state[i][j], new_state[i][j-1] = new_state[i][j-1], new_state[i][j]
        elif direction == 'right':
            new_state[i][j], new_state[i][j+1] = new_state[i][j+1], new_state[i][j]
        return new_state

    def get_possible_moves(self, state):
        """
        Get possible moves based on the blank tile's position.
        :param state: a 3*3 list of integers.
        :return list of possible directions.
        """
        i, j = self.find_blank(state)
        moves = []
        if i > 0:
            moves.append('up')
        if i < 2:
            moves.append('down')
        if j > 0:
            moves.append('left')
        if j < 2:
            moves.append('right')
        return moves

    def solve(self):
        """
        Solve the puzzle using BFS.
        :return list of moves to reach the goal state.
        """
        queue = deque()
        queue.append((self.initial_state, []))
        visited = set()

        while queue:
            current_state, path = queue.popleft()
            if current_state == self.goal_state:
                return path
            state_tuple = tuple(tuple(row) for row in current_state)
            if state_tuple in visited:
                continue
            visited.add(state_tuple)
            possible_moves = self.get_possible_moves(current_state)
            for move in possible_moves:
                new_state = self.move(current_state, move)
                new_state_tuple = tuple(tuple(row) for row in new_state)
                if new_state_tuple not in visited:
                    queue.append((new_state, path + [move]))
        return []

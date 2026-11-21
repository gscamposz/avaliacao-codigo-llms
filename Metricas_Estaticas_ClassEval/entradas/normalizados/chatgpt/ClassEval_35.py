
from collections import deque


class EightPuzzle:
    """
    This class is an implementation of the classic 8-puzzle game,
    including methods for finding the blank tile, making moves,
    getting possible moves, and solving the puzzle using a
    breadth-first search algorithm.
    """

    def __init__(self, initial_state):
        """
        Initialize the initial state and goal state of the puzzle.
        """
        self.initial_state = initial_state
        self.goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def find_blank(self, state):
        """
        Find the position of the blank tile (0).
        :return: Tuple (row, column).
        """
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    return (i, j)
        return None

    def move(self, state, direction):
        """
        Move the blank tile in the specified direction.
        :return: New state after moving.
        """
        blank = self.find_blank(state)

        if blank is None:
            return state

        i, j = blank

        directions = {
            'up': (-1, 0),
            'down': (1, 0),
            'left': (0, -1),
            'right': (0, 1)
        }

        if direction not in directions:
            return state

        di, dj = directions[direction]
        new_i, new_j = i + di, j + dj

        if not (0 <= new_i < 3 and 0 <= new_j < 3):
            return state

        new_state = [row[:] for row in state]

        new_state[i][j], new_state[new_i][new_j] = (
            new_state[new_i][new_j],
            new_state[i][j]
        )

        return new_state

    def get_possible_moves(self, state):
        """
        Return all valid directions for the blank tile.
        :return: List of possible moves.
        """
        blank = self.find_blank(state)

        if blank is None:
            return []

        i, j = blank
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
        Solve the puzzle using breadth-first search (BFS).
        :return: List of directions leading to the goal state,
                 or None if no solution exists.
        """
        if self.initial_state == self.goal_state:
            return []

        open_list = deque([(self.initial_state, [])])

        def state_to_tuple(state):
            return tuple(tuple(row) for row in state)

        visited = {state_to_tuple(self.initial_state)}

        while open_list:
            current_state, path = open_list.popleft()

            possible_moves = self.get_possible_moves(current_state)

            for direction in possible_moves:
                new_state = self.move(current_state, direction)
                new_state_tuple = state_to_tuple(new_state)

                if new_state_tuple in visited:
                    continue

                new_path = path + [direction]

                if new_state == self.goal_state:
                    return new_path

                visited.add(new_state_tuple)
                open_list.append((new_state, new_path))

        return None

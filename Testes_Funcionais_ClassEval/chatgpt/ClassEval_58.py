
import random


class MinesweeperGame:
    """
    This is a class that implements mine sweeping games including
    minesweeping and winning judgment.
    """

    def __init__(self, n, k) -> None:
        """
        Initializes the MinesweeperGame class with the size of
        the board and the number of mines.
        :param n: The size of the board, int.
        :param k: The number of mines, int.
        """
        self.n = n
        self.k = k
        self.minesweeper_map = self.generate_mine_sweeper_map()
        self.player_map = self.generate_playerMap()
        self.score = 0

    def generate_mine_sweeper_map(self):
        """
        Generates a minesweeper map with n*n positions and k mines.
        'X' represents a mine, and numbers represent the number
        of adjacent mines.
        :return: The minesweeper map, list.
        """
        if self.n <= 0:
            raise ValueError("Board size must be positive")

        if self.k < 0 or self.k > self.n * self.n:
            raise ValueError("Invalid number of mines")

        board = [[0 for _ in range(self.n)] for _ in range(self.n)]

        mine_positions = random.sample(
            range(self.n * self.n), self.k
        )

        for position in mine_positions:
            row, col = divmod(position, self.n)
            board[row][col] = 'X'

        for row in range(self.n):
            for col in range(self.n):
                if board[row][col] == 'X':
                    continue

                count = 0

                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        if dx == 0 and dy == 0:
                            continue

                        new_row = row + dx
                        new_col = col + dy

                        if (
                            0 <= new_row < self.n
                            and 0 <= new_col < self.n
                            and board[new_row][new_col] == 'X'
                        ):
                            count += 1

                board[row][col] = count

        return board

    def generate_playerMap(self):
        """
        Generates a player map with n*n unknown positions.
        '-' represents an unknown position.
        :return: The player map, list.
        """
        return [
            ['-' for _ in range(self.n)]
            for _ in range(self.n)
        ]

    def check_won(self, map):
        """
        Checks whether the player has won the game.
        Returns True if all non-mine positions have been revealed
        and only mine positions remain unknown.
        :param map: The player's current map.
        :return: True if the player has won, False otherwise.
        """
        for row in range(self.n):
            for col in range(self.n):
                if self.minesweeper_map[row][col] == 'X':
                    if map[row][col] != '-':
                        return False
                else:
                    if map[row][col] == '-':
                        return False

        return True

    def sweep(self, x, y):
        """
        Sweeps the given position.
        :param x: The x coordinate of the position, int.
        :param y: The y coordinate of the position, int.
        :return: True if the player has won, False if a mine
                 is swept, or the player map if the game continues.
        """
        if not (0 <= x < self.n and 0 <= y < self.n):
            return self.player_map

        if self.player_map[x][y] != '-':
            if self.check_won(self.player_map):
                return True
            return self.player_map

        if self.minesweeper_map[x][y] == 'X':
            self.player_map[x][y] = 'X'
            return False

        self.player_map[x][y] = self.minesweeper_map[x][y]
        self.score += 1

        if self.check_won(self.player_map):
            return True

        return self.player_map

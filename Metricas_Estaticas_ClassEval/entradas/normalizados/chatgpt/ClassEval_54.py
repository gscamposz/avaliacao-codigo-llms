
import random
from collections import deque


class MahjongConnect:
    """
    MahjongConnect is a class representing a game board for
    Mahjong Connect with features like creating the board,
    checking valid moves, finding paths, removing icons,
    and checking if the game is over.
    """

    def __init__(self, BOARD_SIZE, ICONS):
        """
        Initialize the board size and the icon list,
        and create the game board.
        """
        self.BOARD_SIZE = BOARD_SIZE
        self.ICONS = ICONS
        self.board = self.create_board()

    def create_board(self):
        """
        Create the game board with the given board size and icons.
        :return: 2-dimensional list, the game board
        """
        rows, cols = self.BOARD_SIZE

        if rows <= 0 or cols <= 0:
            return [[] for _ in range(max(rows, 0))]

        if not self.ICONS:
            return [[' ' for _ in range(cols)] for _ in range(rows)]

        total = rows * cols
        icons = []

        for i in range(total // 2):
            icon = self.ICONS[i % len(self.ICONS)]
            icons.extend([icon, icon])

        if total % 2:
            icons.append(' ')

        random.shuffle(icons)

        board = [
            icons[i * cols:(i + 1) * cols]
            for i in range(rows)
        ]

        return board

    def is_valid_move(self, pos1, pos2):
        """
        Check if the move of two icons is valid.
        :param pos1: position tuple(x, y) of the first icon
        :param pos2: position tuple(x, y) of the second icon
        :return: True or False
        """
        rows = len(self.board)

        if rows == 0:
            return False

        if pos1 == pos2:
            return False

        x1, y1 = pos1
        x2, y2 = pos2

        if not (0 <= x1 < rows and 0 <= x2 < rows):
            return False

        if not (0 <= y1 < len(self.board[x1])):
            return False

        if not (0 <= y2 < len(self.board[x2])):
            return False

        icon1 = self.board[x1][y1]
        icon2 = self.board[x2][y2]

        if icon1 == ' ' or icon2 == ' ':
            return False

        if icon1 != icon2:
            return False

        return self.has_path(pos1, pos2)

    def has_path(self, pos1, pos2):
        """
        Check if there is a path between two icons.
        A valid path has at most two turns and may pass
        through empty cells or around the board.
        :param pos1: position tuple(x, y)
        :param pos2: position tuple(x, y)
        :return: True or False
        """
        rows = len(self.board)

        if rows == 0:
            return False

        cols = len(self.board[0])

        if cols == 0 or pos1 == pos2:
            return False

        x1, y1 = pos1
        x2, y2 = pos2

        if not (
            0 <= x1 < rows
            and 0 <= x2 < rows
            and 0 <= y1 < cols
            and 0 <= y2 < cols
        ):
            return False

        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        ]

        start = (x1 + 1, y1 + 1)
        target = (x2 + 1, y2 + 1)

        padded = [
            [' '] * (cols + 2)
            for _ in range(rows + 2)
        ]

        for r in range(rows):
            for c in range(cols):
                padded[r + 1][c + 1] = self.board[r][c]

        queue = deque()
        visited = {}

        for direction in range(4):
            state = (start[0], start[1], direction)
            queue.append((start[0], start[1], direction, 0))
            visited[state] = 0

        while queue:
            x, y, direction, turns = queue.popleft()

            if (x, y) == target:
                return True

            for new_direction, (dx, dy) in enumerate(directions):
                new_turns = turns + (
                    0 if direction == new_direction else 1
                )

                if new_turns > 2:
                    continue

                nx = x + dx
                ny = y + dy

                if not (
                    0 <= nx < rows + 2
                    and 0 <= ny < cols + 2
                ):
                    continue

                if (nx, ny) != target and padded[nx][ny] != ' ':
                    continue

                state = (nx, ny, new_direction)

                if (
                    state in visited
                    and visited[state] <= new_turns
                ):
                    continue

                visited[state] = new_turns

                if new_direction == direction:
                    queue.appendleft(
                        (nx, ny, new_direction, new_turns)
                    )
                else:
                    queue.append(
                        (nx, ny, new_direction, new_turns)
                    )

        return False

    def remove_icons(self, pos1, pos2):
        """
        Remove the connected icons on the game board.
        :param pos1: position tuple(x, y)
        :param pos2: position tuple(x, y)
        :return: None
        """
        if self.is_valid_move(pos1, pos2):
            x1, y1 = pos1
            x2, y2 = pos2

            self.board[x1][y1] = ' '
            self.board[x2][y2] = ' '

    def is_game_over(self):
        """
        Check if there are no more icons on the game board.
        :return: True or False
        """
        return all(
            icon == ' '
            for row in self.board
            for icon in row
        )

import random

class Board:
    def __init__(self, size, icons):
        self.BOARD_SIZE = size
        self.ICONS = icons
        self.board = self.create_board()

    def create_board(self):
        rows, cols = self.BOARD_SIZE
        board = []
        for r in range(rows):
            row = []
            for c in range(cols):
                row.append(random.choice(self.ICONS))
            board.append(row)
        return board

    def is_valid_position(self, pos):
        x, y = pos
        return 0 <= x < self.BOARD_SIZE[0] and 0 <= y < self.BOARD_SIZE[1]

    def has_path(self, pos1, pos2):
        if not self.is_valid_position(pos1) or not self.is_valid_position(pos2):
            return False

        # Ensure both positions have the same icon
        icon = self.board[pos1[0]][pos1[1]]
        if self.board[pos2[0]][pos2[1]] != icon:
            return False

        # BFS to check connectivity
        visited = set()
        queue = [pos1]
        visited.add(pos1)

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            current = queue.pop(0)
            if current == pos2:
                return True

            for dx, dy in directions:
                x, y = current[0] + dx, current[1] + dy
                if (x, y) not in visited and self.is_valid_position((x, y)) and self.board[x][y] == icon:
                    visited.add((x, y))
                    queue.append((x, y))

        return False

    def is_valid_move(self, pos1, pos2):
        if not self.is_valid_position(pos1) or not self.is_valid_position(pos2):
            return False

        if pos1 == pos2:
            return False

        if self.board[pos1[0]][pos1[1]] != self.board[pos2[0]][pos2[1]]:
            return False

        return self.has_path(pos1, pos2)

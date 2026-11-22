
class GomokuGame:
    """
    This class is an implementation of a Gomoku game, supporting
    making moves, checking for a winner, and checking if there
    are five consecutive symbols on the game board.
    """

    def __init__(self, board_size):
        """
        Initializes the game with a given board size.
        """
        self.board_size = board_size
        self.board = [
            [' ' for _ in range(board_size)]
            for _ in range(board_size)
        ]
        self.current_player = 'X'

    def make_move(self, row, col):
        """
        Makes a move at the given row and column.
        Returns True if valid, False otherwise.
        """
        if not (0 <= row < self.board_size):
            return False

        if not (0 <= col < self.board_size):
            return False

        if self.board[row][col] != ' ':
            return False

        self.board[row][col] = self.current_player

        if self.current_player == 'X':
            self.current_player = 'O'
        else:
            self.current_player = 'X'

        return True

    def check_winner(self):
        """
        Checks for five consecutive symbols in horizontal,
        vertical, and diagonal directions.
        Returns 'X', 'O', or None.
        """
        directions = [
            (0, 1),
            (1, 0),
            (1, 1),
            (1, -1)
        ]

        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] == ' ':
                    continue

                for direction in directions:
                    if self._check_five_in_a_row(
                        row, col, direction
                    ):
                        return self.board[row][col]

        return None

    def _check_five_in_a_row(self, row, col, direction):
        """
        Checks whether five consecutive cells contain
        the same non-empty symbol in the given direction.
        """
        if not (
            0 <= row < self.board_size
            and 0 <= col < self.board_size
        ):
            return False

        symbol = self.board[row][col]

        if symbol == ' ':
            return False

        dx, dy = direction

        if dx == 0 and dy == 0:
            return False

        for i in range(5):
            new_row = row + i * dx
            new_col = col + i * dy

            if not (
                0 <= new_row < self.board_size
                and 0 <= new_col < self.board_size
            ):
                return False

            if self.board[new_row][new_col] != symbol:
                return False

        return True

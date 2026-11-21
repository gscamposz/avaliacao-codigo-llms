
class TicTacToe:
    """
    The class represents a game of Tic-Tac-Toe and its functions
    include making a move on the board, checking for a winner,
    and determining if the board is full.
    """

    def __init__(self, N=3):
        """
        Initialize a game board with all empty spaces
        and current symbol player, default is 'X'.
        """
        self.board = [[' ' for _ in range(N)] for _ in range(3)]
        self.current_player = 'X'

    def make_move(self, row, col):
        """
        Place the current player's mark at the specified
        position on the board and switch the mark.
        :param row: int, the row index of the position
        :param col: int, the column index of the position
        :return: bool, indicating whether the move was successful
        """
        if not (0 <= row < len(self.board)):
            return False

        if not (0 <= col < len(self.board[row])):
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
        Check if there is a winner on the board in rows,
        columns and diagonals.
        :return: str or None, the mark of the winner
        ('X' or 'O'), or None if there is no winner yet
        """
        rows = len(self.board)
        cols = len(self.board[0])

        for row in self.board:
            if len(row) >= 3:
                for col in range(len(row) - 2):
                    if (row[col] != ' ' and
                            row[col] == row[col + 1] == row[col + 2]):
                        return row[col]

        for col in range(cols):
            if (self.board[0][col] != ' ' and
                    self.board[0][col] == self.board[1][col] ==
                    self.board[2][col]):
                return self.board[0][col]

        if cols >= 3:
            for col in range(cols - 2):
                if (self.board[0][col] != ' ' and
                        self.board[0][col] ==
                        self.board[1][col + 1] ==
                        self.board[2][col + 2]):
                    return self.board[0][col]

            for col in range(2, cols):
                if (self.board[0][col] != ' ' and
                        self.board[0][col] ==
                        self.board[1][col - 1] ==
                        self.board[2][col - 2]):
                    return self.board[0][col]

        return None

    def is_board_full(self):
        """
        Check if the game board is completely filled.
        :return: bool, indicating whether the game board is full
        """
        for row in self.board:
            for cell in row:
                if cell == ' ':
                    return False

        return True

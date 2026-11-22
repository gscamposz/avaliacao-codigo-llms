class TicTacToe:
    """
    The class represents a game of Tic-Tac-Toe and its functions include making a move on the board, checking for a winner, and determining if the board is full.
    """

    def __init__(self, N=3):
        """
        Initialize a 3x3 game board with all empty spaces and current symble player, default is 'X'.
        """
        self.N = N
        self.board = [[' ' for _ in range(N)] for _ in range(N)]
        self.current_player = 'X'

    def make_move(self, row, col):
        """
        Place the current player's mark at the specified position on the board and switch the mark.
        :param row: int, the row index of the position
        :param col: int, the column index of the position
        :return: bool, indicating whether the move was successful or not
        >>> ttt.current_player
        'X'
        >>> ttt.make_move(1, 1)
        >>> ttt.current_player
        'O'
        """
        num_rows = len(self.board)
        num_cols = len(self.board[0]) if num_rows > 0 else 0
        if not (0 <= row < num_rows and 0 <= col < num_cols):
            return False
        if self.board[row][col] != ' ':
            return False
        self.board[row][col] = self.current_player
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True

    def check_winner(self):
        """
        Check if there is a winner on the board in rows, columns and diagonals three directions
        :return: str or None, the mark of the winner ('X' or 'O'), or None if there is no winner yet
        >>> moves = [(1, 0), (2, 0), (1, 1), (2, 1), (1, 2)]
        >>> for move in moves:
        ...     ttt.make_move(move[0], move[1])
        >>> ttt.check_winner()
        'X'
        """
        num_rows = len(self.board)
        num_cols = len(self.board[0]) if num_rows > 0 else 0

        for r in range(num_rows):
            first = self.board[r][0]
            if first != ' ' and all(self.board[r][c] == first for c in range(1, num_cols)):
                return first

        for c in range(num_cols):
            first = self.board[0][c]
            if first != ' ' and all(self.board[r][c] == first for r in range(1, num_rows)):
                return first

        if num_rows == num_cols and num_rows > 0:
            first_diag = self.board[0][0]
            if first_diag != ' ' and all(self.board[i][i] == first_diag for i in range(1, num_rows)):
                return first_diag

            first_anti = self.board[0][num_rows - 1]
            if first_anti != ' ' and all(self.board[i][num_rows - 1 - i] == first_anti for i in range(1, num_rows)):
                return first_anti

        return None

    def is_board_full(self):
        """
        Check if the game board is completely filled.
        :return: bool, indicating whether the game board is full or not
        >>> ttt.is_board_full()
        False
        """
        return all(cell != ' ' for row in self.board for cell in row)
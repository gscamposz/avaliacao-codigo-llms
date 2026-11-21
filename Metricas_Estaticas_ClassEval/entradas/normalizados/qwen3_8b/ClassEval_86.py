class TicTacToe:
    def __init__(self, N=3):
        self.N = N  # Number of columns (assumed to be 3 for Tic-Tac-Toe)
        self.board = [[' ' for _ in range(N)] for _ in range(3)]
        self.current_player = 'X'

    def make_move(self, row, col):
        if not (0 <= row < 3 and 0 <= col < self.N):
            return False  # Invalid position
        if self.board[row][col] != ' ':
            return False  # Cell already occupied
        self.board[row][col] = self.current_player
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True

    def check_winner(self):
        # Check rows
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != ' ':
                return self.board[row][0]

        # Check columns
        for col in range(self.N):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != ' ':
                return self.board[0][col]

        # Check diagonals (only if N == 3)
        if self.N == 3:
            if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
                return self.board[0][0]
            if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
                return self.board[0][2]

        return None  # No winner

    def is_board_full(self):
        for row in range(3):
            for col in range(self.N):
                if self.board[row][col] == ' ':
                    return False
        return True


game = TicTacToe()
game.make_move(1, 0)
game.make_move(2, 0)
game.make_move(1, 1)
game.make_move(2, 1)
game.make_move(1, 2)

print("Winner:", game.check_winner())  # Output: 'X'
print("Board full:", game.is_board_full())  # Output: False

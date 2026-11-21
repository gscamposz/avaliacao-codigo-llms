class GomokuGame:
    def __init__(self, size=15):
        self.size = size
        self.board = [['' for _ in range(size)] for _ in range(size)]
    
    def place_piece(self, x, y, player):
        if self.board[x][y] == '':
            self.board[x][y] = player
            return self.check_winner(x, y, player)
        return False

    def check_winner(self, x, y, player):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dx, dy in directions:
            if self._check_line(x, y, dx, dy, player):
                return player
        return None

    def _check_line(self, x, y, dx, dy, player):
        count = 1
        # Check in one direction
        for i in range(1, 5):
            nx = x + dx * i
            ny = y + dy * i
            if 0 <= nx < self.size and 0 <= ny < self.size and self.board[nx][ny] == player:
                count += 1
            else:
                break
        # Check in the opposite direction
        for i in range(1, 5):
            nx = x - dx * i
            ny = y - dy * i
            if 0 <= nx < self.size and 0 <= ny < self.size and self.board[nx][ny] == player:
                count += 1
            else:
                break
        return count >= 5


game = GomokuGame(size=15)
# Place pieces in a winning line
for i in range(5):
    game.place_piece(i, 5, 'X')  # Horizontal win
    game.place_piece(5, i, 'O')  # Vertical win
    game.place_piece(i, i, 'X')  # Diagonal win
    game.place_piece(i, 14 - i, 'O')  # Anti-diagonal win

# Check for win
winner = game.check_winner(4, 5, 'X')
print(f"Player {winner} wins horizontally!")

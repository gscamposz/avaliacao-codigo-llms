def check_won(self):
    for i in range(self.n):
        for j in range(self.n):
            if self.mine_sweeper_map[i][j] == 'X':
                if self.player_map[i][j] != '-':
                    return False
            else:
                if self.player_map[i][j] != self.mine_sweeper_map[i][j]:
                    return False
    return True


self.mine_sweeper_map = [
    ['X', 1, 2],
    [3, 4, 5],
    [6, 7, 8]
]

self.player_map = [
    ['X', '-', '-'],
    ['-', '-', '-'],
    ['-', '-', '-']
]

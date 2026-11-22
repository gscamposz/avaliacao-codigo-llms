
class PushBoxGame:
    """
    This class implements a functionality of a sokoban game, where the
    player needs to move boxes to designated targets in order to win.
    """

    def __init__(self, map):
        """
        Initialize the push box game with the map and various attributes.
        """
        self.map = map
        self.player_row = 0
        self.player_col = 0
        self.targets = []
        self.boxes = []
        self.target_count = 0
        self.is_game_over = False
        self.init_game()

    def init_game(self):
        """
        Initialize the positions of the player, targets, and boxes
        based on the map.
        """
        self.targets = []
        self.boxes = []
        self.target_count = 0
        self.is_game_over = False

        for row, line in enumerate(self.map):
            for col, char in enumerate(line):
                if char == 'O':
                    self.player_row = row
                    self.player_col = col
                elif char == 'G':
                    self.targets.append((row, col))
                elif char == 'X':
                    self.boxes.append((row, col))

        self.target_count = len(self.targets)

    def check_win(self):
        """
        Check if all boxes are placed on target positions.
        Update and return self.is_game_over.
        """
        self.is_game_over = all(
            box in self.targets for box in self.boxes
        )
        return self.is_game_over

    def move(self, direction):
        """
        Move the player in the specified direction and check
        whether the game has been won.
        """
        directions = {
            'w': (-1, 0),
            's': (1, 0),
            'a': (0, -1),
            'd': (0, 1)
        }

        if self.is_game_over:
            return True

        if direction not in directions:
            return False

        dr, dc = directions[direction]

        new_row = self.player_row + dr
        new_col = self.player_col + dc

        if not self._is_valid_position(new_row, new_col):
            return False

        if (new_row, new_col) in self.boxes:
            box_new_row = new_row + dr
            box_new_col = new_col + dc

            if not self._is_valid_position(
                box_new_row, box_new_col
            ):
                return False

            if (box_new_row, box_new_col) in self.boxes:
                return False

            box_index = self.boxes.index(
                (new_row, new_col)
            )
            self.boxes[box_index] = (
                box_new_row, box_new_col
            )

        self.player_row = new_row
        self.player_col = new_col

        return self.check_win()

    def _is_valid_position(self, row, col):
        """
        Check whether a position is within the map
        and is not a wall.
        """
        if row < 0 or row >= len(self.map):
            return False

        if col < 0 or col >= len(self.map[row]):
            return False

        return self.map[row][col] != '#'

    def print_map(self):
        """
        Print the current game map with the player,
        boxes, targets, and walls.
        """
        display_map = [
            list(row) for row in self.map
        ]

        for row in range(len(display_map)):
            for col in range(len(display_map[row])):
                if display_map[row][col] in ('O', 'X'):
                    display_map[row][col] = ' '

        for row, col in self.targets:
            display_map[row][col] = 'G'

        for row, col in self.boxes:
            display_map[row][col] = 'X'

        display_map[self.player_row][self.player_col] = 'O'

        for row in display_map:
            print(' '.join(row))

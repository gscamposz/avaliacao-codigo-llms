class PushBoxGame:
    """
    This class implements a functionality of a sokoban game, where the player needs to move boxes to designated targets in order to win.
    """

    def __init__(self, map):
        """
        Initialize the push box game with the map and various attributes.
        :param map: list[str], the map of the push box game, represented as a list of strings. 
            Each character on the map represents a different element, including the following:

    * '#' represents a wall that neither the player nor the box can pass through;
    * 'O' represents the initial position of the player;
    * 'G' represents the target position;
    * 'X' represents the initial position of the box.
    >>> map = ["#####", "#O  #", "# X #", "#  G#", "#####"]
    >>> game = PushBoxGame(map)
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
    Initialize the game by setting the positions of the player, targets, and boxes based on the map.
    >>> game = PushBoxGame(["#####", "#O  #", "# X #", "#  G#", "#####"])
    >>> game.targets
    [(3, 3)]
    >>> game.boxes
    [(2, 2)]
    >>> game.player_row
    1
    >>> game.player_col
    1
    """
    self.targets = []
    self.boxes = []
    self.target_count = 0
    self.is_game_over = False

      for r, row in enumerate(self.map):
          for c, ch in enumerate(row):
              if ch == "O":
                  self.player_row = r
                  self.player_col = c
              elif ch == "G":
                  self.targets.append((r, c))
              elif ch == "X":
                  self.boxes.append((r, c))

      self.target_count = len(self.targets)
      self.check_win()

    def check_win(self):
    """
    Check if the game is won. The game is won when all the boxes are placed on target positions.
    And update the value of self.is_game_over.
    :return self.is_game_over: True if all the boxes are placed on target positions, or False otherwise.
    >>> game = PushBoxGame(["#####", "#O  #", "# X #", "#  G#", "#####"])
    >>> game.check_win()
    """
    target_set = set(self.targets)
    box_set = set(self.boxes)
    self.is_game_over = len(target_set) > 0 and target_set.issubset(box_set) and len(self.boxes) >= len(self.targets)
    return self.is_game_over
    def print_map(self):
    """
    Print the current state of the game map.
    """
    target_set = set(self.targets)
    box_set = set(self.boxes)
    for r, row in enumerate(self.map):
    line = ""
    for c, ch in enumerate(row):
    if r == self.player_row and c == self.player_col:
    cell = "O"
    elif (r, c) in box_set:
    cell = "X"
    elif (r, c) in target_set:
    cell = "G"
    elif ch == "#":
    cell = "#"
    else:
    cell = " "
    line += cell + " "
    print(line)
    def move(self, direction):
    """
    Move the player based on the specified direction and check if the game is won.
    :param direction: str, the direction of the player's movement.
    It can be 'w', 's', 'a', or 'd' representing up, down, left, or right respectively.

      :return: True if the game is won, False otherwise.
      >>> game = PushBoxGame(["#####", "#O  #", "# X #", "#  G#", "#####"])       
      >>> game.print_map()
      # # # # # 
      # O     #
      #   X   #
      #     G #
      # # # # #
      >>> game.move('d')
      False
      >>> game.move('s')   
      False
      >>> game.move('a')   
      False
      >>> game.move('s') 
      False
      >>> game.move('d') 
      True
      """
      deltas = {
          "w": (-1, 0),
          "s": (1, 0),
          "a": (0, -1),
          "d": (0, 1),
      }

      if direction not in deltas:
          return self.check_win()

      dr, dc = deltas[direction]
      next_r = self.player_row + dr
      next_c = self.player_col + dc

      if not (0 <= next_r < len(self.map) and 0 <= next_c < len(self.map[next_r])):
          return self.check_win()

      if self.map[next_r][next_c] == "#":
          return self.check_win()

      if (next_r, next_c) in self.boxes:
          box_next_r = next_r + dr
          box_next_c = next_c + dc

          if not (0 <= box_next_r < len(self.map) and 0 <= box_next_c < len(self.map[box_next_r])):
              return self.check_win()

          if self.map[box_next_r][box_next_c] == "#" or (box_next_r, box_next_c) in self.boxes:
              return self.check_win()

          box_idx = self.boxes.index((next_r, next_c))
          self.boxes[box_idx] = (box_next_r, box_next_c)

      self.player_row = next_r
      self.player_col = next_c

      return self.check_win()
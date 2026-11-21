class PushBoxGame:
    def __init__(self, player_pos, boxes, targets):
        self.player_pos = player_pos
        self.boxes = boxes
        self.targets = targets
        self.boxes_set = set(boxes)  # For quick lookup
        self.targets_set = set(targets)  # For quick lookup

    def move(self, direction):
        """Move the player and push boxes accordingly."""
        dr, dc = 0, 0
        if direction == 'w':  # up
            dr, dc = -1, 0
        elif direction == 's':  # down
            dr, dc = 1, 0
        elif direction == 'a':  # left
            dr, dc = 0, -1
        elif direction == 'd':  # right
            dr, dc = 0, 1
        else:
            return False  # Invalid direction

        new_player_pos = (self.player_pos[0] + dr, self.player_pos[1] + dc)

        # Check if the new player position is valid
        if new_player_pos in self.boxes_set:
            # Player is moving into a box; push it
            box_pos = new_player_pos
            new_box_pos = (box_pos[0] + dr, box_pos[1] + dc)

            # Check if the box can be pushed
            if new_box_pos not in self.boxes_set and new_box_pos not in self.targets_set:
                # Move the box
                self.boxes.remove(box_pos)
                self.boxes.append(new_box_pos)
                self.boxes_set.remove(box_pos)
                self.boxes_set.add(new_box_pos)
                self.player_pos = new_player_pos
                return True
            else:
                return False  # Cannot push the box
        elif new_player_pos not in self.boxes_set and new_player_pos not in self.targets_set:
            # Move the player
            self.player_pos = new_player_pos
            return True
        else:
            return False  # Invalid move (into box or target)

    def check_win(self):
        """Check if all boxes are in target positions."""
        return self.boxes_set.issubset(self.targets_set)


# Example game setup
player_pos = (0, 0)
boxes = [(1, 1), (2, 2)]
targets = [(1, 1), (2, 2)]

game = PushBoxGame(player_pos, boxes, targets)

# Try to move the player and push boxes
print(game.move('d'))  # Move right
print(game.move('d'))  # Move right (no box)
print(game.move('s'))  # Move down
print(game.move('d'))  # Move right (no box)
print(game.move('w'))  # Move up (into box)
print("Game won:", game.check_win())

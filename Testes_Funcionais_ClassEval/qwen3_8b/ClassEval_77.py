import random

class SnakeGame:
    def __init__(self, width, height, block_size):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.reset()

    def reset(self):
        """Reset the game state to initial position."""
        self.length = 1
        self.positions = [(self.width // 2, self.height // 2)]
        self.score = 0
        self.random_food_position()

    def random_food_position(self):
        """Place the food at a random, valid grid position."""
        max_x = (self.width - 1) // self.block_size
        max_y = (self.height - 1) // self.block_size
        while True:
            x = random.randint(0, max_x) * self.block_size
            y = random.randint(0, max_y) * self.block_size
            food_pos = (x, y)
            if food_pos not in self.positions:
                self.food_position = food_pos
                break

    def move(self, direction):
        """Update the snake's position based on direction."""
        head = self.positions[0]
        new_head = (head[0] + direction[0], head[1] + direction[1])

        # Check if the new head is at the food
        if new_head == self.food_position:
            self.score += 100
            self.length += 1
            self.random_food_position()
            self.positions.insert(0, new_head)
        else:
            # Check if the new head collides with the body
            if new_head in self.positions:
                self.reset()
            else:
                # Move normally: add new head, remove tail
                self.positions.insert(0, new_head)
                self.positions.pop()


# Create a game instance with a 200x200 grid and 20px block size
game = SnakeGame(200, 200, 20)

# Move the snake to the right
game.move((20, 0))

# Move the snake down
game.move((0, 20))

# Check if food is eaten
print("Score:", game.score)

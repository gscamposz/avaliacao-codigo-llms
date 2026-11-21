
import random


class Snake:
    """
    The class is a snake game, which allows the snake to move
    and eat food, and also enables resetting and generating
    a random food position.
    """

    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_SIZE, food_position):
        """
        Initialize the snake's length, screen dimensions,
        block size, head position, score, and food position.
        """
        self.length = 1
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.BLOCK_SIZE = BLOCK_SIZE
        self.positions = [(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)]
        self.score = 0
        self.food_position = food_position

    def move(self, direction):
        """
        Move the snake in the specified direction.
        Eat food when reached and reset on collision.
        """
        current_head = self.positions[0]

        x = current_head[0] + direction[0] * self.BLOCK_SIZE
        y = current_head[1] + direction[1] * self.BLOCK_SIZE

        new_head = (x, y)

        if (
            x < 0
            or x >= self.SCREEN_WIDTH
            or y < 0
            or y >= self.SCREEN_HEIGHT
        ):
            self.reset()
            return

        if new_head in self.positions[:-1]:
            self.reset()
            return

        self.positions.insert(0, new_head)

        if new_head == self.food_position:
            self.eat_food()

        if len(self.positions) > self.length:
            self.positions.pop()

    def random_food_position(self):
        """
        Generate a random food position that does not
        overlap with the snake.
        """
        possible_positions = [
            (x, y)
            for x in range(0, self.SCREEN_WIDTH, self.BLOCK_SIZE)
            for y in range(0, self.SCREEN_HEIGHT, self.BLOCK_SIZE)
            if (x, y) not in self.positions
        ]

        if possible_positions:
            self.food_position = random.choice(possible_positions)
        else:
            self.food_position = None

    def reset(self):
        """
        Reset the snake to its initial state and generate
        a new food position.
        """
        self.length = 1
        self.positions = [
            (self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2)
        ]
        self.score = 0
        self.random_food_position()

    def eat_food(self):
        """
        Increase the snake's length by one, add 10 points
        to the score, and generate a new food position.
        """
        self.length += 1
        self.score += 10
        self.random_food_position()

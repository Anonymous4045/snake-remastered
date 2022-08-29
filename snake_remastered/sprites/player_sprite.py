"""
The main player class
"""
from ..constants import ASSETS_PATH

import arcade


class Player(arcade.Sprite):
    def __init__(self, x: int, y: int, scale: float = 1.0):
        super().__init__(ASSETS_PATH / "snake_head.png", scale=scale)

        self.position = x, y
        self.position_history: list[tuple[int, int], ...] = [(0, 0)]

        self.score = 0

        self.last_direction = None

    def update(self):
        """Update the player"""

        self.move()

    def move(self):
        self.position_history.append([int(x) for x in self.position])
        if len(self.position_history) - 1 > self.score:
            self.position_history.pop(0)

    def can_move(self, direction: str):
        """Check if the player can move in the givin direction"""

        if any(
            [
                direction == "up"
                and self.position[1] + 32 in [x[1] for x in self.position_history],
                direction == "down"
                and self.position[1] - 32 in [x[1] for x in self.position_history],
                direction == "left"
                and self.position[0] - 32 in [x[0] for x in self.position_history],
                direction == "right"
                and self.position[0] + 32 in [x[0] for x in self.position_history],
            ]
        ):
            return False

        return True

    def eat(self, apple: "Apple"):
        """Eat the apple and increase the score"""
        self.score += 1

        apple.remove_from_sprite_lists()


class SnakeBody(arcade.Sprite):
    def __init__(self, x: int, y: int, scale: float = 1.0):
        super().__init__(ASSETS_PATH / "snake_body.png", scale=scale)

        self.position = x, y

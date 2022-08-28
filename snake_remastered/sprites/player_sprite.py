"""
The main player class
"""
from ..constants import ASSETS_PATH

import arcade


class Player(arcade.Sprite):
    def __init__(self, x: int, y: int, scale: float = 1.0):
        super().__init__(ASSETS_PATH / "snake_head.png", scale=scale)

        self.position = x, y
        self.position_history = []

        self.score = 0

    def on_update(self):
        self.move()

    def move(self):
        self.position_history.append(self.position)
        if len(self.position_history) > self.score:
            self.position_history.pop(0)

        self.position = self.position_history[-1]
        print(f"Player position: {self.position}")

    def eat(apple: "Apple"):
        """Eat the apple and increase the score"""
        self.score += 1

        apple.remove_from_sprite_lists()

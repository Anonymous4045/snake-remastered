"""
Snake with Arcade
"""

from pathlib import Path
from random import randint

from .constants import *
from .sprites.apple_sprite import Apple
from .sprites.player_sprite import Player

import arcade


class GameWindow(arcade.Window):
    """Main application"""

    def __init__(self):
        """initialize variables"""

        print("Starting game...")

        super().__init__(
            title="Snake Remastered",
            fullscreen=True,
            # resizable=True,
            update_rate=1 / FPS,
        )

        arcade.set_background_color(arcade.color.BLACK)

        self.scene: arcade.Scene = None

        self.player: Player = None

        self.physics_engine = None

        self.setup()

    def setup(self):
        """Start the game"""

        self.scene = arcade.Scene()

        self.player = Player(self.width // 2, self.height // 2)
        self.scene.add_sprite("player", self.player)

        self.spawn_apple()

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player, self.scene["apple"]
        )

    def on_draw(self):
        """Display the scene"""

        self.clear()

        self.scene.draw()

    def spawn_apple(self):
        """Spawn an apple in a random place"""

        max_x, max_y = self.grid_size

        grid_pos = randint(0, max_x), randint(0, max_y)
        cord_pos = [pos * 32 for pos in grid_pos]

        apple = Apple(cord_pos)

        self.scene.add_sprite("apple", apple)

    def on_update(self, delta_time):
        """Update the scene"""

        self.physics_engine.update()

    @property
    def grid_size(self):
        """Return the grid size"""

        return self.width // 32, self.height // 32


def main():
    """Create and run the game"""

    window = GameWindow()

    arcade.run()

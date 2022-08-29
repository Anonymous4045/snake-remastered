"""
Snake with Arcade
"""

from pathlib import Path
from random import randint

from .constants import *
from .sprites.apple_sprite import Apple
from .sprites.player_sprite import Player, SnakeBody

import arcade
from arcade import key as k


class GameWindow(arcade.Window):
    """Main application"""

    def __init__(self):
        """initialize variables"""

        print("Starting game...")

        super().__init__(
            title="Snake Remastered",
            resizable=True,
            update_rate=1 / FPS,
        )

        arcade.set_background_color(arcade.color.BLACK)

        self.scene: arcade.Scene = None

        self.player: Player = None

        self.physics_engine: arcade.PhysicsEngineSimple = None

        self.setup()

    def setup(self):
        """Start the game"""

        self.scene = arcade.Scene()

        player_x = self.grid_size[0] // 2 * 32
        player_y = self.grid_size[1] // 2 * 32
        self.player = Player(player_x, player_y)
        self.scene.add_sprite("player", self.player)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player, None)

        self.spawn_apple()

    def on_draw(self):
        """Display the scene"""

        self.clear()

        self.scene.draw()

    def on_update(self, delta_time):
        """Update the scene"""

        self.physics_engine.update()

        self.player.update()

        self.check_collisions()
        if not self.is_in_bounds(self.player):
            self.setup()

        try:
            self.scene.remove_sprite_list_by_name("snake_body")
        except KeyError:
            pass
        for x, y in self.player.position_history[:-1]:
            body = SnakeBody(x, y)
            self.scene.add_sprite("snake_body", body)

    def on_key_press(self, key, modifier):
        """Handle keyboard input"""

        move = {
            "up": key in (k.UP, k.W),
            "down": key in (k.DOWN, k.S),
            "left": key in (k.LEFT, k.A),
            "right": key in (k.RIGHT, k.D),
        }

        if any(move.values()):
            if move["up"] and self.player.can_move("up"):
                self.player.velocity = 0, PLAYER_SPEED
                self.player.last_direction = "up"
            if move["down"] and self.player.can_move("down"):
                self.player.velocity = 0, -PLAYER_SPEED
                self.player.last_direction = "down"
            if move["left"] and self.player.can_move("left"):
                self.player.velocity = -PLAYER_SPEED, 0
                self.player.last_direction = "left"
            if move["right"] and self.player.can_move("right"):
                self.player.velocity = PLAYER_SPEED, 0
                self.player.last_direction = "right"

    def spawn_apple(self):
        """Spawn an apple in a random place"""

        max_x, max_y = self.grid_size

        grid_pos = randint(0, max_x - 1), randint(0, max_y - 1)
        cord_pos = [pos * 32 for pos in grid_pos]

        apple = Apple((10000, 10000))
        apple.position = cord_pos

        if (not self.is_in_bounds(apple)) or cord_pos in self.player.position_history:
            return self.spawn_apple()
        print(cord_pos, self.player.position_history)

        self.scene.add_sprite("apple", apple)

    def check_collisions(self):
        """Check for collisions"""

        player_hitting_apple = arcade.check_for_collision_with_list(
            self.player, self.scene["apple"]
        )
        if player_hitting_apple:
            apple = player_hitting_apple[0]
            self.player.eat(apple)
            self.spawn_apple()

        try:
            player_hit_self = arcade.check_for_collision_with_list(
                self.player, self.scene["snake_body"]
            )
            if player_hit_self:
                self.setup()
        except KeyError:
            pass

    def is_in_bounds(self, sprite):
        """Check if the player hits a wall"""

        if any(
            [
                sprite.left < 0,
                sprite.bottom < 0,
                sprite.right > self.width,
                sprite.top > self.height,
            ]
        ):
            return False

        return True

    @property
    def grid_size(self):
        """Return the grid size"""

        return self.width // 32, self.height // 32


def main():
    """Create and run the game"""

    window = GameWindow()

    arcade.run()

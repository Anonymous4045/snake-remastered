"""
Snake with Arcade
"""

from pathlib import Path
from random import randint

import arcade


# Constants

FPS = 2


# Paths
ROOT_PATH= Path(__file__).parent.parent
ASSETS_PATH = ROOT_PATH / 'assets'


class Player(arcade.Sprite):
    def __init__(self, x: int, y: int, scale: float = 1.0):
        super().__init__(ASSETS_PATH / 'snake_head.png', scale=scale)

        self.position = x, y
        self.position_history = []

        self.score = 0


class Apple(arcade.Sprite):
    def __init__(self, position: tuple[int, int], scale: float = 1.0):
        super().__init__(ASSETS_PATH / 'apple.png', scale=scale, center_x=position[0], center_y=position[1])


class Game(arcade.Window):
    """Main application"""

    def __init__(self):
        """initialize variables"""

        super().__init__(title="Snake Remastered", fullscreen=True, update_rate=1/FPS)
        arcade.set_background_color(arcade.color.BLACK)

        self.scene = None

        self.player = None

        self.physics_engine = None

        self.setup()

    def setup(self):
        """Start the game"""

        self.scene = arcade.Scene()

        self.player = Player(self.width // 2, self.height // 2)
        self.scene.add_sprite('player', self.player)

        self.spawn_apple()

        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.scene['apple'])


    def on_draw(self):
        '''Display the scene'''

        self.clear()

        self.scene.draw()

    def spawn_apple(self):
        '''Spawn an apple in a random place'''

        pos = randint(0, self.width), randint(0, self.height)

        apple = Apple(pos)

        self.scene.add_sprite('apple', apple)

    def on_update(self, delta_time):
        '''Update the scene'''

        self.physics_engine.update()

        self.player.velocity = 40, 0


def main():
    '''Run the game'''

    game = Game()

    arcade.run()


if __name__ == '__main__':
    main()


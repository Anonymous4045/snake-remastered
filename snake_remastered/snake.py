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

    def on_update(self):
        self.move()

    def move(self):
        self.position_history.append(self.position)
        if len(self.position_history) > self.score:
            self.position_history.pop(0)

        self.position = self.position_history[-1]
        print(f'Player position: {self.position}')

    def eat(apple: 'Apple'):
        '''Eat the apple and increase the score'''
        self.score += 1

        apple.remove_from_sprite_lists()



class Apple(arcade.Sprite):
    def __init__(self, position: tuple[int, int], scale: float = 1.0):
        super().__init__(ASSETS_PATH / 'apple.png', scale=scale, center_x=position[0], center_y=position[1])


class Game(arcade.Window):
    """Main application"""

    def __init__(self):
        """initialize variables"""

        print('Starting game...')

        super().__init__(
            title="Snake Remastered",
            fullscreen=True,
            # resizable=True,
            update_rate=1/FPS)

        arcade.set_background_color(arcade.color.BLACK)

        self.scene: arcade.Scene = None

        self.player: Player = None

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

        max_x, max_y = self.grid_size

        grid_pos = randint(0, max_x), randint(0, max_y)
        cord_pos = grid_pos[0] * 32, grid_pos[1] * 32

        apple = Apple(cord_pos)

        self.scene.add_sprite('apple', apple)

    def on_update(self, delta_time):
        '''Update the scene'''

        self.physics_engine.update()

    @property
    def grid_size(self):
        '''Return the grid size'''

        return self.width // 32, self.height // 32


def main():
    '''Create and run the game'''

    game = Game()

    arcade.run()


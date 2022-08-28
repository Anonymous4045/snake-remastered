"""
The apple sprite class
"""

from random import randint

from ..constants import ASSETS_PATH

import arcade


class Apple(arcade.Sprite):
    def __init__(self, position: tuple[int, int], scale: float = 1.0):
        super().__init__(
            ASSETS_PATH / "apple.png",
            scale=scale,
            center_x=position[0],
            center_y=position[1],
        )

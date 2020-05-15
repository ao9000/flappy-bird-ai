import copy
import os
import pygame

ASSET_PATH = "assets"

sprites_dict = {
    # Texts
    "numbers": [
        "sprites/0.png",
        "sprites/1.png",
        "sprites/2.png",
        "sprites/3.png",
        "sprites/4.png",
        "sprites/5.png",
        "sprites/6.png",
        "sprites/7.png",
        "sprites/8.png",
        "sprites/9.png"
    ],
    "gameover": "sprites/gameover.png",
    "message": "sprites/message.png",

    # Backgrounds
    "background-day": "sprites/background-day.png",
    "background-night": "sprites/background-night.png",

    # Base
    "base": "sprites/base.png",

    # Birds
    "bluebird": [
        "sprites/bluebird-downflap.png",
        "sprites/bluebird-midflap.png",
        "sprites/bluebird-upflap.png"
    ],

    "redbird": [
        "sprites/redbird-downflap.png",
        "sprites/redbird-midflap.png",
        "sprites/redbird-upflap.png"
    ],

    "yellowbird": [
        "sprites/yellowbird-downflap.png",
        "sprites/yellowbird-midflap.png",
        "sprites/yellowbird-upflap.png"
    ],

    # Pipes
    "pipe-green": "sprites/pipe-green.png",
    "pipe-red": "sprites/pipe-red.png"
}

# Add relative paths to file names
# Load assets into pygame
for key, value in copy.deepcopy(sprites_dict).items():
    if isinstance(value, list):
        for index, value in enumerate(value):
            sprites_dict[key][index] = pygame.image.load(os.path.join(ASSET_PATH, value))
    else:
        sprites_dict[key] = pygame.image.load(os.path.join(ASSET_PATH, value))

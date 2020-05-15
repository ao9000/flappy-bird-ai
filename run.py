import pygame
import sys
import os
import copy

DISPLAY_WIDTH, DISPLAY_HEIGHT = 288, 512
ASSET_PATH = "assets"


def quit_game():
    pygame.quit()
    sys.exit()


def setup_game_window():
    display_dimensions = (DISPLAY_WIDTH, DISPLAY_HEIGHT)
    screen = pygame.display.set_mode(display_dimensions)
    pygame.display.set_caption("Flappy-Bird-AI")

    return screen


def setup_game_clock():
    clock = pygame.time.Clock()


def load_assets():
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
    transparent_dict = ["bird", "pipe", "numbers", "gameover", "message"]
    for key, value in copy.deepcopy(sprites_dict).items():
        if any(item in key for item in transparent_dict):
            if isinstance(value, list):
                for index, value in enumerate(value):
                    sprites_dict[key][index] = pygame.image.load(os.path.join(ASSET_PATH, value)).convert_alpha()
            else:
                sprites_dict[key] = pygame.image.load(os.path.join(ASSET_PATH, value)).convert_alpha()
        else:
            if isinstance(value, list):
                for index, value in enumerate(value):
                    sprites_dict[key][index] = pygame.image.load(os.path.join(ASSET_PATH, value)).convert()
            else:
                sprites_dict[key] = pygame.image.load(os.path.join(ASSET_PATH, value)).convert()

    return sprites_dict


def main():
    pygame.init()

    screen = setup_game_window()
    sprites_dict = load_assets()

    # Game loop
    while True:
        for event in pygame.event.get():
            # Quit game when X is pressed
            if event.type == pygame.QUIT:
                quit_game()

            # Quit game when ESC key is pressed
            elif event.type == pygame.KEYDOWN:
                if event.key == 27:
                    quit_game()

            # Display background
            screen.blit(sprites_dict['background-day'], (0, 0))

            # Add base
            screen.blit(sprites_dict['base'], (0, DISPLAY_HEIGHT - sprites_dict['base'].get_height()))

            # Update screen
            pygame.display.update()


if __name__ == '__main__':
    main()

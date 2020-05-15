from assets import sprites_dict
import pygame
import sys
import os
import copy

FPS = 30
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


def load_assets():
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

    # Setup window properties
    screen = setup_game_window()

    # Load assets
    # sprites_dict = load_assets()

    # Init clock
    clock = pygame.time.Clock()

    # Game loop
    while True:
        # Define FPS
        clock.tick(FPS)
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

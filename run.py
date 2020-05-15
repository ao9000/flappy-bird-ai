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
            screen.blit(sprites_dict['background-day'].convert(), (0, 0))




            # Update screen
            pygame.display.update()


if __name__ == '__main__':
    main()

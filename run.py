from assets import sprites_dict
from base import Base

import pygame
import sys

FPS = 30
DISPLAY_WIDTH, DISPLAY_HEIGHT = 288, 512


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

    # Initialize background
    screen.blit(sprites_dict['background-day'].convert(), (0, 0))

    # Initialize first & second base
    base1 = Base(0, DISPLAY_HEIGHT - sprites_dict['base'].get_height())
    base2 = Base(DISPLAY_WIDTH, DISPLAY_HEIGHT - sprites_dict['base'].get_height())

    # Game loop
    while True:
        # Define FPS
        clock.tick(FPS)
        # Loop events
        for event in pygame.event.get():
            # Quit game when X is pressed
            if event.type == pygame.QUIT:
                quit_game()

            # Quit game when ESC key is pressed
            elif event.type == pygame.KEYDOWN:
                if event.key == 27:
                    quit_game()

        base1.draw_to_screen(screen)
        base2.draw_to_screen(screen)

        base1.move()
        base2.move()

        # Update screen
        pygame.display.update()


if __name__ == '__main__':
    main()

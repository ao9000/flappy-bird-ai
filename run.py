from assets import sprites_dict
from config_handler import config
from base import Base
from bird import Bird
from pipe import Pipe

import pygame
import sys


def quit_game():
    # Exit pygame window
    pygame.quit()
    sys.exit()


def setup_game_window():
    # Define screen size
    display_dimensions = (config['General']['DISPLAY_WIDTH'], config['General']['DISPLAY_HEIGHT'])
    screen = pygame.display.set_mode(display_dimensions)

    # Define window caption
    pygame.display.set_caption("Flappy-Bird-AI")

    return screen


def base_animation_handler(base_list):
    for base in base_list:
        # Move both bases
        base.move()

        # Check if any base has exited the left side of the screen
        # If true, place base back to the right side
        if base.x + sprites_dict['base'].get_width() <= 0:
            base.x = config['General']['DISPLAY_WIDTH']


def pipes_animation_handler(pipe_list):
    # Check if any pipe has exited the left side of the screen
    # If true, place pipe back to the right side
    for pipe in pipe_list:
        pipe.move()
        if pipe.x + sprites_dict['pipe-green'].get_width() <= 0:
            pipe.random_y()
            pipe.x = config['General']['DISPLAY_WIDTH']


def check_crash(bird, base):
    if bird.rect.collidelist([item.rect for item in base]) != -1:
        return True

    return False


def gameover_text(screen):
    # Game-over text
    screen.blit(sprites_dict['gameover'].convert_alpha(),
                ((config['General']['DISPLAY_WIDTH'] / 2) - (sprites_dict['gameover'].get_width() / 2),
                 (config['General']['DISPLAY_HEIGHT'] / 2) - (sprites_dict['gameover'].get_height() / 2)))


def initialize_game_elements():
    # Initialize first & second base
    base1 = Base(0, config['General']['DISPLAY_HEIGHT'] - Base.height)
    base2 = Base(Base.width, config['General']['DISPLAY_HEIGHT'] - Base.height)

    # Initialize bird
    bird = Bird((config['General']['DISPLAY_WIDTH'] / 2) - Bird.width, config['General']['DISPLAY_HEIGHT'] / 2)

    # Initialize pipes
    pipe1 = Pipe(config['General']['DISPLAY_WIDTH'])
    pipe2 = Pipe(config['General']['DISPLAY_WIDTH'] + Pipe.interval)

    return {
        "base": [base1, base2],
        "bird": bird,
        "pipe": [pipe1, pipe2]
    }


def main():
    # Initialize pygame module
    pygame.init()

    # Setup window properties
    screen = setup_game_window()

    # Initialize clock
    clock = pygame.time.Clock()

    # Initialize game elements
    game_elements_dict = initialize_game_elements()

    # Initialize crash status
    crashed = False
    start = False

    # Game loop
    while True:
        jump = False
        # Define config['General']['FPS']
        clock.tick(config['General']['FPS'])
        # Loop events
        for event in pygame.event.get():
            # Quit game when X is pressed
            if event.type == pygame.QUIT:
                quit_game()

            elif event.type == pygame.KEYDOWN:
                # Quit game when ESC key is pressed
                if event.key == 27:
                    quit_game()
                # Space was pressed, flap bird
                elif event.key == 32:
                    jump = True
                    start = True

        # Check if alive
        if not crashed:
            # Clear previous screen state & render background
            screen.blit(sprites_dict['background-day'].convert(), (0, 0))

            # Draw bird to screen
            game_elements_dict['bird'].draw_to_screen(screen)

            if start:
                # Update pipes coordinates
                pipes_animation_handler(game_elements_dict['pipe'])

                # Draw pipes to the screen
                for pipe in game_elements_dict['pipe']:
                    pipe.draw_to_screen(screen)

                if jump:
                    # Bird jump
                    game_elements_dict['bird'].jump()

                else:
                    # Bird no jump
                    game_elements_dict['bird'].do_nothing()

            # Update base coordinates
            base_animation_handler(game_elements_dict['base'])

            # Draw bases to screen
            for base in game_elements_dict['base']:
                base.draw_to_screen(screen)

            # Check if crashed
            if check_crash(game_elements_dict['bird'], game_elements_dict['base']):
                crashed = True

        else:
            # Dead
            gameover_text(screen)

        # Update screen
        pygame.display.update()


if __name__ == '__main__':
    main()

from assets import sprites_dict
from base import Base
from bird import Bird
from pipe import Pipe
from score import Score

import pygame
import sys
import math

DISPLAY_WIDTH = sprites_dict['background-day'].get_width()
DISPLAY_HEIGHT = sprites_dict['background-day'].get_height()
FPS = 30


def quit_game():
    # Exit pygame window
    pygame.quit()
    sys.exit()


def setup_game_window():
    # Define screen size
    display_dimensions = (DISPLAY_WIDTH, DISPLAY_HEIGHT)
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
            base.x = DISPLAY_WIDTH


def pipes_animation_handler(pipe_list):
    # Check if any pipe has exited the left side of the screen
    # If true, place pipe back to the right side
    for index, pipe in enumerate(pipe_list, start=0):
        pipe.move()
        if pipe.x + sprites_dict['pipe-green'].get_width() <= 0:
            pipe.random_y()
            pipe.passed = False
            pipe.x = pipe_list[index-1].x + pipe.interval


def check_crash(bird, base, pipes):
    if bird.rect.collidelist([item.rect for item in base]) != -1:
        return True

    # Calculate offset
    for pipe in pipes:
        # Lower pipe
        lower_pipe_offset = tuple(map(math.ceil, (pipe.x - bird.x, pipe.lower_y - bird.y)))
        # Upper pipe
        upper_pipe_offset = tuple(map(math.floor, (pipe.x - bird.x, pipe.upper_y - bird.y)))

        if bird.get_mask().overlap(pipe.get_mask()[0], lower_pipe_offset):
            return True

        elif bird.get_mask().overlap(pipe.get_mask()[1], upper_pipe_offset):
            return True

        # Check if bird is above the sky limit and in a pipe
        elif bird.y < 0 and pipe.x < bird.x < (pipe.x + pipe.width):
            return True

    return False


def score_handler(bird, pipes, score):
    # Check if passed pipe
    for pipe in pipes:
        if bird.x > (pipe.x + pipe.width) and not pipe.passed:
            score.score += 1
            pipe.passed = True


def gameover_text(screen):
    # Game-over text
    screen.blit(sprites_dict['gameover'].convert_alpha(),
                ((DISPLAY_WIDTH / 2) - (sprites_dict['gameover'].get_width() / 2),
                 (DISPLAY_HEIGHT / 2) - (sprites_dict['gameover'].get_height() / 2)))


def initialize_game_elements():
    # Initialize first & second base
    base1 = Base(0, DISPLAY_HEIGHT - Base.height)
    base2 = Base(Base.width, DISPLAY_HEIGHT - Base.height)

    # Initialize bird
    bird = Bird((DISPLAY_WIDTH / 2) - Bird.width, DISPLAY_HEIGHT / 2)

    # Initialize pipes
    pipe1 = Pipe(DISPLAY_WIDTH * 2)
    pipe2 = Pipe(pipe1.x + Pipe.interval)

    # Initialize score
    score = Score()

    return {
        "base": [base1, base2],
        "bird": bird,
        "pipe": [pipe1, pipe2],
        "score": score
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

    # Initialize game variables
    crashed = False
    start = False

    # Game loop
    while True:
        jump = False
        # Define
        clock.tick(FPS)
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
                # Draw pipes to the screen
                for pipe in game_elements_dict['pipe']:
                    pipe.draw_to_screen(screen)

                # Update pipes coordinates
                pipes_animation_handler(game_elements_dict['pipe'])

            # Draw bases to screen
            for base in game_elements_dict['base']:
                base.draw_to_screen(screen)

            # Update base coordinates
            base_animation_handler(game_elements_dict['base'])

            if start:
                if jump:
                    # Bird jump
                    game_elements_dict['bird'].jump()

                else:
                    # Bird no jump
                    game_elements_dict['bird'].do_nothing()

                # Check if passed pipe
                score_handler(game_elements_dict['bird'], game_elements_dict['pipe'], game_elements_dict['score'])

                # Render score
                game_elements_dict['score'].draw_to_screen(screen)

                # Check if crashed
                if check_crash(game_elements_dict['bird'], game_elements_dict['base'], game_elements_dict['pipe']):
                    crashed = True

        else:
            # Dead
            gameover_text(screen)

        # Update screen
        pygame.display.update()


if __name__ == '__main__':
    main()

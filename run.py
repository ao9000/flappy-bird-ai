from assets import sprites_dict
from base import Base
from bird import Bird
from pipe import Pipe

import pygame
import sys

FPS = 30
DISPLAY_WIDTH, DISPLAY_HEIGHT = 288, 512


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


def base_animation_handler(base1, base2):
    # Move both bases
    base1.move()
    base2.move()

    # Check if any base has exited the left side of the screen
    # If true, place base back to the right side
    if base1.x + sprites_dict['base'].get_width() <= 0:
        base1.x = DISPLAY_WIDTH
    elif base2.x + sprites_dict['base'].get_width() <= 0:
        base2.x = DISPLAY_WIDTH


def check_collide(bird, base):
    if bird.rect.collidelist([item.rect for item in base]) != -1:
        return True
    
    return False


def gameover(screen):
    # Gameover text
    screen.blit(sprites_dict['gameover'].convert_alpha(),
                ((DISPLAY_WIDTH / 2) - (sprites_dict['gameover'].get_width() / 2),
                 (DISPLAY_HEIGHT / 2) - (sprites_dict['gameover'].get_height() / 2)))


def main():
    # Initialize pygame module
    pygame.init()

    # Setup window properties
    screen = setup_game_window()

    # Initialize clock
    clock = pygame.time.Clock()

    # Initialize first & second base
    base1 = Base(0, DISPLAY_HEIGHT - Base.height)
    base2 = Base(Base.width, DISPLAY_HEIGHT - Base.height)

    # Initialize bird
    bird = Bird((DISPLAY_WIDTH / 2) - Bird.width, DISPLAY_HEIGHT / 2)
    
    dead = False

    # Game loop
    while True:
        bird_jump = False
        # Define FPS
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
                    bird_jump = True

        if dead:
            gameover(screen)
            pygame.display.update()
            continue

        # Clear previous screen state & render background
        screen.blit(sprites_dict['background-day'].convert(), (0, 0))

        # Draw base to screen
        base1.draw_to_screen(screen)
        base2.draw_to_screen(screen)

        # Update base coordinates
        base_animation_handler(base1, base2)

        # Draw bird to screen
        bird.draw_to_screen(screen)

        if bird_jump:
            # Bird jump
            bird.jump()

        else:
            # Bird no jump
            bird.do_nothing()

        if check_collide(bird, [base1, base2]):
            dead = True

        # Update screen
        pygame.display.update()


if __name__ == '__main__':
    main()

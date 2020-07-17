"""
    Test many NeuroEvolution of Augmenting Topologies (NEAT) model at the same time to play Flappy bird
    And see who's the longest surviving bird

    To know more about NEAT, refer to the link https://neat-python.readthedocs.io/en/latest/neat_overview.html
"""

from assets import sprites_dict
from game.base import Base
from game.bird import Bird
from game.pipe import Pipe
from game.score import Score

import pygame
import sys
import math
import neat
import pickle
import os
from tabulate import tabulate

# Global variables
DISPLAY_WIDTH = sprites_dict['background-day'].get_width()
DISPLAY_HEIGHT = sprites_dict['background-day'].get_height()
FPS = 30


def quit_game():
    """
    Exits the pygame window and stops the script
    """

    # Exit pygame window
    pygame.quit()
    sys.exit()


def setup_game_window():
    """
    Setups pygame window and caption

    :return: type: pygame.surface
    The pygame window object
    """

    # Define screen size
    display_dimensions = (DISPLAY_WIDTH, DISPLAY_HEIGHT)
    screen = pygame.display.set_mode(display_dimensions)

    # Define window caption
    pygame.display.set_caption("Flappy-Bird-AI")

    return screen


def base_animation_handler(base_list):
    """
    Moves both base objects simultaneously
    When any one of the base have move beyond the left side of the screen, reset the position of the base back at the
    end of the other base

    :param base_list: type: list
    List containing both bases class instances
    """

    for base in base_list:
        # Move both bases
        base.move()

        # Check if any base has exited the left side of the screen
        # If true, place base back to the right side
        if base.x + sprites_dict['base'].get_width() <= 0:
            base.x = DISPLAY_WIDTH


def pipes_animation_handler(pipe_list):
    """
    Moves both pipe objects simultaneously
    When any one of the pipe have move beyond the left side of the screen, reset the position of the base back at the
    end of the other pipe with added interval width

    Note: A single pipe object contains 2 pipes, the upper & lower pipe sprite

    :param pipe_list: type: list
    List containing both pipe class instances
    """

    # Check if any pipe has exited the left side of the screen
    # If true, place pipe back to the right side
    for index, pipe in enumerate(pipe_list, start=0):
        pipe.move()
        if pipe.x + sprites_dict['pipe-green'].get_width() <= 0:
            pipe.random_y()
            pipe.passed = False
            pipe.x = pipe_list[index - 1].x + pipe.interval


def check_crash(game_elements_dict):
    """
    Check if any of the bird in the population has crashed in any of these ways
    Ways to crash:
        1. Hitting the base
        2. Hitting the pipe (Both upper & lower pipe)
        3. Flying above the screen height and over a pipe

    If any bird were to have crashed, these steps will be followed:
        1. Deduct fitness score according to what object it has crashed into
        2. Remove crashed bird's corresponding genome
        3. Remove crashed bird's network
        4. Remove crashed bird from the surviving bird list
        5. Record the score and fitness of the bird

    :param game_elements_dict: type: dict
    A dictionary containing all the class instances needed for the game to function
    """
    for index, bird in enumerate(game_elements_dict['birds'], start=0):

        # Hit base
        if bird.rect.collidelist([item.rect for item in game_elements_dict['base']]) != -1:
            game_elements_dict['genomes'][index][1].fitness -= 10
            game_elements_dict['ranking'][bird]['fitness score'] = game_elements_dict['genomes'][index][1].fitness
            game_elements_dict['ranking'][bird]['pipe score'] = game_elements_dict['score'].score
            del game_elements_dict['networks'][index]
            del game_elements_dict['genomes'][index]
            del game_elements_dict['birds'][index]

        # Calculate offset for pipe
        for pipe in game_elements_dict['pipe']:
            # Lower pipe
            lower_pipe_offset = tuple(map(math.ceil, (pipe.x - bird.x, pipe.lower_y - bird.y)))
            # Upper pipe
            upper_pipe_offset = tuple(map(math.floor, (pipe.x - bird.x, pipe.upper_y - bird.y)))

            # Hit lower pipe
            if bird.get_mask().overlap(pipe.get_mask()[0], lower_pipe_offset):
                game_elements_dict['genomes'][index][1].fitness -= 1
                game_elements_dict['ranking'][bird]['fitness score'] = game_elements_dict['genomes'][index][1].fitness
                game_elements_dict['ranking'][bird]['pipe score'] = game_elements_dict['score'].score
                del game_elements_dict['networks'][index]
                del game_elements_dict['genomes'][index]
                del game_elements_dict['birds'][index]

            # Hit upper pipe
            elif bird.get_mask().overlap(pipe.get_mask()[1], upper_pipe_offset):
                game_elements_dict['genomes'][index][1].fitness -= 1
                game_elements_dict['ranking'][bird]['fitness score'] = game_elements_dict['genomes'][index][1].fitness
                game_elements_dict['ranking'][bird]['pipe score'] = game_elements_dict['score'].score
                del game_elements_dict['networks'][index]
                del game_elements_dict['genomes'][index]
                del game_elements_dict['birds'][index]

            # Check if bird is above the sky limit and in a pipe
            elif bird.y < 0 and pipe.x < bird.x < (pipe.x + pipe.width):
                game_elements_dict['genomes'][index][1].fitness -= 10
                game_elements_dict['ranking'][bird]['fitness score'] = game_elements_dict['genomes'][index][1].fitness
                game_elements_dict['ranking'][bird]['pipe score'] = game_elements_dict['score'].score
                del game_elements_dict['networks'][index]
                del game_elements_dict['genomes'][index]
                del game_elements_dict['birds'][index]


def check_generation_crash(game_elements_dict):
    """
    Checks if there is any surviving birds in the population

    :param game_elements_dict: type: dict
    A dictionary containing all the class instances needed for the game to function

    :return: type: bool
    True if there are no surviving birds, else False
    """
    # Check if there is any bird surviving
    if len(game_elements_dict['birds']) == 0:
        return True
    else:
        return False


def print_rankings(game_elements_dict):
    """
    Print the Model rankings in table format sorted from the best performing model in descending order

    :param game_elements_dict: type: dict
    A dictionary containing all the class instances needed for the game to function
    """
    # Print rankings
    print("\nModel Rankings")
    print(tabulate(
        sorted(game_elements_dict['ranking'].values(), key=lambda x: (x["pipe score"], x["fitness score"]),
               reverse=True), headers="keys", floatfmt=".2f"))


def update_rankings(game_elements_dict):
    """
    Update ranking of all birds regardless of their states (Dead or alive)

    :param game_elements_dict:  type: dict
    A dictionary containing all the class instances needed for the game to function
    """
    for index, bird in enumerate(game_elements_dict['birds'], start=0):
        game_elements_dict['ranking'][bird]['fitness score'] = game_elements_dict['genomes'][index][1].fitness
        game_elements_dict['ranking'][bird]['pipe score'] = game_elements_dict['score'].score


def score_handler(game_elements_dict):
    """
    Records the game score by incrementing the score each time the bird passes the pipe fully

    Also cycles the pipe index to the next pipe for the bird so to input the correct pipe coordinates for the
    NEAT algorithm

    Lastly, adds fitness score to the surviving birds that passed any pipe

    :param game_elements_dict: type: dict
    A dictionary containing all the class instances needed for the game to function
    """
    if not check_generation_crash(game_elements_dict):
        # Check if passed pipe
        for pipe in game_elements_dict['pipe']:
            if game_elements_dict['birds'][0].x > (pipe.x + pipe.width) and not pipe.passed:
                pipe.passed = True
                game_elements_dict['score'].score += 1

                # Cycle pipe index
                if game_elements_dict['pipe_index'] == 0:
                    game_elements_dict['pipe_index'] = 1
                else:
                    game_elements_dict['pipe_index'] = 0

                # Add fitness score to remaining birds which passed the pipe
                for genome_id, genome in game_elements_dict['genomes']:
                    genome.fitness += 5


def initialize_game_elements(genomes):
    """
    Creates all class instances needed for the game, then saves all instances into a dictionary

    Also creates the birds, networks and genomes list needed for the NEAT algorithm recording purposes
    :param genomes: type list
    List containing the genomes for every bird

    :return: type: dict
    A dictionary containing all the class instances needed for the game to function
    """
    # Initialize first & second base
    base1 = Base(0, DISPLAY_HEIGHT - Base.height)
    base2 = Base(Base.width, DISPLAY_HEIGHT - Base.height)

    # Initialize bird, network and genome list
    # These list will record the surviving birds respective network and genomes
    birds_list = []
    networks_list = []
    genomes_list = []
    ranking = {}
    for genome_id, genome, model_name in genomes:
        # Create network for bird
        # Setup network using genome & config
        network = neat.nn.FeedForwardNetwork.create(genome, config)
        networks_list.append(network)

        # Create bird
        bird = Bird((DISPLAY_WIDTH / 2) - Bird.width, DISPLAY_HEIGHT / 2)
        birds_list.append(bird)

        # Define starting fitness
        genome.fitness = 0
        genomes_list.append((genome_id, genome))

        # Add model names into ranking board
        ranking[bird] = {"model name": model_name,
                         "fitness score": None,
                         "pipe score": None
                         }

    # Initialize pipes
    pipe1 = Pipe(DISPLAY_WIDTH * 2)
    pipe2 = Pipe(pipe1.x + Pipe.interval)
    # Get pipe index
    pipe_x_list = [pipe.x for pipe in [pipe1, pipe2]]
    pipe_index = pipe_x_list.index(min(pipe_x_list))

    # Initialize score
    score = Score()

    return {
        "base": [base1, base2],
        "birds": birds_list,
        "networks": networks_list,
        "genomes": genomes_list,
        "ranking": ranking,
        "pipe": [pipe1, pipe2],
        "pipe_index": pipe_index,
        "score": score
    }


def fitness(genomes, config):
    """
    The main function for the script
    What it does:
        1. Setups game windows & clock
        2. Creates all needed class instances for the game
        3. Main game loop
            3a. Render bird to screen
            3b. Render pipe to screen
            3c. Render base to screen
            3d. Get model output (Jump or no jump) and handle them for each bird
            3e. Handle score increment & render score/fitness for each bird
            3f. Check if all testing birds has crashed, if so print test results table

    :param genomes: type: list
    List containing the genomes for every bird

    :param config: type: neat.config.Config
    The NEAT configuration file object
    """
    # Initialize pygame module
    pygame.init()

    # Setup window properties
    screen = setup_game_window()

    # Initialize clock
    clock = pygame.time.Clock()

    # Initialize game elements
    game_elements_dict = initialize_game_elements(genomes)

    # Initialize game variables
    crashed = False

    # Game loop
    while True:
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

        # Check if alive
        if not crashed:
            # Clear previous screen state & render background
            screen.blit(sprites_dict['background-day'].convert(), (0, 0))

            # Draw all birds to screen with their model name above
            for bird in game_elements_dict['birds']:
                bird.draw_to_screen(screen)
                bird.draw_name_label(game_elements_dict['ranking'][bird]['model name'], screen)

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

            # Neural network output (Flap or no flap?)
            for index, bird in enumerate(game_elements_dict['birds']):
                # Award fitness for surviving
                game_elements_dict['genomes'][index][1].fitness += 0.1

                # Get output of model
                # Pass model bird location, pipes location
                output = game_elements_dict['networks'][index].activate(((bird.y+bird.height/2),
                                                                         game_elements_dict['pipe'][game_elements_dict['pipe_index']].upper_y - bird.y,
                                                                         (bird.y+bird.height) - game_elements_dict['pipe'][game_elements_dict['pipe_index']].lower_y)
                                                                        )
                # Activation function evaluation
                if output[0] > 0.5:
                    bird.jump()
                else:
                    bird.do_nothing()

            # Check if any bird crashed
            check_crash(game_elements_dict)

            # Award points for remaining bird if passed pipe
            score_handler(game_elements_dict)

            # Render score
            game_elements_dict['score'].draw_to_screen(screen)

            # Check if all test birds has crashed
            if check_generation_crash(game_elements_dict):
                crashed = True
                print_rankings(game_elements_dict)

            # Over score threshold, ending test
            if game_elements_dict['score'].score >= 1000:
                print("Score threshold reached, ending test...")
                update_rankings(game_elements_dict)
                print_rankings(game_elements_dict)
                quit_game()

        else:
            # Dead
            pygame.quit()
            break

        # Update screen
        pygame.display.update()


if __name__ == '__main__':
    """
    Running NEAT testing simulation
    
    What it does:
        1. Import our configuration file to use as settings values
        2. Load all models from the model directory
        3. Run a game with all loaded models
    """
    # Import config file
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, 'neat-config.ini')

    # Load all models from directory
    genomes = []
    for model in os.listdir("models"):
        if model.endswith(".pkl"):
            print("Loading model {}...".format(model))
            with open(os.path.join("models/", model), 'rb') as data:
                # Convert loaded genome into required data structure
                genome = pickle.load(data)
                genomes.append((len(genomes) + 1, genome, model))

    # Run game
    fitness(genomes, config)

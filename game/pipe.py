"""
    Flappy bird Pipe class.
    Responsible for creating and moving pipes in the game
"""


from assets import sprites_dict
import pygame
import random


class Pipe:
    """
    Pipe class
    A single pipe instance includes the top and bottom pipe for the same x coordinate
    For every instance of the game, there should be 2 pipe class instances
    One rendered in the screen and another outside of the screen waiting to be rendered in once the first base moves out
    And when the pipe moves completely out of the screen, reset the position to the end of the other pipe

    image contains the loaded pygame sprite for both upper and lower pipes
    width and height contains the width and height of the sprite in pixels
    velocity controls the amount of pixels the base moves every tick
    gap controls the distance in pixels between the upper and lower pipe
    interval controls the distance in pixels between each wave of pipe
    """
    image = [sprites_dict['pipe-green'],
             pygame.transform.flip(sprites_dict['pipe-green'], False, True)]
    width, height = image[0].get_width(), image[0].get_height()
    velocity = 5
    gap = 135
    interval = 215

    def __init__(self, x):
        """
        Constructor for Pipe class

        :param x: type: int
        x coordinates of the pipe
        Note: The coordinates refer to the left corner of the sprite
        """
        self._x = x
        self._upper_y = None
        self._lower_y = None
        self._upper_rect = None
        self._lower_rect = None
        self._passed = False
        self.image = [pipe.convert_alpha() for pipe in self.image]

        # Assign y
        self.random_y()

    # Getter & setter methods
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, val):
        self._x = val

    @property
    def lower_y(self):
        return self._lower_y

    @property
    def upper_y(self):
        return self._upper_y

    @lower_y.setter
    def lower_y(self, val):
        self._upper_y = (val - (self.gap + self.height))
        self._lower_y = val

    @property
    def passed(self):
        return self._passed

    @passed.setter
    def passed(self, val):
        self._passed = val

    def random_y(self):
        """
        Randoms the y coordinate for the pipe
        This function is used when the pipe is being repositioned back into the far right corner of the screen
        """
        # Random y between proportions of the screen
        y = random.randint(round(sprites_dict['background-day'].get_height() * (3 / 10)),
                           round(sprites_dict['background-day'].get_height() * (7 / 10)))

        # Reset pipe back to far right
        self._upper_y = (y - (self.gap + self.height))
        self._lower_y = y

    def move(self):
        """
        Shift both upper & lower pipes towards the left at the same pace according to the velocity value
        """
        # Move both upper & lower pipes
        self._x -= self.velocity

    def get_mask(self):
        """
        Extracts the mask from the sprite to provide pixel based collision detection

        :return: type: pygame.mask.Mask
        The extracted mask object
        """
        masks = [pygame.mask.from_surface(pipe) for pipe in self.image]

        return masks

    def draw_to_screen(self, screen):
        """
        Draw/renders both upper & lower pipes into the game screen

        :param screen: type: pygame.surface
        The surface/screen of the game for displaying purposes
        """
        # Lower pipe
        self._lower_rect = screen.blit(self.image[0], (self._x, self._lower_y))

        # Upper pipe
        self._upper_rect = screen.blit(self.image[1], (self._x, self._upper_y))

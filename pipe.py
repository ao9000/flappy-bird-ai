from assets import sprites_dict
from config_handler import config
import pygame
import random


class Pipe:
    image = [sprites_dict[config['Pipe']['color']], pygame.transform.flip(sprites_dict[config['Pipe']['color']], False, True)]
    width, height = image[0].get_width(), image[0].get_height()
    velocity = config['Pipe']['speed']
    gap = 125
    interval = (config['General']['display_width']/2) + (width/2)

    def __init__(self, x):
        self._x = x
        self._upper_y = None
        self._lower_y = None
        self._upper_rect = None
        self._lower_rect = None

        # Assign y
        self.random_y()

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, val):
        self._x = val

    @property
    def lower_y(self):
        return self._lower_y

    @lower_y.setter
    def lower_y(self, val):
        self._upper_y = (val - (self.gap + self.height))
        self._lower_y = val

    def random_y(self):
        y = random.randint(round(config['General']['display_height'] * (3 / 10)),
                           round(config['General']['display_height'] * (7 / 10)))

        self._upper_y = (y - (self.gap + self.height))
        self._lower_y = y

    def move(self):
        # Move both pipes
        self._x -= self.velocity

    def draw_to_screen(self, screen):
        image = [pipe.convert_alpha() for pipe in self.image]

        # Lower pipe
        self._lower_rect = screen.blit(image[0], (self._x, self._lower_y))

        # Upper pipe
        self._upper_rect = screen.blit(image[1], (self._x, self._upper_y))

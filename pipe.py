from assets import sprites_dict
import pygame
import random


class Pipe:
    image = [sprites_dict['pipe-green'],
             pygame.transform.flip(sprites_dict['pipe-green'], False, True)]
    width, height = image[0].get_width(), image[0].get_height()
    velocity = 5
    gap = 125
    interval = (sprites_dict['background-day'].get_width()/2) + (width/2)

    def __init__(self, x):
        self._x = x
        self._upper_y = None
        self._lower_y = None
        self._upper_rect = None
        self._lower_rect = None
        self._passed = False
        self.image = [pipe.convert_alpha() for pipe in self.image]

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
        y = random.randint(round(sprites_dict['background-day'].get_height() * (3 / 10)),
                           round(sprites_dict['background-day'].get_height() * (7 / 10)))

        self._upper_y = (y - (self.gap + self.height))
        self._lower_y = y

    def move(self):
        # Move both pipes
        self._x -= self.velocity

    def get_mask(self):
        masks = [pygame.mask.from_surface(pipe) for pipe in self.image]

        return masks

    def draw_to_screen(self, screen):
        # Lower pipe
        self._lower_rect = screen.blit(self.image[0], (self._x, self._lower_y))

        # Upper pipe
        self._upper_rect = screen.blit(self.image[1], (self._x, self._upper_y))

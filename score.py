from assets import sprites_dict
from config_handler import config


class Score:
    image = sprites_dict['numbers']

    def __init__(self):
        self._score = 0
        self._rect = None
        self.image = [number.convert_alpha() for number in self.image]

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, val):
        self._score = val

    def get_image(self):
        return self.image[self._score]

    def draw_to_screen(self, screen):
        self._rect = screen.blit(self.image[self.score],
                                 (config['General']['display_width']/2 - self.get_image().get_width()/2,
                                 config['General']['display_height']/8 - self.get_image().get_height()/2))

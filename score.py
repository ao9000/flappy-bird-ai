from assets import sprites_dict
from config_handler import config


class Score:
    image = sprites_dict['numbers']

    def __init__(self):
        self._score = 9933
        self._rect = []
        self.image = [number.convert_alpha() for number in self.image]

    @property
    def score(self):
        return self._score

    @property
    def score_to_str(self):
        return str(self._score)

    @score.setter
    def score(self, val):
        self._score = val

    @property
    def get_image(self):
        if (digits := len(str(self.score))) > 1:
            return [self.image[int(self.score_to_str[number])] for number in range(0, digits)]

        return [self.image[self._score]]

    def draw_to_screen(self, screen):
        image_list = self.get_image
        image_width_list = [image.get_width() for image in image_list]
        self._rect = []

        for index, number in enumerate(image_list, start=0):
            self._rect.append(screen.blit(number,
                                          ((config['General']['display_width'] / 2 - sum(image_width_list) / 2) + sum(image_width_list[0:index]),
                                           config['General']['display_height'] / 8
                                           ))
                              )
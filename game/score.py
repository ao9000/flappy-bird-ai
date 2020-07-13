"""
    Flappy bird Score class
    Responsible for counting and rendering the score to the screen
"""


from assets import sprites_dict


class Score:
    """
    Score class
    For every instance of the game, there should be a single score class instance

    image contains all of the pygame loaded sprites for digits 0-9
    """
    image = sprites_dict['numbers']

    def __init__(self):
        """
        Constructor for Score class
        """
        self._score = 0
        self._rect = []
        self.image = [number.convert_alpha() for number in self.image]

    # Getter & setter methods
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
        """
        Detects the amount of digits in the score, then constructs a list containing the number sprites needed

        :return: type: list
        List of pygame sprites of the numbers that make up the score
        """
        if (digits := len(str(self.score))) > 1:
            return [self.image[int(self.score_to_str[number])] for number in range(0, digits)]

        return [self.image[self._score]]

    def draw_to_screen(self, screen):
        """
        Loops the all digits of the score and draw/renders the player's score into the game screen digit by digit

        :param screen: type: pygame.surface
        The surface/screen of the game for displaying purposes
        """
        image_list = self.get_image
        image_width_list = [image.get_width() for image in image_list]
        self._rect = []

        for index, number in enumerate(image_list, start=0):
            self._rect.append(screen.blit(number,
                                          ((sprites_dict['background-day'].get_width() / 2 - sum(
                                              image_width_list) / 2) + sum(image_width_list[0:index]),
                                           sprites_dict['background-day'].get_height() / 8
                                           ))
                              )

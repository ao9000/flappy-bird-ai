from assets import sprites_dict


class Bird:
    state = 0
    image = sprites_dict['yellowbird']
    width, height = image[0].get_width(), image[0].get_height()

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._rect = None

    def flap(self):
        pass

    def draw_to_screen(self, screen):
        image = [bird.convert_alpha() for bird in self.image]
        self._rect = screen.blit(image[self.state], (self._x, self._y))

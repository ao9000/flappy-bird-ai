from assets import sprites_dict


class Base:
    velocity = 5
    image = sprites_dict['base']
    width, height = image.get_width(), image.get_height()

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._rect = None
        self.image = self.image.convert()

    @property
    def rect(self):
        return self._rect

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, val):
        self._x = val

    def move(self):
        self._x -= self.velocity

    def draw_to_screen(self, screen):
        self._rect = screen.blit(self.image, (self._x, self._y))


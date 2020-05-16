from assets import sprites_dict


class Base:
    velocity = 10
    image = sprites_dict['base']

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._rect = None

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, val):
        self._x = val

    def move(self):
        pass

    def draw_to_screen(self, screen):
        image = self.image.convert_alpha()
        self._rect = screen.blit(image, (self._x, self._y))


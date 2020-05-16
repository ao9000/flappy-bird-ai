from assets import sprites_dict


class Base:
    velocity = 5
    image = sprites_dict['base']

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._rect = None

    def move(self):
        self._x -= self.velocity

        if self._x + self.image.get_width() <= 0:
            self._x = 288

    def draw_to_screen(self, screen):
        image = self.image.convert_alpha()
        self._rect = screen.blit(image, (self._x, self._y))


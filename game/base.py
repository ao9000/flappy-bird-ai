"""
    Flappy bird Base class.
    Responsible for creating the moving Base for the game.
"""


from assets import sprites_dict


class Base:
    """
    Base class
    Every instance of the game should have 2 Base class instances
    One rendered in the screen and another outside of the screen waiting to be rendered in once the first base moves out

    velocity controls the amount of pixels the base moves every tick
    image contains the loaded base pygame sprite object
    width and height contains the sprite width and height in pixels
    """
    velocity = 5
    image = sprites_dict['base']
    width, height = image.get_width(), image.get_height()

    def __init__(self, x, y):
        """
        Constructor for the Base class

        :param x: type: int
        x pixel coordinates of the Base on the screen
        Note: The coordinates refer to the top-left corner of the sprite

        :param y: type: int
        y pixel coordinates of the base on the screen
        Note: The coordinates refer to the top-left corner of the sprite
        """
        self._x = x
        self._y = y
        self._rect = None
        self.image = self.image.convert()

    # Getter & setter methods
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
        """
        Moves the base towards left of the pygame screen at the rate of velocity set
        """
        self._x -= self.velocity

    def draw_to_screen(self, screen):
        """
        Draws/renders the base to the pygame screen

        :param screen: type: pygame.surface
        The surface/screen of the game for displaying purposes
        """
        self._rect = screen.blit(self.image, (self._x, self._y))


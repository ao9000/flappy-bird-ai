import pygame
from game.color import color_to_rgb


class Textbox:
    def __init__(self, text_color, font_name, font_size, center_x=None, center_y=None):
        self._text_color = color_to_rgb(text_color)
        self._font_name = font_name
        self._font_size = font_size
        self._center_x = center_x
        self._center_y = center_y
        self._font = self.load_font()
        self._rect = None
        self._text = None

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, val):
        self._text = val

    @property
    def center_x(self):
        return self._center_x

    @center_x.setter
    def center_x(self, val):
        self._center_x = val

    @property
    def center_y(self):
        return self._center_y

    @center_y.setter
    def center_y(self, val):
        self._center_y = val

    def load_font(self):
        # Font handler
        # Check if custom font or system font
        if self._font_name not in pygame.font.get_fonts():
            # Load custom font from file
            font = pygame.font.Font("fonts/{}.ttf".format(self._font_name), self._font_size)
        else:
            # Load system font
            font = pygame.font.SysFont(self._font_name, self._font_size)

        return font

    def create_textbox(self):
        # Render text on new surface
        text = self.load_font().render(self._text, True, self._text_color)

        return text

    def draw_to_screen(self, screen):
        text = self.create_textbox()

        # Render surface to screen & define rect
        self._rect = screen.blit(text, (self._center_x - (text.get_width() // 2), self._center_y - (text.get_height() // 2)))
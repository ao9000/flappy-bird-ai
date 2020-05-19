from assets import sprites_dict
import pygame


class Bird:
    image = sprites_dict['yellowbird']
    width, height = image[0].get_width(), image[0].get_height()
    state_cycle_rate = 5
    max_tilt = 30
    min_tilt = -90

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._state = 0
        self._animation_tick = 0
        self._tilt_tick = 0
        self._tilt = 0
        self._velocity = 0
        self._rect = None

    def jump(self):
        self._velocity = 10

    def do_nothing(self):
        self._velocity -= 1

    def tilt_down(self):
        self._tilt_tick += 1

        if self._tilt_tick > 15:
            self._tilt -= 10
            self.tilt_handler()

    def tilt_up(self):
        self._tilt = 20
        self.tilt_handler()
        self._tilt_tick = 0

    def tilt_handler(self):
        if self._tilt > self.max_tilt:
            self._tilt = self.max_tilt
        elif self._tilt < self.min_tilt:
            self._tilt = self.min_tilt

    def calculate_new_y(self):
        # Terminal velocity
        if self._velocity > 16:
            self._velocity = 16

        self._y -= self._velocity

    def cycle_bird_state(self):
        self._state += 1
        if self._state > 2:
            self._state = 0

    def flap_animation_tick_handler(self):
        self._animation_tick += 1

        if self._animation_tick >= Bird.state_cycle_rate:
            self.cycle_bird_state()
            self._animation_tick = 0

    @staticmethod
    def tilt_bird(bird, angle):
        tilted_bird = pygame.transform.rotate(bird, angle)

        return tilted_bird

    def draw_to_screen(self, screen):
        image = [bird.convert_alpha() for bird in self.image]

        # Cycle flap animation states
        self.flap_animation_tick_handler()

        # Draw bird
        self._rect = screen.blit(self.tilt_bird(image[self._state], self._tilt), (self._x, self._y))

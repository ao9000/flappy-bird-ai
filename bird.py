from assets import sprites_dict
from config_handler import config
import pygame


class Bird:
    image = sprites_dict[config['Bird']['color']]
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
        self.image = [bird.convert_alpha() for bird in self.image]

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def rect(self):
        return self._rect

    def jump(self):
        # Set velocity for jumping
        self._velocity = 10.5
        self.calculate_new_y()

        # Set tilt for jump
        self.tilt_up()

    def do_nothing(self):
        # Decay velocity when not jumping
        self._velocity -= 1
        self.calculate_new_y()

        # Set tilt for not jumping
        self.tilt_down()

    def calculate_new_y(self):
        # Terminal velocity
        if self._velocity > 12:
            self._velocity = 12

        # Set new y
        self._y -= self._velocity

    def tilt_down(self):
        # Increment tick
        self._tilt_tick += 1

        # If tick pass threshold, tilt down
        if self._tilt_tick > 15:
            self._tilt -= 10
            self.tilt_handler()

    def tilt_up(self):
        # Tilt up
        self._tilt = 20
        self.tilt_handler()
        # Reset tick
        self._tilt_tick = 0

    def tilt_handler(self):
        # Make sure the tilt stays between min & max thresholds
        if self._tilt > self.max_tilt:
            self._tilt = self.max_tilt
        elif self._tilt < self.min_tilt:
            self._tilt = self.min_tilt

    def flap_animation_tick_handler(self):
        # Nose dive
        if self._tilt == -90:
            self._state = 1
        else:
            # Increment tick
            self._animation_tick += 1

            # Cycle animation if pass threshold tick
            if self._animation_tick >= Bird.state_cycle_rate:
                # Cycle animation
                self.cycle_bird_state()
                # Reset tick
                self._animation_tick = 0

    def cycle_bird_state(self):
        # Cycle bird animation
        self._state += 1

        # Set index back into loop
        if self._state > 2:
            self._state = 0

    @staticmethod
    def tilt_bird(bird, angle):
        tilted_bird = pygame.transform.rotate(bird, angle)

        return tilted_bird

    def get_mask(self):
        mask = pygame.mask.from_surface(self.tilt_bird(self.image[self._state], self._tilt))

        return mask

    def draw_to_screen(self, screen):
        # Cycle flap animation states
        self.flap_animation_tick_handler()

        # Draw bird
        self._rect = screen.blit(self.tilt_bird(self.image[self._state], self._tilt), (self._x, self._y))

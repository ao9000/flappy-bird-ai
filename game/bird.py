"""
    Flappy bird Bird class.
    Responsible for creating the human controllable bird for the game
"""


from assets import sprites_dict
from game.textbox import Textbox
import pygame


class Bird:
    """
    Bird class
    For every instance of the game, there should be 1 bird class instance
    The only exception is in the training script where multiple bird class instances are created to perform parallel
    training

    image contains the loaded bird pygame sprite object
    width and height contains the width and height of the sprite in pixels
    state_cycle_rate is the amount of ticks passed before switching a different flapping state
    max_tilt is the maximum angle of tilt allowed for the bird when it is flapping up (Calculated from normal state)
    min_tilt is the maximum angle of tilt allowed for the bird when it is nose diving down
    (Calculated from normal state)
    """
    image = sprites_dict['yellowbird']
    width, height = image[0].get_width(), image[0].get_height()
    state_cycle_rate = 5
    max_tilt = 30
    min_tilt = -90

    def __init__(self, x, y):
        """
        Constructor for Bird class

        :param x: type: int
        x pixel coordinates of the Bird on the screen
        Note: The coordinates refer to the top-left corner of the sprite

        :param y: type: int
        y pixel coordinates of the Bird on the screen
        Note: The coordinates refer to the top-left corner of the sprite
        """
        self._x = x
        self._y = y
        self._state = 0
        self._animation_tick = 0
        self._tilt_tick = 0
        self._tilt = 0
        self._velocity = 0
        self._rect = None
        self._label = Textbox("black", "arialbd", 16)
        self.image = [bird.convert_alpha() for bird in self.image]

    # Getter & setter methods
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
        """
        Simulates the jumping/flapping of the bird by increasing the velocity of the bird and tilting the bird
        """
        # Set velocity for jumping and calculates new y coordinates
        self._velocity = 10.5
        self.calculate_new_y()

        # Set tilt up angle for jump
        self.tilt_up()

    def do_nothing(self):
        """
        Simulates velocity and angle decay when the bird is not jumping/flapping
        """
        # Decay velocity when not jumping
        self._velocity -= 1
        self.calculate_new_y()

        # Decay tilt when not jumping
        self.tilt_down()

    def calculate_new_y(self):
        """
        Calculates and updates the new y coordinate based on the velocity and the current bird position
        """
        # Ensure velocity does not pass terminal velocity
        if self._velocity > 12:
            self._velocity = 12

        # Updates new y
        self._y -= self._velocity

    def tilt_down(self):
        """
        Increment the tilt_tick until passing a threshold to actually tilt the bird downwards. Then tilts the bird down
        incrementally until it reaches the min_tilt value.
        """
        # Increment tick to give immunity to tilt until reaching certain threshold
        self._tilt_tick += 1

        # If tick pass threshold, tilt down
        if self._tilt_tick > 15:
            self._tilt -= 10
            self.tilt_handler()

    def tilt_up(self):
        """
        Tilt the bird up a fixed angle. Multiple calls of this function can stack additively and
        resets the tilt_tick to provide tilt immunity to the bird
        """
        # Tilt up
        self._tilt = 20
        self.tilt_handler()

        # Reset tilt_tick to provide tilt immunity
        self._tilt_tick = 0

    def tilt_handler(self):
        """
        Ensures that the tilt angle does not pass between the min_tilt & max_tilt thresholds.
        If passed, set the tilt angle back to the min or max respectively
        """
        # Make sure the tilt stays between min & max thresholds
        if self._tilt > self.max_tilt:
            self._tilt = self.max_tilt
        elif self._tilt < self.min_tilt:
            self._tilt = self.min_tilt

    def flap_animation_tick_handler(self):
        """
        Sets the gliding animation state for when the bird is at a nose dive position tilt
        Otherwise, increment the animation_tick until it reaches a threshold. Once passing the threshold, cycle the
        bird state to simulate bird flapping animation
        """
        # If nose dive, set to non-flapping state
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
        """
        Cycles the bird animation state between 0 to 2
        """
        # Cycle bird animation
        self._state += 1

        # Set index back into loop
        if self._state > 2:
            self._state = 0

    @staticmethod
    def tilt_bird(image, angle):
        """
        Rotates the pygame sprite according to the provided angle and returns the rotated sprite.

        :param image: type: list
        List containing the loaded pygame bird state images

        :param angle: type: int
        Angle of tilt for the bird

        :return: type: pygame.Surface
        pygame sprite of the tilted bird
        """
        tilted_bird = pygame.transform.rotate(image, angle)

        return tilted_bird

    def get_mask(self):
        """
        Extracts the mask from the sprite to provide pixel based collision detection

        :return: type: pygame.mask.Mask
        The extracted mask object
        """
        mask = pygame.mask.from_surface(self.tilt_bird(self.image[self._state], self._tilt))

        return mask

    def draw_name_label(self, model_name, screen):
        """
        Draws/renders a textbox containing the bird model name above the bird
        Only used in the testing script

        :param model_name: type: str
        Model name of the bird being tested

        :param screen: type: pygame.surface
        The surface/screen of the game for displaying purposes
        """
        # Draw label of bird to screen
        # Set coordinates
        self._label.center_x = self._x + self.width/2
        self._label._center_y = self.y
        self._label.text = model_name[:-4]

        # Draw label above bird
        self._label.draw_to_screen(screen)

    def draw_to_screen(self, screen):
        """
        Draws/renders the bird to the pygame screen

        :param screen: type: pygame.surface
        The surface/screen of the game for displaying purposes
        """
        # Cycle flap animation states
        self.flap_animation_tick_handler()

        # Draw bird
        self._rect = screen.blit(self.tilt_bird(self.image[self._state], self._tilt), (self._x, self._y))

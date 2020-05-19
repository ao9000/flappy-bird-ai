from assets import sprites_dict


class Bird:
    image = sprites_dict['yellowbird']
    width, height = image[0].get_width(), image[0].get_height()
    state_cycle_rate = 5

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._state = 0
        self._animation_tick = 0
        self._tilt = 0
        self._velocity = 0
        self._rect = None

    def jump(self):
        self._velocity += 30

    def do_nothing(self):
        self._velocity -= 1

        if self._velocity > 16:
            self._velocity = 16

    def calculate_new_y(self):
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

    def draw_to_screen(self, screen):
        image = [bird.convert_alpha() for bird in self.image]

        # Bird velocity
        self.do_nothing()
        self.calculate_new_y()
        print(self._velocity)

        # Cycle flap animation states
        self.flap_animation_tick_handler()
        self._rect = screen.blit(image[self._state], (self._x, self._y))

# coding: utf-8

import rpicard.exception.errorcode as errorcode
from rpicard.exception.rpicardexp import RpiCarDExp
from rpicard.config.config import sys_config
from rpicard.cardriver.director.wheel import Wheel
from rpicard.cardriver.comm.gpiowrapper import gpio_wrapper

class Director(object):

    """
    A class controlling movement of the car
    """

    def __init__(self):
        self._initialized = False

    def _read_wheel_config(self, key):
        forward_pin = sys_config.get_int('Wheel', key + '_forward')
        backward_pin = sys_config.get_int('Wheel', key + '_backward')
        if forward_pin is None or backward_pin is None:
            raise RpiCarDExp(errorcode.CONFIG_NOT_FOUND,
                    '%s wheel pin config not found, forward: %s, backward: %s'
                        % (key, str(forward_pin), str(backward_pin)))
        return {'forward_pin': forward_pin, 'backward_pin': backward_pin}

    def init(self):
        """
        Read pins config from sys_config, then initialize the pins of four wheels.
        """
        if not self._initialized:
            self._front_left = Wheel(self._read_wheel_config('front_left'))
            self._front_right = Wheel(self._read_wheel_config('front_right'))
            self._back_left = Wheel(self._read_wheel_config('back_left'))
            self._back_right = Wheel(self._read_wheel_config('back_right'))
            
            # output initial level
            pins = []
            pins.extend(self._front_left.pins())
            pins.extend(self._front_right.pins())
            pins.extend(self._back_left.pins())
            pins.extend(self._back_right.pins())
            gpio_wrapper.output(pins)
            self._initialized = True

    def set_manually(self, front_left, front_right, back_left, back_right):
        """
        Set wheels of the car manually

        :front_left: 0: stop, 1: forward, 2:backward
        :front_right: 0: stop, 1: forward, 2:backward
        :back_left: 0: stop, 1: forward, 2:backward
        :back_right: 0: stop, 1: forward, 2:backward
        """
        pins = []
        # front left
        if front_left == 0:
            pins.extend(self._front_left.stop())
        elif front_left == 2:
            pins.extend(self._front_left.roll_backward())
        else:
            pins.extend(self._front_left.roll_forward())

        # front right
        if front_right == 0:
            pins.extend(self._front_right.stop())
        elif front_right == 2:
            pins.extend(self._front_right.roll_backward())
        else:
            pins.extend(self._front_right.roll_forward())

        # back left
        if back_left == 0:
            pins.extend(self._back_left.stop())
        elif back_left == 2:
            pins.extend(self._back_left.roll_backward())
        else:
            pins.extend(self._back_left.roll_forward())

        # back right
        if back_right == 0:
            pins.extend(self._back_right.stop())
        elif back_right == 2:
            pins.extend(self._back_right.roll_backward())
        else:
            pins.extend(self._back_right.roll_forward())

    def go_forward(self):
        """
        Make the car go forward.
        """
        pins = []
        pins.extend(self._front_left.roll_forward())
        pins.extend(self._front_right.roll_forward())
        pins.extend(self._back_left.roll_forward())
        pins.extend(self._back_right.roll_forward())
        gpio_wrapper.output(pins)

    def go_backward(self):
        """
        Make the car go backward.
        """
        pins = []
        pins.extend(self._front_left.roll_backward())
        pins.extend(self._front_right.roll_backward())
        pins.extend(self._back_left.roll_backward())
        pins.extend(self._back_right.roll_backward())
        gpio_wrapper.output(pins)

    def stop(self):
        """
        Make the car stop.
        """
        pins = []
        pins.extend(self._front_left.stop())
        pins.extend(self._front_right.stop())
        pins.extend(self._back_left.stop())
        pins.extend(self._back_right.stop())
        gpio_wrapper.output(pins)

    def turn_left(self, level):
        """
        Make the car turn left. level:
        1: stop front left wheel
        2: stop both left wheels, front and back
        3: make front left wheel roll backward
        4: make bot left wheels roll backward, front and back

        :level: how soon it turn
        """
        pins = []
        pins.extend(self._front_right.roll_forward())
        pins.extend(self._back_right.roll_forward())
        if (level == 1):
            pins.extend(self._front_left.stop())
            pins.extend(self._back_left.roll_forward())
        elif (level == 2):
            pins.extend(self._front_left.stop())
            pins.extend(self._back_left.stop())
        elif (level == 3):
            pins.extend(self._front_left.roll_backward())
            pins.extend(self._back_left.stop())
        elif (level == 4):
            pins.extend(self._front_left.roll_backward())
            pins.extend(self._back_left.roll_backward())
        else:
            raise RpiCarDExp(errorcode.PARAM_ERROR, "level should between 1 and 4.")

        gpio_wrapper.output(pins)

    def turn_right(self, level):
        """
        Make the car turn right. level:
        1: stop front right wheel
        2: stop both right wheels, front and back
        3: make front right wheel roll backward
        4: make bot right wheels roll backward, front and back

        :level: how soon it turn
        """
        pins = []
        pins.extend(self._front_left.roll_forward())
        pins.extend(self._back_left.roll_forward())
        if (level == 1):
            pins.extend(self._front_right.stop())
            pins.extend(self._back_right.roll_forward())
        elif (level == 2):
            pins.extend(self._front_right.stop())
            pins.extend(self._back_right.stop())
        elif (level == 3):
            pins.extend(self._front_right.roll_backward())
            pins.extend(self._back_right.stop())
        elif (level == 4):
            pins.extend(self._front_right.roll_backward())
            pins.extend(self._back_right.roll_backward())
        else:
            raise RpiCarDExp(errorcode.PARAM_ERROR, "level should between 1 and 4.")

        gpio_wrapper.output(pins)

    def turn_left_in_reverse(self, level):
        """
        Make the car turn left when it goes backward. level:
        1: stop back left wheel
        2: stop both left wheels, front and back
        3: make back left wheel roll forward
        4: make bot left wheels roll forward, front and back

        :level: how soon it turn
        """
        pins = []
        pins.extend(self._front_right.roll_backward())
        pins.extend(self._back_right.roll_backward())
        if (level == 1):
            pins.extend(self._back_left.stop())
            pins.extend(self._front_left.roll_backward())
        elif (level == 2):
            pins.extend(self._back_left.stop())
            pins.extend(self._front_left.stop())
        elif (level == 3):
            pins.extend(self._back_left.roll_forward())
            pins.extend(self._front_left.stop())
        elif (level == 4):
            pins.extend(self._back_left.roll_forward())
            pins.extend(self._front_left.roll_forward())
        else:
            raise RpiCarDExp(errorcode.PARAM_ERROR, "level should between 1 and 4.")

        gpio_wrapper.output(pins)

    def turn_right_in_reverse(self, level):
        """
        Make the car turn right when it goes backward. level:
        1: stop back right wheel
        2: stop both right wheels, front and back
        3: make back right wheel roll forward
        4: make bot right wheels roll forward, front and back

        :level: how soon it turn
        """
        pins = []
        pins.extend(self._front_left.roll_backward())
        pins.extend(self._back_left.roll_backward())
        if (level == 1):
            pins.extend(self._back_right.stop())
            pins.extend(self._front_right.roll_backward())
        elif (level == 2):
            pins.extend(self._back_right.stop())
            pins.extend(self._front_right.stop())
        elif (level == 3):
            pins.extend(self._back_right.roll_forward())
            pins.extend(self._front_right.stop())
        elif (level == 4):
            pins.extend(self._back_right.roll_forward())
            pins.extend(self._front_right.roll_forward())
        else:
            raise RpiCarDExp(errorcode.PARAM_ERROR, "level should between 1 and 4.")

        gpio_wrapper.output(pins)

director = Director()

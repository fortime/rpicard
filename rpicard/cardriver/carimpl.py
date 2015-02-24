# coding: utf-8

from rpicard.cardriver.director.director import director
from rpicard.facade.carfacade import CarFacade

class CarImpl(CarFacade):

    """
    Implementation of CarFacade.
    """

    def __init__(self):
        CarFacade.__init__(self)

        # initialize director
        director.init()

    def set_manually(self, front_left, front_right, back_left, back_right):
        """
        Set wheels of the car manually

        :front_left: 0: stop, 1: forward, 2:backward
        :front_right: 0: stop, 1: forward, 2:backward
        :back_left: 0: stop, 1: forward, 2:backward
        :back_right: 0: stop, 1: forward, 2:backward
        """
        director.set_manually(front_left, front_right, back_left, back_right)

    def go_forward(self):
        """
        Make the car go forward.
        """
        director.go_forward()

    def go_backward(self):
        """
        Make the car go backward.
        """
        director.go_backward()

    def stop(self):
        """
        Make the car stop.
        """
        director.stop()

    def turn_left(self, level):
        """
        Make the car turn left. level:
        1: stop front left wheel
        2: stop both left wheels, front and back
        3: make front left wheel roll backward
        4: make bot left wheels roll backward, front and back

        :level: how soon it turn
        """
        director.turn_left(level)

    def turn_right(self, level):
        """
        Make the car turn right. level:
        1: stop front right wheel
        2: stop both right wheels, front and back
        3: make front right wheel roll backward
        4: make bot right wheels roll backward, front and back

        :level: how soon it turn
        """
        director.turn_right(level)

    def turn_left_in_reverse(self, level):
        """
        Make the car turn left when it goes backward. level:
        1: stop back left wheel
        2: stop both left wheels, front and back
        3: make back left wheel roll backward
        4: make bot left wheels roll backward, front and back

        :level: how soon it turn
        """
        director.turn_left_in_reverse(level)

    def turn_right_in_reverse(self, level):
        """
        Make the car turn right when it goes backward. level:
        1: stop back right wheel
        2: stop both right wheels, front and back
        3: make back right wheel roll backward
        4: make bot right wheels roll backward, front and back

        :level: how soon it turn
        """
        director.turn_right_in_reverse(level)

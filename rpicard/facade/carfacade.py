# coding: utf-8

class CarFacade(object):

    """
    A facade of car.
    """

    def __init__(self):
        pass

    def set_manually(self, front_left, front_right, back_left, back_right):
        """
        Set wheels of the car manually

        :front_left: 0: stop, 1: forward, 2:backward
        :front_right: 0: stop, 1: forward, 2:backward
        :back_left: 0: stop, 1: forward, 2:backward
        :back_right: 0: stop, 1: forward, 2:backward
        """
        pass

    def go_forward(self):
        """
        Make the car go forward.
        """
        pass

    def go_backward(self):
        """
        Make the car go backward.
        """
        pass

    def stop(self):
        """
        Make the car stop.
        """
        pass

    def turn_left(self, level):
        """
        Make the car turn left. level:
        1: stop front left wheel
        2: stop both left wheels, front and back
        3: make front left wheel roll backward
        4: make bot left wheels roll backward, front and back

        :level: how soon it turn
        """
        pass

    def turn_right(self, level):
        """
        Make the car turn right. level:
        1: stop front right wheel
        2: stop both right wheels, front and back
        3: make front right wheel roll backward
        4: make bot right wheels roll backward, front and back

        :level: how soon it turn
        """
        pass

    def turn_left_in_reverse(self, level):
        """
        Make the car turn left when it goes backward. level:
        1: stop back left wheel
        2: stop both left wheels, front and back
        3: make back left wheel roll backward
        4: make bot left wheels roll backward, front and back

        :level: how soon it turn
        """
        pass

    def turn_right_in_reverse(self, level):
        """
        Make the car turn right when it goes backward. level:
        1: stop back right wheel
        2: stop both right wheels, front and back
        3: make back right wheel roll backward
        4: make bot right wheels roll backward, front and back

        :level: how soon it turn
        """
        pass

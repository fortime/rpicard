# coding: utf-8

import RPi.GPIO as GPIO

class Wheel(object):

    """
    Wheel properties:
    1. forward: pin, level, last_level
    2. backward: pin, level, last_level
    pin is in GPIO.BOARD mode  
    """

    def __init__(self, forward_pin, backward_pin):
        """
        init pins for forward and backward

        :forward_pin: wheel will roll forward, when output of the pin is high\
        and of the backward_pin is low
        :backward_pin: wheel will roll backward, when output of the pin is high\
        and of the forward_pin is low
        """
        self._forward = [forward_pin, GPIO.LOW, GPIO.HIGH]
        self._backward = [backward_pin, GPIO.LOW, GPIO.HIGH]

    def roll_forward(self):
        """
        set forward with GPIO.HIGH, and backward with GPIO.LOW
        :returns: pins properties
        """
        self._forward[2] = self._forward[1]
        self._forward[1] = GPIO.HIGH
        self._backward[2] = self._backward[1]
        self._backward[1] = GPIO.LOW
        return [tuple(self._forward), tuple(self._backward)]

    def roll_backward(self):
        """
        set backward with GPIO.HIGH, and backward with GPIO.LOW
        :returns: pins properties
        """
        self._forward[2] = self._forward[1]
        self._forward[1] = GPIO.LOW
        self._backward[2] = self._backward[1]
        self._backward[1] = GPIO.HIGH
        return [tuple(self._forward), tuple(self._backward)]

    def stop(self):
        """
        set forward and backward with GPIO.LOW
        :returns: pins properties
        """
        self._forward[2] = self._forward[1]
        self._forward[1] = GPIO.LOW
        self._backward[2] = self._backward[1]
        self._backward[1] = GPIO.LOW
        return [tuple(self._forward), tuple(self._backward)]
        
    def pins(self):
        """
        return pins properties
        :returns: pins properties
        """
        return [tuple(self._forward), tuple(self._backward)]

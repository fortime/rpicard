# coding: utf-8

import RPi.GPIO as GPIO

class GpioWrapper(object):

    """
    A wrapper for gpio
    """
    _out_pins = []
    _in_pins = []

    def __init__(self):
        """
        """
        GPIO.setmode(GPIO.BOARD);

    def output(self, pins):
        """
        Set output of pins.

        :pins: [(pin_no, level, last_level), ...]

        """
        for pin in pins:
            self._output(pin)

    def _output(self, pin):
        """
        Set output of pin.

        :pin: (pin_no, level, last_level)

        """
        pin_no, level, last_level = pin
        # remove pin_no from _in_pins
        if pin_no in GpioWrapper._in_pins:
            GpioWrapper._in_pins.remove(pin_no)
        # set out mode
        if pin_no not in GpioWrapper._out_pins:
            GPIO.setmode(pin_no, GPIO.OUT)
            GpioWrapper._out_pins.append(pin_no)
        if level != last_level:
            GPIO.output(pin_no, level)

gpio_wrapper = GpioWrapper()

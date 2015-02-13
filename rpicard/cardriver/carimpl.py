# coding: utf-8

from rpicard.facade.carfacade import CarFacade

class CarImpl(CarFacade):

    """
    Implementation of CarFacade.
    """

    test_v = 0

    def __init__(self):
        CarFacade.__init__(self)

    def turn_left(self, abc):
        """
        Make the car turn left.

        :abc: sth
        :returns: sth

        """
        CarImpl.test_v += 1
        import os
        return [{'1': abc, '2': 2, 'test_v': CarImpl.test_v}, '123', (21421, 42134), os.path.dirname(os.path.realpath(__file__))]

        

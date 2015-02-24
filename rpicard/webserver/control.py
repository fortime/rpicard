# coding: utf-8

import json
import logging
import traceback
import web
import rpicard.exception.errorcode as errorcode
from rpicard.exception.rpicardexp import RpiCarDExp
from rpicard.facade.carfacade import CarFacade
from rpicard.rpc.rpcproxy import RpcProxy

logger = logging.getLogger(__name__)

class Control(object):

    """
    Web entrance to control the car.
    """

    card = RpcProxy(CarFacade)

    def __init__(self):
        pass

    def _check_param(self):
        """
        Checking parameters.

        :returns: checked parameters
        """
        param = web.input()
        if not param.has_key('rl'):
            raise RpiCarDExp(errorcode.PARAM_NOT_EXISTS, 'rd does not exist.')
        if not param.has_key('md'):
            raise RpiCarDExp(errorcode.PARAM_NOT_EXISTS, 'rd does not exist.')
        rl, md = None, None
        try:
            rl = int(param.rl)
            md = int(param.md)
        except:
            raise RpiCarDExp(errorcode.PARAM_ERROR,\
                    'param invalid, rl=%s, md=%s.' % (param.rl, param.md))

        return (rl, md)

    def _control(self, rl, md):
        """
        Control the car.

        :rl: level of rotation
        :md: moving direction
        """
        if md == 0:
            Control.card.stop()
        elif md == 1:
            if rl == 0:
                Control.card.go_forward()
            elif rl > 0:
                Control.card.turn_right(rl)
            else:
                Control.card.turn_left(0 - rl)
        elif md == 2:
            if rl == 0:
                Control.card.go_backward()
            elif rl > 0:
                Control.card.turn_right_in_reverse(rl)
            else:
                Control.card.turn_left_in_reverse(0 - rl)
        else:
            raise RpiCarDExp(errorcode.PARAM_ERROR, 'md`%d` is invalid' % md)

    def GET(self):
        """
        Entrance.
        :returns: handled result in json
        """
        result = None
        try:
            rotation_level, moving_direction\
                    = self._check_param()
            self._control(rotation_level, moving_direction)
            result = {'retcode': '0', 'retmsg': 'OK'}
        except RpiCarDExp as exp:
            result = {'retcode': exp.retcode(), 'retmsg': exp.retmsg()}
        except:
            logger.warn(traceback.format_exc())
            result = {'retcode': errorcode.UNKNOWN_ERROR, 'retmsg': 'UNKNOWN ERROR'}

        web.header('Content-Type', 'application/json')
        return json.dumps(result)

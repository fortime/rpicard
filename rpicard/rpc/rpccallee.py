# coding: utf-8

import logging
import pickle
import traceback
import sys
import rpicard.exception.errorcode as errorcode
from rpicard.exception.rpicardexp import RpiCarDExp
from rpicard.config.config import Config
from rpicard.config.config import sys_config

logger = logging.getLogger(__name__)

class RpcCallee(object):

    """
    A class impletements the server part of rpc.
    """

    # rpc config
    _rpc_callee_config = None

    def invoke(self, req_data):
        """
        Invoke _internal_invoke to deal with req_data, and catch exceptions.

        :req_data: request data from client side
        :returns: retcode, retmsg and the true return of the local method

        """
        retobj = None
        retcode = '0'
        retmsg = 'OK'
        try:
            retobj = self._internal_invoke(req_data)
        except RpiCarDExp as ex:
            retmsg = RpiCarDExp.retmsg()
            retcode = RpiCarDExp.retcode()
            logger.info(traceback.format_exc())
        except BaseException as base_ex:
            retcode = errorcode.SYSTEM_ERROR
            retmsg = str(base_ex)
            logger.info(traceback.format_exc())
        except:
            retcode = errorcode.UNKNOWN_ERROR
            retmsg = 'Unknown Exception'
            logger.warn(traceback.format_exc())

        return self._to_res_data(retcode, retmsg, retobj)

    def _internal_invoke(self, req_data):
        """
        Invoke the local method according to req_data

        :req_data: request data from client side
        :returns: the true return of the local method

        """
        # read rpc callee config
        if RpcCallee._rpc_callee_config is None:
            file_path = sys_config.get('Rpc', 'callee_config')
            if file_path is None:
                raise RpiCarDExp(errorcode.CONFIG_NOT_FOUND, 'No rpc callee config')
            RpcCallee._rpc_callee_config = Config()
            RpcCallee._rpc_callee_config.read_config(file_path)

        req_obj = pickle.loads(req_data)
        method = self._reflect_method(req_obj)
        return method(*req_obj['args'], **req_obj['kwargs'])

    def _reflect_method(self, req_obj):
        """
        Find the module and class of the method, and return a callable method.

        :req_obj: request data obj
        :returns: a callable method

        """
        module_from_client= req_obj['module']
        clazz_from_client = req_obj['clazz']
        name_from_client = req_obj['name'] 

        section = ".".join((module_from_client, clazz_from_client))
        module = RpcCallee._rpc_callee_config.get(section, 'module')
        clazz = RpcCallee._rpc_callee_config.get(section, 'clazz')

        __import__(module)
        module_obj = sys.modules[module]
        clazz_obj = getattr(module_obj, clazz)
        target_obj = clazz_obj()
        return getattr(target_obj, name_from_client)


    def _to_res_data(self, retcode, retmsg, retobj):
        """
        Generate response data

        :retcode: retcode
        :retmsg: retmsg
        :retobj: retobj

        """
        res = {}
        res['retcode'] = retcode
        res['retmsg'] = retmsg
        res['retobj'] = retobj
        return pickle.dumps(res)

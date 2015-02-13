# coding: utf-8

import logging
import pickle
import traceback
import urllib2
import rpicard.exception.errorcode as errorcode
from rpicard.exception.rpicardexp import RpiCarDExp
from rpicard.config.config import Config
from rpicard.config.config import sys_config

logger = logging.getLogger(__name__)

class RpcCaller(object):

    """
    A class impletements the client part of rpc, using HTTP to invoke the 
    function in the server.
    """

    def __init__(self, metadata, url, conn_timeout=500, read_timeout=1000):
        """
        Set metadata of caller.

        :metadata: a string tuple of module name, class name, caller name
        :url: url for rpc
        :conn_timeout: timeout(millisecond) for connection
        :read_timeout: timeout(millisecond) for reading

        """
        self._module, self._clazz, self._name = metadata
        self._url = url

        if isinstance(conn_timeout, int):
            self._conn_timeout = conn_timeout
        else:
            self._conn_timeout = 500

        if isinstance(read_timeout, int):
            self._read_timeout = read_timeout
        else:
            self._read_timeout = 1000

    def __call__(self, *args, **kwargs):
        """
        Call throught HTTP

        :args: argument name list
        :kwargs: dict of arguments

        """
        #urllib2.Request
        req_data = self._to_req_data(*args, **kwargs)
        req = urllib2.Request(url = self._url, data = req_data, headers = {'Content-Type': 'application/octet-stream; charset=utf-8'})
        res = urllib2.urlopen(req, timeout=self._read_timeout)
        res_data = res.read()
        res_obj = pickle.loads(res_data)
        
        retcode = res_obj.get('retcode')
        retmsg = res_obj.get('retmsg')
        if retcode is None or retmsg is None:
            raise RpiCarDExp(errorcode.RPC_UNKNOWN_RETURN, 'Unknown error, retcode: %s, retmsg: %s' % (retcode, retmsg))
        elif retcode != '0':
            raise RpiCarDExp(retcode, retmsg)
        return res_obj.get('retobj')

    def _to_req_data(self, *args, **kwargs):
        """
        Generate request data

        :args: argument name list
        :kwargs: dict of arguments

        """
        req = {}
        req['module'] = self._module
        req['clazz'] = self._clazz
        req['name'] = self._name
        req['args'] = args
        req['kwargs'] = kwargs
        return pickle.dumps(req)

    def set_conn_timeout(self, conn_timeout):
        """
        Set connection timeout.

        :conn_timeout: timeout in millisecond

        """
        if isinstance(conn_timeout, int):
            self._conn_timeout = conn_timeout

    def set_read_timeout(self, read_timeout):
        """
        Set read timeout.

        :read_timeout: timeout in millisecond

        """
        if isinstance(read_timeout, int):
            self._read_timeout = read_timeout

class RpcProxy(object):

    """
    A rpc proxy return a proxy of a object, making a call 
    of method becoming a rpc call.
    """

    # cache of callers
    _rpc_callers = {}

    # rpc config
    _rpc_caller_config = None

    def __init__(self, obj):
        """
        Set the obj.

        :obj: the obj to be proxied
        """
        self._obj = obj
        
    def __getattr__(self, name):
        """
        Return the proxied method 

        :name: the name of method to be called
        :returns: proxied method

        """
        # read rpc caller config
        if RpcProxy._rpc_caller_config is None:
            file_path = sys_config.get('Rpc', 'caller_config')
            if file_path is None:
                raise RpiCarDExp(errorcode.CONFIG_NOT_FOUND, 'No rpc caller config')
            RpcProxy._rpc_caller_config = Config()
            RpcProxy._rpc_caller_config.read_config(file_path)

        metadata = (self._obj.__module__, self._obj.__class__.__name__, name)
        key = '.'.join(metadata)
        caller = RpcProxy._rpc_callers.get(key)
        if caller is None:
            rpc_url = RpcProxy._rpc_caller_config.get('.'.join(metadata[0:2]), 'url')
            conn_timeout = RpcProxy._rpc_caller_config.get_int('.'.join(metadata[0:2]), 'conn_timeout')
            read_timeout = RpcProxy._rpc_caller_config.get_int('.'.join(metadata[0:2]), 'read_timeout')
            caller = RpcCaller(metadata, rpc_url, conn_timeout, read_timeout)
            RpcProxy._rpc_callers[key] = caller
        return caller

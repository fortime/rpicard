# coding: utf-8

import sys
import os

if __name__ == "__main__":
    os.chdir('..')
    sys.path = sys.path[1:]
    sys.path.insert(0, os.getcwd())

import web
from rpicard import logutil
from rpicard.facade.carfacade import CarFacade
from rpicard.config.config import sys_config
from rpicard.rpc.rpcproxy import RpcProxy

urls = (
    '/', 'rpicard.webserver.resource.Index',
    '/resource', 'rpicard.webserver.resource.Resource',
    '/control', 'rpicard.webserver.control.Control'
    )

def start_server(argv):
    sys_config.read_config('etc/rpicard.conf')
    logutil.init_log()
    web.webapi.debug = logutil.CustomWsgiLog()
    if __name__ == "__main__":
        tmp = globals().copy()  
        tmp['__name__'] = 'rpicard.webrpicard'
        app = web.application(urls, tmp)
    else:
        app = web.application(urls, globals())
    app.run(logutil.CustomWsgiLog)

if __name__ == "__main__":
    start_server(sys.argv)

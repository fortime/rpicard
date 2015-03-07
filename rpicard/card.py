# coding: utf-8

import sys
import os

if __name__ == "__main__":
    # change working path
    os.chdir('..')
    sys.path = sys.path[1:]
    sys.path.insert(0, os.getcwd())

import web
import logging
from rpicard import logutil
from rpicard.config.config import sys_config
from rpicard.rpc.rpccallee import RpcCallee

class Rpc:
    def POST(self):
        return RpcCallee().invoke(web.data())

    def GET(self):
        raise web.notfound()

urls = (
    '/rpc', 'Rpc'
    )

def start_server(argv):
    sys_config.read_config('etc/card.conf')
    logutil.init_log()
    web.webapi.debug = logutil.CustomWsgiLog()
    if __name__ == "__main__":
        tmp = globals().copy()  
        tmp['__name__'] = 'rpicard.card'
        app = web.application(urls, tmp)
    else:
        app = web.application(urls, globals())
    app.run(logutil.CustomWsgiLog)

if __name__ == "__main__":
    start_server(sys.argv)

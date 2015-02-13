# coding: utf-8

import sys
import os

if __name__ == "__main__":
    os.chdir('..')
    sys.path = sys.path[1:]
    sys.path.insert(0, os.getcwd())

from rpicard import logutil
from rpicard.facade.carfacade import CarFacade
from rpicard.config.config import sys_config
from rpicard.rpc.rpcproxy import RpcProxy

def start_server(argv):
    sys_config.read_config('etc/rpicard.conf')
    logutil.init_log()
    car = RpcProxy(CarFacade())
    print car.turn_left(argv[1])

if __name__ == "__main__":
    start_server(sys.argv)

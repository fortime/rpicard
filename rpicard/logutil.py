# coding: utf-8

import logging
import logging.config
import sys
from rpicard.config.config import sys_config

def init_log():
    log_config=sys_config.get('Log', 'log_config')
    logging.config.fileConfig(log_config, disable_existing_loggers=False)

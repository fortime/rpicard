# coding: utf-8

import logging
import logging.config
import sys
from logging.handlers import RotatingFileHandler
from rpicard.config.config import sys_config

class CustomRotatingFileHandler(RotatingFileHandler):
    def __init__(self, filename, mode='a', maxBytes=0, backupCount=0, encoding=None, delay=0):
        RotatingFileHandler.__init__(self, filename, mode, maxBytes, backupCount, encoding, delay)

    def _open(self):
        import os
        dirname = os.path.dirname(self.baseFilename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
            os.chmod(dirname, 0777)
        return RotatingFileHandler._open(self)

class CustomWsgiLog(object):

  logger = logging.getLogger("WSGI")

  def __init__(self, app=None):
    self._app = app
    self._msg = ''
    
  def __call__(self, environ, start_response):
    
    def new_start_response(status, response_headers, *args):
      has_key = False
      if environ.has_key('wsgi.errors'):
        old_value = environ['wsgi.errors']
        has_key = True
      # redirect web access log
      environ['wsgi.errors'] = self
      res = start_response(status, response_headers, *args)
      if has_key:
        environ['wsgi.errors'] = old_value
      else:
        environ.pop('wsgi.errors')
      return res
    
    return self._app(environ, new_start_response)
  
  def write(self, *args):
    msg = ''.join(args)
    if msg == '\n':
      CustomWsgiLog.logger.info(self._msg)
      self._msg = ''
    else:
      self._msg += msg

def init_log():
    log_config=sys_config.get('Log', 'log_config')
    logging.config.fileConfig(log_config, disable_existing_loggers=False)


# coding:utf-8

import web
import logging
import traceback
import rpicard
import os
import rpicard.exception.errorcode as errorcode
from rpicard.exception.rpicardexp import RpiCarDExp

logger = logging.getLogger(__name__)

class Index:
    def GET(self):
        raise web.seeother('/resource?t=1&path=index')

class Resource:

    base_path = None

    def _get_full_path(self, second, path):
        """
        Get full path of resource.

        :second: second part of the path
        :path: relative file path without suffix
        :returns: full path
        """
        if Resource.base_path == None:
            Resource.base_path = os.path.normpath(path)
        full_path =  os.path.join(os.path.dirname(rpicard.__file__), 'static', second, path)
        if full_path != os.path.abspath(full_path):
            raise RpiCarDExp(errorcode.PARAM_ERROR, "path '%s' is invalid" % path)
        return ".".join((full_path, second))

    def _get_html(self, path):
        """
        Get the html resource.

        :path: relative file path without suffix
        :returns: file content
        """
        full_path = self._get_full_path('html', path)
        web.header('Content-Type', 'text/html')
        return open(full_path).read()

    def _get_js(self, path):
        """
        Get the js resource.

        :path: relative file path without suffix
        :returns: file content
        """
        full_path = self._get_full_path('js', path)
        web.header('Content-Type', 'application/x-javascript')
        return open(full_path).read()

    def _get_css(self, path):
        """
        Get the css resource.

        :path: relative file path without suffix
        :returns: file content
        """
        full_path = self._get_full_path('css', path)
        web.header('Content-Type', 'text/css')
        return open(full_path).read()

    def GET(self):
        """
        Get the resource specified by path and t

        :returns: file content
        """
        # :t: file type: 1.html, 2.js, 3.css
        content = None
        try:
            path = web.input().path
            t = web.input().t
            # check path, t

            if t == '1':
                content = self._get_html(path)
            elif t == '2':
                content = self._get_js(path)
            elif t == '3':
                content = self._get_css(path)
        except RpiCarDExp as exp:
            logger.warn("Get file in '%s' of type '%s' failed, retcode: %s, retmsg: %s." % (path, t, exp.retcode(), exp.retmsg()))
        except:
            logger.warn(traceback.format_exc())

        if content == None:
            raise web.notfound()
        return content

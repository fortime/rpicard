# coding: utf-8

class RpiCarDExp(Exception):

    """
    An exception used for this project.
    """

    def __init__(self, retcode, retmsg):
        """
        Init.

        :retcode: retcode
        :retmsg: retmsg
        """
        Exception.__init__(self)
        self._retcode = retcode
        self._retmsg = retmsg

    def retcode(self):
        """
        return retcode.

        :returns: retcode

        """
        return self._retcode

    def retmsg(self):
        """
        return retmsg.

        :returns: retmsg

        """
        return self._retmsg

    def __str__(self):
        return self._retmsg

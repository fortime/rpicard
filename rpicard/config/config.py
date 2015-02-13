# coding: utf-8

from ConfigParser import SafeConfigParser

class Config(object):

    """
    A class for reading config.
    """

    def __init__(self):
        """
        """
        pass

    def read_config(self, file_path):
        """
        Read config from file

        :file_path: TODO
        :returns: TODO

        """
        self._config = SafeConfigParser()
        self._config.read(file_path)

    def get(self, section, key):
        """
        Get the value of key in section. None will be return 
        if value is not found.

        :section: section
        :key: key
        :returns: value or None

        """
        try:
            return self._config.get(section, key)
        except:
            return None

    def get_int(self, section, key):
        """
        Get the value in int of key in section. None will be return
        if value is not found or not int.

        :section: section
        :key: key
        :returns: value in int or None

        """
        try:
            return self._config.getint(section, key)
        except:
            return None

sys_config = Config()

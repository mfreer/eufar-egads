__author__ = "mfreer"
__date__ = "$Date:: 2011-02-22 16:13#$"
__version__ = "$Revision:: 45        $"
__all__ = ["FileCore", "get_file_list"]

import glob

class FileCore(object):
    """
    Abstract class which holds basic file access methods and attributes.
    Designed to be subclassed by NetCDF, NASA Ames and basic text file
    classes.

    **Constructor Variables**
    
    :param string filename: Optional -
        Name of file to open.
    :param char perms: Optional -
        Permissions used to open file. Options are ``w`` for write (overwrites data in file),
        ``a`` and ``r+`` for append, and ``r`` for read. ``r`` is the default value

    """

    def __init__(self, filename=None, perms='r', **kwargs):
        """
        Initializes file instance.

        :param string filename: Optional -
            Name of file to open.
        :param char perms: Optional -
            Permissions used to open file. Options are ``w`` for write (overwrites data in file),
            ``a`` and ``r+`` for append, and ``r`` for read. ``r`` is the default value
        """

        self.f = None
        self.filename = filename
        self.perms = perms

        for key, val in kwargs.iteritems():
            setattr(self, key, val)

        if filename is not None:
            self._open_file(filename, perms)

    def open(self, filename, perms=None):
        """
        Opens file given filename.

        :param string filename:
            Name of file to open.
        :param char perms: Optional -
            Permissions used to open file. Options are ``w`` for write (overwrites data in file),
            ``a`` and ``r+`` for append, and ``r`` for read. ``r`` is the default value
        """

        if perms is not None:
            self.perms = perms
        else:
            perms = self.perms


        self._open_file(filename, perms)

    def close(self):
        """
        Close opened file.
        """

        if self.f is not None:
            self.f.close()
            self.f = None
            self.filename = None



def get_file_list(path):
    """

    Given path, returns a list of all files in that path. Wildcards are supported.

    Example::
    
        file_list = get_file_list('data/*.nc')
    """

    return glob.glob(path)

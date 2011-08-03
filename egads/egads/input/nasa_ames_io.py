__author__ = "mfreer"
__date__ = "$Date:: 2010-10-19 19:10#$"
__version__ = "$Revision:: 38        $"
__all__ = ["EgadsNetCdf"]


import numpy
import nappy

class NasaAmes(object):
    """
    EGADS module for interfacing with NASA Ames files.

    This module adapts the NAPpy library to the file access methods used
    in EGADS
    """

    def __init__(self, filename=None, perms='r'):
        """
        Initializes instance of NasaAmes object

        Parameters
        ----------
        filename : string, optional
            Name of file to open.
        perms : char, optional
            Permissions used to open file. Options are 'w' for write (overwrites
            data), 'a' for append 'r+' for read and write, and 'r' for read. 'r'
            is the default value.
        """


__author__ = "mfreer"
__date__ = "$Date::                  $"
__revision__ = "$Revision::           $"
__version__ = "unknown"
try: 
    from _version import __version__
except ImportError:
    # No _version.py in tree, so we dont know what the version is
    pass

# TODO Add docstrings to file

# from tests import test_all


import core
import core.metadata
import algorithms
import input

from core.egads_core import *

from tests.test_all import test

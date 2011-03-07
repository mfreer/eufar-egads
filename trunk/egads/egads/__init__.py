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


from core.egads_core import *
import algorithms
import input
from tests.test_all import test

""" :TODO: Fill in docstring

"""

__author__ = "Matt Freer"
__date__ = "$Date: 2009-10-13 14:51:27 +0200 (Tue, 13 Oct 2009) $"
__version__ = "$Revision: 15 $"

import types

class ToolboxData(object):
    """The purpose of this class is to hold data and metadata, and provide methods
    to read data and metadata from various file formats.

    """

    def __init__(self, value=None, units=None, long_name=None, standard_name=None,
                name=None, fill_value=None, valid_range=None, sampled_rate=None,
                category=None, calibration_coeff=None, dependencies=None,
                processor=None):
        """Initialize Toolbox class"""
        self.value = value
        self.units = units
        self.long_name = long_name
        self.standard_name = standard_name
        self.name = name
        self.fill_value = fill_value
        self.valid_range = valid_range
        self.sampled_rate = sampled_rate
        self.category = category
        self.calibration_coeff = calibration_coeff
        self.dependencies = dependencies
        self.processor = processor


        self._user_attrubute_dict = {}


    def print_data(self):
        """ Print out data and metadata contained in ToolboxData object."""
        print self.value, self.units

    def unit_check(self, desired_units):
        """To be added: will be used to check that the variable is in
        desired units and convert if necessary."""
        # TODO add unit checking
        pass

    def attach_method(self, function, myclass):
        f = types.MethodType(function, self, myclass)
        exec('self.' + function.__name__ + ' = f')

    def __len__(self):
        return self.value.shape

    def __repr__(self):
        pass




class ToolboxProcessor(object):
    """ Defines the basic structure for setting up a toolbox for processing
    aircraft data.

    """

    def __init__(self):
        pass

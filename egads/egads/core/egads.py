""" :TODO: Fill in docstring

"""

__author__ = "mfreer"
__date__ = "$Date$"
__version__ = "$Revision$"

import types

class ToolboxData(object):
    """
    This class is designed around the EUFAR N6Sp recommendations
    for data and metadata. It allows a set of data and metadata to be shared
    in the Python environment in a consistent manner.

    """

    def __init__(self, value=None, units=None, long_name=None, standard_name=None,
                name=None, fill_value=None, valid_range=None, sampled_rate=None,
                category=None, calibration_coeff=None, dependencies=None,
                processor=None, **attrs):
        """
        Initializes instance with standard and user-provided attributes. If
        no attributes are provided, all standard attributes are set to None.

        """
        self.value = value
        self.units = units
        self.long_name = long_name
        self.standard_name = standard_name
        self.cdf_name = name
        self.fill_value = fill_value
        self.valid_range = valid_range
        self.sampled_rate = sampled_rate
        self.category = category
        self.calibration_coeff = calibration_coeff
        self.dependencies = dependencies
        self.processor = processor

        for key, val in attrs:
            setattr(self, key, val)
        
        self._user_attrubute_dict = {}

    def get_description(self):
        """
        Generate and return a description of the current data instance.

        """


        outstr = ('Current variable is %i with units of %s. \n' % (self.value.shape, self.units) +
                'Its descriptive name is: %s, and its CF name is: %s\n ' % (self.long_name, self.standard_name))

        return outstr


    def get_units(self):
        """
        Return the units used in the current instance.

        """
        return self.units

    def set_units(self, units):
        """
        Sets units for current instance.

        """
        self.units = units

    def print_data(self):
        """
        Print out data and metadata contained in ToolboxData object.

        """
        print self.value, self.units

    def unit_check(self, desired_units):
        """
        To be added: will be used to check that the variable is in
        desired units and convert if necessary.

        """
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

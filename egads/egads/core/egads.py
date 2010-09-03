__author__ = "mfreer"
__date__ = "$Date$"
__version__ = "$Revision$"

import types

class EgadsData(object):
    """
    This class is designed using the EUFAR N6SP data and metadata recommendations.
    Its purpose is to allow related data and metadata to be passed between
    functions and algorithms in a consistent, linked manner.
    """

    def __init__(self, value=None, units=None, long_name=None, standard_name=None,
                 cdf_name=None, fill_value=None, valid_range=None, sampled_rate=None,
                 category=None, calibration_coeff=None, dependencies=None,
                 processor=None, ** attrs):
        """
        Initializes EgadsData instance with standard attributes. If no attributes
        are provided, all standard attributes are set to None.

        Parameters
        -----------
        value : scalar or array-like, optional
            Scalar or array of values for EgadsData object.
        units : string, optional
            Units of EgadsData object. Best practice is to conform to UDUNITS
            conventions for unit names (see :TODO: add link for names)
        long_name : string, optional
            Descriptive name for EgadsData object.
        standard_name : string, optional
            Standard name for EgadsData object conforming to CF conventions
            standard name table (see :TODO: add link for standard name table)
        cdf_name : string, optional
            Name of variable if read in from NetCDF file. This will be populated
            automatically, in most instances.
        fill_value : scalar, optional
            Value typically from NetCDF file (in the form of _FillValue) that
            indicates values used to pre-fill the quantity in question.
        valid_range : vector, optional
            A vector of two number specifying the range of valid values for this
            variable. Should be composed of the valid minimum, followed by the
            valid maximum. If one of these values is 'None', then the relevant
            min or max range will be considered unlimited.
        sampled_rate : scalar, optional
            Rate at which the data was sampled in Hz.
        category : list, optional
            Names of probe category.
        calibration_coeff : list, optional
            Coefficients used to convert analog channels to digital counts (raw
            variables only).
        dependencies : list, optional
            List of input variables used to produce this variable (derived variables
            only).
        processor: string, optional
            List of toolbox processors used to produce this variable. Added
            automatically (derived variables only).

        """

        self.value = value
        self.units = units
        self.long_name = long_name
        self.standard_name = standard_name
        self.cdf_name = cdf_name
        self.fill_value = fill_value
        self.valid_range = valid_range
        self.sampled_rate = sampled_rate
        self.category = category
        self.calibration_coeff = calibration_coeff
        self.dependencies = dependencies
        self.processor = processor

        for key, val in attrs.iteritems():
            setattr(self, key, val)

        def __len__(self):

            return _get_shape()



        def print_description(self):
            """
            Generate and return a description of current EgadsData instance.

            """

            outstr = self._get_description()

            print outstr

        def get_units(self):
            """
            Return units used in current EgadsData instance.

            """

            return self.units

        def get_shape(self):
            """
            Return shape of current EgadsData instance.

            """

            return _get_shape()


        def _get_description(self):
            """
            Generate description of current EgadsData instance.

            """

            outstr = ('Current variable is %i with units of %s. \n' % (self.value.shape, self.units) +
                      'Its descriptive name is: %s and its CF name is: %s\n' % (self.long_name, self.standard_name))

            return outstr

        def _get_shape(self):
            """
            Get shape of current EgadsData instance.

            """

            return self.value.shape


__author__ = "mfreer"
__date__ = "$Date::                  $"
__version__ = "$Revision::           $"
__all__ = ["EgadsData", "EgadsAlgorithm"]

from collections import defaultdict
import types
import weakref
import datetime
from functools import wraps

import egads.core.metadata
import numpy


class EgadsData(object):
    """
    This class is designed using the EUFAR N6SP data and metadata recommendations.
    Its purpose is to store related data and metadata and allow them to be
    passed between functions and algorithms in a consistent manner.
    """

    __refs__ = defaultdict(list)

    def __init__(self, value=None, variable_metadata=None, **attrs):
        """
        Initializes EgadsData instance with standard attributes. If no attributes
        are provided, all standard attributes are set to None.

        Parameters
        -----------
        value : scalar or array-like, optional
            Scalar or array of values for EgadsData object.
        units : string, optional
            Units of EgadsData object. Best practice is to conform to UDUNITS
            conventions for unit names
            (see http://www.unidata.ucar.edu/software/udunits/udunits-2/udunits2lib.html)
        long_name : string, optional
            Descriptive name for EgadsData object.
        standard_name : string, optional
            Standard name for EgadsData object conforming to CF conventions
            standard name table (see http://cf-pcmdi.llnl.gov/documents/cf-standard-names/)
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

        if isinstance(value, EgadsData):
            self.__dict__ = value.__dict__.copy()
            self.value = value.value.copy()
        else:
            if isinstance(value, numpy.ndarray):
                self.value = value.copy()
            elif value is None:
                self.value = numpy.array([])
            else:
                self.value = numpy.array(value)

        if variable_metadata is None:
            self.metadata = egads.core.metadata.VariableMetadata({})
        else:
            self.metadata = variable_metadata

        for key, val in attrs.iteritems():
            self.metadata[key] = val

        self.__refs__[self.__class__].append(weakref.ref(self))


    def __len__(self):

        return len(self.value)


    def __repr__(self):
        try:
            return repr(['EgadsData', self.value])
        except AttributeError:
            return repr(None)


    def __add__(self, other):
        if isinstance(other, EgadsData):
            data = EgadsData(self.value + other.value, self.units)
            return data
        else:
            data = EgadsData(self.value + other, self.units)
            return data


    def __radd__(self, other): #TODO: fix radd to work with other classes
        return self.__add__(other)


    def __sub__(self, other):
        if isinstance(other, EgadsData):
            data = EgadsData(self.value - other.value, self.units)
            return data
        else:
            data = EgadsData(self.value - other, self.units)
            return data


    def __rsub__(self, other):
        if isinstance(other, EgadsData):
            data = EgadsData(other.value - self.value, self.units)
            return data
        else:
            data = EgadsData(other - self.value, self.units)
            return data


    def __mul__(self, other):
        if isinstance(other, EgadsData):
            data = EgadsData(self.value * other.value)
            return data
        else:
            data = EgadsData(self.value * other)
            return data


    def __rmul__(self, other):
        return self.__mul__(other)


    def __div__(self, other):
        if isinstance(other, EgadsData):
            data = EgadsData(self.value / other.value)
            return data
        else:
            data = EgadsData(self.value / other)
            return data


    def __rdiv__(self, other):
        if isinstance(other, EgadsData):
            data = EgadsData(other.value / self.value)
            return data
        else:
            data = EgadsData(other / self.value)
            return data


    def __pow__(self, other):
        if isinstance(other, EgadsData):
            data = EgadsData(self.value ** other.value)
            return data
        else:
            data = EgadsData(self.value ** other)
            return data


    def __rpow__(self, other):
        if isinstance(other, EgadsData):
            data = EgadsData(other.value ** self.value)
            return data
        else:
            data = EgadsData(other ** self.value)
            return data


    def __neg__(self):
        data = self
        data.value = -data.value
        return data


    def __eq__(self, other):
        if isinstance(other, EgadsData):
            return numpy.array_equal(self.value, other.value)
        else:
            return numpy.array_equal(self.value, other)


    def __ne__(self, other):
        if isinstance(other, EgadsData):
            return self.value != other.value
        else:
            return self.value != other
    

    def __getattr__(self, name):
        if name is "shape":
            return self.value.shape
        else:
            raise AttributeError


    def __setattr__(self, name, value):
        if name is "value":
            if isinstance(value, EgadsData):
                self.__dict__ = value.__dict__.copy()
                self.__dict__[name] = value.value.copy()
            else:
                if isinstance(value, numpy.ndarray):
                    self.__dict__[name] = value.copy()
                else:
                    self.__dict__[name] = numpy.array(value)
        else:
            if name is "__dict__":
                for key, attr in value.iteritems():
                    self.__dict__[key] = attr
            else:
                self.__dict__[name] = value


    def copy(self):
        """
        Generate and return a copy of the current EgadsData instance.
        """

        var_copy = EgadsData()
        var_copy.__dict__ = self.__dict__.copy()
        var_copy.value = self.value.copy()

        return var_copy


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


    def print_shape(self):
        """
        Prints shape of current EgadsData instance
        """

        print self._get_shape()


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


    @classmethod
    def _get_instances(cls):
        """
        Generator which returns currently defined instances of EgadsData.

        """

        for inst_ref in cls.__refs__[cls]:
            inst = inst_ref()
            if inst is not None:
                yield inst



class EgadsAlgorithm(object):
    """
    EGADS algorithm base class. All egads algorithms should inherit this class.

    The EgadsAlgorithm class provides base methods for algorithms in EGADS and
    initializes algorithm attributes.

    """

    def __init__(self):
        """
        Initializes EgadsAlgorithm instance with None values for all standard
        attributes.

        """
        self.name = self.__class__.__name__
        self.version = None
        self.date = None
        self.inputs = None
        self.outputs = None
        self.author = None

        self.metadata = None

        self._output_fields = ['name', 'units', 'long_name', 'standard_name',
            'fill_value', 'valid_range', 'sampled_rate',
            'category', 'calibration_coeff', 'dependencies']

        self.output_properties = {}

        for key in self._output_fields:
            self.output_properties[key] = None

    def run(self):
        """
        Skeleton class for run method. Raises not implemented AssertionError
        in this context, and should be redefined by EgadsAlgorithm children
        classes.

        """
        raise AssertionError('Algorithm not implemented')

    def _call_algorithm(self, *args):
        """
        Does check on arguments to pass to algorithm.

        If arguments are EgadsData instances, a check is done for expected units.
        Then the numeric value is passed to the algorithm. If argument is not
        EgadsData instance, units are assumed to be correct, and numeric value
        is passed to algorithm.

        """

        out_arg = []

        for arg in args:
            if isinstance(arg, EgadsData):
                #TODO Add unit checking
                out_arg.append(arg.value)
            else:
                out_arg.append(numpy.array(arg))

        result = self._algorithm(*out_arg)

        return result

    def _algorithm(self):
        """
        Skeleton algorithm method. To be defined in EgadsAlgorithm children.

        """

        raise AssertionError('Algorithm not implemented')


    def get_info(self):
        #TODO: Add docstring
        print self.__doc__

    def time_stamp(self):
        #TODO: Add docstring

        return str(datetime.datetime.today())

    def _populate_data_object(self, value, metadata):
        """
        Method for automatically populating new EgadsData instance 
        with calculated value and algorithm/variable metadata.
        
        
        """

        result = EgadsData(value, metadata)

        for key, val in self.output_properties.iteritems():
            result.__setattr__(key, val)


        return result


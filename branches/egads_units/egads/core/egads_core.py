__author__ = "mfreer"
__date__ = "$Date::                  $"
__version__ = "$Revision::           $"
__all__ = ["EgadsData", "EgadsAlgorithm"]

from collections import defaultdict
import types
import weakref
import datetime
from functools import wraps

import numpy
import quantities as pq

import metadata

#from .units import unit_registry
#from .units import Unit

#import quantities as units

class EgadsData(pq.Quantity):
    """
    This class is designed using the EUFAR N6SP data and metadata recommendations.
    Its purpose is to store related data and metadata and allow them to be
    passed between functions and algorithms in a consistent manner.

    **Constructor Variables**

    :param value: Optional -
        Scalar or array of values to initialize EgadsData object.
    :param VariableMetadata variable_metadata: Optional -
        VariableMetadata dictionary object containing relevant metadata
        for the current EgadsData instance.
    :param **attrs: Optional -
        Keyword/value pairs of additional metadata which will be added into
        the existing variable_metadata object.


    """

    __refs__ = defaultdict(list)

    def __new__(cls, value=None, units='', variable_metadata={}, **attrs):
        if isinstance(units, metadata.VariableMetadata):
            if not variable_metadata:
                variable_metadata = units
            units = units.get('units', '')


        ret = pq.Quantity.__new__(cls, value, units)

        if variable_metadata:
            ret.metadata = metadata.VariableMetadata(variable_metadata)
        else:
            ret.metadata = variable_metadata

        return ret


    def __init__(self, value=None, units='', variable_metadata=None, **attrs):
        """
        Initializes EgadsData instance with standard attributes. If no attributes
        are provided, all standard attributes are set to None.

        :param value: Optional -
            Scalar or array of values to initialize EgadsData object.
        :param VariableMetadata variable_metadata: Optional -
            VariableMetadata dictionary object containing relevant metadata
            for the current EgadsData instance.
        :param **attrs: Optional -
            Keyword/value pairs of additional metadata which will be added into
            the existing variable_metadata object.

        """



        for key, val in attrs.iteritems():
            self.metadata[key] = val

        self.__refs__[self.__class__].append(weakref.ref(self))


    @property
    def value(self):
        return self.view(type=numpy.ndarray)
    @value.setter
    def value(self, value, indx=None):

        print value, indx
#
#    @property
#    def units(self):
#        try:
#            return self.metadata['units'].symbol
#        except KeyError:
#            return ''
#    @units.setter
#    def units(self, units):
#        if isinstance(units, str):
#            self.metadata['units'] = unit_registry[units]
#        elif isinstance(units, units.Unit):
#            self.metadata['units'] = units
#
#    def __len__(self):
#        return len(self.value)



    def __repr__(self):
        try:
            return repr(['EgadsData', self.value, self.units])
        except AttributeError:
            return repr(None)
#
#
#    def __add__(self, other):
#        if isinstance(other, EgadsData):
#            data = EgadsData(self.value + other.value, self.units)
#            return data
#        else:
#            data = EgadsData(self.value + other, self.units)
#            return data
#
#
#    def __radd__(self, other): #TODO: fix radd to work with other classes
#        return self.__add__(other)
#
#
#    def __sub__(self, other):
#        if isinstance(other, EgadsData):
#            data = EgadsData(self.value - other.value, self.units)
#            return data
#        else:
#            data = EgadsData(self.value - other, self.units)
#            return data
#
#
#    def __rsub__(self, other):
#        if isinstance(other, EgadsData):
#            data = EgadsData(other.value - self.value, self.units)
#            return data
#        else:
#            data = EgadsData(other - self.value, self.units)
#            return data
#
#
#    def __mul__(self, other):
#        if isinstance(other, EgadsData):
#            data = EgadsData(self.value * other.value)
#            return data
#        else:
#            data = EgadsData(self.value * other)
#            return data
#
#
#    def __rmul__(self, other):
#        return self.__mul__(other)
#
#
#    def __div__(self, other):
#        if isinstance(other, EgadsData):
#            data = EgadsData(self.value / other.value)
#            return data
#        else:
#            data = EgadsData(self.value / other)
#            return data
#
#
#    def __rdiv__(self, other):
#        if isinstance(other, EgadsData):
#            data = EgadsData(other.value / self.value)
#            return data
#        else:
#            data = EgadsData(other / self.value)
#            return data
#
#
#    def __pow__(self, other):
#        if isinstance(other, EgadsData):
#            data = EgadsData(self.value ** other.value)
#            return data
#        else:
#            data = EgadsData(self.value ** other)
#            return data
#
#
#    def __rpow__(self, other):
#        if isinstance(other, EgadsData):
#            data = EgadsData(other.value ** self.value)
#            return data
#        else:
#            data = EgadsData(other ** self.value)
#            return data
#
#
#    def __neg__(self):
#        data = self
#        data.value = -data.value
#        return data
#
#
#    def __eq__(self, other):
#        if isinstance(other, EgadsData):
#            return numpy.array_equal(self.value, other.value)
#        else:
#            return numpy.array_equal(self.value, other)
#
#
#    def __ne__(self, other):
#        if isinstance(other, EgadsData):
#            return self.value != other.value
#        else:
#            return self.value != other
#
##
#    def __getattr__(self, name):
#        if name is "shape":
#            return self.value.shape
#        else:
#            raise AttributeError


#    def __setattr__(self, name, value):
#        if name is "value":
#            if isinstance(value, EgadsData):
#                self.__dict__ = value.__dict__.copy()
#                self.__dict__[name] = value.value.copy()
#            else:
#                if isinstance(value, numpy.ndarray):
#                    self.__dict__[name] = value.copy()
#                else:
#                    self.__dict__[name] = numpy.array(value)
#        else:
#            if name is "__dict__":
#                for key, attr in value.iteritems():
#                    self.__dict__[key] = attr
#            else:
#                self.__dict__[name] = value


    def copy(self):
        """
        Generate and return a copy of the current EgadsData instance.
        """

        var_copy = super(EgadsData, self).copy()
        var_copy.__dict__ = self.__dict__.copy()
        var_copy.metadata = self.metadata.copy()

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

    **Constructor Variables**

    :param bool return_Egads: Optional - 
        Flag used to configure which object type will be returned by the current
        EgadsAlgorithm. If ``true`` an :class: EgadsData instance with relevant
        metadata will be returned by the algorithm, otherwise an array or
        scalar will be returned.

    """

    def __init__(self, return_Egads=True):
        """
        Initializes EgadsAlgorithm instance with None values for all standard
        attributes.

        :param bool return_Egads: Optional -
            Flag used to configure which object type will be returned by the current
            EgadsAlgorithm. If ``true`` an :class: EgadsData instance with relevant
            metadata will be returned by the algorithm, otherwise an array or
            scalar will be returned.
        """
        self.name = self.__class__.__name__

        self.return_Egads = return_Egads

        self.metadata = None
        self.output_metadata = None

        self._output_fields = ['name', 'units', 'long_name', 'standard_name',
            'fill_value', 'valid_range', 'sampled_rate',
            'category', 'calibration_coeff', 'dependencies']

        self.output_properties = {}

        for key in self._output_fields:
            self.output_properties[key] = None

    def run(self, *args):
        """
        Basic run method. This method should be called from EgadsAlgorithm children,
        passsing along the correct inputs to the _call_algorithm method.

        """

        output = self._call_algorithm(*args)

        if len(self.metadata['Outputs']) > 1:
            result = []
            for i, value in enumerate(output):
                result.append(self._return_result(value, self.output_metadata[i]))
            result = tuple(result)
        else:
            result = self._return_result(output, self.output_metadata)


        return result


    def _return_result(self, value, metadata):


        if self.return_Egads is True:
            result = EgadsData(value, metadata)
        else:
            result = value


        return result


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

        self.time_stamp()

        return result

    def _algorithm(self):
        """
        Skeleton algorithm method. Must be defined in EgadsAlgorithm children.

        """

        raise AssertionError('Algorithm not implemented')


    def get_info(self):
        #TODO: Add docstring
        print self.__doc__

    def time_stamp(self):
        #TODO: Add docstring

        if len(self.metadata['Outputs']) > 1:
            for output in self.output_metadata:
                output['DateProcessed'] = self.now()
        else:
            self.output_metadata['DateProcessed'] = self.now()

    def now(self):

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


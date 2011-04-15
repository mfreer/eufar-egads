__author__ = "mfreer"
__date__ = "$Date::                  $"
__version__ = "$Revision::           $"
__all__ = ["NetCdf","EgadsNetCdf"]

import numpy
import netCDF4
import egads

from egads.input import FileCore

class NetCdf(FileCore):
    """
    EGADS class for reading and writing to generic NetCDF files.

    This module adapts the Python NetCDF4 0.8.2 library to the file access
    methods used in EGADS.

    """

    TYPE_DICT = {'char':'s1',
        'byte':'b',
        'short':'i2',
        'int':'i4',
        'float':'f4',
        'double':'f8'}


    def __del__(self):
        """
        If NetCDF file is still open on deletion of object, close it.
        """

        if self.f is not None:
            self.f.close()

    def open(self, filename, perms=None):
        """
        Opens NetCDF file given filename.

        Parameters
        -----------
        filename : string
            Name of NetCDF file to open.
        perms : char, optional
            Permissions used to open file. Options are 'w' for write (overwrites data in file),
            'a' and 'r+' for append, and 'r' for read. 'r' is the default value
        """

        if perms is not None:
            self.perms = perms
        else:
            perms = self.perms

        self._open_file(filename, perms)

    def close(self):
        """
        Closes currently open NetCDF file.

        """

        self._close_file()

    def get_attribute_list(self, varname=None):
        """
        Returns a dictionary of attributes avd values found either in current
        NetCDF file, or attached to a given variable.

        Parameters
        -----------
        varname : string, optional
            Name of variable to get list of attributes from. If no variable name is
            provided, the function returns top-level NetCDF attributes.

        """

        return self._get_attribute_list(varname)

    def get_attribute_value(self, attrname, varname=None):
        """
        Returns value of an attribute given its name. If a variable name is provided,
        the attribute is returned from the variable specified, otherwise the global
        attribute is examined.

        Parameters
        -----------
        name : string
            Name of attribute to examine
        varname : string, optional
            Name of variable attribute is attached to. If none specified, global
            attributes are examined.

        Returns
        -------
        attr_value : string
            Value of attribute examined

        """

        attrs = self._get_attribute_list(varname)

        return attrs[attrname]

    def get_dimension_list(self, varname=None):
        """
        Returns a dictionary of dimensions and their sizes found in the current
        NetCDF file. If a variable name is provided, the dimension names and
        lengths associated with that variable are returned.

        Parameters
        -----------
        varname : string, optional
            Name of variable to get list of associated dimensions for. If no variable
            name is provided, the function returns all dimensions in the NetCDF file.

        """

        return self._get_dimension_list(varname)

    def get_variable_list(self):
        """
        Returns a list of variables found in the current NetCDF file.

        Parameters
        -----------
        None

        """
        
        return self._get_variable_list()

    def get_filename(self):
        """
        If file is open, returns the filename.

        Parameters
        -----------
        None

        """

        return self.filename

    def get_perms(self):
        """
        Returns the current permissions on the file that is open. Returns None if
        no file is currently open. Options are 'w' for write (overwrites
        data in file),'a' and 'r+' for append, and 'r' for read.

        Parameters
        -----------
        None

        """

        if self.f is not None:
            return self.perms
        else:
            return 



    def read_variable(self, varname, input_range=None):
        """
        Reads a variable from currently opened NetCDF file.
        
        Parameters
        -----------
        varname : string
            Name of NetCDF variable to read in.
        input_range : vector, optional
            Range of values in each dimension to input. TODO add example

        Returns
        -------
        value : array
            Values from specified variable read in from NetCDF file.
        """

        try:
            varin = self.f.variables[varname]
        except KeyError:
            print "ERROR: Variable %s does not exist in %s" % (varname, self.filename)
            raise KeyError
        except Exception:
            print "Error: Unexpected error"
            raise

        if input_range is None:
            value = varin[:]
        else:
            obj = 'slice(input_range[0], input_range[1])'
            for i in xrange(2, len(input_range), 2):
                obj = obj + ', slice(input_range[%i], input_range[%i])' % (i, i + 1)

            value = varin[eval(obj)]

        return value

    def write_variable(self, value, varname, dims=None, type='double', fill_value=None):
        """
        Writes/creates variable in currently opened NetCDF file.

        Parameters
        -----------
        value : arraylike
            Array of values to output to NetCDF file.
        varname : string
            Name of variable to create/write to.
        dims : tuple of strings, optional
            Name(s) of dimensions to assign to variable. If variable already exists
            in NetCDF file, this parameter is optional. For scalar variables,
            pass an empty tuple.
        type : string, optional
            Data type of variable to write. Defaults to 'double'. If variable exists,
            data type remains unchanged. Options for type are 'double', 'float',
            'int', 'short', 'char', and 'byte'
        fill_value : value, optional
            Overrides default NetCDF _FillValue, if provided.

        """

        if self.f is not None:
            try:
                varout = self.f.variables[varname]
            except KeyError:
                varout = self.f.createVariable(varname, self.TYPE_DICT[type.lower()], dims)

            varout[:] = value


    def add_dim(self, name, size):
        """
        Adds dimension to currently open file.

        Parameters
        -----------
        name : string
            Name of dimension to add
        size : integer
            Integer size of dimension to add.

        """

        if self.f is not None:
            self.f.createDimension(name, size)
        else:
            raise # TODO add file execption

    def add_attribute(self, attrname, value, varname=None):
        """
        Adds attribute to currently open file. If varname is included, attribute
        is added to specified variable, otherwise it is added to global file
        attributes.

        Parameters
        -----------
        name : string
            Attribute name.
        value : string
            Value to assign to attribute name.
        varname : string, optional
            If varname is provided, attribute name and value are added to specified
            variable in the NetCDF file.
        """

        if self.f is not None:
            if varname is not None:
                varin = self.f.variables[varname]
                setattr(varin, attrname, value)
            else:
                setattr(self.f, attrname, value)
        else:
            print 'ERROR: No file open'



    def _open_file(self, filename, perms):
        """
        Private method for opening NetCDF file.

        Parameters
        -----------
        filename: string
            Name of NetCDF file to open.
        perms : char
            Permissions used to open file. Options are 'w' for write (overwrites data in file),
            'a' and 'r+' for append, and 'r' for read.
        """

        self.close()

        try:
            self.f = netCDF4.Dataset(filename, perms)
            self.filename = filename
            self.perms = perms
        except RuntimeError:
            print "ERROR: File %s doesn't exist" % (filename)
            raise RuntimeError
        except Exception:
            print "ERROR: Unexpected error"
            raise

    def _close_file(self):
        """
        Private method for closing NetCDF file.
        """

        if self.f is not None:
            self.f.close()
            self.f = None
            self.filename = None

    def _get_attribute_list(self, var=None):
        """
        Private method for getting attributes from a NetCDF file. Gets global
        attributes if no variable name is provided, otherwise gets attributes
        attached to specified variable. Function returns dictionary of values.
        """

        if self.f is not None:
            if var is not None:
                varin = self.f.variables[var]
                return varin.__dict__
            else:
                return self.f.__dict__
        else:
            raise # TODO add specific file exception

    def _get_dimension_list(self, var=None):
        """
        Private method for getting list of dimension names and lengths. If
        variable name is provided, method returns list of dimension names
        attached to specified variable, if none, returns all dimensions in the file.
        """

        dimdict = {}

        if self.f is not None:
            file_dims = self.f.dimensions

            if var is not None:
                varin = self.f.variables[var]
                dims = varin.dimensions

                for dimname in dims:
                    dimobj = file_dims[dimname]
                    dimdict[dimname] = len(dimobj)
            else:
                dims = file_dims

                for dimname, dimobj in dims.iteritems():
                    dimdict[dimname] = len(dimobj)

            return dimdict
        else:
            raise # TODO add specific file exception

        return None


    def _get_variable_list(self):
        """
        Private method for getting list of variable names.
        """

        if self.f is not None:
            return self.f.variables.keys()
        else:
            raise # TODO Add specific file execption




class EgadsNetCdf(NetCdf):
    """
    EGADS class for reading and writing to NetCDF files following EUFAR
    conventions. Inherits from the general EGADS NetCDF module.

    """

    FILE_ATTR_DICT= {'conventions':'Conventions',
                     'title':'title',
                     'source':'source',
                     'institution':'institution',
                     'project':'project',
                     'history':'history'}

    VAR_ATTR_DICT = {'units':'units',
             'long_name':'long_name',
             'standard_name':'standard_name',
             'fill_value':'_FillValue',
             'valid_range':'valid_range',
             'sampled_rate':'SampledRate',
             'category':'Category',
             'calibration_coeff':'CalibrationCoeff',
             'dependencies':'Dependencies',
             'processor':'Processor'}


    def __init__(self, filename=None, perms='r'):
        """
        Initializes NetCDF instance.

        Parameters
        -----------
        filename : string, optional
            Name of NetCDF file to open.
        perms : char, optional
            Permissions used to open file. Options are 'w' for write (overwrites
            data), 'a' and 'r+' for append, and 'r' for read. 'r' is the default
            value.
        """

        self.f = None
        self.filename = filename
        self.perms = perms
        self.conventions = None
        self.title = None
        self.source = None
        self.institution = None
        self.project = None
        self.history = None

        if filename is not None:
            self.open(filename, perms)

    def open(self, filename, perms=None):
        """
        Opens NetCDF file given filename.

        Parameters
        -----------
        filename : string
            Name of NetCDF file to open.
        perms : char, optional
            Permissions used to open file. Options are 'w' for write (overwrites data in file),
            'a' and 'r+' for append, and 'r' for read. 'r' is the default value
        """

        if perms is not None:
            self.perms = perms
        else:
            perms = self.perms

        self._open_file(filename, perms)

        for key, val in self.FILE_ATTR_DICT.iteritems():
            attribute = getattr(self.f, val,None)
            setattr(self, key, attribute)


    def close(self):
        """
        Close currently open NetCDF file.
        """

        self._close_file()
        self.conventions = None
        self.title = None
        self.source = None
        self.institution = None
        self.project = None
        self.history = None

    def read_variable(self, varname, input_range=None):
        """
        Reads in a variable from currently opened NetCDF file and maps the NetCDF
        attributies to an EgadsData instance.

        Parameters
        -----------
        varname : string
            Name of NetCDF variable to read in.
        input_range : vector, optional
            Range of values in each dimension to input. :TODO: add example

        Returns
        -------
        data : EgadsData
            Values and metadata of the specified variable in an EgadsData instance.
        """

        try:
            varin = self.f.variables[varname]
        except KeyError:
            print "ERROR: Variable %s does not exist in %s" % (varname, self.filename)
            raise KeyError
        except Exception:
            print "Error: Unexpected error"
            raise

        if input_range is None:
            value = varin[:]
        else:
            obj = 'slice(input_range[0], input_range[1])'
            for i in xrange(2, len(input_range), 2):
                obj = obj + ', slice(input_range[%i], input_range[%i])' % (i, i + 1)

            value = varin[eval(obj)]

        data = egads.EgadsData()
        data.cdf_name = varname
        data.value = value

        for key, val in self.VAR_ATTR_DICT.iteritems():
                attribute = getattr(varin, val,None)
                setattr(data, key, attribute)

        return data

    def write_variable(self, data, varname=None, dims=None, type='double'):
        """
        Writes/creates varible in currently opened NetCDF file.

        Parameters
        -----------
        data : EgadsData
            Instance of EgadsData object to write out to file. All data and
            attributes will be written out to the file.
        varname : string, optional
            Name of variable to create/write to. If no varname is provided, and
            if cdf_name attribute in EgadsData object is defined, then the variable
            will be written to cdf_name.
        dims : tuple of strings, optional
            Name(s) of dimensions to assign to variable. If variable already exists
            in NetCDF file, this parameter is optional. For scalar variables,
            pass an empty tuple.
        type : string, optional
            Data type of variable to write. Defaults to 'double'. If variable exists,
            data type remains unchanged. Options for type are 'double', 'float',
            'int', 'short', 'char', and 'byte'

        """

        if self.f is not None:
            try:
                varout = self.f.variables[varname]
            except KeyError:
                varout = self.f.createVariable(varname, self.TYPE_DICT[type.lower()], dims)

            varout[:] = data.value

            for key, val in self.VAR_ATTR_DICT.iteritems():
                attribute = getattr(data, key)
                setattr(varout, val, attribute)





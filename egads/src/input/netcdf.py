__author__ = "Matt Freer"
__date__ = "$Date: 2009-10-13 14:51:27 +0200 (Tue, 13 Oct 2009) $"
__version__ = "$Revision: 15 $"

import egads
import netCDF4


class NetCdf(object):
    """
    EGADS I/O module for reading and writing to NetCDF files.

    This module allows users to read and write from NetCDF files following the
    EUFAR N6SP file conventions.
    """

    def __init__(self,filename = None, perms = None):
        """
        :TODO: fill in docstring
        """
        if filename is not None:
            self.f = self._open_file(filename, perms)
        else:
            self.f = None
            self.filename = None

        self._std_file_attributes = {'title':'title',
                                     'source':'source',
                                     'instutition':'institution',
                                     'project':'project',
                                     'history':'history'}

        self._std_var_attributes = {'units': 'units',
                                    'long_name': 'long_name',
                                    'standard_name': 'standard_name',
                                    'fill_value': '_FillValue',
                                    'valid_range':'',
                                    'sampled_rate': 'SampledRate',
                                    'category':'Category',
                                    'calibration_coeff':'CalibrationCoefficient',
                                    'dependencies':'Dependencies',
                                    'processor':'Processor'}

    def __del__(self):
        """
        If NetCDF file is open, close it.
        """
        if self.f is not None:
            self.f.close()


    def read(self, varname, filename = None, input_range=None, attrs=None, data=None):
        """ Returns a ToolboxData object after reading data from a NetCDF file
            given a filename and variable name. Input range and additional attributes
            can be provided by the user."""

        if data is None:
            data = egads.ToolboxData()

        if filename is not None:
            self._open_file(filename,'r')

        # read in given variable and give an error and halt if it doesnt exist
        try:
            varin = self.f.variables[varname]
        except KeyError:
            print "ERROR: Variable %s does not exist in %s" % (varname, filename)
            raise KeyError
        except Exception:
            print "ERROR: Unexpected error"
            raise

        # read in data from variable, or data subset given a valid input_range
        if input_range is None:
            data.value = varin[:]
        else:
            obj = 'slice(input_range[0],input_range[1])'
            for i in xrange(2, len(input_range), 2):
                obj = obj + ',slice(input_range[%i],input_range[%i])' % (i, i + 1)
                        
            data.value = varin[eval(obj)]
            
        data.dimensions = varin.shape
        data.name = varname

        # read in standard variable attributes from file
        self._get_attribute(data, varin, self._std_var_attributes)

        # :TODO: add inputs from other attributes


        return data

    def write(self, data, varname, dimnames, filename = None, type='f8',
              overwrite='yes', create='no'):
        """
        Writes given variable and its attribues to NetCDF file.


        """

        if filename is not None:
            if create.lower() == 'no':
                self._open_file(filename,'r+')
            else:
                dims = dict(zip(dimnames,data.value.shape))
                self.create_file(filename,dims = dims)


        if overwrite == 'yes':
            try:
                varout = self.f.variables[varname]
            except KeyError:
                varout = self.f.createVariable(varname, type, (dimnames))
        else:
            if varname not in self.f.variables:
                varout = self.f.createVariable(varname, type, (dimnames))

        varout[:] = data.value
        self._set_attribute(varout,data)



    def create_file(self, filename, attrs=None, dims=None):
        """
        Method for creating new NetCDF file. must provide filename. Optional arguments
        include dictionaries for file attribues and dimensions.
        """

        self._open_file(filename,'w')
        if attrs is not None:
            self._set_attribute(self.f, attrs)

        if dims is not None:
            self._set_dim(dims)




    def add_dim(self, dimname, dimlength,filename = None):
        """
        Add dimension to NetCDF file.

        Adds a user defined dimension with dimname and dimlength to filename
        NetCDF file. Uses NetCDF4 library methods.

        """

        if filename is not None:
            self._open_file(filename, 'r+')

        dims = dict(zip(dimname,dimlength))

        self._set_dim(dims)
        

        
    def add_variable(self, filename, varname, dimnames, type='double'):
        pass

    def add_attribute(self, filename, attrname, attrvalue, variable=None):
        """
        TODO add docstring
        """
        pass




    def read_attribute(self, filename, attribute, variable=None):
        pass

    def check_file(self, filename):
        pass


    def _open_file(self,filename,perms,log_error = 'no'):
        """
        Method for opening NetCDF file, with error handling. Displays message
        to user and returns RuntimeError if given file doesn't exist.
        """
        try:
            self.f = netCDF4.Dataset(filename, perms)
            self.filename = filename
            self._get_attribute(self, self.f, self._std_file_attributes)
        except RuntimeError:
            print "ERROR: File %s doesnt exist" % (filename)
            raise RuntimeError
        except Exception:
            print "ERROR: Unexpected error"
            raise

    def _set_attribute(self,obj,data,attrs = None):
        """
        TODO Add docstring
        """
        if attrs is None:
            attrs = self._std_var_attributes
        for key, val in attrs.iteritems():
            dataattr = getattr(data, key, None)
            if dataattr is not None:
                setattr(obj, val, dataattr)

    def _get_attribute(self,data, obj,attrs):
        """
        TODO Add doctstring
        """
        for key, val in attrs.iteritems():
            if val != '':
                setattr(data, key, getattr(obj, val,None))




    def _set_dim(self, dims):
        """
        Create dimensions in NetCDF file given a dictionary of dimension names
        and their values.
        """

        for key, val in dims.iteritems():
            self.f.createDimension(key,val)


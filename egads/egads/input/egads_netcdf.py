__author__ = "mfreer"
__date__ = "$Date$"
__version__ = "$Revision$"
__all__ = ["EgadsNetCdf"]

import egads
import netCDF4
import netcdf


class EgadsNetCdf(netcdf.NetCdf):
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

                



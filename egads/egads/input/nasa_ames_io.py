__author__ = "mfreer"
__date__ = "$Date:: 2010-10-19 19:10#$"
__version__ = "$Revision:: 38        $"
__all__ = ["NasaAmes"]


import egads
import nappy


from egads.input import FileCore

class NasaAmes(FileCore):
    """
    EGADS module for interfacing with NASA Ames files.

    This module adapts the NAPpy library to the file access methods used
    in EGADS
    """

    def __init__(self, filename=None, perms='r'):
        """
        Initializes NASA Ames instance.

        :param string filename:
            Optional - Name of NetCDF file to open.
        :param char perms:
            Optional -  Permissions used to open file.
            Options are ``w`` for write (overwrites data),
            ``a`` and ``r+`` for append, and ``r`` for read. ``r`` is the default
            value.
        """
        self.file_metadata = None

        FileCore.__init__(self, filename, perms)


    def read_variable(self, varname):
        #TODO Add read_variable method.
        pass

    def write_variable(self, data, varname):
        #TODO Add write_variable method.
        pass

    def get_variable_list(self):
        #TODO Add get_variable_list method.
        pass

    def get_perms(self):
        #TODO Add get_perms method.
        pass

    def convert_to_netcdf(self, nc_file=None, mode='w', variables=None, aux_variables=None,
                          global_attributes=[], time_units=None, time_warning=True,
                          rename_variables={}):
        """
        Converts currently open NASA Ames file to NetCDF file.

        :param string nc_file:
            Optional - Name of output NetCDF file. If none is provided, suffix on current
            NA file is changed to .nc
        :param char mode:
            Optional - ``w`` for write (ovewrites data), ``a`` for append. Default: ``w``.
        :param list variables:
            Optional - List of variable names to transfer to the NetCDF file. If none
            are provided, all variables will be transferred.
        :param list aux_variables:
            Optional - List of aux variable names to transfer to the NetCDF file. If
            none are provided, all compatible aux variables will be transfered.
        :param list global_attributes:
            Optional - List of additional global attributesto add to NetCDF file.
        :param string time_units:
            Optional - Valid time units string (i.e. 'seconds since 2010-08-10 10:00:00')
            to use for time units if there is a valid time axis.
        :param bool time_warning:
            Optional - Suppresses time units warning for invalid time units if set to False.
            Default: True.
        :param dict rename_variables:
            Optional - Dictionary of {old_name: new_name} variable ID pairs used to
            rename variables as they are written to the NetCDF file.

        """
        if 'Conventions' not in global_attributes:
            global_attributes.append(('Conventions','CF-1.0'))

        nappy.convertNAToNC(self.filename, nc_file, mode, variables, aux_variables,
                            global_attributes, time_units, time_warning, rename_variables)

    def convert_to_csv(self, csv_file=None, annotation=False, no_header=False):
        """
        Converts currently open NASA Ames file to CSV file.

        :param string csv_file:
            Optional - Name of output CSV file. If none is provided, suffix on currently open
            NA file is changed to .csv
        :param bool annotation:
            Optional - Adds additional left-hand column to output file if set to True. Default: False.
        :param bool no_header:
            Optional - Removes all header information from output if set to True. Default: False.

        """

        nappy.convertNAtoCSV(self.filename, csv_file, annotation, no_header)

    def _open_file(self, filename, perms):
        """
        Private method for opening NASA Ames file using Nappy API.

        :parm string filename:
            Name of NASA Ames file to open.
        :param char perms:
            Permissions used to open file. Options are ``w`` for write (overwrites data in file),
            ``a`` and ``r+`` for append, and ``r`` for read.

        """

        self.close()

        try:
            self.f = nappy.openNAFile(filename)
            self.filename = filename
            self.perms = perms
            attr_dict = {}
            attr_dict['Comments'] = self.f.getNormalComments
            attr_dict['SpecialComments'] = self.f.getSpecialComments()
            attr_dict['Organisation'] = self.f.getOrganisation()
            dates = self.f.getFileDates()
            attr_dict['CreationDate'] = dates[0]
            attr_dict['RevisionDate'] = dates[1]
            attr_dict['Originator'] = self.f.getOriginator()
            attr_dict['Mission'] = self.f.getMission()
            attr_dict['Source'] = self.f.getSource()
            self.file_metadata = egads.core.metadata.FileMetadata(attr_dict, self.filename,
                                                                  conventions = "NASAAmes")
        except RuntimeError:
            print "ERROR: File %s doesn't exist" % (filename)
            raise RuntimeError
        except Exception:
            print "ERROR: Unexpected error"
            raise


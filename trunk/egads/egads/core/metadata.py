__author__ = "mfreer"
__date__ = "$Date::                  $"
__version__ = "$Revision::           $"
__all__ = ['Metadata', 'FileMetadata','VariableMetadata','AlgorithmMetadata']


FILE_ATTR_DICT = {'Conventions':'conventions',
                  'title':'title',
                  'source':'source',
                  'institution':'institution',
                  'project':'project',
                  'date_created':'date_created',
                  'geospatial_lat_min':'geospatial_lat_min',
                  'geospatial_lat_max':'geospatial_lat_max',
                  'geospatial_lon_min':'geospatial_lon_min',
                  'geospatial_lon_max':'geospatial_lon_max',
                  'geospatial_vertical_min':'geospatial_vertical_min',
                  'geospatial_vertical_max':'geospatial_vertical_max',
                  'geospatial_vertical_positive':'geospatial_vertical_positive',
                  'geospatial_vertical_units':'geospatial_vertical_units',
                  'time_coverage_start':'time_coverage_start',
                  'time_coverage_end':'time_coverage_end',
                  'time_coverage_duration':'time_coverage_duration',
                  'history':'history',
                  'references':'references',
                  'comment':'comment'}



VAR_ATTR_DICT = {'units':'units',
                 '_FillValue':'fill_value',
                 'long_name':'long_name',
                 'standard_name':'standard_name',
                 'valid_range':'valid_range',
                 'valid_min':'valid_min',
                 'valid_max':'valid_max',
                 'SampledRate':'sampled_rate',
                 'Category':'category',
                 'CalibrationCoefficients':'calibration_coefficients',
                 'InstrumentLocation':'instrument_location',
                 'instrumentCoordinates':'instrument_coordinates',
                 'Dependencies':'dependencies',
                 'Processor':'processor',
                 'Comments':'comments',
                 'ancillary_variables':'ancillary_variables',
                 'flag_values':'flag_values',
                 'flag_masks':'flag_masks',
                 'flag_meanings':'flag_meanings'}

FILE_ATTR_LIST = ['Conventions',
                  'title',
                  'source',
                  'institution',
                  'project',
                  'date_created',
                  'geospatial_lat_min',
                  'geospatial_lat_max',
                  'geospatial_lon_min',
                  'geospatial_lon_max',
                  'geospatial_vertical_min',
                  'geospatial_vertical_max',
                  'geospatial_vertical_positive',
                  'geospatial_vertical_units',
                  'time_coverage_start',
                  'time_coverage_end',
                  'time_coverage_duration',
                  'history',
                  'references',
                  'comment']



VAR_ATTR_LIST = ['units',
                 '_FillValue',
                 'long_name',
                 'standard_name',
                 'valid_range',
                 'valid_min',
                 'valid_max',
                 'SampledRate',
                 'Category',
                 'CalibrationCoefficients',
                 'InstrumentLocation',
                 'instrumentCoordinates',
                 'Dependencies',
                 'Processor',
                 'Comments',
                 'ancillary_variables',
                 'flag_values',
                 'flag_masks',
                 'flag_meanings']

ALG_ATTR_LIST = ['units',
                 'long_name',
                 'standard_name',
                 'valid_range',
                 'Category',
                 'CalibrationCoefficient',
                 'Inputs',
                 'Outputs',
                 'Dependencies',
                 'Processor',
                 'ProcessorVersion',
                 'ProcessorDate',
                 'DateProcessed']


class Metadata(dict):
    """
    This is a generic class to designed to provide basic metadata storage and handling
    capabilities.


    """

    def __init__(self, metadata_dict, conventions = None, metadata_list=None):
        """
        Initialize Metadata instance with given metadata in dict form.


        :param dict metadata_dict:
            Dictionary object containing metadata names and values.

        """

        dict.__init__(self, metadata_dict)

        self._metadata_list = metadata_list

        self._conventions = conventions

    def add_items(self, metadata_dict):
        """
        Method to add metadata items to current Metadata instance.

        :param metadata_dict:
            Dictionary object containing metadata names and values.
        """

        for key, var in metadata_dict:
            self[key] = var

        return

    def set_conventions(self,conventions):
        """
        Sets conventions to be used in current Metadata instance

        :param list conventions:
            List of conventions used in current metadata instance.

        """

        self._conventions = conventions

    def parse_dictionary_objs(self):
        pass

class FileMetadata(Metadata):
    """
    This class is designed to provide basic storage and handling capabilities
    for file metadata.

    """

    def __init__(self, metadata_dict, filename, conventions_keyword='Conventions', conventions=None):
        """
        Initialize Metadata instance with given metadata in dict form. Tries to
        determine which conventions are used by the metadata. The user can optionally
        supply which conventions the metadata uses.

        :param dict metadata_dict:
            Dictionary object containing metadata names and values.
        :param string filename:
            Filename for origin of file metadata.
        :param string conventions_keyword: Optional -
            Keyword contained in metadata dictionary used to detect which metadata
            conventions are used.
        :param list conventions: Optional -
            List of metadata conventions used in provided metadata dictionary.
        """


        if conventions is None:
            try:
                conventions = [s.strip() for s in metadata_dict[conventions_keyword].split(',')]
            except KeyError:
                conventions = None

        Metadata.__init__(self, metadata_dict, conventions,
                          metadata_list=FILE_ATTR_LIST)

        if filename is None:
            self._filename = None
        else:
            self._filename = filename


        self.update()

    def set_filename(self, filename):
        """
        Sets file object used for current FileMetadata instance.

        :param string filename:
            Filename of provided metadata.
        """

        self._filename = filename


    def parse_dictionary_objs(self):
        pass


class VariableMetadata(Metadata):
    """
    This class is designed to provide storage and handling capabilities for
    variable metadata.
    """

    def __init__(self, metadata_dict, parent_metadata_obj=None, conventions=None):
        """
        Initialize VariableMetadata instance with given metadata in dict form.
        If VariableMetadata comes from a file, the file metadata object can be
        provided to auto-detect conventions. Otherwise, the user can specify which
        conventions are used in the variable metadata.

        :param dict metadata_dict:
            Dictionary object contaning variable metadata names and values
        :param Metadata parent_metadata_obj: Metadata, optional
            Metadata object for the parent object of current variable (file,
            algorithm, etc). This field is optional.
        :param list conventions: Optional -
            List of metadata conventions used in provided metadata dictionary.
        """

        Metadata.__init__(self, metadata_dict, metadata_list=VAR_ATTR_LIST)

        self.origin = parent_metadata_obj

        if conventions is None:
            if parent_metadata_obj is None:
                self._conventions = None
                self.parent = None
            else:
                self._conventions = parent_metadata_obj._conventions
                self.parent = parent_metadata_obj
        else:
            self._conventions = conventions

    def set_parent(self, parent_metadata_obj):
        """
        Sets parent object of VariableMetadata instance.

        :param Metadata parent_metadata_obj: Optional -
            Metadata object for the parent object of the current variable (file,
            algorithm, etc)
        """

        self.parent = parent_metadata_obj



    def parse_dictionary_objs(self):
        pass

class AlgorithmMetadata(Metadata):
    """
    This class is designed to provide storage and handling capabilities for 
    EGADS algorithm metadata. Stores instances of VariableMetadata objects
    to use to populate algorithm variable outputs.
    """

    def __init__(self, metadata_dict, child_variable_metadata=None):
        """
        Initialize AlgorithmMetadata instance with given metadata in dict form and
        any child variable metadata.

        :param dict metadata_dict:
            Dictionary object containing variable metadata names and values
        :param list child_varable_metadata: Optional -
            List containing VariableMetadata

        """

        Metadata.__init__(self, metadata_dict, metadata_list=ALG_ATTR_LIST)
        
        self.child_metadata = []

        if isinstance(child_variable_metadata, list):
            for child in child_variable_metadata:
                self.assign_children(child)
        elif child_variable_metadata is not None:
            self.assign_children(child_variable_metadata)


    def assign_children(self, child):
        """
        Assigns children to current AlgorithmMetadata instance. Children are
        typically VariableMetadata instances. If VariableMetadata instance is
        used, this method also assigns current AlgorithmMetadata instance
        as parent in VariableMetadata child.

        :param VariableMetadata child:
            Child metadata object to add to current instance children.
        """


        self.child_metadata.append(child)

        if isinstance(child, VariableMetadata):
            child.set_parent(self)
            
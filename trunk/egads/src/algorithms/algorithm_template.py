__author__ = ""
__date__ = "$Date: 2009-11-26 15:34:16 +0100 (Thu, 26 Nov 2009) $"
__version__ = "$Revision: 20 $"


import egads

def algorithm_template(inputs):
    """
    This file provides a template for creation of EGADS algorithms.

    FILE        algorithm_template.py

    VERSION     $Revision: 20 $

    CATEGORY    None

    PURPOSE     Template for EGADS algorithm files

    DESCRIPTION ...

    INPUT       inputs      units   description

    OUTPUT      outputs     units   description

    SOURCE      sources

    REFERENCES

    """

    name = 'algorithm_template'

    ## Do processing here:


    result = egads.ToolboxData(value = output,
                               units = '%',
                               long_name = 'relative humidity',
                               standard_name = 'relative humidity',
                               processor_version = __version__,
                               processor_date = __date__)


    result.units = '%'
    result.long_name = 'relative humidity'
    result.processor = name
    result.processor_version = __version__
    result.processor_date = __date__



    return result



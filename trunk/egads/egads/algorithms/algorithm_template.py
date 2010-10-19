__author__ = "mfreer"
__date__ = "$Date$"
__version__ = "$Revision$"
__all__ = ['']

import egads
import inspect

def algorithm_template(inputs):
    """
    This file provides a template for creation of EGADS algorithms.

    FILE        algorithm_template.py

    VERSION     $Revision$

    CATEGORY    None

    PURPOSE     Template for EGADS algorithm files

    DESCRIPTION ...

    INPUT       inputs      units   description

    OUTPUT      outputs     units   description

    SOURCE      sources

    REFERENCES

    """


    ## Do processing here:


    result = egads.EgadsData(value = output,
                               units = '%',
                               long_name = 'template',
                               standard_name = 'template',
                               fill_value = None,
                               valid_range = None,
                               sampled_rate = None,
                               category = None,
                               calibration_coeff = None,
                               dependencies = None,
                               processor = inspect.stack()[0][3],
                               processor_version = __version__,
                               processor_date = __date__)



    return result



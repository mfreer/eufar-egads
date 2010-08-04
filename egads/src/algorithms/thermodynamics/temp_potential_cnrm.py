__author__ = "mfreer"
__date__ = "$Date$"
__version__ = "$Revision$"


import egads
import inspect

def temp_potential_cnrm(T_s, P_s, Racpa):
    """
    This file provides a template for creation of EGADS algorithms.

    FILE        algorithm_template.py

    VERSION     $Revision$

    CATEGORY    Thermodynamics

    PURPOSE     Calculates potential temperature

    DESCRIPTION Calculates potential temperature given static temperature, pressure,
                and the ratio of gas constant and specific heat of air.

    INPUT       T_s     vector  K or C  static temperature
                P_s     vector  hPa     static pressure
                Racpa   coeff.          gas constant of air divided by
                                        specific heat of air at constant pressure

    OUTPUT      theta   vector  same as T_s     potential temperature

    SOURCE      CNRM/GMEI/TRAMM

    REFERENCES  Triplet-Roche.

    """

    theta = T_s.value * (1000/P_s.value) ** (Racpa.value)

    result = egads.ToolboxData(value = theta,
                               units = 'K',
                               long_name = 'potential temperature',
                               standard_name = 'air_potential_temperature',
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



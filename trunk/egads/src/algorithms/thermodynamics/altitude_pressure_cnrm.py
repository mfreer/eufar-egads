__author__ = "mfreer"
__date__ = "$Date:  $"
__version__ = "$Revision: 1$"

from math import log

import egads
import inspect

def altitude_pressure_cnrm(T_v, P_s, P_surface, R_a_g):
    """

    FILE        altitude_pressure_cnrm.py

    VERSION     $Revision: 20 $

    CATEGORY    Thermodymics

    PURPOSE     Calculate pressure altitude

    DESCRIPTION Caluclate pressure altitude using virtual temperatue

    INPUT       T_v         vector  K or C  virtual temperature
                P_s         vector  hPa     static pressure
                P_surface   coeff.  hPa     surface pressure
                R_a_g       coeff           Gas constant of air divided by gravity

    OUTPUT      alt_p       vector  m       pressure altitude

    SOURCE      CNRM/GMEI/TRAMM

    REFERENCES

    """

    alt_p = R_a_g.value * T_v.value * log(P_surface.value/P_s.value)

    result = egads.ToolboxData(value = alt_p,
                               units = 'm',
                               long_name = 'pressure_altitude',
                               standard_name = '',
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



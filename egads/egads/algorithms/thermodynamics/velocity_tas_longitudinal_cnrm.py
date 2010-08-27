__author__ = "mfreer"
__date__ = "$Date$"
__version__ = "$Revision$"


import egads
import inspect

from math import sqrt, tan

def velocity_tas_longitudinal_cnrm(V_t, alpha, beta):
    """

    FILE        velocity_tas_longitudinal_cnrm.py

    VERSION     $Revision$

    CATEGORY    Thermodynamics

    PURPOSE     Calculates the longitudinal true air speed

    DESCRIPTION Calculates the true air speed along the longitudinal axis of the
                aircraft.

    INPUT       V_t     vector  m/s     true air speed
                alpha   vector  rad     angle of attack
                beta    vector  rad     sideslip angle

    OUTPUT      V_tx    vector  m/s     longitudinal true airspeed

    SOURCE      CNRM/GMEA/TRAMM

    REFERENCES  NCAR-RAF Bulletin #23

    """


    V_tx = V_t.value / sqrt(1 + tan(alpha.value) ** 2 + tan(beta.value) ** 2)


    result = egads.EgadsData(value = V_tx,
                               units = 'm/s',
                               long_name = 'longitudinal true air speed',
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



__author__ = "mfreer"
__date__ = "$Date$"
__version__ = "$Revision$"
__all__ = ["pressure_angle_incidence_cnrm"]

import egads
import inspect
from numpy import multiply, power, zeros, logical_and

def pressure_angle_incidence_cnrm(P_sr, delta_P_r, delta_P_h, delta_P_v, C_alpha, C_beta, C_errstat):
    """

    FILE        pressure_angle_incidence_cnrm.py

    VERSION     $Revision$

    CATEGORY    Thermodynamic

    PURPOSE     Calculate static pressure, error-corrected dynamic pressure, angle
                of attack and sideslip

    DESCRIPTION Calculates static pressure and dynamic pressure by correction of
                static error. Angle of attack and sideslip are calculated from the horizontal and vertical differential pressures.

    INPUT       P_sr        vector      hPa     raw static pressure
                delta_P_r   vector      hPa     raw dynamic pressure
                delta_P_h   vector      hPa     horizontal differential pressure
                delta_P_v   vector      hPa     vertical differential pressure
                C_alpha     coeff.[2]   ()      angle of attack calibration coeff.
                C_beta      coeff.[2]   ()      sideslip calibration coeff.
                C_errstat   coeff.[4]   ()      static error coefficients

    OUTPUT      P_s         vector      hPa     static pressure
                delta_P     vector      hPa     static error corrected dynamic pressure
                alpha       vector      rad     angle of attack
                beta        vector      rad     sideslip angle

    SOURCE      CNRM/GMEI/TRAMM

    REFERENCES

    """
    errstat25 = (C_errstat.value[0] + C_errstat.value[1] * 25 + C_errstat.value[2] * 25**2 +
                C_errstat.value[3] * 25 ** 3)

    errstat = zeros(P_sr.shape)


    errstat[delta_P_r.value > 25] = (C_errstat.value[0] + multiply(C_errstat.value[1], delta_P_r.value) +
                                multiply(C_errstat.value[2], power(delta_P_r.value, 2)) +
                                multiply(C_errstat.value[3], power(delta_P_r.value, 3)))
                                
    errstat[logical_and(delta_P_r.value > 0, delta_P_r.value <= 25)] = delta_P_r.value/25 * errstat25

    P_s_value = P_sr.value - errstat

 
    delta_P_value = delta_P_r.value + errstat

    alpha_value = C_alpha.value[0] + C_alpha.value[1] * delta_P_v.value / delta_P_value

    beta_value = C_beta.value[0] + C_beta.value[1] * delta_P_h.value / delta_P_value


    P_s = egads.EgadsData(value = P_s_value,
                               units = 'hPa',
                               long_name = 'static pressure',
                               standard_name = 'air_pressure',
                               fill_value = None,
                               valid_range = None,
                               sampled_rate = None,
                               category = None,
                               calibration_coeff = None,
                               dependencies = None,
                               processor = inspect.stack()[0][3],
                               processor_version = __version__,
                               processor_date = __date__)

    delta_P = egads.EgadsData(value = delta_P_value,
                               units = 'hPa',
                               long_name = 'dynamic pressure',
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

    alpha = egads.EgadsData(value = alpha_value,
                               units = 'rad',
                               long_name = 'angle of attack',
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
    beta = egads.EgadsData(value = beta_value,
                               units = 'rad',
                               long_name = 'sideslip angle',
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



    return P_s, delta_P, alpha, beta



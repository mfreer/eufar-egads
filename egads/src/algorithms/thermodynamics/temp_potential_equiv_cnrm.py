__author__ = "mfreer"
__date__ = "$Date$"
__version__ = "$Revision$"


import egads
import inspect

def temp_potential_equiv_cnrm(T_s, theta, r, c_pa):
    """

    FILE        temp_potential_equiv_cnrm.py

    VERSION     $Revision$

    CATEGORY    Thermodynamics

    PURPOSE     Calculates equivalent potential temperature

    DESCRIPTION Calculates equivalent potential temperature of air. The
                equivalent potential temperature is the temperature a parcel
                of air would reach if all water vapor in the parcel would
                condense, and the parcel was brought adiabatially to 1000 hPa.

    INPUT       T_s     vector      K or C      static temperature
                theta   vector      K or C      potential temperature
                r       vector      g/kg        water vapor mixing ratio
                c_pa    coeff.      J/kg/K      specific heat of dry air at
                                                constant pressure

    OUTPUT      theta_e vector      same unit as T_s    equivalent potential temperature

    SOURCE      CNRM/GMEI/TRAMM

    REFERENCES  Directly copied from the CAM routine which is identical to the
                algorithm P. Durand cited in the formula book created for PYREX.

    """

    L = 3136.17 - 2.34 * T_s.value

    theta_e = theta.value * (1 + r.value * L / (c_pa.value * T_s.value))


    result = egads.ToolboxData(value = theta_e,
                               units = 'K',
                               long_name = 'equivalent potential temperature',
                               standard_name = 'equivalent_potential_temperature',
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



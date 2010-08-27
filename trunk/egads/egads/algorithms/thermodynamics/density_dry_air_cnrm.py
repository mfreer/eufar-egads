__author__ = "mfreer"
__date__ = "$Date$"
__version__ = "$Revision$"


import egads
import inspect

def density_dry_air_cnrm(P_s, T_s):
    """
    FILE        density_dry_air_cnrm.py

    VERSION     $Revision$

    CATEGORY    Thermodynamics

    PURPOSE     Calculates density of dry air

    DESCRIPTION Calculates density of dry air given static temperature and
                pressure. If virtual temperature is used instead of static, this
                algorithm calculates density of humid air.

    INPUT       P_s     vector  hPa     static pressure
                T_s     vector  K or C  static temperature

    OUTPUT      rho     vector  kg/m3   density

    SOURCE      CNRM/GMEI/TRAMM

    REFERENCES  Equation of state for a perfect gas, Triplet-Roche, page 34.

    """

    R_a = 287.05 #J/kg/K

    rho = (P_s.value * 100) / (R_a * T_s.value)


    result = egads.EgadsData(value = rho,
                               units = 'kg/m3',
                               long_name = 'density',
                               standard_name = 'air_density',
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



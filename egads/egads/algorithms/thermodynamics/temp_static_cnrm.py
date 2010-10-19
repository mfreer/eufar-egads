__author__ = "mfreer"
__date__ = "$Date$"
__version__ = "$Revision$"
__all__ = ["temp_static_cnrm"]

import egads
import inspect

def temp_static_cnrm(Tt, dP, P_s, r_f, Racpa):
    """

    FILE        temp_static_cnrm.py

    VERSION     $Revision$

    CATEGORY    Thermodynamic

    PURPOSE     Calculate static temperature

    DESCRIPTION Calculates static temperature of the air based on total temperature and dynamic
                pressure

    INPUT       T_t         vector  K or C  total temperature
                dP          vector  hPa     dynamic pressure
                P_s         vector  hPa     static pressure
                r_f         coeff.  ()
                Racpa       coeff.  ()      R_a/c_pa

    OUTPUT      T_s         vector  K       static temperature

    SOURCE      CNRM/GMEI/TRAMM

    REFERENCES

    """


    T_s = Tt.value / (1 + r_f.value * ((1 + dP.value / P_s.value)
                                   ** Racpa.value - 1))

    result = egads.EgadsData(value = T_s,
                               units = 'K',
                               long_name = 'static temperature',
                               standard_name = 'air_temperature',
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



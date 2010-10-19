__author__ = "mfreer"
__date__ = "$Date::                  $"
__version__ = "$Revision::           $"
__all__ = ["temp_virtual_cnrm"]

import egads
import inspect

def temp_virtual_cnrm(T_s, r):
    """

    FILE        temp_virtual_cnrm.py

    VERSION     $Revision$

    CATEGORY    Thermodynamics

    PURPOSE     Calculate virtual temperature

    DESCRIPTION Calculates virtual temperature given static pressure and mixing ratio.

    INPUT       T_s     vector      K or C      static temperature
                r       vector      g/kg        water vapor mixing ratio

    OUTPUT      T_v     vector      same units as T_s   virtual temperature

    SOURCE      CNRM/GMEI/TRAMM

    REFERENCES  Triplet-Roche, page 56.

    """
    
    RvRa = 1.608

    T_v = T_s.value * (1 + RvRa * r.value) / (1 + r.value)



    result = egads.EgadsData(value = T_v,
                               units = 'K',
                               long_name = 'virtual temperature',
                               standard_name = 'virtual_temperature',
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


if __name__=="__main__":
    import doctest
    doctest.testmod()
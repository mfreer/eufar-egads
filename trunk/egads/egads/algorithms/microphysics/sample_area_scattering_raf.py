__author__ = "mfreer"
__date__ = "$Date::                  $"
__version__ = "$Revision::           $"
__all__ = ['sample_area_scattering_raf']

import egads
import inspect

def sample_area_scattering_raf(DOF, BD):
    """

    FILE        sample_area_scattering_raf.py

    VERSION     $Revision$

    CATEGORY    Microphysics

    PURPOSE     Calculation of sampling area for scattering probes

    DESCRIPTION Calculation of sampling area for scattering probes such as the FSSP,
                CAS, CIP, etc., given depth of field and beam diameter.

    INPUT       DOF     coeff.      m   Depth of field
                BD      coeff.      m   Beam diameter

    OUTPUT      SA      coeff.      m2  Sample area

    SOURCE      NCAR-RAF

    REFERENCES  NCAR-RAF Bulletin No. 24

    """

    SA = DOF.value * BD.value


    result = egads.EgadsData(value = SA,
                               units = 'm2',
                               long_name = 'sample area',
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



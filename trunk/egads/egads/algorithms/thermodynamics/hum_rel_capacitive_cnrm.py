__author__ = "mfreer"
__date__ = "$Date$"
__version__ = "$Revision$"
__all__ = ["hum_rel_capacitive_cnrm"]

from numpy import multiply, power
import scipy

import egads
import inspect

def hum_rel_capacitive_cnrm(Ucapf, T_s, P_s, dP, C_t, Fmin, C_0, C_1, C_2):
    """

    FILE        hum_rel_capacitive_cnrm.py

    VERSION     $Revision$

    CATEGORY    Thermodynamics

    PURPOSE     Calculate relative humidity from capacitive probe

    DESCRIPTION Calculates relative humidity of the air based on the frequency
                of the capacitive probe.

    INPUT       Ucapf       vector  Hz      output frequency of capacitive probe
                T_s         vector  C       Static temperature
                P_s         vector  hPa     static pressure
                dP          vector  hPa     dynamic pressure
                C_t         coeff.  %/C     temperature correction coefficient
                Fmin        coeff.  Hz      minimal acceptible frequency
                C_0         coeff.  ()      calibration law 0th degree coefficient
                C_1         coeff.  ()      calibration law 1st degree coefficient
                C_2         coeff.  ()      calibration law 2nd degree coefficient

    OUTPUT      H_u         vector  %       relative humidity

    SOURCE      CNRM/GMEI/TRAMM

    REFERENCES

    """

    tempUcapf = scipy.array(Ucapf.value)
    tempUcapf[tempUcapf < Fmin.value] = Fmin.value
    Ucapf.value = tempUcapf.tolist()

    H_u = P_s.value / (P_s.value + dP.value) * (C_0.value +
                                                         multiply(C_1.value, Ucapf.value) +
                                                         multiply(C_2.value, power(Ucapf.value, 2)) +
                                                         multiply(C_t.value, (T_s.value - 20.0)))



    result = egads.EgadsData(value = H_u,
                               units = '%',
                               long_name = 'relative humidity',
                               standard_name = 'relative_humidity',
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



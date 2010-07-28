
__author__ = "freer"
__date__ = "$Date: 2009-11-26 15:34:16 +0100 (Thu, 26 Nov 2009) $"
__version__ = "$Revision: 20 $"


from numpy import multiply, power
import scipy

import egads

def hum_rel_capacitve_cnrm(Ucapf, T_s, P_s, dP, C_t, Fmin, C_0, C_1, C_2):
    """
    FILE        hum_rel_capacitive_cnrm.py

    VERSION     $Revision: 20 $

    CATEGORY    Thermodynamics

    PURPOSE     Calculate relative humidity from capacitive probe

    DESCRIPTION Calculates relative humidity of the air based on the frequency
                of the capacitive probe.

    INPUT       Ucapf       Hz      output frequency of capacitive probe
                T_s         C       Static temperature
                P_s         hPa     static pressure
                dP          hPa     dynamic pressure
                C_t         %/C     temperature correction coefficient
                Fmin        Hz      minimal acceptible frequency
                C_0         ()      calibration law 0th degree coefficient
                C_1         ()      calibration law 1st degree coefficient
                C_2         ()      calibration law 2nd degree coefficient

    OUTPUT      H_u         %       relative humidity

    SOURCE      CNRM/GMEI/TRAMM

    REFERENCES

    """

    name = 'hum_rel_capacitive_cnrm'
    inputs = 'capacitive frequency [Hz], static temperature [K or C], \
                    static pressure [hPa], dynamic pressure [hPa], \
                    temperature correction coefficient [%/C], \
                    minimum acceptible frequency [Hz], 0th degree coeff., \
                    1st degree coeff., 2nd degree coeff'
    outputs = 'relative humidity [%]'



    tempUcapf = scipy.array(Ucapf.value)
    tempUcapf[tempUcapf < Fmin.value] = Fmin.value
    Ucapf.value = tempUcapf.tolist()

    H_u = P_s.value / (P_s.value + dP.value) * (C_0.value +
                                                         multiply(C_1.value, Ucapf.value) +
                                                         multiply(C_2.value, power(Ucapf.value, 2)) +
                                                         multiply(C_t.value, (T_s.value - 20.0)))

    result = egads.ToolboxData(value = H_u,
                               units = '%',
                               long_name = 'relative humidity',
                               standard_name = 'relative humidity')


    result.units = '%'
    result.long_name = 'relative humidity'
    result.processor = __name__
    result.processor_version = __version__
    result.processor_date = __date__



    return result



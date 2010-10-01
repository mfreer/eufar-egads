__author__ = "mfreer"
__date__ = "$Date: 2010-08-27 17:53:04 +0200 (Fri, 27 Aug 2010) $"
__version__ = "$Revision: 15 $"
__all__ = ['sample_volume_general_raf']

import egads
import inspect

def sample_volume_general_raf(V_t, SA, t_s):
    """

    FILE        sample_volume_general_raf.py

    VERSION     $Revision: 15 $

    CATEGORY    Microphysics

    PURPOSE     Calculate sample volume for microphysics probes.

    DESCRIPTION Calculate sample volume for microphysics probes given true air
                speed, probe sample area and sample rate.

    INPUT       V_t     vector[time]    m/s     True air speed
                SA      vector[bins]    m2      Probe sample area
                t_s     coeff           s       Probe sample rate

    OUTPUT      SV      array[time, bins]   m3  Sample volume

    SOURCE      NCAR-RAF

    REFERENCES  NCAR-RAF Bulletin No. 24

    """

    
    SV = V_t.value * SA.value.transpose() * t_s.value

    result = egads.EgadsData(value = SV,
                               units = 'm3',
                               long_name = 'sample volume',
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



__author__ = "mfreer"
__date__ = "$Date::                  $"
__version__ = "$Revision::           $"
__all__ = ['number_conc_total_raf']

import egads
import inspect

def number_conc_total_raf(n_i, SV):
    """

    FILE        number_conc_total_raf.py

    VERSION     $Revision$

    CATEGORY    Microphysics

    PURPOSE     Calculates total number concentration for a particle probe

    DESCRIPTION Calculates total number concentration for a generic particle
                probe given counts for each bin and probe sample volume.

    INPUT       n_i     array[time, bins]   ()      Particle counts in each bin over time
                SV      array[time, bins]   m3      Sample volume for each bin over time

    OUTPUT      N_t     vector[time]        m-3     Total number concentration

    SOURCE      NCAR-RAF

    REFERENCES  NCAR-RAF Bulletin No. 24

    """

    n_shape = n_i.value.shape
    
    time = n_shape[0]

    for t in xrange(time):
        N_t = sum(n_i.value[t,:]/SV.value[t,:])

    result = egads.ToolboxData(value = N_t,
                               units = 'm-3',
                               long_name = 'total number concentration',
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



__author__ = "mfreer"
__date__ = "$Date::                  $"
__version__ = "$Revision::           $"
__all__ = ['diameter_mean_raf']

import egads
import inspect

def diameter_mean_raf(n_i, d_i):
    """
    This file calculates mean diameter given an array of particle counts and
    a vector of their corresponding sizes.

    FILE        diameter_mean_raf.py

    VERSION     $Revision$

    CATEGORY    Microphysics

    PURPOSE     Calculates mean diameter of particles.

    DESCRIPTION Calculates mean diameter of particles given an array of particle
                counts and a vector of their corresponding sizes, using the methods
                given in the NCAR RAF Bulletin #24

    INPUT       n_i     array[time, bins]   ()  Particle counts in each bin over time
                d_i     vector[bins]        um  Diameter of each channel

    OUTPUT      D_bar       vector[time]        um  Mean diameter

    SOURCE      NCAR-RAF

    REFERENCES  NCAR-RAF Bulletin No. 24

    """

    N_t = n_i.value.sum(1)

    n_shape = n_i.value.shape

    time = n_shape[0]

    D_bar = []

    for t in xrange(time):
        D_bar[t] = sum(n_i.value[t, :] * d_i.value[:]) / (N_t[t])

    result = egads.EgadsData(value = D_bar,
                               units = 'um',
                               long_name = 'mean diameter',
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



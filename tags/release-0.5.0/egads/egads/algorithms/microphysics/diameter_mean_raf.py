__author__ = "mfreer"
__date__ = "$Date::                  $"
__version__ = "$Revision::           $"
__all__ = ['DiameterMeanRaf']

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata

class DiameterMeanRaf(egads_core.EgadsAlgorithm):
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

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'um',
                                                               'long_name':'mean diameter',
                                                               'standard_name':'',
                                                               'Category':['PMS Probe']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['n_i', 'd_i'],
                                                          'InputUnits':['', 'um'],
                                                          'Outputs':['D_bar'],
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)



    def run(self, n_i, d_i):

        return egads_core.EgadsAlgorithm.run(self, n_i, d_i)

    def _algorithm(self, n_i, d_i):

        N_t = n_i.sum(1)

        n_shape = n_i.shape

        time = n_shape[0]

        D_bar = []

        for t in xrange(time):
            D_bar[t] = sum(n_i[t, :] * d_i[:]) / (N_t[t])


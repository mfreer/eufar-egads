__author__ = "mfreer"
__date__ = "$Date::                  $"
__version__ = "$Revision::           $"
__all__ = ['NumberConcTotalRaf']

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata

class NumberConcTotalRaf(egads_core.EgadsAlgorithm):
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

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'m-3',
                                                               'long_name':'total number concentration',
                                                               'standard_name':'',
                                                               'Category':['PMS Probe']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['n_i', 'SV'],
                                                          'InputUnits':['', 'm3'],
                                                          'Outputs':['N_t'],
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)


    def run(self, n_i, SV):

        return egads_core.EgadsAlgorithm.run(self, n_i, SV)

    def _algorithm(self, n_i, SV):


        n_shape = n_i.shape

        time = n_shape[0]

        for t in xrange(time):
            N_t = sum(n_i[t,:]/SV[t,:])

        return N_t


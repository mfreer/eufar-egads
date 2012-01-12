__author__ = "mfreer"
__date__ = "$Date::                  $"
__version__ = "$Revision::           $"
__all__ = ['SampleVolumeGeneralRaf']

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata

class SampleVolumeGeneralRaf(egads_core.EgadsAlgorithm):
    """

    FILE        sample_volume_general_raf.py

    VERSION     $Revision$

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
    
    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'m3',
                                                               'long_name':'sample volume',
                                                               'standard_name':'',
                                                               'Category':['PMS Probe']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['V_t','SA','t_s'],
                                                          'InputUnits':['m/s','m2', 's'],
                                                          'Outputs':['SV'],
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)



    def run(self, V_t, SA, t_s):

        return egads_core.EgadsAlgorithm.run(self, V_t, SA, t_s)
    

    def _algorithm(self, V_t, SA, t_s):

        SV = V_t * SA.transpose() * t_s

        return SV

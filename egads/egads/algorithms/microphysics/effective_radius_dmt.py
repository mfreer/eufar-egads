__author__ = "mfreer"
__date__ = "$Date::                  $"
__version__ = "$Revision::           $"
__all__ = ['']

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata

class EffectiveRadiusDmt(egads_core.EgadsAlgorithm):

    """
    FILE        effective_radius_dmt.py

    VERSION     $Revision$

    CATEGORY    Microphysics

    PURPOSE     Calculation of effective radius of a size distribution.

    DESCRIPTION This algorithm calculates the effective radius given a size distribution.
                In general, this definition is only meaningful for water clouds.

    INPUT       n_i    array[time, bins]    cm-3    number concentration of hydrometeors
                                                    in size category i
                d_i    vector[bins]         um      average diameter in size category i

    OUTPUT      r

    SOURCE      sources

    REFERENCES

    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'%',
                                                               'long_name':'template',
                                                               'standard_name':'',
                                                               'Category':['']})


        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':[''],
                                                          'InputUnits':[''],
                                                          'Outputs':['template'],
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)


    def run(self, inputs):

        return egads_core.EgadsAlgorithm.run(self, inputs)


    def _algorithm(self, inputs):

        return result



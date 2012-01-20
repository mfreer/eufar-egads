__author__ = "mfreer"
__date__ = "$Date::                  $"
__version__ = "$Revision::           $"
__all__ = ['']

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata

class AlgorithmTemplate(egads_core.EgadsAlgorithm):
    """
    This file provides a template for creation of EGADS algorithms.

    FILE        algorithm_template.py

    VERSION     $Revision$

    CATEGORY    None

    PURPOSE     Template for EGADS algorithm files

    DESCRIPTION ...

    INPUT       inputs      units   description

    OUTPUT      outputs     units   description

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

        ## Do processing here:


        return result



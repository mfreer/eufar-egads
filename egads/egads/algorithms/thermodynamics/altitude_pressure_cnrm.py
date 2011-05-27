__author__ = "mfreer"
__date__ = "$Date::                  $"
__version__ = "$Revision::           $"
__all__ = ["AltitudePressureCnrm"]

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata

from numpy import log

class AltitudePressureCnrm(egads_core.EgadsAlgorithm):
    """

    FILE        altitude_pressure_cnrm.py

    VERSION     $Revision$

    CATEGORY    Thermodymics

    PURPOSE     Calculate pressure altitude

    DESCRIPTION Calculate pressure altitude using virtual temperature

    INPUT       T_v         vector  K or C  virtual temperature
                P_s         vector  hPa     static pressure
                P_surface   coeff.  hPa     surface pressure
                R_a_g       coeff           Gas constant of air divided by gravity

    OUTPUT      alt_p       vector  m       pressure altitude

    SOURCE      CNRM/GMEI/TRAMM

    REFERENCES
    """
    
    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'m',
                                                               'long_name':'pressure altitude',
                                                               'standard_name':'',
                                                               'Category':['Thermodynamic','Aircraft State']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['T_v', 'P_s', 'P_surface', 'R_a_g'],
                                                          'InputUnits':['K','hPa','hPa',''],
                                                          'Outputs':['alt_p'],
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)



    def run(self, T_v, P_s, P_surface, R_a_g):

        return egads_core.EgadsAlgorithm.run(self, T_v, P_s, P_surface, R_a_g)


    def _algorithm(self, T_v, P_s, P_surface, R_a_g):

        alt_p = R_a_g * T_v * log(P_surface / P_s)

        return alt_p

import egads.core.metadata as egads_metadata

__author__ = "mfreer"
__date__ = "$Date::                  $"
__version__ = "$Revision::           $"
__all__ = ["AltitudePressureCnrm"]

import egads
import inspect
from numpy import log

doc = """

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


class AltitudePressureCnrm(egads.EgadsAlgorithm):
    __doc__ = doc
    
    def __init__(self):
        egads.EgadsAlgorithm.__init__(self)

        self.alt_p_metadata = egads_metadata.VariableMetadata({'units':'m',
                                                               'long_name':'pressure altitude',
                                                               'standard_name':'',
                                                               'Category':['Thermodynamic','Aircraft State']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['T_v', 'P_s', 'P_surface', 'R_a_g'],
                                                          'InputUnits':['K','hPa','hPa',''],
                                                          'Outputs':['alt_p'],
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.time_stamp()},
                                                          self.alt_p_metadata)



    def run(self, T_v, P_s, P_surface, R_a_g, return_EGADS=True):
        self.__doc__ = __doc__

        alt_p = self._call_algorithm(T_v, P_s, P_surface,
                                       R_a_g)

        if return_EGADS:
            result = egads.EgadsData(alt_p, self.alt_p_metadata)
        else:
            result = alt_p

        return result


    def _algorithm(self, T_v, P_s, P_surface, R_a_g):
        self.__doc__ = doc


        alt_p = R_a_g * T_v * log(P_surface / P_s)

        return alt_p
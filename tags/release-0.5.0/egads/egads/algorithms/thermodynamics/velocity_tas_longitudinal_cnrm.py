__author__ = "mfreer"
__date__ = "$Date::                  $"
__version__ = "$Revision::           $"
__all__ = ["VelocityTasLongitudinalCnrm"]

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata

from numpy import sqrt, tan


class VelocityTasLongitudinalCnrm(egads_core.EgadsAlgorithm):
    """

    FILE        velocity_tas_longitudinal_cnrm.py

    VERSION     $Revision$

    CATEGORY    Thermodynamics

    PURPOSE     Calculates the longitudinal true air speed

    DESCRIPTION Calculates the true air speed along the longitudinal axis of the
                aircraft.

    INPUT       V_t     vector  m/s     true air speed
                alpha   vector  rad     angle of attack
                beta    vector  rad     sideslip angle

    OUTPUT      V_tx    vector  m/s     longitudinal true airspeed

    SOURCE      CNRM/GMEA/TRAMM

    REFERENCES  NCAR-RAF Bulletin #23

    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'m/s',
                                                               'long_name':'longitudinal true air speed',
                                                               'standard_name':'',
                                                               'Category':['Thermodynamic','Aircraft State']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['V_t', 'alpha', 'beta'],
                                                          'InputUnits':['m/s','rad','rad'],
                                                          'Outputs':['V_tx'],
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)

    def run(self, V_t, alpha, beta):

        return egads_core.EgadsAlgorithm.run(self, V_t, alpha, beta)


    def _algorithm(self, V_t, alpha, beta):

        V_tx = V_t / sqrt(1 + tan(alpha) ** 2 + tan(beta) ** 2)

        return V_tx





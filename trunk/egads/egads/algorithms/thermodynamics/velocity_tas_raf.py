__author__ = "mfreer"
__date__ = "$Date::                  $"
__version__ = "$Revision::           $"
__all__ = ['VelocityTasRaf']


import numpy

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata


class VelocityTasRaf(egads_core.EgadsAlgorithm):

    """
    FILE        velocity_tas_raf.py

    VERSION     $Revision$

    CATEGORY    Thermodynamics

    PURPOSE     Calculates true air speed based on Mach number, measured temperature
                and thermometer recovery factor.

    DESCRIPTION Calculation of true air speed given Mach number, measured temperature
                and thermometer recovery factor. Typical values of thermometer
                recovery value range from 0.75-0.9 for platinum wire ratiometer 
                (flash bulb type) thermometers, and around 1.0 for TAT type thermometers.

    INPUT       T_r    vector[time]    K    measured temperature
                M      vector[time]    _    mach number
                e      coeff           _    thermometer recovery factor
    
    OUTPUT      V_t    vector[time]    m/s  true air speed

    SOURCE      NCAR-EOL

    REFERENCES  NCAR-RAF Bulletin #23

    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)


        self.output_metadata = egads_metadata.VariableMetadata({'units':'m/s',
                                                               'long_name':'true air speed',
                                                               'standard_name':'platform_speed_wrt_air',
                                                               'Category':['Aircraft State']})


        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['T_r', 'M', 'e'],
                                                          'InputUnits':['K', '', ''],
                                                          'Outputs':['V_t'],
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)


    def run(self, T_r, M, e):

        return egads_core.EgadsAlgorithm.run(self, T_r, M, e)

    def _algorithm(self, T_r, M, e):

        R = 287.04 # J/kg/K
        gamma = 1.4

        V_t = numpy.sqrt(R * gamma * T_r * M ** 2 / (1.0 + 0.5 * (gamma - 1) * e * M ** 2))


        return V_t


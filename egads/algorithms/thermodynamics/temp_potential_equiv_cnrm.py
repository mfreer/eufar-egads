__author__ = "mfreer"
__date__ = "$Date::                  $"
__version__ = "$Revision::           $"
__all__ = ["TempPotentialEquivCnrm"]

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata


class TempPotentialEquivCnrm(egads_core.EgadsAlgorithm):
    """

    FILE        temp_potential_equiv_cnrm.py

    VERSION     $Revision$

    CATEGORY    Thermodynamics

    PURPOSE     Calculates equivalent potential temperature

    DESCRIPTION Calculates equivalent potential temperature of air. The
                equivalent potential temperature is the temperature a parcel
                of air would reach if all water vapor in the parcel would
                condense, and the parcel was brought adiabatially to 1000 hPa.

    INPUT       T_s     vector      K or C      static temperature
                theta   vector      K or C      potential temperature
                r       vector      g/kg        water vapor mixing ratio
                c_pa    coeff.      J/kg/K      specific heat of dry air at
                                                constant pressure

    OUTPUT      theta_e vector      same unit as T_s    equivalent potential temperature

    SOURCE      CNRM/GMEI/TRAMM

    REFERENCES  Directly copied from the CAM routine which is identical to the
                algorithm P. Durand cited in the formula book created for PYREX.

    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'K',
                                                               'long_name':'equivalent potential temperature',
                                                               'standard_name':'equivalent_potential_temperature',
                                                               'Category':['Thermodynamic','Atmos State']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['T_s', 'theta', 'r', 'c_pa'],
                                                          'InputUnits':['K','K','g/kg','J/kg/K'],
                                                          'Outputs':['theta_e'],
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)


    def run(self, T_s, theta, r, c_pa):

        return egads_core.EgadsAlgorithm.run(self, T_s, theta, r, c_pa)


    def _algorithm(self, T_s, theta, r, c_pa):
        L = 3136.17 - 2.34 * T_s

        theta_e = theta * (1 + r * L / (c_pa * T_s))

        return theta_e




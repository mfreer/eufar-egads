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

__author__ = "mfreer"
__date__ = "$Date::                  $"
__version__ = "$Revision::           $"
__all__ = ["AltitudePressureCnrm"]

import egads
import inspect
from numpy import log


class AltitudePressureCnrm(egads.EgadsAlgorithm):

    def __init__(self):
        egads.EgadsAlgorithm.__init__(self)

        self.version = __version__
        self.date = __date__
        self.inputs = ['T_v', 'P_s', 'P_surface', 'R_a_g']
        self.outputs = ['alt_p']

        self.output_properties['units'] = 'm'
        self.output_properties['long_name'] = 'pressure altitude'
        self.output_properties['standard_name'] = ''
        self.output_properties['fill_value'] = None
        self.output_properties['valid_range'] = None
        self.output_properties['sampled_rate'] = None
        self.output_properties['category'] = ['Thermodynamic','Aircraft State']
        self.output_properties['calibration_coeff'] = None
        self.output_properties['dependencies'] = None
        self.output_properties['processor'] = self.name
        self.output_properties['processor_version'] = __version__
        self.output_properties['processor_date'] = __date__



    def run(self, T_v, P_s, P_surface, R_a_g):
        self.__doc__ = altitude_pressure_cnrm.__doc__

        alt_p = altitude_pressure_cnrm(T_v.value, P_s.value, P_surface.value,
                                       R_a_g.value)

        result = self._populate_data_object(alt_p)

        return result


def altitude_pressure_cnrm(T_v, P_s, P_surface, R_a_g):

    alt_p = R_a_g * T_v * log(P_surface / P_s)

    return alt_p
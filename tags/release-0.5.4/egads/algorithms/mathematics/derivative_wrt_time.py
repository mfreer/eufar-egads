__author__ = "mfreer"
__date__ = "$Date::                  $"
__version__ = "$Revision::           $"
__all__ = ['DerivativeWrtTime']

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata

class DerivativeWrtTime(egads_core.EgadsAlgorithm):
    """

    FILE        derivative_wrt_time.py

    VERSION     $Revision$

    CATEGORY    Mathematics

    PURPOSE     Calculate first derivative of a generic parameter

    DESCRIPTION Calculates the first derivative of a generic parameter wrt time. Calculations
                of this derivative are centered for all except the first and last values in the vector
                (Nones are returned for these values). Returns None for scalar parameters.

    INPUT       x        vector        _                    Parameter to calculate first derivative
                t        vector        s                    Time signal 

    OUTPUT      x_dot    vector        units of 'x'/s       First derivative of x

    SOURCE      sources

    REFERENCES

    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'input0/s',
                                                               'long_name':'first derivative of input0',
                                                               'standard_name':'',
                                                               'Category':['']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['x', 't'],
                                                          'InputUnits':[None, 's'],
                                                          'Outputs':['x_dot'],
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)

    def run(self, x, t):

        return egads_core.EgadsAlgorithm.run(self, x, t)

    def _algorithm(self, x, t):

        x_dot = []

        for i, x_elem in enumerate(x):
            i_up = i + 1
            i_down = i - 1

            if i_down < 0:
                i_down = 0
            if i_up >= len(x):
                i_up = len(x) - 1

            x_dot.append((x[i_up] - x[i_down]) / (t[i_up] - t[i_down]))


        return x_dot


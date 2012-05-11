__author__ = "mfreer"
__date__ = "$Date:: 2012-02-03 17:40#$"
__version__ = "$Revision:: 118       $"
__all__ = ['InterpolationLinear']

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata

class InterpolationLinear(egads_core.EgadsAlgorithm):
    """

    FILE        interpolation_linear.py

    VERSION     $Revision: 118 $

    CATEGORY    Transforms

    PURPOSE     Calculate linear interpolation of a variable.

    DESCRIPTION Calculates the one-dimensional piecewise linear interpolation 
                of a variable between two coordinate systems.

    INPUT       x            vector            _    x-coordinates of the data 
                                                    points (must be increasing)
                f            vector            _    data points to interpolate
                x_interp     vector            _    new set of coordinates to use in interpolation
                f_left       coeff, optional   _    value to return for x_interp < x[0]. 
                                                    default is f[0]
                f_right      coeff, optional   _    value to return when x_interp > x[-1]. 
                                                    default is f[-1]
                                                    
    OUTPUT      f_interp     vector            _    interpolated values of f

    SOURCE      sources

    REFERENCES

    """

    def __init__(self, return_Egads=True):

        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'%',
                                                               'long_name':'template',
                                                               'standard_name':'',
                                                               'Category':['']})

        # 3 cont. Complete metadata with parameters specific to algorithm, including
        #         a list of inputs, a corresponding list of units, and the list of 
        #         outputs.
        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':[''],
                                                          'InputUnits':[''],
                                                          'Outputs':['template'],
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)

    # 4. Replace the 'inputs' parameter in the three instances below with the list
    #    of input parameters to be used in the algorithm.
    def run(self, inputs):

        return egads_core.EgadsAlgorithm.run(self, inputs)

    # 5. Implement algorithm in this section.
    def _algorithm(self, inputs):

        ## Do processing here:


        return result



__author__ = "mfreer"
__date__ = "$Date::                  $"
__version__ = "$Revision::           $"
__all__ = ['DiameterMedianVolumeDmt']

import numpy

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata



class DiameterMedianVolumeDmt(egads_core.EgadsAlgorithm):

    """


    FILE        diameter_median_volume_dmt.py

    VERSION     $Revision$

    CATEGORY    Microphysics

    PURPOSE     Calculation of median volume diameter

    DESCRIPTION Calculates the median volume diameter given a size distribution. 
                The median volume  diameter is the size of droplet below which 
                50% of the total water volume resides.

    INPUT       n_i    array[time,bins]        cm-3   number concentration of 
                                                      hydrometeors in bin i
                d_i    vector[bins]            um     average diameter of bin i
                rho_i  vector[bins], optional  g cm-3 density of hydrometeor in bin i
                                                      default is 1.0 g/cm^3
                                                      
    OUTPUT      D_mvd  vector[time]            um     median volume diameter

    SOURCE      

    REFERENCES  "Data Analysis User's Guide", Droplet Measurement Technologies, 2009,
                44 pp.

    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)


        self.output_metadata = egads_metadata.VariableMetadata({'units':'um',
                                                               'long_name':'median volume diameter',
                                                               'standard_name':'',
                                                               'Category':['Microphysics']})


        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['n_i', 'd_i', 'rho_i'],
                                                          'InputUnits':['cm^-3', 'um', 'g/cm^3'],
                                                          'Outputs':['D_mvd'],
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)


    def run(self, n_i, d_i, rho_i=1.0):

        return egads_core.EgadsAlgorithm.run(self, n_i, d_i, rho_i)

    def _algorithm(self, n_i, d_i, rho_i):

        rho_i = numpy.array(rho_i)
        if len(rho_i) == 1:
            rho_i = numpy.ones(len(d_i)) * rho_i

        LWC_alg = egads.algorithms.microphysics.MassConcDmt(return_Egads=False)

        LWC_total = LWC_alg.run(n_i, d_i, rho_i)

        LWC_i = []
        S_n = numpy.zeros(len(n_i))
        i = 0
        while S_n < 0.5 * LWC_total and i <= len(d_i):
            LWC_i.append(LWC_alg.run(n_i[:][i], d_i[i], rho_i[i]))
            S_n += LWC_i[i]
            i = i + 1

        i = i - 1

        S_n1 = numpy.sum(LWC_i[:i - 1])

        D_mvd = d_i[i - 1] + (0.5 - S_n1 / S_n) * (d_i[i] - d_i[i - 1])



        return D_mvd



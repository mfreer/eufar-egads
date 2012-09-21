__author__ = "mfreer"
__date__ = "$Date::                  $"
__version__ = "$Revision::           $"
__all__ = ['CompareParamLcss']

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata

import numpy

class CompareParamLcss(egads_core.EgadsAlgorithm):

    """
    This file provides a template for creation of EGADS algorithms.

    FILE        algorithm_template.py

    VERSION     $Revision$

    CATEGORY    None

    PURPOSE     Template for EGADS algorithm files

    DESCRIPTION ...

    INPUT       inputs    var_type      units   description

    OUTPUT      outputs   var_type      units   description

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

    def run(self, R, S, epsilon):

        return egads_core.EgadsAlgorithm.run(self, R, S, epsilon)

    def _algorithm(self, R, S, epsilon):

        m = len(R)
        n = len(S)
        d = R.ndim


        if R.min(0) < S.min(0):
            data_min = R.min(0)
        else:
            data_min = S.min(0)

        if R.max(0) > S.max(0):
            data_max = R.max(0)
        else:
            data_max = S.max(0)

        if d > 1:
            G_shape = []
            G_coords = []
            for k in range(d + 1):
                G_shape.append(((data_max[k] + 3 * epsilon) - (data_min[k] - epsilon)) / epsilon)
                G_coords.append(numpy.arange(data_min[k] - epsilon, data_max[k] + 3 * epsilon, epsilon))

            G = numpy.ndarray(tuple(G_shape), dtype=list)

        else:
            G_shape = ((data_max + 3 * epsilon) - (data_min - epsilon)) / epsilon
            G_coords = numpy.arange(data_min - epsilon, data_max + 3 * epsilon, epsilon)
            G = numpy.ndarray(G_shape, dtype=list)




        for item, data in numpy.ndenumerate(G): G[item] = []


#        M = numpy.zeros(R.shape)
        for i in range(m):


            if d > 1:
                nearest_idx = []
                nearest_idx_up = []
                nearest_idx_down = []
                for k in range(d):
                    nearest_idx.append(numpy.abs(R[i, k] - G_coords[:, k]).argmin())
                    nearest_idx_up.append(numpy.abs(R[i, k] + epsilon - G_coords[:, k]).argmin())
                    nearest_idx_down.append(numpy.abs(R[i, k] - epsilon - G_coords[:, k]).argmin())

                for k in range(d):
                    G[tuple(nearest_idx)].append(i)
                    G[tuple(nearest_idx_up)].append(i)
                    G[tuple(nearest_idx_down)].append(i)

            else:
                nearest_idx = numpy.abs(R[i] - G_coords[:]).argmin()
                nearest_idx_up = numpy.abs(R[i] + epsilon - G_coords[:]).argmin()
                nearest_idx_down = numpy.abs(R[i] - epsilon - G_coords[:]).argmin()

                G[nearest_idx].append(i)
                G[nearest_idx_up].append(i)
                G[nearest_idx_down].append(i)



        L = numpy.ndarray(n, dtype=list)
        for item, data in numpy.ndenumerate(L): L[item] = []


        for i in range(n):
            if d > 1:
                nearest_idx = []
                for k in range(d):
                    nearest_idx.append(numpy.abs(S[i, k] - G_coords[:, k]).argmin())

                for item in G[tuple(nearest_idx)]:
                    all_flag = True
                    for k in range(d):
                        if abs(S[i, k] - R[item[k], k]) >= epsilon:
                            all_flag = False
                            break

                    if all_flag is True:
                        L[i].append(item[k])

            else:
                nearest_idx = numpy.abs(S[i] - G_coords[:]).argmin()

                for item in G[nearest_idx]:
                    all_flag = True
                    if abs(S[i] - R[item]) >= epsilon:
                        all_flag = False
                        break

                    if all_flag is True:
                        L[i].append(item)

        matches = numpy.zeros(n)

        matches.fill(m)
        matches[0] = 0

        max = 0

        for j in range(n):
            c = 0
            temp = matches[0]

            for k in L[j]:
                if temp < k:
                    while matches[c] < k:
                        c += 1

                    temp = matches[c]
                    matches[c] = k

                    if c > max:
                        max = c


        return max



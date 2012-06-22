__author__ = "mfreer"
__date__ = "$Date::                  $"
__version__ = "$Revision::           $"
__all__ = ['']

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata


class IsoDateTimeToElements(egads_core.EgadsAlgorithm):

    """
    FILE        iso_datetime_to_elements.py

    VERSION     $Revision$

    CATEGORY    Transforms

    PURPOSE     Splits a series of ISO string date-times (yyyymmddThhmmss or similar)
                into composant values.

    DESCRIPTION ...

    INPUT       date_time    vector    yyyymmddThhmmss    ISO date-time string

    OUTPUT      year         vector    _                  year
                month        vector    _                  month
                day          vector    _                  day
                hour         vector    _                  hour
                minute       vector    _                  minute
                second       vector    _                  second

    SOURCE      sources

    REFERENCES

    """
# TODO: complete section below - currently is just code skeleton
#    def __init__(self, return_Egads=True):
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


    def run(self, inputs):

        return egads_core.EgadsAlgorithm.run(self, inputs)

    # 5. Implement algorithm in this section.
    def _algorithm(self, inputs):

        year = numpy.array([], 'i')
        month = numpy.array([], 'i')
        day = numpy.array([], 'i')
        hour = numpy.array([])

        print date_time, date_time.__class__, len(date_time)

        for element in date_time:
            date_time_sep = dateparser.parse(str(element))

            year = numpy.append(year, date_time_sep.year)
            month = numpy.append(month, date_time_sep.month)
            day = numpy.append(day, date_time_sep.day)
            hour = numpy.append(hour,
                                date_time_sep.hour +
                                date_time_sep.minute / 60.0 +
                                date_time_sep.second / 3600.0)


        return result



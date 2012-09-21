__author__ = "mfreer"
__date__ = "$Date::                  $"
__version__ = "$Revision::           $"
__all__ = ['IsotimeToElements']

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata

import datetime
import dateutil.parser

class IsotimeToElements(egads_core.EgadsAlgorithm):

    """
    FILE        isotime_to_elements.py

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
    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = []
        self.output_metadata.append(egads_metadata.VariableMetadata({'units':'',
                                                               'long_name':'year',
                                                               'standard_name':'',
                                                               'Category':['']}))

        self.output_metadata.append(egads_metadata.VariableMetadata({'units':'',
                                                               'long_name':'month',
                                                               'standard_name':'',
                                                               'Category':['']}))

        self.output_metadata.append(egads_metadata.VariableMetadata({'units':'',
                                                               'long_name':'day',
                                                               'standard_name':'',
                                                               'Category':['']}))

        self.output_metadata.append(egads_metadata.VariableMetadata({'units':'hour',
                                                               'long_name':'hour',
                                                               'standard_name':'',
                                                               'Category':['']}))

        self.output_metadata.append(egads_metadata.VariableMetadata({'units':'min',
                                                               'long_name':'minute',
                                                               'standard_name':'',
                                                               'Category':['']}))

        self.output_metadata.append(egads_metadata.VariableMetadata({'units':'s',
                                                               'long_name':'second',
                                                               'standard_name':'',
                                                               'Category':['']}))


        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['date_time'],
                                                          'InputUnits':[''],
                                                          'Outputs':['year', 'month', 'day', 'hour', 'minute', 'second'],
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)


    def run(self, date_time):

        return egads_core.EgadsAlgorithm.run(self, date_time)

    def _algorithm(self, date_time):

        year = []
        month = []
        day = []
        hour = []
        minute = []
        second = []

        for time in date_time:
            time_tuple = dateutil.parser.parse(time)
            year.append(time_tuple.year)
            month.append(time_tuple.month)
            day.append(time_tuple.day)
            hour.append(time_tuple.hour)
            minute.append(time_tuple.minute)
            second.append(time_tuple.second)



        return year, month, day, hour, minute, second


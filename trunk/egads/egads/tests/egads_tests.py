"""
Test suite for EgadsData class.

Uses NetCDF4 Python library to test know inputs and outputs against the EGADS
NetCDF library (based on NetCDF4).

"""

import os
import unittest

import egads
import numpy
from numpy.random.mtrand import uniform
from numpy.testing import assert_array_equal

__author__ = "Matt Freer"
__date__ = "$Date: 2010-09-17 17:54:22 +0200 (Fri, 17 Sep 2010) $"
__version__ = "$Revision: 25 $"

UNITS1 = 'm'
UNITS2 = 's'


class EgadsDataScalarTestCase(unittest.TestCase):
    """ Test EgadsData class with scalar values """
    def setUp(self):
        self.value1 = 1
        self.value2 = 5


    def test_egads_scalar_assignment(self):
        egadstest = egads.EgadsData(self.value1)
        
        self.assertEqual(self.value1, egadstest.value, 'Scalar assignment not equal')
        
        egadstest2 = egads.EgadsData()
        egadstest2.value = self.value2
        
        self.assertEqual(self.value2, egadstest2.value, 'Scalar assignment not equal')

    def test_egads_to_egads_calcs(self):
        """test scalar operations between multiple egads parameters """
        egadstest1 = egads.EgadsData(self.value1, UNITS1)
        egadstest2 = egads.EgadsData(self.value2, UNITS1)
        
        self.assertEqual(self.value1 + self.value2, egadstest1 + egadstest2, 'Egads to Egads scalar addition not equal')
        self.assertEqual(self.value1 - self.value2, egadstest1 - egadstest2, 'Egads to Egads scalar subtraction not equal')
        self.assertEqual(self.value1 * self.value2, egadstest1 * egadstest2, 'Egads to Egads scalar multiplication not equal')
        self.assertEqual(self.value1 / self.value2, egadstest1 / egadstest2, 'Egads to Egads scalar division not equal')
        self.assertEqual(self.value1 ** self.value2, egadstest1 ** egadstest2, 'Egads to Egads scalar power not equal')

    def test_egads_to_other_calcs(self):
        """ test scalar operations between egads class and other scalar"""
        egadstest1 = egads.EgadsData(self.value1, UNITS1)

        self.assertEqual(self.value1 + self.value2, egadstest1 + self.value2, 'Egads to other scalar addition not equal')
        self.assertEqual(self.value1 - self.value2, egadstest1 - self.value2, 'Egads to other scalar subtraction not equal')
        self.assertEqual(self.value1 * self.value2, egadstest1 * self.value2, 'Egads to other scalar multiplication not equal')
        self.assertEqual(self.value1 / self.value2, egadstest1 / self.value2, 'Egads to other scalar division not equal')
        self.assertEqual(self.value1 ** self.value2, egadstest1 ** self.value2, 'Egads to other scalar power not equal')

    def test_other_to_egads_calcs(self):
        """ test scalar operations between other scalar and egads class"""
        egadstest1 = egads.EgadsData(self.value1, UNITS1)

        self.assertEqual(self.value2 + self.value1, self.value2 + egadstest1, 'Other to Egads scalar addition not equal')
        self.assertEqual(self.value2 - self.value1, self.value2 - egadstest1, 'Other to Egads scalar subtraction not equal')
        self.assertEqual(self.value2 * self.value1, self.value2 * egadstest1, 'Other to Egads scalar multiplication not equal')
        self.assertEqual(self.value2 / self.value1, self.value2 / egadstest1, 'Other to Egads scalar division not equal')
        self.assertEqual(self.value2 ** self.value1, self.value2 ** egadstest1, 'Other to Egads scalar power not equal')

class EgadsDataVectorTestCase(unittest.TestCase):
    """ Test EgadsData class with vector values """

    def setUp(self):
        self.value1 = numpy.array([1,2,3,4,5])
        self.value2 = numpy.array([2,2,2,2,2])
        self.scalar = 5


    def test_egads_vector_assignment(self):
        egadstest = egads.EgadsData(self.value1)

        assert_array_equal(self.value1, egadstest.value, 'Vector assignment not equal')

        egadstest2 = egads.EgadsData()
        egadstest2.value = self.value2

        assert_array_equal(self.value2, egadstest2.value, 'Vector assignment not equal')

    def test_egads_to_egads_calcs(self):
        """test vector operations between multiple egads parameters """
        egadstest1 = egads.EgadsData(self.value1, UNITS1)
        egadstest2 = egads.EgadsData(self.value2, UNITS1)

        assert_array_equal(self.value1 + self.value2, egadstest1 + egadstest2, 'Egads to Egads vector addition not equal')
        self.assertEqual(self.value1 - self.value2, egadstest1 - egadstest2, 'Egads to Egads vector subtraction not equal')
        self.assertEqual(self.value1 * self.value2, egadstest1 * egadstest2, 'Egads to Egads vector multiplication not equal')
        self.assertEqual(self.value1 / self.value2, egadstest1 / egadstest2, 'Egads to Egads vector division not equal')
        self.assertEqual(self.value1 ** self.value2, egadstest1 ** egadstest2, 'Egads to Egads vector power not equal')
        
    def test_egads_to_other_calcs(self):
        """ test vector operations between egads class and other vector"""
        egadstest1 = egads.EgadsData(self.value1, UNITS1)

        assert_array_equal(self.value1 + self.value2, egadstest1 + self.value2, 'Egads to other vector addition not equal')
        self.assertEqual(self.value1 - self.value2, egadstest1 - self.value2, 'Egads to other vector subtraction not equal')
        self.assertEqual(self.value1 * self.value2, egadstest1 * self.value2, 'Egads to other vector multiplication not equal')
        self.assertEqual(self.value1 / self.value2, egadstest1 / self.value2, 'Egads to other vector division not equal')
        self.assertEqual(self.value1 ** self.value2, egadstest1 ** self.value2, 'Egads to other vector power not equal')

    def test_other_to_egads_calcs(self):
        """ test vector operations between other vector and egads class"""
        egadstest1 = egads.EgadsData(self.value1, UNITS1)

        self.assertEqual(self.value2 + self.value1, self.value2 + egadstest1, 'Other to Egads vector addition not equal')
        self.assertEqual(self.value2 - self.value1, self.value2 - egadstest1, 'Other to Egads vector subtraction not equal')
        self.assertEqual(self.value2 * self.value1, self.value2 * egadstest1, 'Other to Egads vector multiplication not equal')
        self.assertEqual(self.value2 / self.value1, self.value2 / egadstest1, 'Other to Egads vector division not equal')
        self.assertEqual(self.value2 ** self.value1, self.value2 ** egadstest1, 'Other to Egads vector power not equal')




def suite():
    egads_scalar_suite = unittest.TestLoader().loadTestsFromTestCase(EgadsDataScalarTestCase)
    egads_vector_suite = unittest.TestLoader().loadTestsFromTestCase(EgadsDataVectorTestCase)
    return unittest.TestSuite([egads_scalar_suite, egads_vector_suite])

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=5).run(suite())

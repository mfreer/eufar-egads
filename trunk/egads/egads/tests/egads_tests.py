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
__date__ = "$Date$"
__version__ = "$Revision$"

UNITS1 = 'm'
UNITS2 = 's'


class EgadsDataScalarTestCase(unittest.TestCase):
    """ Test EgadsData class with scalar values """
    def setUp(self):
        self.value1 = 1
        self.value2 = 5


    def test_egads_scalar_assignment(self):
        """ Test initialization of EgadsData instance with vector input """

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
        """ Test initialization of EgadsData instance with vector input """ 
        egadstest = egads.EgadsData(self.value1)

        assert_array_equal(self.value1, egadstest.value, 'Vector assignment not equal')

        egadstest2 = egads.EgadsData()
        egadstest2.value = self.value2

        assert_array_equal(self.value2, egadstest2.value, 'Vector assignment not equal')

    def test_egads_to_egads_calcs(self):
        """test vector operations between multiple egads parameters """
        egadstest1 = egads.EgadsData(self.value1, UNITS1)
        egadstest2 = egads.EgadsData(self.value2, UNITS1)

        add = egadstest1 + egadstest2
        subtract = egadstest1 - egadstest2
        multiply = egadstest1 * egadstest2
        divide = egadstest1 / egadstest2
        power = egadstest1 ** egadstest2

        assert_array_equal(self.value1 + self.value2, add.value, 'Egads to Egads vector addition not equal')
        assert_array_equal(self.value1 - self.value2, subtract.value, 'Egads to Egads vector subtraction not equal')
        assert_array_equal(self.value1 * self.value2, multiply.value, 'Egads to Egads vector multiplication not equal')
        assert_array_equal(self.value1 / self.value2, divide.value, 'Egads to Egads vector division not equal')
        assert_array_equal(self.value1 ** self.value2, power.value, 'Egads to Egads vector power not equal')
        
    def test_egads_to_other_calcs(self):
        """ test vector operations between egads class and other vector"""
        egadstest1 = egads.EgadsData(self.value1, UNITS1)

        add = egadstest1 + self.value2
        subtract = egadstest1 - self.value2
        multiply = egadstest1 * self.value2
        divide = egadstest1 / self.value2
        power = egadstest1 ** self.value2

        assert_array_equal(self.value1 + self.value2, add.value, 'Egads to Egads vector addition not equal')
        assert_array_equal(self.value1 - self.value2, subtract.value, 'Egads to Egads vector subtraction not equal')
        assert_array_equal(self.value1 * self.value2, multiply.value, 'Egads to Egads vector multiplication not equal')
        assert_array_equal(self.value1 / self.value2, divide.value, 'Egads to Egads vector division not equal')
        assert_array_equal(self.value1 ** self.value2, power.value, 'Egads to Egads vector power not equal')

    def test_other_to_egads_calcs(self):
        """ test vector operations between other vector and egads class"""
        egadstest1 = egads.EgadsData(self.value1, UNITS1)
        print egadstest1.value, self.value2
        add = self.value2 + egadstest1
        #print type(add), self.value2
        subtract = self.value2 - egadstest1
        multiply = self.value2 * egadstest1
        divide = self.value2 / egadstest1
        power = self.value2 ** egadstest1

        #assert_array_equal(self.value1 + self.value2, add.value, 'Egads to Egads vector addition not equal')
        assert_array_equal(self.value1 - self.value2, subtract.value, 'Egads to Egads vector subtraction not equal')
        assert_array_equal(self.value1 * self.value2, multiply.value, 'Egads to Egads vector multiplication not equal')
        assert_array_equal(self.value1 / self.value2, divide.value, 'Egads to Egads vector division not equal')
        assert_array_equal(self.value1 ** self.value2, power.value, 'Egads to Egads vector power not equal')


class EgadsValueAssignmentTestCase(unittest.TestCase):
    """ Test assignment of EgadsData class"""

    def setUp(self):
        self.value1 = egads.EgadsData([1,2,3], 'm')
        

    def test_self_assignment(self):
        """ Testing assignment of EgadsData class to self """

        value2 = self.value1.copy()

        self.assertEqual(self.value1.units, value2.units, 'Units do not match after assignment')
        assert_array_equal(self.value1.value, value2.value, 'Values do not match after assignment')

        value2.value[1] = 100
        value2.units = 's'

        self.assertEqual(self.value1.units, 'm', ['Original units have changed to', self.value1.units])
        assert_array_equal(self.value1.value, numpy.array([1,2,3]), 'Original array has changed')

        self.value1.units = 'cm'
        self.value1.value[1] = 200

        self.assertEqual(value2.units, 's', 'New units have changed')
        assert_array_equal(value2.value, numpy.array([1,100,3]), 'New array has changed')

    def test_call_copy(self):
        """ Testing copy of EgadsData using call to self """

        value2 = egads.EgadsData(self.value1)

        self.assertEqual(self.value1.units, value2.units, 'Units do not match after assignment')
        assert_array_equal(self.value1.value, value2.value, 'Values do not match after assignment')

        value2.value[1] = 100
        value2.units = 's'

        self.assertEqual(self.value1.units, 'm', ['Original units have changed to', self.value1.units])
        assert_array_equal(self.value1.value, numpy.array([1,2,3]), 'Original array has changed')

        self.value1.units = 'cm'
        self.value1.value[1] = 200

        self.assertEqual(value2.units, 's', 'New units have changed')
        assert_array_equal(value2.value, numpy.array([1,100,3]), 'New array has changed')



def suite():
    egads_scalar_suite = unittest.TestLoader().loadTestsFromTestCase(EgadsDataScalarTestCase)
    egads_vector_suite = unittest.TestLoader().loadTestsFromTestCase(EgadsDataVectorTestCase)
    egads_assignment_suite = unittest.TestLoader().loadTestsFromTestCase(EgadsValueAssignmentTestCase)
    return unittest.TestSuite([egads_scalar_suite, egads_vector_suite, egads_assignment_suite])

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=5).run(suite())
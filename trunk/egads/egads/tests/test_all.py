# To change this template, choose Tools | Templates
# and open the template in the editor.

import unittest

import input_tests
import thermodynamics_tests



def test():
    suite = unittest.TestSuite()
    suite.addTest(input_tests.suite())
#    suite.addTest(thermodynamics_tests.suite())

    unittest.TextTestRunner(verbosity=5).run(suite)

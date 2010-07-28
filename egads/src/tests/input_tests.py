""" :TODO: fill in docstring

"""

import input
import egads
import netCDF4
import unittest
import tempfile
import os
from numpy.random.mtrand import uniform
from numpy.testing import assert_array_equal

__author__ = "Matt Freer"
__date__ = "$Date: 2009-10-13 14:51:27 +0200 (Tue, 13 Oct 2009) $"
__version__ = "$Revision: 15 $"

FILE_NAME = tempfile.mktemp('.nc')
FILE_NAME_ALT = tempfile.mktemp('.nc')
VAR_NAME = 'test_var'
VAR_UNITS = 's'

VAR_MULT_NAME = 'test_mult_var'
VAR_MULT_UNITS = 'm'

DIM1_NAME = 'x'
DIM1_LEN = 10
DIM2_NAME = 'y'
DIM2_LEN = 5

random_data = uniform(size=(DIM1_LEN))
random_mult_data = uniform(size=(DIM1_LEN, DIM2_LEN))


class NetCdfFileInputTestCase(unittest.TestCase):
    """ Test input from NetCDF file """
    def setUp(self):
        self.file = FILE_NAME
        f = netCDF4.Dataset(self.file,'w')
        f.createDimension(DIM1_NAME, DIM1_LEN)
        f.createDimension(DIM2_NAME, DIM2_LEN)
        v1 = f.createVariable(VAR_NAME, 'f8',(DIM1_NAME))
        v2 = f.createVariable(VAR_MULT_NAME, 'f8', (DIM1_NAME, DIM2_NAME))
        v1.units = VAR_UNITS
        v2.units = VAR_MULT_UNITS
        v1[:] = random_data
        v2[:] = random_mult_data
        
        f.close()



    def tearDown(self):
        os.remove(self.file)

    def test_bad_file_name(self):
        """test handling of missing file """

        data = input.NetCdf()
        self.assertRaises(RuntimeError, data.read,
                          'blah','test.nc')



    def test_bad_variable(self):
        """ test handling of missing variable name"""

        data = input.NetCdf()
        self.assertRaises(KeyError, data.read,'blah',self.file)

    def test_bad_attribute(self):
        """ test handling of bad attribute name"""
        self.fail('Test not implemented.')

    def test_load_data_1d(self):
        """test reading 1D netcdf data"""

        data = input.NetCdf().read(VAR_NAME,self.file,)

        self.assertEqual(len(data.value), DIM1_LEN, "Input dimensions don't match")
        self.assertTrue(data.units == VAR_UNITS, "Input units don't match")
        assert_array_equal(data.value, random_data)

    def test_load_data_2d(self):
        """ test reading 2D netcdf data"""

        data = input.NetCdf().read(VAR_MULT_NAME,self.file)

        self.assertEqual(data.dimensions, (DIM1_LEN, DIM2_LEN), "Input dimensions don't match")
        self.assertTrue(data.units == VAR_MULT_UNITS, "Input units don't match")
        assert_array_equal(data.value,random_mult_data)


    def test_read_range_1d(self):
        """ test reading subset of data"""
        data = input.NetCdf().read(VAR_NAME,self.file,input_range = (0,DIM1_LEN-2))
        assert_array_equal(data.value,random_data[:DIM1_LEN-2])

        data = input.NetCdf().read(VAR_NAME, self.file,input_range = (-1, DIM1_LEN))
        assert_array_equal(data.value,random_data[-1:DIM1_LEN])

        data = input.NetCdf().read(VAR_NAME, self.file, input_range = (None, DIM1_LEN))
        assert_array_equal(data.value,random_data[0:DIM1_LEN])

        data = input.NetCdf().read(VAR_NAME, self.file, input_range = (None, DIM1_LEN+1))
        assert_array_equal(data.value, random_data[0:DIM1_LEN])

    def test_read_range_2d(self):
        """ test reading subset of data in 2d"""

        data = input.NetCdf().read(VAR_MULT_NAME,self.file,input_range = (0,DIM1_LEN-2))
        assert_array_equal(data.value,random_mult_data[:DIM1_LEN-2,:])
    
        data = input.NetCdf().read(VAR_MULT_NAME,self.file,input_range = (None, None, 0,DIM1_LEN-2))
        assert_array_equal(data.value,random_mult_data[:,:DIM1_LEN-2])




class NetCdfFileOutputTestCase(unittest.TestCase):
    """ Test ouput to NetCDF file """
    def setUp(self):
        self.data_1d = egads.ToolboxData(value = random_data, units = VAR_UNITS)
        self.data_2d = egads.ToolboxData(value = random_mult_data, units = VAR_MULT_UNITS)
        self.file = FILE_NAME
        f = netCDF4.Dataset(self.file,'w')
        f.createDimension(DIM1_NAME, DIM1_LEN)
        f.createDimension(DIM2_NAME, DIM2_LEN)
        v1 = f.createVariable(VAR_NAME, 'f8',(DIM1_NAME))
        v2 = f.createVariable(VAR_MULT_NAME, 'f8', (DIM1_NAME, DIM2_NAME))
        v1.units = VAR_UNITS
        v2.units = VAR_MULT_UNITS
        v1[:] = random_data
        v2[:] = random_mult_data


        pass

    def tearDown(self):
        os.remove(self.file)
    
    def test_create_file(self):
        """ test creation of new NetCDF file """
        self.fail('Test not implemented')



    def test_output_variable_1d_newfile(self):
        """ test output of variable in file """

        self.assertRaises(RuntimeError,input.NetCdf().write,
                          self.data_1d, VAR_NAME, DIM1_NAME, FILE_NAME_ALT)
        input.NetCdf().write(self.data_1d, VAR_NAME, DIM1_NAME, FILE_NAME_ALT,create = 'yes')
        f = netCDF4.Dataset(FILE_NAME_ALT,'r')
        varin = f.variables[VAR_NAME]
        self.assertTrue(varin.units == VAR_UNITS, "Output units don't match")
        self.assertTrue(varin.shape == (DIM1_LEN,),"Output dimensions don't match")
        assert_array_equal(varin[:],random_data)
        os.remove(FILE_NAME_ALT)

    def test_output_variable_1d_existfile(self):
        """ test output of variable in file """

        input.NetCdf().write(self.data_1d, VAR_NAME, DIM1_NAME, self.file)
        f = netCDF4.Dataset(self.file,'r')
        varin = f.variables[VAR_NAME]
        self.assertTrue(varin.units == VAR_UNITS, "Output units don't match")
        self.assertTrue(varin.shape == (DIM1_LEN,),"Output dimensions don't match")
        assert_array_equal(varin[:],random_data)


def suite():
    in_suite = unittest.TestLoader().loadTestsFromTestCase(NetCdfFileInputTestCase)
    out_suite = unittest.TestLoader().loadTestsFromTestCase(NetCdfFileOutputTestCase)
    return unittest.TestSuite([in_suite, out_suite])

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=5).run(suite())

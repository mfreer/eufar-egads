"""
Test suite for NetCDF and text file input and output libraries.

Uses NetCDF4 Python library to test known inputs and outputs against the EGADS
NetCDF library (based on NetCDF4).

"""

__author__ = "mfreer"
__date__ = "$Date::                  $"
__version__ = "$Revision::           $"

import os
import tempfile
import unittest
import csv

import egads.input as input
import netCDF4
from numpy.random.mtrand import uniform
from numpy.testing import assert_array_equal


FILE_NAME = tempfile.mktemp('.nc')
FILE_NAME_ALT = tempfile.mktemp('.nc')
VAR_NAME = 'test_var'
VAR_UNITS = 's'
VAR_LONG_NAME = 'test variable'
VAR_STD_NAME = ''
CATEGORY = 'TEST'

VAR_MULT_NAME = 'test_mult_var'
VAR_MULT_UNITS = 'm'

GLOBAL_ATTRIBUTE = 'test_file'
CONVENTIONS = 'EUFAR-N6SP'
TITLE = 'Test file'
SOURCE = 'Generated for testing purposes'
INSTITUTION = 'EUFAR'
PROJECT = 'N6SP'


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
        f = netCDF4.Dataset(self.file, 'w')
        f.attribute = GLOBAL_ATTRIBUTE
        f.Conventions = CONVENTIONS
        f.title = TITLE
        f.source = SOURCE
        f.institution = INSTITUTION
        f.project = PROJECT

        f.createDimension(DIM1_NAME, DIM1_LEN)
        f.createDimension(DIM2_NAME, DIM2_LEN)
        v1 = f.createVariable(VAR_NAME, 'f8', (DIM1_NAME))
        v2 = f.createVariable(VAR_MULT_NAME, 'f8', (DIM1_NAME, DIM2_NAME))
        v1.units = VAR_UNITS
        v2.units = VAR_MULT_UNITS
        v1.long_name = VAR_LONG_NAME
        v1.standard_name = VAR_STD_NAME
        v1.Category = CATEGORY
        v1[:] = random_data
        v2[:] = random_mult_data
        
        f.close()



    def tearDown(self):
        os.remove(self.file)

    def test_bad_file_name(self):
        """test handling of missing file """

        self.assertRaises(RuntimeError, input.NetCdf, 'test.nc')

    def test_open_file(self):
        """ test opening of file using open method """

        data = input.NetCdf()
        data.open(self.file)

        self.assertEqual(data.filename, self.file, 'file opening failed')
        self.assertEqual(data.get_perms(), 'r', 'file permissions do not match')

        data.close()

        data_write = input.NetCdf()
        data_write.open(self.file, 'w')

        self.assertEqual(data_write.filename, self.file, 'file opening failed for write')
        self.assertEqual(data_write.get_perms(), 'w', 'file permissions do not match')

        data_write.close()


    def test_bad_variable(self):
        """ test handling of missing variable name"""

        data = input.NetCdf(self.file)
        self.assertRaises(KeyError, data.read_variable, 'blah')

    def test_bad_attribute(self):
        """ test handling of bad attribute name"""
        data = input.NetCdf(self.file)
        self.assertRaises(KeyError, data.get_attribute_value, 'bad_attr')
        self.assertRaises(KeyError, data.get_attribute_value, 'bad_attr', VAR_NAME)


    def test_read_attribute(self):
        """ test reading attribute from file """
        
        data = input.NetCdf(self.file)
        self.assertEqual(data.get_attribute_value('units',VAR_NAME), VAR_UNITS, 
                        'Variable attributes do not match')
        self.assertEqual(data.get_attribute_value('attribute'),GLOBAL_ATTRIBUTE,
                         'Global attributes do not match')
    
    def test_read_dimensions(self):
        """ test reading dimensions from file """
        
        data = input.NetCdf(self.file)
        dimdict = {DIM1_NAME : DIM1_LEN, DIM2_NAME : DIM2_LEN}
        self.assertEqual(data.get_dimensions(), dimdict,
                        'dimensions dictionary does not match')

        vardimdict = {DIM1_NAME : DIM1_LEN}
        self.assertEqual(data.get_dimensions(VAR_NAME), vardimdict,
                         'variable dimensions do not match')

    def test_load_data_1d(self):
        """test reading 1D netcdf data"""

        data = input.NetCdf(self.file).read_variable(VAR_NAME)

        self.assertEqual(len(data), DIM1_LEN, "Input dimensions don't match")
        assert_array_equal(data, random_data)

    def test_load_data_2d(self):
        """ test reading 2D netcdf data"""

        data = input.NetCdf(self.file).read_variable(VAR_MULT_NAME)

        self.assertEqual(data.shape, (DIM1_LEN, DIM2_LEN), "Input dimensions don't match")
        assert_array_equal(data, random_mult_data)


    def test_read_range_1d(self):
        """ test reading subset of data"""
        data = input.NetCdf(self.file).read_variable(VAR_NAME, input_range=(0, DIM1_LEN-2))
        assert_array_equal(data, random_data[:DIM1_LEN-2])

        data = input.NetCdf(self.file).read_variable(VAR_NAME, input_range=(-1, DIM1_LEN))
        assert_array_equal(data, random_data[-1:DIM1_LEN])

        data = input.NetCdf(self.file).read_variable(VAR_NAME, input_range=(None, DIM1_LEN))
        assert_array_equal(data, random_data[0:DIM1_LEN])

        data = input.NetCdf(self.file).read_variable(VAR_NAME, input_range=(None, DIM1_LEN + 1))
        assert_array_equal(data, random_data[0:DIM1_LEN])

    def test_read_range_2d(self):
        """ test reading subset of data in 2d"""

        data = input.NetCdf(self.file).read_variable(VAR_MULT_NAME, input_range=(0, DIM1_LEN-2))
        assert_array_equal(data, random_mult_data[:DIM1_LEN-2, :],)
    
        data = input.NetCdf(self.file).read_variable(VAR_MULT_NAME, input_range=(None, None, 0, DIM1_LEN-2))
        assert_array_equal(data, random_mult_data[:, :DIM1_LEN-2])

    def test_read_n6sp_data(self):
        """ test reading in data using N6SP formatted NetCDF """

        infile = input.EgadsNetCdf(self.file)

        self.assertEqual(infile.history, None, 'NetCDF history attribute doesnt match')
        self.assertEqual(infile.title, TITLE, 'NetCDF title attribute doesnt match')

        data = infile.read_variable(VAR_NAME)

        assert_array_equal(data.value, random_data)
        self.assertEqual(data.units, VAR_UNITS, 'EgadsData units attribute doesnt match')
        self.assertEqual(data.long_name, VAR_LONG_NAME, 'EgadsData long name attribute doesnt match')
        self.assertEqual(data.standard_name, VAR_STD_NAME,'EgadsData standard name attribute doesnt match')





class NetCdfFileOutputTestCase(unittest.TestCase):
    """ Test ouput to NetCDF file """
    def setUp(self):
        self.file = FILE_NAME

        f = input.NetCdf(self.file, 'w')

        f.add_dim(DIM1_NAME, DIM1_LEN)
        f.add_dim(DIM2_NAME, DIM2_LEN)

        f.write_variable(random_data, VAR_NAME,(DIM1_NAME,),'double')
        f.write_variable(random_mult_data, VAR_MULT_NAME, (DIM1_NAME, DIM2_NAME,),
                        'double')

        f.add_attribute('units', VAR_UNITS, VAR_NAME)
        f.add_attribute('units', VAR_MULT_UNITS, VAR_MULT_NAME)

#        self.data_1d = egads.EgadsData(value=random_data, units=VAR_UNITS)
#        self.data_2d = egads.EgadsData(value=random_mult_data, units=VAR_MULT_UNITS)
#        f = netCDF4.Dataset(self.file, 'w')
#        f.createDimension(DIM1_NAME, DIM1_LEN)
#        f.createDimension(DIM2_NAME, DIM2_LEN)
#        v1 = f.createVariable(VAR_NAME, 'f8', (DIM1_NAME))
#        v2 = f.createVariable(VAR_MULT_NAME, 'f8', (DIM1_NAME, DIM2_NAME))
#        v1.units = VAR_UNITS
#        v2.units = VAR_MULT_UNITS
#        v1[:] = random_data
#        v2[:] = random_mult_data


        pass

    def tearDown(self):
        os.remove(self.file)
    
    def test_create_file(self):
        """ test creation of new NetCDF file """
        self.fail('Test not implemented')

    def test_dimension_creation(self):
        """ test creation of dimensions in file """

        f = netCDF4.Dataset(self.file, 'r')


        self.assertTrue(DIM1_NAME in f.dimensions, 'Dim1 missing')
        self.assertTrue(DIM2_NAME in f.dimensions, 'Dim2 missing')

        self.assertEqual(DIM1_LEN, len(f.dimensions[DIM1_NAME]),
                         'Dim1 length not equal')
        self.assertEqual(DIM2_LEN, len(f.dimensions[DIM2_NAME]),
                         'Dim2 length not equal')

    def test_1d_variable_creation(self):
        """ test creation of 1d variable in file """
        
        f = netCDF4.Dataset(self.file, 'r')

        varin = f.variables[VAR_NAME]

        self.assertEqual(varin.shape, (DIM1_LEN,), 'Variable dimensions dont match')
        self.assertEqual(varin.units, VAR_UNITS, 'Variable units dont match')
        assert_array_equal(varin[:], random_data)

    def test_2d_variable_creation(self):
        """ test creation of 2d variable in file """

        f = netCDF4.Dataset(self.file, 'r')

        varin = f.variables[VAR_MULT_NAME]

        self.assertEqual(varin.shape, (DIM1_LEN,DIM2_LEN), 'Variable dimensions dont match')
        self.assertEqual(varin.units, VAR_MULT_UNITS, 'Variable units dont match')
        assert_array_equal(varin[:], random_mult_data)

class EgadsFileInputTestCase(unittest.TestCase):
    """ Test input from text file"""
    def setUp(self):
        self.filename = tempfile.mktemp('.txt')
        self.strdata1ln = 'testtesttest\n'
        self.strdata2ln = 'testtesttest\n testtesttest\n'
        f = open(self.filename,'w')
        f.write(self.strdata2ln)
        f.close()

    def test_open_file(self):
        """ Test opening of file """

        f = input.EgadsFile(self.filename,'r')

        self.assertEqual(f.filename, self.filename, 'Filenames do not match')

        self.assertRaises(RuntimeError, input.EgadsFile, 'nofile.txt')

        self.assertEqual(f.pos, 0, 'File position is not correct')

        f.close()


    def test_read_data(self):
        """ Test reading data from file """

        f = input.EgadsFile(self.filename,'r')

        data = f.read()

        self.assertEqual(self.strdata2ln, data, 'Data read in does not match')
        
        f.reset()
        
        data = f.read(4)
        self.assertEqual(self.strdata2ln[0:4], data, 'Characters read in do not match')

        f.close()



    def test_read_data_one_line(self):
        """ Test reading one line of data from file """

        f = input.EgadsFile(self.filename,'r')

        data = f.read_line()

        self.assertEqual(self.strdata1ln, data, 'One line data does not match')

        f.close()


    def test_seek_file(self):
        """ Test file seek function """

        f = input.EgadsFile(self.filename,'r')

        f.seek(3)

        data = f.read(1)

        self.assertEqual(4, f.pos, 'Positions do not match')
        self.assertEqual(self.strdata2ln[3], data, 'Data from pos 3 does not match')

        f.seek(3,'c')

        data = f.read(1)

        self.assertEqual(8, f.pos, 'Positions do not match')
        self.assertEqual(self.strdata2ln[7], data, 'Data from pos 7 does not match')


        f.seek(4)

        data = f.read(1)

        self.assertEqual(5, f.pos, 'Positions do not match')
        self.assertEqual(self.strdata2ln[4], data, 'Data from pos 3 does not match')

        f.close()

class EgadsFileOutputTestCase(unittest.TestCase):
    """ Test output to text file """

    def setUp(self):
        self.filename = tempfile.mktemp('.txt')
        self.f = input.EgadsFile(self.filename,'w')


        self.strdata1ln = 'testtesttest\n'
        self.strdata2ln = 'testtesttest\n testtesttest\n'
        self.intdata = [123,456]

    def tearDown(self):

        self.f.close()

    def test_write_string_oneline(self):
        """ Test writing one line string to file. """

        self.f.write(self.strdata1ln)

        g = open(self.filename)

        data = g.read()

        self.assertEqual(data, self.strdata1ln, "Written one line string data does not match.")

        g.close()

    def test_write_string_twoline(self):
        """ Test writing two line string to file. """

        self.f.write(self.strdata2ln)

        g = open(self.filename)

        data = g.read()

        self.assertEqual(data, self.strdata2ln, "Written two line string data does not match.")

        g.close()

    def test_write_int(self):
        """ Test writing integers to file. """

        self.f.write(str(self.intdata))

        g = open(self.filename)

        data = g.read()

        self.assertEqual(data, str(self.intdata), "Written int data does not match.")


class EgadsCsvInputTestCase(unittest.TestCase):
    """Test input from CSV file."""

    def setUp(self):
        self.filename = tempfile.mktemp('.csv')
        self.titles = ['Time', 'Lat', 'Lon', 'Alt']
        self.data = [['1', 0, 1, 0.3],
                     ['2', 1, 0, 1.5],
                     ['3', 2, -1, 1.7]]

        self.times = ['1','2','3']
        self.lats = [0,1,2]
        self.lons = [1,0,-1]
        self.alts = [0.3, 1.5, 1.7]

        self.data_as_str = [['1','2','3'],
                            ['0','1','2'],
                            ['1','0','-1'],
                            ['0.3','1.5','1.7']]

        self.format = ['s','i','i','f']

        f = open(self.filename,'w')
        writer = csv.writer(f)

        writer.writerow(self.titles)
        writer.writerows(self.data)

        f.close()

        self.f = input.EgadsCsv(self.filename)

    def tearDown(self):

        self.f.close()

    def test_open_file(self):
        """ Test opening of file """

        self.assertEqual(self.f.filename, self.filename, 'Filenames do not match')

        self.assertRaises(RuntimeError, input.EgadsFile, 'nofile.txt')

        self.assertEqual(self.f.pos, 0, 'File position is not correct')

        self.assertEqual(self.f.delimiter, ',', 'Delimiter value not correct')

        self.assertEqual(self.f.quotechar, '"', 'Quote character not correct')


    def test_read_data(self):
        """ Test reading data from csv file."""

        title = self.f.read(1)

        time, lat, lon, alt = self.f.read(format = self.format)

        self.f.reset()

        self.f.skip_line()

        data_str = self.f.read()

        self.assertEqual(title, self.titles, 'Titles do not match')
    
        assert_array_equal(time, self.times, 'Values do not match')
        assert_array_equal(lat, self.lats, 'Values do not match')
        assert_array_equal(lon, self.lons, 'Values do not match')
        assert_array_equal(alt, self.alts, 'Values do not match')

        assert_array_equal(data_str, self.data_as_str, 'Non-formatted data does not match')

class EgadsCsvOutputTestCase(unittest.TestCase):
    """ Test writing of CSV files. """

    def setUp(self):
        self.filename = tempfile.mktemp('.csv')
        self.titles = 'Time, Lat, Lon, Alt'
        self.data = [['1', 0, 1, 0.3],
                     ['2', 1, 0, 1.5],
                     ['3', 2, -1, 1.7]]

        self.data_as_str = [['1', '0', '1', '0.3'],
                     ['2', '1', '0', '1.5'],
                     ['3', '2', '-1', '1.7']]

        self.format = ['s','i','i','f']

        f = input.EgadsCsv(self.filename,'w')

        f.write(self.titles)
        f.writerows(self.data)

        f.close()





def suite():
    netcdf_in_suite = unittest.TestLoader().loadTestsFromTestCase(NetCdfFileInputTestCase)
    netcdf_out_suite = unittest.TestLoader().loadTestsFromTestCase(NetCdfFileOutputTestCase)
    text_in_suite = unittest.TestLoader().loadTestsFromTestCase(EgadsFileInputTestCase)
    text_out_suite = unittest.TestLoader().loadTestsFromTestCase(EgadsFileOutputTestCase)
    csv_in_suite = unittest.TestLoader().loadTestsFromTestCase(EgadsCsvInputTestCase)
    csv_out_suite = unittest.TestLoader().loadTestsFromTestCase(EgadsCsvOutputTestCase)

    return unittest.TestSuite([netcdf_in_suite, netcdf_out_suite, text_in_suite, 
                               text_out_suite, csv_in_suite, csv_out_suite])

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=5).run(suite())

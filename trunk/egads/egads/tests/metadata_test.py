"""
Test suite for Metadata classes.

"""
__author__ = "mfreer"
__date__ = "$Date:: 2011-08-24 11:48#$"
__version__ = "$Revision:: 70        $"


import unittest
import egads.core.metadata as metadata

class MetadataCreationTestCase(unittest.TestCase):
    """ Test creation of metadata instances """ 
    
    def setUp(self):
        pass
    
    def test_creation_of_metadata_object(self):
        pass
    
    


class MetadataConventionComplianceTestCase(unittest.TestCase):
    """ Test working of compliance checker in metadata cases. """

    def setUp(self):
        var_metadata_dict = 
        
        var_metadata = metadata.VariableMetadata();
        
    def test_provide_convention_compliance_string(self):
        pass
    
    def test_provide_convention_compliance_list(self):
        pass
    
    def test_provide_convention_compliance_none(self):
        pass
    
    def test_provide_nonexisting_convention_compliance(self):
        pass
    
    def test_metadata_with_no_conventions(self):
        pass
    
    def test_variable_metadata(self):
        pass
    
    def test_file_metadata(self):
        pass
    
    def test_complete_metadata(self):
        pass
    
    def test_incomplete_metadata(self):
        pass
    
    
    
    



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
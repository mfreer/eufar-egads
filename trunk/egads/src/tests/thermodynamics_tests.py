__author__ = "Matt Freer"
__date__ = "$Date: 2009-10-13 14:51:27 +0200 (Tue, 13 Oct 2009) $"
__version__ = "$Revision: 15 $"

import unittest
import egads
from egads.algorithms import thermodynamics

Ucapf = egads.ToolboxData(value = [],
                          units = 'Hz',
                          long_name = 'output frequency of capacitive probe')

P_s = egads.ToolboxData(value = [],
                        units = 'hPa',
                        long_name = 'static pressure')

dP = egads.ToolboxData(value = [],
                       units = 'hPa',
                       long_name = 'dynamic pressure')



T_s = egads.ToolboxData(value = [],
                        units = 'K',
                        long_name = 'static temperature')

T_v = egads.ToolboxData(value = [],
                        units = 'K',
                        long_name = 'virtual temperature')
P_surface = egads.ToolboxData(value = [1013.25],
                              units = 'hPa',
                              long_name = 'surface pressure')

R_a_g = egads.ToolboxData(value = [287.058/9.8],
                          units = 'm/K',
                          long_name = 'air gas constant divided by gravity')



class  Thermodynamics_testsTestCase(unittest.TestCase):
    #def setUp(self):
    #    self.foo = Thermodynamics_tests()
    #

    #def tearDown(self):
    #    self.foo.dispose()
    #    self.foo = None

    def test_altitude_pressure_cnrm(self):
        alt_p = thermodynamics.altitude_pressure_cnrm(T_v, P_s, P_surface, R_a_g)
        pass

    def test_density_dry_air_cnrm(self):
        rho = thermodynamics.density_dry_air_cnrm(P_s, T_s)
        pass

    def test_hum_rel_capacitive_cnrm(self):


        pass

    def test_pressure_angle_incidence_cnrm(self):
        pass

    def test_temp_potential_cnrm(self):
        pass

    def test_temp_potential_equiv_cnrm(self):
        pass

    def test_temp_virtual_cnrm(self):
        pass

    def test_velocity_tas_cnrm(self):
        pass

    def test_velocity_tas_longitudinal(self):
        pass


if __name__ == '__main__':
    unittest.main()


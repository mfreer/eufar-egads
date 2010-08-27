__author__ = "Matt Freer"
__date__ = "$Date$"
__version__ = "$Revision$"

import unittest
import egads
from egads import *
from egads.algorithms import thermodynamics

Ucapf = egads.EgadsData(value = [],
                          units = 'Hz',
                          long_name = 'output frequency of capacitive probe')

P_s = egads.EgadsData(value = [],
                        units = 'hPa',
                        long_name = 'static pressure')

dP = egads.EgadsData(value = [],
                       units = 'hPa',
                       long_name = 'dynamic pressure')



T_s = egads.EgadsData(value = [],
                        units = 'K',
                        long_name = 'static temperature')

T_v = egads.EgadsData(value = [],
                        units = 'K',
                        long_name = 'virtual temperature')
P_surface = egads.EgadsData(value = [1013.25],
                              units = 'hPa',
                              long_name = 'surface pressure')

R_a_g = egads.EgadsData(value = [287.058/9.8],
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
        H_u = thermodynamics.hum_rel_capacitive_cnrm(Ucapf, T_s, P_s, dP, C_t,
                                                     Fmin, C_0, C_1, C_2)

        pass

    def test_pressure_angle_incidence_cnrm(self):
        P_s, dP, alpha, beta = thermodynamics.pressure_angle_incidence_cnrm(
                                             P_sr, delta_P_r, delta_P_h,
                                             delta_P_v, C_alpha, C_beta,
                                             C_errstat)
        pass

    def test_temp_potential_cnrm(self):
        theta = thermodynamics.temp_potential_cnrm(T_s, P_s, Racpa)

        pass

    def test_temp_potential_equiv_cnrm(self):
        pass

    def test_temp_virtual_cnrm(self):
        T_v = thermodynamics.temp_virtual_cnrm(T_s, r)

        pass

    def test_velocity_tas_cnrm(self):
        pass

    def test_velocity_tas_longitudinal(self):
        pass


if __name__ == '__main__':
    unittest.main()


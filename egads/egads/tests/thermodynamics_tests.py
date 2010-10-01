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

P_sr = P_s

dP = egads.EgadsData(value = [],
                       units = 'hPa',
                       long_name = 'dynamic pressure')

delta_P_r = dP

delta_P_v = dP
delta_P_v.value = delta_P_v.value * 0.1

delta_P_h = dP
delta_P_h.value = delta_P_h.value * 0.15

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

C_t = egads.EgadsData(value = 1, units = '%/C', long_name = 'temperature correction coeff')

Fmin = egads.EgadsData(value = 2, units = 'Hz', long_name = 'minimum acceptible frequency')

C_0 = egads.EgadsData(value = 0.5, units = '', long_name = '0th calibration coeff')

C_1 = egads.EgadsData(value = 0.6, units = '', long_name = '1st calibration coeff')

C_2 = egads.EgadsData(value = 0.5, units = '', long_name = '2nd calibration coeff')

C_alpha = egads.EgadsData(value = [1,0.9], units = '', long_name = 'angle of attack calibration')
C_beta = egads.EgadsData(value = [0.8,0.9], units = '', long_name = 'sideslip calibration')
C_errstat = egads.EgadsData(value = [1,0.9,1,0.8], units = '', long_name = 'static error coeffs')



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
        theta_e = thermodynamics.temp_potential_equiv_cnrm(T_s, theta,
                                                           r, c_pa)
        pass

    def test_temp_static_cnrm(self):
        T_s = thermodynamics.temp_static_cnrm(Tt, dP, P_s, r_f, Racpa)
        pass

    def test_temp_virtual_cnrm(self):
        T_v = thermodynamics.temp_virtual_cnrm(T_s, r)

        pass

    def test_velocity_tas_cnrm(self):
        V_p = thermodynamics.velocity_tas_cnrm(T_s, P_s, dP, cpa, Racpa)
        pass

    def test_velocity_tas_longitudinal(self):
        V_tx = thermodynamics.velocity_tas_longitudinal_cnrm(V_t, alpha, beta)
        pass


if __name__ == '__main__':
    unittest.main()


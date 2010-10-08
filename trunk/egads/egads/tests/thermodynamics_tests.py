__author__ = "Matt Freer"
__date__ = "$Date$"
__version__ = "$Revision$"
__all__ = ['ThermodynamicsTestCase']

import unittest
import egads
from egads import *
from egads.algorithms import thermodynamics



class  ThermodynamicsTestCase(unittest.TestCase):
    def setUp(self):
        self.Ucapf = egads.EgadsData(value = [],
                              units = 'Hz',
                              long_name = 'output frequency of capacitive probe')

        self.P_s = egads.EgadsData(value = [],
                                units = 'hPa',
                                long_name = 'static pressure')

        self.P_sr = self.P_s

        self.dP = egads.EgadsData(value = [],
                               units = 'hPa',
                               long_name = 'dynamic pressure')

        self.delta_P_r = self.dP

        self.delta_P_v = self.dP
        self.delta_P_v.value = self.delta_P_v.value * 0.1

        self.delta_P_h = self.dP
        self.delta_P_h.value = self.delta_P_h.value * 0.15

        self.T_s = egads.EgadsData(value = [],
                                units = 'K',
                                long_name = 'static temperature')

        self.T_v = egads.EgadsData(value = [],
                                units = 'K',
                                long_name = 'virtual temperature')
        self.P_surface = egads.EgadsData(value = [1013.25],
                                      units = 'hPa',
                                      long_name = 'surface pressure')

        self.R_a_g = egads.EgadsData(value = [287.058/9.8],
                                  units = 'm/K',
                                  long_name = 'air gas constant divided by gravity')

        self.C_t = egads.EgadsData(value = 1, units = '%/C', long_name = 'temperature correction coeff')

        self.Fmin = egads.EgadsData(value = 2, units = 'Hz', long_name = 'minimum acceptible frequency')

        self.C_0 = egads.EgadsData(value = 0.5, units = '', long_name = '0th calibration coeff')

        self.C_1 = egads.EgadsData(value = 0.6, units = '', long_name = '1st calibration coeff')

        self.C_2 = egads.EgadsData(value = 0.5, units = '', long_name = '2nd calibration coeff')

        self.C_alpha = egads.EgadsData(value = [1,0.9], units = '', long_name = 'angle of attack calibration')
        self.C_beta = egads.EgadsData(value = [0.8,0.9], units = '', long_name = 'sideslip calibration')
        self.C_errstat = egads.EgadsData(value = [1,0.9,1,0.8], units = '', long_name = 'static error coeffs')


    #def tearDown(self):
    #    self.foo.dispose()
    #    self.foo = None

    def test_altitude_pressure_cnrm(self):
        alt_p = thermodynamics.altitude_pressure_cnrm(self.T_v, self.P_s, self.P_surface, self.R_a_g)
        pass

    def test_density_dry_air_cnrm(self):
        rho = thermodynamics.density_dry_air_cnrm(self.P_s, self.T_s)
        pass

    def test_hum_rel_capacitive_cnrm(self):
        H_u = thermodynamics.hum_rel_capacitive_cnrm(self.Ucapf, self.T_s, self.P_s,
                                                     self.dP, self.C_t,
                                                     self.Fmin, self.C_0,
                                                     self.C_1, self.C_2)

        pass

    def test_pressure_angle_incidence_cnrm(self):
        P_s, dP, alpha, beta = thermodynamics.pressure_angle_incidence_cnrm(
                                             self.P_sr, self.delta_P_r, self.delta_P_h,
                                             self.delta_P_v, self.C_alpha, self.C_beta,
                                             self.C_errstat)
        pass

    def test_temp_potential_cnrm(self):
        theta = thermodynamics.temp_potential_cnrm(self.T_s, self.P_s, self.Racpa)

        pass

    def test_temp_potential_equiv_cnrm(self):
        theta_e = thermodynamics.temp_potential_equiv_cnrm(self.T_s, self.theta,
                                                           self.r, self.c_pa)
        pass

    def test_temp_static_cnrm(self):
        T_s = thermodynamics.temp_static_cnrm(self.Tt, self.dP, self.P_s, self.r_f, self.Racpa)
        pass

    def test_temp_virtual_cnrm(self):
        T_v = thermodynamics.temp_virtual_cnrm(self.T_s, self.r)

        pass

    def test_velocity_tas_cnrm(self):
        V_p = thermodynamics.velocity_tas_cnrm(self.T_s, self.P_s, self.dP, self.cpa, self.Racpa)
        pass

    def test_velocity_tas_longitudinal(self):
        V_tx = thermodynamics.velocity_tas_longitudinal_cnrm(self.V_t, self.alpha, self.beta)
        pass


if __name__ == '__main__':
    unittest.main()


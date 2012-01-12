__author__ = "mfreer"
__date__ = "$Date::                  $"
__version__ = "$Revision::           $"
__all__ = ['ThermodynamicsTestCase']

import numpy
import unittest

import egads
from egads import *
from egads.algorithms import thermodynamics



class  ThermodynamicsTestCase(unittest.TestCase):
    def setUp(self):
        self.Ucapf = egads.EgadsData(value=[10],
                                     units='Hz',
                                     long_name='output frequency of capacitive probe')
        
        self.Racpa = egads.EgadsData(value=287.058 / 1003.5,
                                     units='',
                                     long_name='Air gas constant divided by specific heat cap')

        self.cpa = egads.EgadsData(value=1003.5,
                                   units='J kg-1 K-1',
                                   long_name='specific heat of air at constant pressure')


        self.V_t = egads.EgadsData(value=200,
                                   units='m/s',
                                   long_name='true air speed')

        self.P_s = egads.EgadsData(value=[920],
                                   units='hPa',
                                   long_name='static pressure')

        self.P_sr = self.P_s

        self.T_t = egads.EgadsData(value=345,
                                   units='K',
                                   long_name='total temperature')

        self.dP = egads.EgadsData(value=[177.31],
                                  units='hPa',
                                  long_name='dynamic pressure')

        self.delta_P_r = self.dP.copy()

        self.delta_P_v = self.dP.copy()
        self.delta_P_v.value = self.delta_P_v.value * 0.1

        self.delta_P_h = self.dP.copy()
        self.delta_P_h.value = self.delta_P_h.value * 0.15

        self.r = egads.EgadsData(value=1e-3, units='g/kg', long_name='water vapor mixing ratio')

        self.T_s = egads.EgadsData(value=[298.15],
                                   units='K',
                                   long_name='static temperature')

        self.T_v = egads.EgadsData(value=[29],
                                   units='K',
                                   long_name='virtual temperature')

        self.theta = egads.EgadsData(value=288.76752,
                                     units='K',
                                     long_name='potential temperature')
                                     
        self.P_surface = egads.EgadsData(value=[1013.25],
                                         units='hPa',
                                         long_name='surface pressure')

        self.R_a_g = egads.EgadsData(value=[287.058 / 9.8],
                                     units='m/K',
                                     long_name='air gas constant divided by gravity')

        self.C_t = egads.EgadsData(value=1, units='%/C', long_name='temperature correction coeff')

        self.Fmin = egads.EgadsData(value=2, units='Hz', long_name='minimum acceptible frequency')

        self.C_0 = egads.EgadsData(value=0.5, units='', long_name='0th calibration coeff')

        self.C_1 = egads.EgadsData(value=0.6, units='', long_name='1st calibration coeff')

        self.C_2 = egads.EgadsData(value=0.5, units='', long_name='2nd calibration coeff')

        self.C_alpha = egads.EgadsData(value=[1, 0.9], units='', long_name='angle of attack calibration')
        self.C_beta = egads.EgadsData(value=[0.8, 0.9], units='', long_name='sideslip calibration')
        self.C_errstat = egads.EgadsData(value=[0.01, 0.009, 0.0001, 0.00008], units='', long_name='static error coeffs')

        self.r_f = egads.EgadsData(value=0.5, units='', long_name='probe recovery factor')

        self.alpha = egads.EgadsData(value=0.01,
                                     units='rad',
                                     long_name='angle of attack')

        self.beta = egads.EgadsData(value=0.005,
                                    units='rad',
                                    long_name='sideslip')

        self.array_test = egads.EgadsData(value=numpy.zeros(10)+10)

        self.array_shape = self.array_test.shape

        self.coeff_test = egads.EgadsData(value=1)
        self.coeff2_test = egads.EgadsData(value = [1,1])
        self.coeff4_test = egads.EgadsData(value = [1,1,1,1])

    #def tearDown(self):
    #    self.foo.dispose()
    #    self.foo = None

    def test_altitude_pressure_cnrm(self):
        alt_p = thermodynamics.AltitudePressureCnrm().run(self.T_v, self.P_s, self.P_surface, self.R_a_g)

        self.assertAlmostEqual(alt_p.value, 82.0105, 3, 'Altitudes dont match')

        alt_p = thermodynamics.AltitudePressureCnrm().run(self.array_test, self.array_test,
                                                      self.coeff_test, self.coeff_test)

        self.assertEqual(alt_p.shape, self.array_shape, 'Altitude pressure array shapes dont match')


    def test_density_dry_air_cnrm(self):
        rho = thermodynamics.DensityDryAirCnrm().run(self.P_s, self.T_s)

        self.assertAlmostEqual(rho.value, 1.0749, 3, 'Densities dont match')

        rho = thermodynamics.DensityDryAirCnrm().run(self.array_test, self.array_test)

        self.assertEqual(rho.shape, self.array_shape, 'Density array shapes dont match')


    def test_hum_rel_capacitive_cnrm(self):
        H_u = thermodynamics.HumRelCapacitiveCnrm().run(self.Ucapf, self.T_s, self.P_s,
                                                     self.dP, self.C_t,
                                                     self.Fmin, self.C_0,
                                                     self.C_1, self.C_2)

        self.assertAlmostEqual(H_u.value, 51.5624, 3, "Humidites dont match")

        H_u = thermodynamics.HumRelCapacitiveCnrm().run(self.array_test, self.array_test, self.array_test,
                                                     self.array_test, self.coeff_test,
                                                     self.coeff_test, self.coeff_test,
                                                     self.coeff_test, self.coeff_test)

        self.assertEqual(H_u.shape, self.array_shape, 'Humidity array shapes dont match')


    def test_pressure_angle_incidence_cnrm(self):
        P_s, dP, alpha, beta = thermodynamics.PressureAngleIncidenceCnrm().run(self.P_sr, self.delta_P_r, self.delta_P_h,
                                                                            self.delta_P_v, self.C_alpha, self.C_beta,
                                                                            self.C_errstat)

        self.assertAlmostEqual(P_s.value, 469.296, 2, 'Static pressure doesnt match')
        self.assertAlmostEqual(dP.value, 628.0132, 3, 'dynamic pressure doesnt match')
        self.assertAlmostEqual(alpha.value, 1.0254, 3, 'angle of attack doesnt match')
        self.assertAlmostEqual(beta.value, 0.83811, 3, 'sideslip doenst match')

        P_s, dP, alpha, beta = thermodynamics.PressureAngleIncidenceCnrm().run(self.array_test, self.array_test, self.array_test,
                                                                            self.array_test, self.coeff2_test, self.coeff2_test,
                                                                            self.coeff4_test)

        self.assertEqual(P_s.shape, self.array_shape, 'Static pressure array shapes dont match')
        self.assertEqual(dP.shape, self.array_shape, 'Dynamic pressure array shapes dont match')
        self.assertEqual(alpha.shape, self.array_shape, 'Angle of attack array shapes dont match')
        self.assertEqual(beta.shape, self.array_shape, 'sideslip array shapes dont match')


    def test_temp_potential_cnrm(self):
        theta = thermodynamics.TempPotentialCnrm().run(self.T_s, self.P_s, self.Racpa)

        self.assertAlmostEqual(theta.value, 305.34692, 3, 'Potential temp doesnt match')

        theta = thermodynamics.TempPotentialCnrm().run(self.array_test, self.array_test, self.coeff_test)

        self.assertEqual(theta.shape, self.array_shape, 'Potential temp array shapes dont match')

    def test_temp_potential_equiv_cnrm(self):
        theta_e = thermodynamics.TempPotentialEquivCnrm().run(self.T_s, self.theta,
                                                           self.r, self.cpa)

        self.assertAlmostEqual(theta_e.value, 288.7698, 3, 'Equivalent potential temp doesnt match')

        theta_e = thermodynamics.TempPotentialEquivCnrm().run(self.array_test, self.array_test,
                                                           self.array_test, self.coeff_test)

        self.assertEqual(theta_e.shape, self.array_shape, 'Equiv potential temp array shapes dont match')

    def test_temp_static_cnrm(self):
        T_s = thermodynamics.TempStaticCnrm().run(self.T_t, self.dP, self.P_s, self.r_f, self.Racpa)

        self.assertAlmostEqual(T_s.value, 336.30515, 3, 'Static temp doesnt match')

        T_s = thermodynamics.TempStaticCnrm().run(self.array_test, self.array_test,
                                              self.array_test, self.coeff_test,
                                              self.coeff_test)

        self.assertEqual(T_s.shape, self.array_shape, 'Static temp array shapes dont match')

    def test_temp_virtual_cnrm(self):
        T_v = thermodynamics.TempVirtualCnrm().run(self.T_s, self.r)

        self.assertAlmostEqual(T_v.value, 298.33109, 3, 'Virtual temp doesnt match')

        T_v = thermodynamics.TempVirtualCnrm().run(self.array_test, self.array_test)

        self.assertEqual(T_v.shape, self.array_shape, 'Virtual temp array shapes dont match')

    def test_velocity_tas_cnrm(self):
        V_p = thermodynamics.VelocityTasCnrm().run(self.T_s, self.P_s, self.dP, self.cpa, self.Racpa)

        self.assertAlmostEqual(V_p.value, 175.9018, 3, 'TAS doenst match')

        V_p = thermodynamics.VelocityTasCnrm().run(self.array_test, self.array_test,
                                               self.array_test, self.coeff_test,
                                               self.coeff_test)

        self.assertEqual(V_p.shape, self.array_shape, 'TAS array shapes dont match')

    def test_velocity_tas_longitudinal(self):
        V_tx = thermodynamics.VelocityTasLongitudinalCnrm().run(self.V_t, self.alpha, self.beta)

        self.assertAlmostEqual(V_tx.value, 199.9875, 3, 'Longitudinal TAS doesnt match')

        V_tx = thermodynamics.VelocityTasLongitudinalCnrm().run(self.array_test,
                                                             self.array_test,
                                                             self.array_test)

        self.assertEqual(V_tx.shape, self.array_shape, 'Longitudinal TAS array shapes dont match')



def suite():
    egads_thermo_suite = unittest.TestLoader().loadTestsFromTestCase(ThermodynamicsTestCase)
    return unittest.TestSuite([egads_thermo_suite])

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=5).run(suite())


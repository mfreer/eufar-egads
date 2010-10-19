__author__ = "mfreer"
__date__ = "$Date::                  $"
__version__ = "$Revision::           $"
__all__ = ['sample_area_oap_center_in_raf']

import egads
import inspect

def sample_area_oap_center_in_raf(Lambda, D_arms, dD, M, N):
    """

    FILE        sample_area_oap_all_in_raf.py

    VERSION     $Revision$

    CATEGORY    Microphysics

    PURPOSE     Calculation of 'center-in' sample area size for OAP probes

    DESCRIPTION Calculation of 'center-in' sample area size for OAP probes such as
                the 2DP, CIP, etc. The sample area varies by the number of shadowed
                diodes. This routine calculates a sample area per bin.

    INPUT       Lambda      coeff.  nm      Laser wavelength
                D_arms      coeff.  mm      Distance between probe arms
                dD          coeff.  um      Diode diameter
                M           coeff.  ()      Probe magnification factor
                N           coeff.  ()      Number of diodes in array

    OUTPUT      SA          Vector  m2      Sample area

    SOURCE      NCAR-RAF

    REFERENCES  NCAR-RAF Bulletin No. 24

    """

    SA = numpy.array([])
    Lambda_mm = Lambda.value * 1e-6                 # convert wavelength to mm
    dD_mm = dD.value * 1e-3                         # convert diameter to mm

    ESW = N.value * dD_mm

    for i in range(N.value):
        X = i+1
        R = X * dD_mm/2.0
        DOF = 6 * R ** 2 / (Lambda_mm)
        if DOF > D_arms.value:
            DOF = D_arms.value


        SA = numpy.append(SA, DOF * ESW * 1e-6)              # convert mm2 to m2



    result = egads.EgadsData(value = SA,
                               units = 'm2',
                               long_name = 'sample area, center in',
                               standard_name = '',
                               fill_value = None,
                               valid_range = None,
                               sampled_rate = None,
                               category = None,
                               calibration_coeff = None,
                               dependencies = None,
                               processor = inspect.stack()[0][3],
                               processor_version = __version__,
                               processor_date = __date__)



    return result



__author__ = "mfreer"
__date__ = "$Date$"
__version__ = "$Revision$"


import egads
import inspect

def velocity_tas_cnrm(T_s, P_s, dP, cpa, Racpa):
    """

    FILE        velocity_tas_cnrm.py

    VERSION     $Revision$

    CATEGORY    Thermodynamics

    PURPOSE     Calculate true airspeed

    DESCRIPTION Calculates true airspeed based on static temperature, static pressure
                and dynamic pressure using St Venant's formula.

    INPUT       T_s         vector  K or C      static temperature
                P_s         vector  hPa         static pressure
                dP          vector  hPa         dynamic pressure
                cpa         coeff.  J K-1 kg-1  specific heat of air (dry air is 1004 J K-1 kg-1)
                Racpa       coeff.  ()          R_a/c_pa

    OUTPUT      V_p         vector  m s-1       true airspeed

    SOURCE      CNRM/GMEI/TRAMM

    REFERENCES  "Mecanique des fluides", by S. Candel, Dunod.

                 Bulletin NCAR/RAF Nr 23, Feb 87, by D. Lenschow and
                 P. Spyers-Duran

    """


    V_p = (2 * cpa.value * T_s.value * ((1 + dP.value / P_s.value) ** Racpa.value
                        -1)) ** .5


    result = egads.ToolboxData(value = V_p,
                               units = 'm/s',
                               long_name = 'True Air Speed',
                               standard_name = 'platform_speed_wrt_air',
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



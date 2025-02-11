"""
Module :mod:`openquake.hazardlib.scalerel.watson2023` implements
:class:`Watson2023Crustal`
:class:`Watson2023Interface`

@ Author: E Watson

"""

from numpy import power, log10
from openquake.hazardlib.scalerel.base import BaseMSRSigma, BaseASRSigma

class Watson2023Crustal(BaseMSRSigma, BaseASRSigma):
    """
    Implements both magnitude-area and area-magnitude scaling relationships for crustal plate boundary faults.
    Intended to incorporate uncertainty between Leonard (2014), Wells & Coppersmith (1994) and Shaw (2023).
    """

    def get_median_area(self, mag, rake):
        """
        Rake ignored.
        Calculates median fault area from magnitude.
        """
        return power(10.0, (mag - 4.00))

    def get_std_dev_area(self, mag, rake):
        """
        Return 0.0 for now.
        """
        return 0.0

    def get_median_mag(self, area, rake):
        """
        Rake ignored.
        C = 4.0 provided a reasonable mid-point between Leonard (2014), Wells & Coppersmith (1994) and Shaw (2023) for a range of areas and magnitudes. 
        Adopted same functional form as Shaw (2023).
        """

        return log10(area)+4.00

    def get_std_dev_mag(self, area, rake):
        """
        Rake ignored.
        A standard deviation of 0.3 magnitude units on the median was selected to cover the range of values from Leonard (2014), Wells & Coppersmith (1994) and Shaw (2023).
        """
        return 0.3

class Watson2023Interface(BaseMSRSigma, BaseASRSigma):
    """
    Implements both magnitude-area and area-magnitude scaling relationships for subduction interface.
    Intended to incorporate uncertainty between Strasser (2010), Thingbaijam (2017) and Shaw (2023). Allen & Hayes was ignored because it gave unreasonably large magnitude values.
    """

    def get_median_area(self, mag, rake):
        """
        Rake ignored.
        Calculates median fault area from magnitude.
        """
        return power(10.0, (mag - 3.80))

    def get_std_dev_area(self, mag, rake):
        """
        Return 0.0 for now.
        """
        return 0.0

    def get_median_mag(self, area, rake):
        """
        Rake ignored.
        C = 3.8 provided a reasonable mid-point between Strasser (2010), Thingbaijam (2017) and Shaw (2023) for a range of areas and magnitudes. 
        Adopted same functional form as Shaw (2023).
        """

        return log10(area)+3.80

    def get_std_dev_mag(self, area, rake):
        """
        Rake ignored.
        A standard deviation of 0.3 magnitude units on the median was selected to cover the range of values from Strasser (2010), Thingbaijam (2017) and Shaw (2023).
        """
        return 0.3
        
class Watson2023Interface_Chile(BaseMSRSigma, BaseASRSigma):
    """
    Implements both magnitude-area and area-magnitude scaling relationships for subduction interface. Modified for Nazca subduction interface in Chile (Sections 1 and 2 of Pagani et al. 2021 model).
    Intended to incorporate uncertainty between Strasser (2010), Thingbaijam (2017) and Shaw (2023). Allen & Hayes was ignored because it gave unreasonably large magnitude values.
    """

    def get_median_area(self, mag, rake):
        """
        Rake ignored.
        Calculates median fault area from magnitude.
        """
        return power(10.0, (mag - 3.70))

    def get_std_dev_area(self, mag, rake):
        """
        Return 0.0 for now.
        """
        return 0.0

    def get_median_mag(self, area, rake):
        """
        Rake ignored.
        C = 3.7 provided a reasonable mid-point between Strasser (2010), Thingbaijam (2017) and Shaw (2023) for a range of areas and magnitudes. 
        Adopted same functional form as Shaw (2023).
        """

        return log10(area)+3.70

    def get_std_dev_mag(self, area, rake):
        """
        Rake ignored.
        A standard deviation of 0.37 magnitude units on the median was selected to cover the range of values from Strasser (2010), Thingbaijam (2017) and Shaw (2023).
        """
        return 0.37
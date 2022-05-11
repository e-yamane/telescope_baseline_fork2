# -*- coding: utf-8 -*-
import math


class Parameters:
    """This class is parameter holder

    The parameter holder class Parameters is implemented in Singleton pattern (see. GoF book).
    Below properties are defined.

    Properties:
    Only getter is implemented without attribute:
        telescope_through_put, total_efficiency, orbital_period, earth_mu, earth_c1, earth_c2, inclination

    Only getter is implemented with attribute:
        pixel_size, maneuver_time, large_maneuver_time, detector_format_x, detector_format_y,
        detector_placement_x, detector_placement_y, orbital_eccentricity

    Getter and Setter are implemented:
        aperture_diameter, aperture_inner_diameter, focal_length, full_well_electron, saturation_magnitude,
        quantum_efficiency, attitude_control_error, high_wavelength_limit, low_wavelength_limit, filter_efficiency,
        one_mirror_efficiency, number_of_mirrors, read_out_noise, dark_current, galactic_center_photon_flux,
        standard_magnitude, faint_end_magnitude, orbital_height

    Not implemented yet
        saturation time, ltan

    Known problem:
        Thread safety is not guaranteed.

    """
    __instance = None


    @staticmethod
    def get_instance():
        if Parameters.__instance is None:
            Parameters()
        return Parameters.__instance

    def __init__(self):
        if Parameters.__instance is None:
            Parameters.__instance = self
        else:
            raise Exception("Singleton Class")
        self.__EARTH_MASS = 5.9724E24  # kg
        self.__CONST_OF_GRAVITATION = 6.6743E-11  # meter^3 kg^-1 s^-2
        self.__EQUATORIAL_EARTH_RADIUS = 6.3781E6  # meter
        self.__POLAR_EARTH_RADIUS = 6.3568E6  # meter
        self.__EARTH_J2 = 1.082632
        self.__ONE_YEAR = 31556926  # seconds
        self.__orbital_eccentricity = 0
        self.__aperture_diameter = 0.4  # meter
        self.__aperture_inner_diameter = 0.14  # meter
        self.__focal_length = 4.8  # meter
        self.__pixel_size = 1.0e-5  # meter
        self.__maneuver_time = 115  # second
        self.__large_maneuver_time = 220  # second
        self.__full_well_electron = 100000
        self.__saturation_magnitude = 10.0
        self.__standard_magnitude = 12.5
        self.__faint_end_magnitude = 14.5
        self.__quantum_efficiency = 0.8
        self.__attitude_control_error = 275  # mas / 7 seconds
        self.__high_wavelength_limit = 1.6e-6  # meter
        self.__low_wavelength_limit = 1.0e-6  # meter
        self.__filter_efficiency = 0.95
        self.__one_mirror_efficiency = 0.98
        self.__number_of_mirrors = 5
        self.__read_out_noise = 25  # electrons / read
        self.__dark_current = 5  # electrons / sec / pixel
        self.__galactic_center_photon_flux = 5  # electrons / sec / pixel
        self.__detector_format_x = 1952
        self.__detector_format_y = 1952
        self.__detector_placement_x = 2
        self.__detector_placement_y = 2
        self.__orbital_height = 5.5E5  # meter

    @property
    def aperture_diameter(self):
        return self.__aperture_diameter

    @aperture_diameter.setter
    def aperture_diameter(self, value):
        if value < self.__aperture_inner_diameter:
            raise Exception('diameter value is smaller than inner diameter.')
        self.__aperture_diameter = value

    @property
    def aperture_inner_diameter(self):
        return self.__aperture_inner_diameter

    @aperture_inner_diameter.setter
    def aperture_inner_diameter(self, value):
        if value > self.__aperture_diameter:
            raise Exception('inner diameter value is larger than diameter.')
        self.__aperture_inner_diameter = value

    @property
    def focal_length(self):
        return self.__focal_length

    @focal_length.setter
    def focal_length(self, value):
        self.__focal_length = value

    @property
    def pixel_size(self):
        return self.__pixel_size

    @property
    def maneuver_time(self):
        return self.__maneuver_time

    @property
    def large_maneuver_time(self):
        return self.__large_maneuver_time

    @property
    def full_well_electron(self):
        return self.__full_well_electron

    @full_well_electron.setter
    def full_well_electron(self, value):
        if value < 0:
            raise Exception('full well electron should be positive.')
        self.__full_well_electron = value

    @property
    def saturation_magnitude(self):
        return self.__saturation_magnitude

    @saturation_magnitude.setter
    def saturation_magnitude(self, value):
        self.__saturation_magnitude = value

    @property
    def quantum_efficiency(self):
        return self.__quantum_efficiency

    @quantum_efficiency.setter
    def quantum_efficiency(self, value):
        if not 0 <= value <= 1:
            raise Exception('Quantum Efficiency should be between 0 and 1.')
        self.__quantum_efficiency = value

    @property
    def attitude_control_error(self):
        return self.__attitude_control_error

    @attitude_control_error.setter
    def attitude_control_error(self, value):
        if value < 0:
            raise Exception('Attitude Control Error should be positive.')
        self.__attitude_control_error = value

    @property
    def high_wavelength_limit(self):
        return self.__high_wavelength_limit

    @high_wavelength_limit.setter
    def high_wavelength_limit(self, value):
        self.__high_wavelength_limit = value

    @property
    def low_wavelength_limit(self):
        return self.__low_wavelength_limit

    @low_wavelength_limit.setter
    def low_wavelength_limit(self, value):
        self.__low_wavelength_limit = value

    @property
    def filter_efficiency(self):
        return self.__filter_efficiency

    @filter_efficiency.setter
    def filter_efficiency(self, value):
        self.__filter_efficiency = value

    @property
    def one_mirror_efficiency(self):
        return self.__one_mirror_efficiency

    @one_mirror_efficiency.setter
    def one_mirror_efficiency(self, value):
        self.__one_mirror_efficiency = value

    @property
    def number_of_mirrors(self):
        return self.__number_of_mirrors

    @number_of_mirrors.setter
    def number_of_mirrors(self, value):
        self.__number_of_mirrors = value

    @property
    def telescope_through_put(self):
        return math.pow(self.__one_mirror_efficiency, self.__number_of_mirrors)

    @property
    def total_efficiency(self):
        return self.telescope_through_put * self.__filter_efficiency * self.__quantum_efficiency

    @property
    def read_out_noise(self):
        return self.__read_out_noise

    @read_out_noise.setter
    def read_out_noise(self, value):
        self.__read_out_noise = value

    @property
    def dark_current(self):
        return self.__dark_current

    @dark_current.setter
    def dark_current(self, value):
        self.__dark_current = value

    @property
    def galactic_center_photon_flux(self):
        return self.__galactic_center_photon_flux

    @galactic_center_photon_flux.setter
    def galactic_center_photon_flux(self, value):
        self.__galactic_center_photon_flux = value

    @property
    def detector_format_x(self):
        return self.__detector_format_x

    @property
    def detector_format_y(self):
        return self.__detector_format_y

    @property
    def detector_placement_x(self):
        return self.__detector_placement_x

    @property
    def detector_placement_y(self):
        return self.__detector_placement_y

    @property
    def standard_magnitude(self):
        return self.__standard_magnitude

    @standard_magnitude.setter
    def standard_magnitude(self, value):
        self.__standard_magnitude = value

    @property
    def faint_end_magnitude(self):
        return self.__faint_end_magnitude

    @faint_end_magnitude.setter
    def faint_end_magnitude(self, value):
        self.__faint_end_magnitude = value

    @property
    def orbital_height(self):
        return self.__orbital_height

    @orbital_height.setter
    def orbital_height(self, value):
        self.__orbital_height = value

    @property
    def orbital_period(self):
        return 2 * math.pi * math.pow(self.__EQUATORIAL_EARTH_RADIUS + self.orbital_height, 1.5) / math.sqrt(
            self.__CONST_OF_GRAVITATION * self.__EARTH_MASS)

    @property
    def earth_mu(self):
        return self.__CONST_OF_GRAVITATION * self.__EARTH_MASS

    @property
    def earth_c1(self):
        return -3 * math.pi * self.__EARTH_J2 * math.pow(self.__EQUATORIAL_EARTH_RADIUS / 1000, 2) \
               * self.__ONE_YEAR * math.sqrt(self.earth_mu) / 2 / math.pi * 180 / math.pi / math.pow(10000, 1.5)

    @property
    def earth_c2(self):
        return 360 / self.earth_c1

    @property
    def orbital_eccentricity(self):
        return self.__orbital_eccentricity

    @property
    def inclination(self):
        return math.acos(self.earth_c2 * math.pow((self.__EQUATORIAL_EARTH_RADIUS + self.__orbital_height) / 1000, 3.5)
                         * math.pow(1 - self.orbital_eccentricity * self.orbital_eccentricity, 2) * math.sqrt(1000))

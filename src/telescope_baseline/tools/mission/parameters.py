# -*- coding: utf-8 -*-
import math


class Parameters:
    """This class is parameter holder

    The parameter holder class Parameters is implemented in Singleton pattern (see. GoF book).
    Below properties are defined.

    Properties:
    Only getter is implemented without attribute:
        telescope_through_put, total_efficiency, orbital_period, earth_mu, earth_c1, earth_c2, inclination,
        aperture_inner_diameter,

    Only getter is implemented with attribute:
        pixel_size, maneuver_time, large_maneuver_time, detector_format_x, detector_format_y,
        detector_placement_x, detector_placement_y, orbital_eccentricity

    Getter and Setter are implemented:
        effective_pupil_diameter, central_obscuration_ratio, effective_focal_length, full_well_electron,
        saturation_magnitude, spider_type, spider_thickness
        quantum_efficiency, attitude_control_error, high_wavelength_limit, low_wavelength_limit, filter_efficiency,
        one_mirror_efficiency, number_of_mirrors, read_out_noise, dark_current, galactic_center_photon_flux,
        standard_magnitude, faint_end_magnitude, orbital_altitude, exposure_time

    Not implemented yet
        saturation time, ltan

    Functions:
        cpix

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
            raise Exception("Parameters is already instantiated.")
        self.__EARTH_MASS = 5.9724E24  # kg
        self.__CONST_OF_GRAVITATION = 6.6743E-11  # meter^3 kg^-1 s^-2
        self.__EQUATORIAL_EARTH_RADIUS = 6.3781E6  # meter
        self.__POLAR_EARTH_RADIUS = 6.3568E6  # meter
        self.__EARTH_J2 = 1.082632
        self.__ONE_YEAR = 31556926  # seconds
        self.__orbital_eccentricity = 0
        self.__effective_pupil_diameter = 0.36  # meter
        self.__central_obscuration_ratio = 0.35
        self.__effective_focal_length = 4.8  # meter
        self.__pixel_size = 1.0e-5  # meter
        self.__maneuver_time = 115  # second
        self.__large_maneuver_time = 220  # second
        self.__full_well_electron = 100000
# TODO: Definition of magnitude should be contains colour
        self.__saturation_magnitude = 10.0
        self.__standard_magnitude = 12.5
        self.__faint_end_magnitude = 14.5
        self.__quantum_efficiency = 0.8
        self.__attitude_control_error_mas = 275  # mas / 7 seconds
        self.__high_wavelength_limit = 1.6e-6  # meter
        self.__low_wavelength_limit = 1.0e-6  # meter
        self.__filter_efficiency = 0.95
        self.__one_mirror_efficiency = 0.98
        self.__number_of_mirrors = 5
        self.__read_out_noise = 25  # electrons / read
        self.__dark_current = 5  # electrons / sec / pixel
        self.__background_photon_flux = 5  # electrons / sec / pixel
        self.__detector_placement_x = 2
        self.__detector_placement_y = 2
        self.__detector_separation_x = 0.02196  # meter
        self.__detector_separation_y = 0.02196  # meter
        self.__orbital_altitude = 5.5E5  # meter
        self.__spider_type = ''
        self.__spider_thickness = 0
        self.__window_size_x = 9
        self.__window_size_y = 9
        self.__pixel_sampling_frequency = 2e5  # Hz
        self.__ncol_ch = 123
        self.__nrow_ch = 1952
        self.__n_ch = 16
        self.__npix_pre = 8
        self.__npix_post = 8
        self.__exposure_time = 10.0  # second(s)
# TODO: check it should be const or variable?
        self.__cell_pix = 13
        self.__use_M_flag = False

    @property
    def effective_pupil_diameter(self):
        return self.__effective_pupil_diameter

    def set_effective_pupil_diameter(self, value):
        self.__effective_pupil_diameter = value

    @property
    def central_obscuration_ratio(self):
        return self.__central_obscuration_ratio

    def set_central_obscuration_ratio(self, value):
        self.__central_obscuration_ratio = value

    @property
    def aperture_inner_diameter(self):
        return self.__effective_pupil_diameter * self.__central_obscuration_ratio

    @property
    def effective_focal_length(self):
        return self.__effective_focal_length

    def set_effective_focal_length(self, value):
        if self.__use_M_flag:
            return
        self.__effective_focal_length = value

    def set_effective_focal_length_from_M(self, m):
        self.__use_M_flag = True
        self.__effective_focal_length = self.__pixel_size * m * 1000 / self.__cell_pix

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

    def set_full_well_electron(self, value):
        if value < 0:
            raise ValueError('full well electron should be positive.')
        self.__full_well_electron = value

    @property
    def saturation_magnitude(self):
        return self.__saturation_magnitude

    def set_saturation_magnitude(self, value):
        self.__saturation_magnitude = value

    @property
    def quantum_efficiency(self):
        return self.__quantum_efficiency

    def set_quantum_efficiency(self, value):
        if not 0 <= value <= 1:
            raise ValueError('Quantum Efficiency should be between 0 and 1.')
        self.__quantum_efficiency = value

    @property
    def attitude_control_error_mas(self):
        return self.__attitude_control_error_mas

    def set_attitude_control_error_mas(self, value):
        if value < 0:
            raise ValueError('Attitude Control Error should be positive.')
        self.__attitude_control_error_mas = value

    @property
    def high_wavelength_limit(self):
        return self.__high_wavelength_limit

    def set_high_wavelength_limit(self, value):
        self.__high_wavelength_limit = value

    @property
    def low_wavelength_limit(self):
        return self.__low_wavelength_limit

    def set_low_wavelength_limit(self, value):
        self.__low_wavelength_limit = value

    @property
    def filter_efficiency(self):
        return self.__filter_efficiency

    def set_filter_efficiency(self, value):
        self.__filter_efficiency = value

    @property
    def one_mirror_efficiency(self):
        return self.__one_mirror_efficiency

    def set_one_mirror_efficiency(self, value):
        self.__one_mirror_efficiency = value

    @property
    def number_of_mirrors(self):
        return self.__number_of_mirrors

    def set_number_of_mirrors(self, value):
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

    def set_read_out_noise(self, value):
        self.__read_out_noise = value

    @property
    def dark_current(self):
        return self.__dark_current

    def set_dark_current(self, value):
        self.__dark_current = value

# TODO: The unit of background photon flux should be independent of diameter and band
    @property
    def background_photon_flux(self):
        return self.__background_photon_flux

    def set_background_photon_flux(self, value):
        self.__background_photon_flux = value

    @property
    def detector_format_x(self):
        return self.__nrow_ch

    @property
    def detector_format_y(self):
        return self.__ncol_ch * self.__n_ch - self.__npix_pre - self.__npix_post

    @property
    def detector_placement_x(self):
        return self.__detector_placement_x

    @property
    def detector_placement_y(self):
        return self.__detector_placement_y

    @property
    def standard_magnitude(self):
        return self.__standard_magnitude

    def set_standard_magnitude(self, value):
        self.__standard_magnitude = value

    @property
    def faint_end_magnitude(self):
        return self.__faint_end_magnitude

    def set_faint_end_magnitude(self, value):
        self.__faint_end_magnitude = value

    @property
    def orbital_altitude(self):
        return self.__orbital_altitude

    def set_orbital_altitude(self, value):
        self.__orbital_altitude = value

    @property
    def orbital_period(self):
        return 2 * math.pi * math.pow(self.__EQUATORIAL_EARTH_RADIUS + self.orbital_altitude, 1.5) / math.sqrt(
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
        return math.acos(self.earth_c2 * math.pow((self.__EQUATORIAL_EARTH_RADIUS + self.__orbital_altitude) / 1000, 3.5)
                         * math.pow(1 - self.orbital_eccentricity * self.orbital_eccentricity, 2) * math.sqrt(1000))

    @property
    def spider_type(self):
        return self.__spider_type

    def set_spider_type(self, value):
        self.__spider_type = value

    @property
    def spider_thickness(self):
        return self.__spider_thickness

    def set_spider_thickness(self, value):
        self.__spider_thickness = value

    @property
    def window_size_x(self):
        return self.__window_size_x

    def set_window_size_x(self, value):
        self.__window_size_x = value

    @property
    def window_size_y(self):
        return self.__window_size_y

    def set_window_size_y(self, value):
        self.__window_size_y = value

    @property
    def ncol_ch(self):
        return self.__ncol_ch

    @property
    def nrow_ch(self):
        return self.nrow_ch

    @property
    def npix_pre(self):
        return self.__npix_pre

    @property
    def npix_post(self):
        return self.__npix_post

    @property
    def n_ch(self):
        return self.__n_ch

    @property
    def pixel_sampling_frequency(self):
        return self.__pixel_sampling_frequency

    @property
    def detector_separation_x(self):
        return self.__detector_separation_x

    @property
    def detector_separation_y(self):
        return self.__detector_separation_y

    @property
    def exposure_time(self):
        return self.__exposure_time

    def set_exposure_time(self, value):
        self.__exposure_time = value

    def cpix(self, wave_length=1.4e-5):
        return wave_length * self.__effective_focal_length / self.__effective_pupil_diameter / self.__pixel_size


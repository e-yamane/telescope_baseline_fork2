import math

import pytest
from telescope_baseline.tools.mission.parameters import Parameters


def test_singleton():
    sg = Parameters.get_instance()
    two = Parameters.get_instance()
    assert -0.0001 < sg.aperture_diameter - two.aperture_diameter < 0.0001
    sg.aperture_diameter = 0.2
    assert 0.19999 < two.aperture_diameter < 0.200001
    assert -0.0001 < sg.aperture_diameter - two.aperture_diameter < 0.0001


def test_singleton_2():
    one = Parameters.get_instance()
    one.aperture_diameter = 0.2
    two = Parameters.get_instance()
    assert -0.0001 < one.aperture_diameter - 0.2 < 0.0001


def test_efficiency():
    # number of mirror = 5, mirror reflection rate = 0.98, QE = 0.8, filter through put = 0.9 is assumed
    sg = Parameters.get_instance()
    sg.__number_of_mirrors = 5
    sg.__one_mirror_efficiency = 0.98
    sg.__filter_efficiency = 0.9
    sg.__quantum_efficiency = 0.8
    assert 0.6869 < sg.total_efficiency < 0.6870


def test_period():
    sg = Parameters.get_instance()
    sg.__orbital_height = 550
    assert 5738 < sg.orbital_period < 5740


def test_inclination():
    sg = Parameters.get_instance()
    sg.__orbital_height = 550
    assert 97.5 < math.degrees(sg.inclination) < 97.7

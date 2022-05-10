import math

import pytest
from tools.mission.parameters import Parameters


@pytest.fixture
def sg():
    one = Parameters()
    return one


def test_singleton(sg):
    two = Parameters()
    assert -0.0001 < sg.aperture_diameter - two.aperture_diameter < 0.0001
    sg.aperture_diameter = 0.2
    assert 0.19999 < two.aperture_diameter < 0.200001


def test_efficiency(sg):
    # number of mirror = 5, mirror reflection rate = 0.98, QE = 0.8, filter through put = 0.9 is assumed
    assert 0.6869 < sg.total_efficiency < 0.6870


def test_period(sg):
    # height = 550 km is assumed
    assert 5738 < sg.orbital_period < 5740


def test_inclination(sg):
    # height = 550km is assumed
    assert 97.5 < math.degrees(sg.inclination) < 97.7

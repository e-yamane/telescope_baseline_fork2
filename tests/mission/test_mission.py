import math

from pytest import approx
from telescope_baseline.tools.mission.parameters import Parameters


def test_singleton():
    sg = Parameters.get_instance()
    two = Parameters.get_instance()
    assert -0.0001 < sg.aperture_diameter - two.aperture_diameter < 0.0001
    sg.set_aperture_diameter(0.2)
    assert 0.19999 < two.aperture_diameter < 0.200001
    assert -0.0001 < sg.aperture_diameter - two.aperture_diameter < 0.0001


def test_singleton_2():
    one = Parameters.get_instance()
    one.set_aperture_diameter(0.2)
    two = Parameters.get_instance()
    assert -0.0001 < one.aperture_diameter - 0.2 < 0.0001


def test_efficiency():
    # number of mirror = 5, mirror reflection rate = 0.98, QE = 0.8, filter through put = 0.9 is assumed
    sg = Parameters.get_instance()
    # sg.set_number_of_mirrors(5)
    # sg.set_one_mirror_efficiency(0.98)
    sg.set_filter_efficiency(0.95)
    sg.set_quantum_efficiency(0.8)
    assert sg.total_efficiency == approx(0.6152292079156423)


def test_troughput():
    sg = Parameters.get_instance()
    val = sg.telescope_through_put
    assert val == approx(0.8095121156784766)


def test_period():
    sg = Parameters.get_instance()
    sg.set_orbital_height(550000)
    assert 5738 < sg.orbital_period < 5740


def test_inclination():
    sg = Parameters.get_instance()
    sg.set_orbital_height(550000)
    assert 97.5 < math.degrees(sg.inclination) < 97.7

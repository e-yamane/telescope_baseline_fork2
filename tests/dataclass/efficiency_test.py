"""test for wl_eff

"""
from pytest import approx
import pkg_resources
from telescope_baseline.dataclass.efficiency import Efficiency


def test_from_json():
    testdata = 'data/teleff.json'
    speclist = pkg_resources.resource_filename('telescope_baseline', testdata)
    efficiency = Efficiency.from_json(speclist)
    assert efficiency.efficiency[3] == approx(0.84)
    assert efficiency.wavelength[3] == approx(1.4)

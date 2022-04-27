"""test for wl_eff

"""
import pytest
import pkg_resources
import numpy as np
from telescope_baseline.dataclass.wl_eff import WlEfic

def test_from_json():
    speclist=pkg_resources.resource_filename('telescope_baseline', 'data/teleff.json')
    wl_eff = WlEfic.from_json(speclist)
    assert wl_eff.efficiency[10] == 0.023012329078860527
    assert wl_eff.wavelength[10] == 0.51

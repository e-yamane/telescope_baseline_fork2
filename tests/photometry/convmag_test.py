"""test for nstar.

"""
import pytest
from telescope_baseline.photometry.convmag import get_magdict, get_flux
from astropy import units as u
import numpy as np

def test_get_magdict():
    band = "J"
    mag = 10.0
    magdict = get_magdict()
    mask = magdict['band'] == band
    flux = get_flux(band, mag, magdict)
    assert flux.to(u.erg/u.s/u.m/u.m/u.nm).value - 3.3113112148259078e-09 == 0.0


if __name__ == "__main__":
    test_get_magdict()

    

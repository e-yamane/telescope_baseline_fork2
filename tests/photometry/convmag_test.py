"""test for nstar.

"""
import pytest
from telescope_baseline.photometry.convmag import get_magdict, get_flux, get_mag
from astropy import units as u
import numpy as np

def test_get_flux():
    band = "J"
    mag = 10.0
    magdict = get_magdict()
    mask = magdict['band'] == band
    flux = get_flux(band, mag, magdict)
    assert flux.to(u.erg/u.s/u.m/u.m/u.nm).value == pytest.approx(3.3113112148259078e-09)

def test_get_mag():
    band = "J"
    magdict = get_magdict()
    flux=3.3113112148259078e-09*u.erg/u.s/u.m/u.m/u.nm
    assert get_mag(band, flux, magdict)==pytest.approx(10.0)


if __name__ == "__main__":
    test_get_flux()
    test_get_mag()

    

from exocounts import exocounts
from exocounts import convmag
from astropy import constants as const
from astropy import units as u
import numpy as np

ejas=exocounts.InstClass()
ejas.lamb = 1.25*u.micron #micron
ejas.dlam = 0.7*u.micron #micron
#ejas.lamb = 1.3*u.micron #micron
#ejas.dlam = 0.6*u.micron #micron

ejas.dtel = 0.34*u.m #telescope diameter m
ejas.dstel = 0.14*u.m #secondary telescope diameter m or 12.4 (3 tels)

QE=0.7
ejas.throughput = QE*0.85*0.95
ejas.ndark = 15.5/u.s #dark current
ejas.nread = 15.0 #nr
ejas.fullwell = 150000.

target=exocounts.TargetClass()
target.teff = 3000.0*u.K #K
target.rstar = 0.2*const.R_sun #Rsolar
target.d = 15.0*u.pc #pc

obs=exocounts.ObsClass(ejas,target) 

obs.texposure = 0.0833*u.h #cadence [hour]
obs.tframe = 12.5*u.s  #time for one frame [sec]
obs.napix = 15 # number of the pixels in aperture 
obs.mu = 1 
S=1.8*1.8*np.pi #core size
obs.effnpix = S/3.0 #3 is an approx. increment factor of PSF
obs.mu = 1 

target.d=16.0*u.pc #change targets
obs.target = target
obs.update()

magdict=convmag.get_magdict()
print("H mag=",convmag.get_mag("H",obs.flux,magdict))
print("J mag=",convmag.get_mag("J",obs.flux,magdict))
print("Hw mag=",0.7*convmag.get_mag("J",obs.flux,magdict)+0.3*convmag.get_mag("H",obs.flux,magdict))
print("V mag=",convmag.get_mag("V",obs.flux,magdict))
print("=========================")
print("saturation?",obs.sat)
print("dark [ppm]=",obs.sigd)
print("readout [ppm]=",obs.sigr)
print("photon [ppm]=",obs.sign)
print("=========================")
print("photon relative=",obs.sign_relative)

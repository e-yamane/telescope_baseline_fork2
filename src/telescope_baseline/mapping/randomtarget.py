import numpy as np
import matplotlib.pyplot as plt
from healpy.visufunc import projscatter,projplot
from healpy.pixelfunc import  vec2ang, pix2ang, nside2npix
import healpy as hp

def rantarget(N=200):
    #target
    vec=np.random.normal(0.0,1.0,3*N).reshape((3,N))
    vec=vec/np.sqrt(np.sum(vec**2,axis=0))
    ang=np.array(vec2ang(vec))
    return ang

def reference(Mside=16):
    """

    Returns:
       theta,phi
    
    """
    #reference
    Mpix=nside2npix(Mside)
    refang=np.array(pix2ang(16,np.arange(0,Mpix)))
    return refang

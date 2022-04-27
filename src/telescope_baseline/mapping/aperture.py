import numpy as np
from healpy.pixelfunc import ang2vec, vec2ang

def single_detector_convex(ang_detector,PA,width):
    """
    Args: 
        ang_detector: theta, phi of the detector
        PA: position angle of the detector (north up)
        width: detector width in radian
    Returns:
        detecter covex
    
    """
    
    thetac,phic=ang_detector
    ez=np.array([0.0,0.0,1.0])
    half_diagonal_angle=width/np.sqrt(2.0)
    e0=Roty(half_diagonal_angle)@ez
    convex0=np.array([Rotz(-3.0*np.pi/4.0)@e0,Rotz(-np.pi/4.0)@e0,Rotz(np.pi/4.0)@e0,Rotz(3.0*np.pi/4.0)@e0])
    #for i in range(0,4):
    #    c=Rotz(phic)@Roty(thetac)@Rotz(PA)@convex0[i,:]
    C=np.einsum('ij,kj->ki',Rotz(PA),convex0)
    C=np.einsum('ij,kj->ki',Roty(thetac),C)
    C=np.einsum('ij,kj->ki',Rotz(phic),C)
    print(C)
    return C.T


def Roty(theta):
    return np.array([[np.cos(theta),0.0,np.sin(theta)],[0.0,1.0,0.0],[-np.sin(theta),0.0,np.cos(theta)]])

def Rotz(theta):
    return np.array([[np.cos(theta),-np.sin(theta),0.0],[np.sin(theta),np.cos(theta),0.0],[0.0,0.0,1.0]])

def vec2ring(x):
    """convert a vector to a ring
    Args:
        vertex list (vertex, coodinate)

    Returns:
        ring (edge, left-right, coordinate)

    """
    Nvertex, Ncoordinate=np.shape(x)
    if Nvertex%2 == 1:
        print("Nvertex needs to be even")
    rs=(int(Nvertex/2),2,Ncoordinate)
    x1=x.reshape(rs) 
    x0=np.roll(x,1,axis=0).reshape(rs)
    return np.hstack([x0,x1]).reshape((Nvertex,2,Ncoordinate))

def cos_angle_from_normal_vectorAB(a,b,x):
    """cos angle between the normal vector defined by a, b and x
    Args:
       a: 3D vetcor of A
       b: 3D vector of B
       x: vectors whose cos angle from normal vector of the ABO plane to be computed
     
    Returns:
       cos_angles
    """
    return x@np.cross(a,b) 


def convex_on_sphere(angv,angw):
    """checking if the points 
    Args:
        angv: list of theta,phi points that defines the convex on a sphere
        angw: theta,phi lists in or out of the convex on a sphere

    Returns:
        1 (in convex) or 0 (out of convex)
    """

    v=ang2vec(angv[0],angv[1])
    w=ang2vec(angw[0],angw[1])
    Nvertex,Ncoordinate=np.shape(v)
    ring=vec2ring(v)
    cosa=[]
    for i in range(0,Nvertex):
        cosa.append(cos_angle_from_normal_vectorAB(ring[i,0,:],ring[i,1,:],w))
    cosa = np.array(cosa)
    mask=(cosa>=0.0)*(cosa<=1.0)
    return np.prod(mask,axis=0)


def test_single_detector_convex():
    convex=single_detector_convex(np.array([np.pi/10.0,np.pi/9.0]),np.pi/5.0,np.pi/8.0)


def test_single_detector_convex_in():
    convex=single_detector_convex(np.array([np.pi/10.0,np.pi/9.0]),np.pi/5.0,np.pi/8.0)
    w=np.array([0,0,1])
    q=np.array([1/np.sqrt(2.0),1/np.sqrt(2.0),1/np.sqrt(4.0)])
    v=np.array([w,q,w,q])
    angw=np.array(vec2ang(v))    
    ans=convex_on_sphere(convex,angw)    
    print(ans)
    
if __name__ == "__main__":
    from telescope_baseline.mapping.randomtarget import rantarget
    targets=rantarget(N=100000)
    convex=single_detector_convex(np.array([np.pi/4.0,0.0*np.pi/9.0]),np.pi/5.0,np.pi/4.0)
    ans=convex_on_sphere(convex,targets)
    ans=np.array(ans,dtype=np.bool)
    print(ans)
    print(np.shape(targets))
    
    import matplotlib.pyplot as plt
    from healpy.visufunc import projscatter
    import healpy as hp
    Nside=16
    emparr=np.zeros(hp.nside2npix(Nside))
    hp.mollview(emparr,cmap="bwr")
    projscatter(targets,alpha=0.4,marker="+")
    projscatter(targets[:,ans],alpha=0.4,marker="+")
    print(np.sum(ans))
    #    frame()
    plt.show()

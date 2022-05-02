import numpy as np
from healpy.pixelfunc import ang2vec, vec2ang

                         

def square_convex(center,PA,width):
    """compute a single sqaure convex
    Args: 
        center: theta, phi of the center
        PA: position angle of the detector (north up)
        width: detector width in radian
    Returns:
        detecter convex (ang)
    
    """
    
    thetac,phic=center
    ez=np.array([0.0,0.0,1.0])
    half_diagonal_angle=width/np.sqrt(2.0)
    e0=Roty(half_diagonal_angle)@ez
    convex0=np.array([Rotz(-3.0*np.pi/4.0)@e0,Rotz(-np.pi/4.0)@e0,Rotz(np.pi/4.0)@e0,Rotz(3.0*np.pi/4.0)@e0])
    #for i in range(0,4):
    #    c=Rotz(phic)@Roty(thetac)@Rotz(PA)@convex0[i,:]
    C=np.einsum('ij,kj->ki',Rotz(PA),convex0)
    C=np.einsum('ij,kj->ki',Roty(thetac),C)
    C=np.einsum('ij,kj->ki',Rotz(phic),C)
    Cang = vec2ang(C)
    return np.array(Cang)


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
       a: 3D vetcor of A, (3,) or (N, 3)
       b: 3D vector of B, (3,) or (N, 3)
       x: vectors whose cos angle from normal vector of the ABO plane to be computed 3 or (M, 3)
     
    Returns:
       cos_angles, float or (N,M)
    """
    return (x@np.cross(a,b).T).T


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
    #cosa=[]
    #for i in range(0,Nvertex):
    #    cosa.append(cos_angle_from_normal_vectorAB(ring[i,0,:],ring[i,1,:],w))
    #cosa = np.array(cosa)
    cosa=cos_angle_from_normal_vectorAB(ring[:,0,:],ring[:,1,:],w)
    mask=(cosa>=0.0)*(cosa<=1.0)
    return np.prod(mask,axis=0)

def inout_single_square_covex(targets,center,PA,width):
    """checking if targets are in or out single square convex
    
    Args:
        center: theta, phi of the center in radian
        PA: position angle in radian
        width: square width

    Returns:
        in = 1 or out = 0 mask
    """
    convex=square_convex(center,PA,width)
    ans=convex_on_sphere(convex,targets)
    ans=np.array(ans,dtype=np.bool)
    return ans


def inout_four_sqaure_convexes(targets, center,PA,width,each_width):
    """checking if targets are in or out four square convexes
    
    Args:
        center: theta, phi of the center in radian
        PA: position angle in radian
        width: the separation of squares
        each_width: square width

    Returns:
        in = 1 or out = 0 mask

    """    
    convex=square_convex(center,PA,width)
    convex=np.array(convex)
    convexes=[]
    Ntarget=np.shape(targets)[1]
    answers=np.zeros(Ntarget,dtype=np.bool)
    for i in range(0,4):
        each_convex=square_convex(convex[:,i],PA,each_width)
        convexes.append(each_convex)
        ans=convex_on_sphere(each_convex,targets)        
        ans=np.array(ans,dtype=np.bool)
        answers = answers + ans 
    return answers

def inout_detector(targets, center,PA, width_mm=22.4, each_width_mm=19.52,  EFL_mm=4370.0):
    """checking if targets are in or out four square convexes
    
    Args:
        center: theta, phi of the center in radian
        PA: position angle in radian
        width_mm: the separation of detector chips
        each_width_mm: the chip width in the unit of mm
        EFL_mm: effective focal length in the unit of mm
    Returns:
        in = 1 or out = 0 mask

    """
    return inout_four_sqaure_convexes(targets, np.array([np.pi/2.0,0.0]),0.0,width_mm/EFL_mm, each_width_mm/EFL_mm)
 

if __name__ == "__main__":
    
    def test_inout_detector():
        np.random.seed(1)
        Ntarget=100000
        targets=np.array([np.random.normal(loc=np.pi/2.0,scale=np.pi/100.0,size=Ntarget),np.random.normal(loc=0.0,scale=np.pi/100.0,size=Ntarget)])
        each_width_mm=19.52
        width_mm=22.4
        EFL_mm=4370.0
        center=np.array([np.pi/2.0,0.0])
        PA=0.0
        ans=inout_detector(targets, center,PA, width_mm=width_mm, each_width_mm=each_width_mm, EFL_mm=EFL_mm)
        assert np.sum(ans)==1296
        return targets,ans

    
    targets,ans=test_inout_detector()
    line="# of stars in the detector="+str(np.sum(ans))
    print(line)
    
    import matplotlib.pyplot as plt
    from healpy.visufunc import projscatter
    import healpy as hp
    Nside=16
    emparr=np.zeros(hp.nside2npix(Nside))        
    hp.orthview(emparr,cmap="bwr")
    plt.title(line)
    projscatter(targets,alpha=0.4,marker="+")
    projscatter(targets[:,ans],alpha=0.4,marker="+")
    plt.show()

import numpy as np
from telescope_baseline.mapping.pixelfunc import ang2vec, vec2ang


def lb2ang(l,b):
    """convert l and b to ang (theta in radian, phi in radian)
    Args:
       l: galactic coordinate l
       b: galactic coordinate b
    Returns:
       ang (theta in radian, phi in radian)

    """
    phi=l/180.0*np.pi
    theta=np.pi/2.0-b/180.0*np.pi
    return np.array([theta,phi])

def ang2lb(ang):
    """convert ang (theta in radian, phi in radian) to l and b 
    Args:
       ang (theta in radian, phi in radian)
    Returns:
       l: galactic coordinate l
       b: galactic coordinate b

    """
    theta, phi=ang
    l=phi*180.0/np.pi
    b=90.0 - theta*180.0/np.pi
    return l, b
    
def basic_convex(center,PA,width,anglist,scale):
    """compute a single convex
    Args: 
        center: theta, phi of the center
        PA: position angle of the detector (north up)
        width: detector width in radian
        anglist: angular position list of the convex
        scale: scale of convex
    Returns:
        detecter convex (ang)
    
    """
    
    thetac,phic=center
    ez=np.array([0.0,0.0,1.0])
    half_diagonal_angle=width*scale
    e0=Roty(half_diagonal_angle)@ez
    convex0=[]
    for ang in anglist:
        convex0.append(Rotz(ang)@e0)
    convex0=np.array(convex0)
    C=np.einsum('ij,kj->ki',Rotz(PA),convex0)
    C=np.einsum('ij,kj->ki',Roty(thetac),C)
    C=np.einsum('ij,kj->ki',Rotz(phic),C)
    Cang = vec2ang(C)
    return np.array(Cang)

def square_convex(center,PA,width):
    """compute a single sqaure convex
    Args: 
        center: theta, phi of the center
        PA: position angle of the detector (north up)
        width: detector width in radian
    Returns:
        detecter convex (ang)
    
    """
    anglist=[-3.0*np.pi/4.0,-np.pi/4.0,np.pi/4.0,3.0*np.pi/4.0]
    scale=1.0/np.sqrt(2.0)
    return basic_convex(center,PA,width,anglist,scale)

def ang_detector_unit(direction,scale,center,PA,width):
    """compute a relative ang position in the unit of the detectir size from the original position center/PA/width
    Args: 
        direction: TBLR =top,bottom,left,right
        scale: scale in the detector one side unit
        center: theta, phi of the center
        PA: position angle of the detector (north up)
        width: detector width in radian
    Returns:
        ang (theta, phi)
    
    """

    anglist=[-np.pi/2.0,0.0,np.pi/2.0,np.pi]
    dic={"R":0,"B":1,"L":2,"T":3}
    bc=basic_convex(center,PA,width,anglist,2*scale)
    i=dic[direction]
    return bc[:,i]
    
def lb_detector_unit(direction,scale,l_center,b_center, PA_deg, width_mm=22.4, EFL_mm=4370.0):
    """compute a relative l,b position in the unit of the detectir size from the original position center/PA/width
    Args: 
        direction: TBLR =top,bottom,left,right
        scale: scale in the detector one side unit
        l_center: center of galactic coordinate, l (deg)
        b_center: center of galactic coordinate, b (deg)
        PA_deg: position angle in deg
        width_mm: the separation of detector chips
        EFL_mm: effective focal length in the unit of mm
    Returns:
        l,b
    
    """
    PA=PA_deg/180.0*np.pi

    return ang2lb(ang_detector_unit(direction,scale,lb2ang(l_center,b_center),PA,width_mm/EFL_mm))
    
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
    ans=np.array(ans,dtype=np.bool_)
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
    answers=np.zeros(Ntarget,dtype=np.bool_)
    for i in range(0,4):
        each_convex=square_convex(convex[:,i],PA,each_width)
        convexes.append(each_convex)
        ans=convex_on_sphere(each_convex,targets)        
        ans=np.array(ans,dtype=np.bool_)
        answers = answers + ans 
    return answers

def inout_detector(targets,l_center,b_center,PA_deg, width_mm=22.4, each_width_mm=19.52,  EFL_mm=4370.0):
    """checking if targets are in or out four square convexes
    
    Args:
        l_center: center of galactic coordinate, l (deg)
        b_center: center of galactic coordinate, b (deg)
        PA_deg: position angle in deg
        width_mm: the separation of detector chips
        each_width_mm: the chip width in the unit of mm
        EFL_mm: effective focal length in the unit of mm
    Returns:
        in = 1 or out = 0 mask

    """
    center=lb2ang(l_center,b_center)
    PA=PA_deg/180.0*np.pi
    return inout_four_sqaure_convexes(targets, center, PA, width_mm/EFL_mm, each_width_mm/EFL_mm)

def inout_Lshape(targets,l_center,b_center,PA_deg, width_mm=22.4, each_width_mm=19.52,  EFL_mm=4370.0, left=0.0, top=0.0):
    """checking if targets are in or out (extended) L shape formation
    
    Args:
        l_center: center of galactic coordinate, l (deg)
        b_center: center of galactic coordinate, b (deg)
        PA_deg: position angle in deg
        width_mm: the separation of detector chips
        each_width_mm: the chip width in the unit of mm
        EFL_mm: effective focal length in the unit of mm
        left: shift to left of the upper two fields 
        top: shift to top of the upper two fields 

    Returns:
        in = 1 or out = 0 mask

    """
    center=lb2ang(l_center,b_center)
    PA=PA_deg/180.0*np.pi
    width=width_mm/EFL_mm
    each_width=each_width_mm/EFL_mm
    
    ans=[]    
    ans.append(inout_four_sqaure_convexes(targets, center, PA, width, each_width))
    ans.append(inout_four_sqaure_convexes(targets, ang_detector_unit("R",0.5,center,PA,width), PA, width, each_width))
    pos=ang_detector_unit("L",left,center,PA,width)
    ans.append(inout_four_sqaure_convexes(targets, ang_detector_unit("T",1.0+top,pos,PA,width), PA, width, each_width))
    ans.append(inout_four_sqaure_convexes(targets, ang_detector_unit("T",1.5+top,pos,PA,width), PA, width, each_width))
        
    return ans

if __name__ == "__main__":
    import pkg_resources           
    from telescope_baseline.mapping.read_catalog import read_jasmine_targets
    from telescope_baseline.mapping.plot_mapping import plot_targets
    
    each_width_mm=19.52
    width_mm=22.4
    EFL_mm=4370.0
    l_center=-1.2
    b_center=0.0
    PA_deg=0.0

    hdf=pkg_resources.resource_filename('telescope_baseline', 'data/cat.hdf')
    targets,l,b=read_jasmine_targets(hdf)
    #    ans=inout_detector(targets,l_center,b_center,PA_deg, width_mm=width_mm, each_width_mm=each_width_mm, EFL_mm=EFL_mm)

    #right L
    ans=inout_Lshape(targets,l_center,b_center,PA_deg, width_mm=width_mm, each_width_mm=each_width_mm, EFL_mm=EFL_mm, left=1.0,top=-0.75)

    #mid L
    l_center,b_center=lb_detector_unit("L",1.5,l_center,b_center, PA_deg, width_mm=width_mm, EFL_mm=EFL_mm)
    l_center,b_center=lb_detector_unit("B",0.75,l_center,b_center, PA_deg, width_mm=width_mm, EFL_mm=EFL_mm)    
    ans2=inout_Lshape(targets,l_center,b_center,PA_deg, width_mm=width_mm, each_width_mm=each_width_mm, EFL_mm=EFL_mm, left=0.5)
    ans=np.vstack([ans,ans2])
    
    #left L
    l_center,b_center=lb_detector_unit("L",1.5,l_center,b_center, PA_deg, width_mm=width_mm, EFL_mm=EFL_mm)
    ans2=inout_Lshape(targets,l_center,b_center,PA_deg, width_mm=width_mm, each_width_mm=each_width_mm, EFL_mm=EFL_mm)
    ans=np.vstack([ans,ans2])

    for i,ans_each in enumerate(ans):
            print("N in "+str(i)+"-th map=",np.sum(ans_each))
    print("N in total=",np.sum(np.max(ans,axis=0)))
    plot_targets(l,b,ans)
    

import numpy as np
from healpy.pixelfunc import ang2vec, vec2ang

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



    
#if __name__ == "__main__":
#    test_convex_on_sphere_map()

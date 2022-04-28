from telescope_baseline.mapping.aperture import cos_angle_from_normal_vectorAB, vec2ring, convex_on_sphere
from healpy.pixelfunc import vec2ang
import numpy as np
import pytest

def test_cos_angle_from_normal_vectorAB():
    a=np.array([1,0,0])
    b=np.array([0,1,0])
    v=cos_angle_from_normal_vectorAB(a,b,[ np.cross(a,b)])
    assert v[0]==1

def test_vec2ring():
    a=np.array([[1,1,1],[2,2,2],[3,3,3],[4,4,4],[5,5,5],[6,6,6]])
    assert np.sum(vec2ring(a)[0,0,:]) == 6*3
    assert np.sum(vec2ring(a)[0,1,:]) == 1*3
    assert np.sum(vec2ring(a)[1,0,:]) == 1*3
    assert np.sum(vec2ring(a)[1,1,:]) == 2*3

def test_convex_on_sphere():
    ex=np.array([1,0,0])
    ey=np.array([0,1,0])
    ea=np.array([0,1.0/np.sqrt(2.0),1.0/np.sqrt(2.0)])
    eb=np.array([1.0/np.sqrt(2.0),0,1])
    v=np.array([ex,ey,ea,eb])
    angv=np.array(vec2ang(v)) # (Nvertex, theta-phi)
    
    w=np.array([0,0,1])
    angw=np.array(vec2ang(w)).T[0] # (Nvertex, theta-phi)
    assert convex_on_sphere(angv,angw)==0

    w=np.array([1/np.sqrt(2.0),1/np.sqrt(2.0),1/np.sqrt(4.0)])
    angw=np.array(vec2ang(w)).T[0] 
    assert convex_on_sphere(angv,angw)==1

def test_convex_on_sphere_map():
    ex=np.array([1,0,0])
    ey=np.array([0,1,0])
    ea=np.array([0,1.0/np.sqrt(2.0),1.0/np.sqrt(2.0)])
    eb=np.array([1.0/np.sqrt(2.0),0,1])
    v=np.array([ex,ey,ea,eb])
    angv=np.array(vec2ang(v)) # (theta-phi, Nvertex)
    
    w=np.array([0,0,1])
    q=np.array([1/np.sqrt(2.0),1/np.sqrt(2.0),1/np.sqrt(4.0)])
    v=np.array([w,q,w,q])
    angw=np.array(vec2ang(v))
    ans=convex_on_sphere(angv,angw)
    assert (np.sum((ans - [0,1,0,1])**2)) == 0

def test_single_detector_convex_in():
    from telescope_baseline.mapping.randomtarget import rantarget
    np.random.seed(1)
    targets=rantarget(N=100000)
    convex=single_detector_convex(np.array([np.pi/2.0,np.pi/2.0]),np.pi/3.0,np.pi/4.0)
    ans=convex_on_sphere(convex,targets)
    ans=np.array(ans,dtype=np.bool)
    assert np.sum(ans)==3171
    return targets,ans

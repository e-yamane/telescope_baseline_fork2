"""mapping set

 * Lshape -> large_frame  

"""
import numpy as np
from telescope_baseline.mapping.aperture import lb_detector_unit, inout_four_sqaure_convexes, ang_detector_unit, lb2ang, ang2lb

def inout_Lshape(targets,l_center,b_center,PA_deg, width_mm=22.4, each_width_mm=19.52,  EFL_mm=4370.0, left=0.0, top=0.0):
    """checking if targets are in or out (extended) L shape formation
    
    Args:
        targats: targets coordinate list (in radian)
        l_center: center of galactic coordinate, l (deg)
        b_center: center of galactic coordinate, b (deg)
        PA_deg: position angle in deg
        width_mm: the separation of detector chips
        each_width_mm: the chip width in the unit of mm
        EFL_mm: effective focal length in the unit of mm
        left: shift to left of the upper two fields 
        top: shift to top of the upper two fields 

    Returns:
        answer: inout mask sequence (in = 1 or out = 0 mask)
        convexes: convex positions 

    """
    center=lb2ang(l_center,b_center)
    PA=PA_deg/180.0*np.pi
    width=width_mm/EFL_mm
    each_width=each_width_mm/EFL_mm
    
    ans=[]
    convexpos=[]
    a,p=inout_four_sqaure_convexes(targets, center, PA, width, each_width)
    ans.append(a)
    convexpos=p
    a,p=inout_four_sqaure_convexes(targets, ang_detector_unit("R",0.5,center,PA,width), PA, width, each_width)
    ans.append(a)    
    convexpos=np.vstack([convexpos,p])
    pos=ang_detector_unit("L",left,center,PA,width)
    a,p=inout_four_sqaure_convexes(targets, ang_detector_unit("T",1.0+top,pos,PA,width), PA, width, each_width)
    ans.append(a)
    convexpos=np.vstack([convexpos,p])
    a,p=inout_four_sqaure_convexes(targets, ang_detector_unit("T",1.5+top,pos,PA,width), PA, width, each_width)
    ans.append(a)        
    convexpos=np.vstack([convexpos,p])

    return ans, convexpos

def inout_large_frame(targets,l_center,b_center,PA_deg, width_mm=22.4, each_width_mm=19.52,  EFL_mm=4370.0, left=0.0, top=0.0):
    """in or out large frame

    Args:
        targats: targets coordinate list (in radian)
        l_center: center of galactic coordinate, l (deg)
        b_center: center of galactic coordinate, b (deg)
        PA_deg: position angle in deg
        width_mm: the separation of detector chips
        each_width_mm: the chip width in the unit of mm
        EFL_mm: effective focal length in the unit of mm
        left: shift to left of the upper two fields 
        top: shift to top of the upper two fields 

    Returns:
        inout mask sequence of inout mask of four detectors (in = 1 or out = 0 mask)
        convex position 
    """
    #shift
    l_center,b_center=lb_detector_unit("L",left,l_center,b_center, PA_deg, width_mm=width_mm, EFL_mm=EFL_mm)
    l_center,b_center=lb_detector_unit("T",top,l_center,b_center, PA_deg, width_mm=width_mm, EFL_mm=EFL_mm)
    
    #right L
    ans,pos=inout_Lshape(targets,l_center,b_center,PA_deg, width_mm=width_mm, each_width_mm=each_width_mm, EFL_mm=EFL_mm, left=1.0,top=-0.75)
    
    #mid L
    l_center,b_center=lb_detector_unit("L",1.5,l_center,b_center, PA_deg, width_mm=width_mm, EFL_mm=EFL_mm)
    l_center,b_center=lb_detector_unit("B",0.75,l_center,b_center, PA_deg, width_mm=width_mm, EFL_mm=EFL_mm)    
    ans2,pos2=inout_Lshape(targets,l_center,b_center,PA_deg, width_mm=width_mm, each_width_mm=each_width_mm, EFL_mm=EFL_mm, left=0.5)
    ans=np.vstack([ans,ans2])
    pos=np.vstack([pos,pos2])
    #left L
    l_center,b_center=lb_detector_unit("L",1.5,l_center,b_center, PA_deg, width_mm=width_mm, EFL_mm=EFL_mm)
    ans2,pos2=inout_Lshape(targets,l_center,b_center,PA_deg, width_mm=width_mm, each_width_mm=each_width_mm, EFL_mm=EFL_mm)
    ans=np.vstack([ans,ans2])
    pos=np.vstack([pos,pos2])

    return ans,pos

def obsn_MPSv1(targets,l_center,b_center,PA_deg, width_mm=22.4, each_width_mm=19.52,  EFL_mm=4370.0, left=0.0, top=0.0):
    """number of observed for MPSv1

    Args:
        targats: targets coordinate list (in radian)
        l_center: center of galactic coordinate, l (deg)
        b_center: center of galactic coordinate, b (deg)
        PA_deg: position angle in deg
        width_mm: the separation of detector chips
        each_width_mm: the chip width in the unit of mm
        EFL_mm: effective focal length in the unit of mm
        left: shift to left of the upper two fields 
        top: shift to top of the upper two fields 

    Returns:
        number of observation
        position
    """
    ans1,pos1=inout_large_frame(targets,l_center,b_center,PA_deg, width_mm=width_mm, each_width_mm=each_width_mm, EFL_mm=EFL_mm, left=0.125+left,top=-0.125/2.0+top)
    ans2,pos2=inout_large_frame(targets,l_center,b_center,PA_deg, width_mm=width_mm, each_width_mm=each_width_mm, EFL_mm=EFL_mm, left=-0.125+left,top=-0.125/2.0+top)
    ans3,pos3=inout_large_frame(targets,l_center,b_center,PA_deg, width_mm=width_mm, each_width_mm=each_width_mm, EFL_mm=EFL_mm, left=0.125+left,top=0.125/2.0+top)
    ans4,pos4=inout_large_frame(targets,l_center,b_center,PA_deg, width_mm=width_mm, each_width_mm=each_width_mm, EFL_mm=EFL_mm, left=-0.125+left,top=0.125/2.0+top)

    ans=np.vstack([ans1,ans2,ans3,ans4])
    pos=np.vstack([pos1,pos2,pos3,pos4])

    nans=np.sum(ans,axis=0)
    return nans, pos

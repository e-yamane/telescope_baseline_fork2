"""mapping set

 * Lshape -> large_frame  

"""
import numpy as np
from telescope_baseline.mapping.aperture import lb_detector_unit, inout_four_sqaure_convexes, ang_detector_unit, lb2ang

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
        inout mask sequence of four detectors (in = 1 or out = 0 mask)

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

    """
    #shift
    l_center,b_center=lb_detector_unit("L",left,l_center,b_center, PA_deg, width_mm=width_mm, EFL_mm=EFL_mm)
    l_center,b_center=lb_detector_unit("T",top,l_center,b_center, PA_deg, width_mm=width_mm, EFL_mm=EFL_mm)
    
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

    return ans

def obsn_MPSv1(targets,l_center,b_center,PA_deg, width_mm=22.4, each_width_mm=19.52,  EFL_mm=4370.0):
    """number of observed for MPSv1

    Args:
        targats: targets coordinate list (in radian)
        l_center: center of galactic coordinate, l (deg)
        b_center: center of galactic coordinate, b (deg)
        PA_deg: position angle in deg
        width_mm: the separation of detector chips
        each_width_mm: the chip width in the unit of mm
        EFL_mm: effective focal length in the unit of mm

    Returns:
        number of observation
    """
    ans1=inout_large_frame(targets,l_center,b_center,PA_deg, width_mm=width_mm, each_width_mm=each_width_mm, EFL_mm=EFL_mm, left=0.125,top=-0.125/2.0)
    ans2=inout_large_frame(targets,l_center,b_center,PA_deg, width_mm=width_mm, each_width_mm=each_width_mm, EFL_mm=EFL_mm, left=-0.125,top=-0.125/2.0)
    ans3=inout_large_frame(targets,l_center,b_center,PA_deg, width_mm=width_mm, each_width_mm=each_width_mm, EFL_mm=EFL_mm, left=0.125,top=0.125/2.0)
    ans4=inout_large_frame(targets,l_center,b_center,PA_deg, width_mm=width_mm, each_width_mm=each_width_mm, EFL_mm=EFL_mm, left=-0.125,top=0.125/2.0)

    ans=np.vstack([ans1,ans2,ans3,ans4])
    nans=np.sum(ans,axis=0)
    return nans


    

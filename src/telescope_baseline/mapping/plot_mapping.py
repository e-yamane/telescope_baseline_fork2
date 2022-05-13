import matplotlib.pyplot as plt
import numpy as np
from telescope_baseline.mapping.aperture import ang2lb
from matplotlib import patches

def add_region(pos,ax,autoshift=True,alpha=0.3):
    """plot a patch of detector region on sky

    Args:
       pos: position list in l,b
       ax: ax for plotting
       autoshift: if True, convert l to -180, 180 deg
       alpha: alpha

    """
    for i in range(len(pos)):
        xy=np.array(ang2lb(pos[i]))
        if autoshift:
            xy[0]=np.mod(xy[0]+180.0,360.0)-180.0
        xy=xy.T
        patch = patches.Polygon(xy=xy, closed=True,fill=False,ls="--",lw=0.5,color="green",alpha=alpha)
        ax.add_patch(patch)
        

def plot_targets(l,b,ans,pos=None,outfile="map.png"):
    """plot targets in general

    Args:
       l: l
       b: b
       ans: targets position
       pos: detector position
       outfile: output file name

    """
    
    fig=plt.figure()
    ax=fig.add_subplot(111,aspect=1.0)
    ax.plot(l,b,".",alpha=0.03,color="black")
    if len(np.shape(ans))==1:
        ax.plot(l[ans],b[ans],".",alpha=0.1)
        ax.set_title("N in Detector ="+str(len(b[ans]))+" Hw<12.5")
    else:
        for ans_each in ans:
            ax.plot(l[ans_each],b[ans_each],".",alpha=0.05,color="C3")
    if pos is not None:
        add_region(pos,ax)
    ax.set_xlabel("l (deg)")
    ax.set_ylabel("b (deg)")
    plt.gca().invert_xaxis()
    plt.savefig(outfile)        
    plt.show()

def plot_n_targets(l,b,nans,pos=None,outfile="nmap.png",cmap="CMRmap"):
    """plot targets in general

    Args:
       l: l
       b: b
       ans: targets position
       pos: detector position
       outfile: output file name

    """

    fig=plt.figure()
    ax=fig.add_subplot(111,aspect=1.0)
    cb=ax.scatter(l,b,s=1,c=nans,alpha=0.9,cmap=cmap)
    if pos is not None:
        add_region(pos,ax)
    ax.set_facecolor('gray')
    labels(cb,outfile,ax)

def plot_ae_targets(l,b,nans,pos=None,outfile="aemap.png",cmap="CMRmap",vmax=50.0):
    """plot astrometric error
    """
    fig=plt.figure()
    ax=fig.add_subplot(111,aspect=1.0)
    cb=ax.scatter(l,b,s=1,c=nans,alpha=0.9, cmap=cmap, vmax=vmax)
    if pos is not None:
        add_region(pos,ax)
    ax.set_facecolor('black')
    labels(cb,outfile,ax)

def labels(cb,outfile,ax):
    plt.colorbar(cb,shrink=0.5)
    ax.set_xlabel("l (deg)")
    ax.set_ylabel("b (deg)")
    plt.gca().invert_xaxis()
    plt.savefig(outfile)        
    plt.show()

    
def hist_n_targets(nans,scale=1.0,outfile="nhist.png"):
    nans=nans[nans>0]
    orign=int(np.max(nans))
    nans=nans*scale
    fig=plt.figure()
    ax=fig.add_subplot(111)
    cb=ax.hist(nans, bins=orign, alpha=0.5, ec='navy', range=(0.5*scale, np.max(nans)+0.5*scale))
    ax.set_xlabel("N")
    ax.set_ylabel("number of the targets")
    plt.savefig(outfile)        
    plt.show()

def hist_ae_targets(final_ac,outfile="fac.png"):
    fig=plt.figure()    
    ax=fig.add_subplot(111)
    cb=ax.hist(final_ac[final_ac<100.0], alpha=0.5, bins=25, ec='navy')
    ax.set_ylabel("number of targets")
    ax.set_xlabel("final accuracy [umas]")
    plt.savefig(outfile)        
    plt.show()

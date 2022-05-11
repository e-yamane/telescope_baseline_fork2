import matplotlib.pyplot as plt
import numpy as np

def plot_targets(l,b,ans,outfile="map.png"):
    fig=plt.figure()
    ax=fig.add_subplot(111,aspect=1.0)
    ax.plot(l,b,".",alpha=0.03,color="black")
    if len(np.shape(ans))==1:
        ax.plot(l[ans],b[ans],".",alpha=0.1)
        ax.set_title("N in Detector ="+str(len(b[ans]))+" Hw<12.5")
    else:
        for ans_each in ans:
            ax.plot(l[ans_each],b[ans_each],".",alpha=0.05,color="C3")
    ax.set_xlabel("l (deg)")
    ax.set_ylabel("b (deg)")
    plt.gca().invert_xaxis()
    plt.savefig(outfile)        
    plt.show()

def plot_n_targets(l,b,nans,outfile="nmap.png",cmap="CMRmap"):
    fig=plt.figure()
    ax=fig.add_subplot(111,aspect=1.0)
    cb=ax.scatter(l,b,s=1,c=nans,alpha=0.9,cmap=cmap)
    ax.set_facecolor('gray')
    labels(cb,outfile,ax)

def plot_ae_targets(l,b,nans,outfile="aemap.png",cmap="CMRmap",vmax=50.0):
    """plot astrometric error
    """
    fig=plt.figure()
    ax=fig.add_subplot(111,aspect=1.0)
    cb=ax.scatter(l,b,s=1,c=nans,alpha=0.9, cmap=cmap, vmax=vmax)
    ax.set_facecolor('black')
    labels(cb,outfile,ax)

def labels(cb,outfile,ax):
    plt.colorbar(cb,shrink=0.5)
    ax.set_xlabel("l (deg)")
    ax.set_ylabel("b (deg)")
    plt.gca().invert_xaxis()
    plt.savefig(outfile)        
    plt.show()

    
def hist_n_targets(nans,scale,outfile="nhist.png"):
    nans=nans[nans>0]
    orign=np.max(nans)
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

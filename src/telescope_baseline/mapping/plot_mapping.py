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

def plot_n_targets(l,b,nans,outfile="nmap.png"):
    fig=plt.figure()
    ax=fig.add_subplot(111,aspect=1.0)
    cb=ax.scatter(l,b,c=nans,alpha=0.1,cmap="CMRmap")
    plt.colorbar(cb)
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

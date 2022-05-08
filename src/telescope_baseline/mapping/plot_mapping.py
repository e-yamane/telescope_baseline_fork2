import matplotlib.pyplot as plt

def plot_targets(l,b,ans,outfile="map.png"):
    fig=plt.figure()
    ax=fig.add_subplot(111,aspect=1.0)
    plt.plot(l,b,".",alpha=0.03,color="gray")
    plt.plot(l[ans],b[ans],".",alpha=0.1)
    plt.title("N in Detector ="+str(len(b[ans]))+" Hw<12.5")
    plt.xlabel("l (deg)")
    plt.ylabel("b (deg)")
    plt.gca().invert_xaxis()
    plt.savefig(outfile)        
    plt.show()

import matplotlib.pyplot as plt
import numpy as np

def plot_targets(l,b,ans,outfile="map.png"):
    fig=plt.figure()
    ax=fig.add_subplot(111,aspect=1.0)
    plt.plot(l,b,".",alpha=0.03,color="gray")
    if len(np.shape(ans))==1:
        plot_targets_each(l,b,ans)
        plt.title("N in Detector ="+str(len(b[ans]))+" Hw<12.5")
    else:
        for ans_each in ans:
            plt.plot(l[ans_each],b[ans_each],".",alpha=0.1)
            print(np.sum(ans_each))
    plt.xlabel("l (deg)")
    plt.ylabel("b (deg)")
    plt.gca().invert_xaxis()
    plt.savefig(outfile)        
    plt.show()


if __name__ == "__main__":
    import pkg_resources           
    from telescope_baseline.mapping.read_catalog import read_jasmine_targets
    from telescope_baseline.mapping.plot_mapping import plot_targets, plot_n_targets, hist_n_targets
    from telescope_baseline.mapping.mapset import obsn_MPSv1
    import matplotlib.pyplot as plt
    import numpy as np
    each_width_mm=19.52
    width_mm=22.4
    EFL_mm=4370.0
    l_center=-1.2
    b_center=0.0
    PA_deg=0.0

    hdf=pkg_resources.resource_filename('telescope_baseline', 'data/cat_hw14.5.hdf')
    targets,l,b,hw=read_jasmine_targets(hdf)
    nans=obsn_MPSv1(targets,l_center,b_center,PA_deg, width_mm=width_mm, each_width_mm=each_width_mm, EFL_mm=EFL_mm)
            
    scale=50.0*6000/12.0
    Nstar=10**(hw/-2.5)/10**(12.5/-2.5)
    
    print("Nobs=",len(nans[nans>0]))
#    plot_n_targets(l,b,nans*scale) #number
    ac=6000 # micro arcsec per frame
    final_ac=ac/np.sqrt(nans*scale)/np.sqrt(Nstar)


    def plot_s_targets(l,b,nans,outfile="nmap.png",cmap="CMRmap"):
        fig=plt.figure()
        ax=fig.add_subplot(111,aspect=1.0)
        cb=ax.scatter(l,b,c=nans,alpha=0.1,cmap=cmap, vmax=50.0)
        ax.set_facecolor('black')
        plt.colorbar(cb,shrink=0.5)
        ax.set_xlabel("l (deg)")
        ax.set_ylabel("b (deg)")
        plt.gca().invert_xaxis()
        plt.savefig(outfile)        
        plt.show()

    
    plot_s_targets(l,b,final_ac,cmap="CMRmap_r")
    
    fig=plt.figure()    
    ax=fig.add_subplot(111)
    cb=ax.hist(final_ac[final_ac<100.0], alpha=0.5, bins=25, ec='navy')
    ax.set_ylabel("number of targets")
    ax.set_xlabel("final accuracy [umas]")
    plt.savefig("fac.png")        
    plt.show()

#    hist_n_targets(nans,final_ac)

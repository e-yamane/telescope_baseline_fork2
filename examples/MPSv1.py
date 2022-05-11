if __name__ == "__main__":
    import pkg_resources           
    from telescope_baseline.mapping.read_catalog import read_jasmine_targets
    from telescope_baseline.mapping.plot_mapping import plot_targets, plot_n_targets, hist_n_targets, plot_ae_targets, hist_ae_targets
    from telescope_baseline.mapping.mapset import obsn_MPSv1
    import matplotlib.pyplot as plt
    import numpy as np
    import tqdm
    each_width_mm=19.52
    width_mm=22.4
    EFL_mm=4370.0
    l_center=-1.2
    b_center=0.0
    PA_deg=0.0

    hdf=pkg_resources.resource_filename('telescope_baseline', 'data/cat_hw14.5.hdf')
    targets,l,b,hw=read_jasmine_targets(hdf)
    Nstar=10**(hw/-2.5)/10**(12.5/-2.5)
    
    Ng=11
    dizLmax=1.5
    grid=np.linspace(-dizLmax,dizLmax,Ng)
    dummy_array=np.ones((Ng,Ng))
    gx=(grid[:,np.newaxis]*dummy_array).flatten()
    gy=(grid[np.newaxis,:]*dummy_array).flatten()
    
    nans=np.zeros_like(hw)
    for i in tqdm.tqdm(range(0,Ng*Ng)):
        nans_each=obsn_MPSv1(targets,l_center,b_center,PA_deg, width_mm=width_mm, each_width_mm=each_width_mm, EFL_mm=EFL_mm,left=gx[i],top=gy[i])
        nans=nans+nans_each
 
    scale=50.0*6000/12.0/(Ng*Ng)
    
    print("Nobs=",len(nans[nans>0]))
#    plot_n_targets(l,b,nans*scale) #number
    ac=6000 # micro arcsec per frame
    print(ac,scale,Nstar)
    final_ac=ac/np.sqrt(nans*scale)/np.sqrt(Nstar)    
    plot_ae_targets(l,b,final_ac,cmap="CMRmap_r")    
    hist_ae_targets(final_ac)

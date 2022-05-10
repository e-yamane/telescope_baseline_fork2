if __name__ == "__main__":
    import pkg_resources           
    from telescope_baseline.mapping.read_catalog import read_jasmine_targets
    from telescope_baseline.mapping.plot_mapping import plot_targets, plot_n_targets, hist_n_targets
    from telescope_baseline.mapping.mapset import obsn_MPSv1
    each_width_mm=19.52
    width_mm=22.4
    EFL_mm=4370.0
    l_center=-1.2
    b_center=0.0
    PA_deg=0.0

    hdf=pkg_resources.resource_filename('telescope_baseline', 'data/cat.hdf')
    targets,l,b=read_jasmine_targets(hdf)
    nans=obsn_MPSv1(targets,l_center,b_center,PA_deg, width_mm=width_mm, each_width_mm=each_width_mm, EFL_mm=EFL_mm)
            
    scale=50.0*6000/12.0
    hist_n_targets(nans,scale)
    plot_n_targets(l,b,nans*scale)

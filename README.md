## plot_stat_map
> script to plot fMRI statistical maps: saves high resolution PNG images for every x y z slice + a thresholded colorbar  

[nilearn function: plot_stat_map](https://nilearn.github.io/modules/generated/nilearn.plotting.plot_stat_map.html#nilearn.plotting.plot_stat_map)  

<img src='example_fig.png' width='500'>

**to run**:
- `$ python plot_stat_map.py <vmin> <vmax> [<options>]`
- `vmin` `vmax` lower and upper bound for colormap
-  `-m, --mask` activation outside brain (mni152) is masked
-  `-v, --verbose` print progress information to screen
- select stats and background NIFTI files, then name output directory

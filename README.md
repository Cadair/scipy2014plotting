scipy2014plotting
=================

My entry for the "SciPy John Hunter Excellence in Plotting Contest"

See: [this](https://conference.scipy.org/scipy2014/participate/plotting_contest/) for more information on the competition.

Getting the Data
----------------
This plot requires a few hundred megs of data files, which are hosted online and can be downloaded using the `get_data.py` script.

The download script requires both the `requests` package and `progressbar`.

The files required in the data directory are:

* [`'http://files.figshare.com/1425846/gband_image_00200.fits'`]('http://files.figshare.com/1425846/gband_image_00200.fits')
* [`'http://files.figshare.com/1425877/Fieldline_surface_Slog_p30_0_A20r2_r60__B005_00400.vtp'`]('http://files.figshare.com/1425877/Fieldline_surface_Slog_p30_0_A20r2_r60__B005_00400.vtp')
* [`'http://cadair.com/Slog_p30-0_A20r2_B005_00400.gdf.bz2'`]('http://cadair.com/Slog_p30-0_A20r2_B005_00400.gdf.bz2')

Making the Plot
---------------
The script that contains the plotting routine is in `create_plot.py` there are some helper routines in `mayavi_plotting_functions.py` and some custom yt fields in `yt_fields.py`. 
These helper routines have been extracted from the [pysac library](https://bitbucket.org/swatsheffield/pysac).

Requirements for the `create_plot.py` script:

* mayavi / tvtk / vtk
* h5py
* yt 2.6.x
* numpy
* astropy


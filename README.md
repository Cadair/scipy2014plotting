scipy2014plotting
=================

My entry for the "SciPy John Hunter Excellence in Plotting Contest"

[See:](https://conference.scipy.org/scipy2014/participate/plotting_contest/) for more information on the competition.

Getting the Data
----------------
This plot requires a few hundred megs of data files, which are hosted online and can be downloaded using the `get_data.py` script.

The download script requires both the `requests` package and `progressbar`.

Making the Plot
---------------
The script that contains the plotting routine is in `create_plot.py` there are some helper routines in `mayavi_plotting_functions.py`. 
These helper routines have been extracted from the [pysac library](https://bitbucket.org/swatsheffield/pysac).

Requirements for the `create_plot.py` script:

* mayavi /tvtk / vtk
* h5py
* yt
* numpy
* astropy


# -*- coding: utf-8 -*-
"""
Created on Tue Mar  4 10:22:17 2014

@author: stuart
"""
import numpy as np
import yt.mods as ytm
from tvtk.api import tvtk
from mayavi import mlab
from tvtk.util.ctf import PiecewiseFunction
from tvtk.util.ctf import ColorTransferFunction

from astropy.io import fits

# pysac imports
# These files normally live in pysac
import yt_fields
import mayavi_plotting_functions as mpf

ds = ytm.load('./data/Slog_p30-0_A20r2_B005_00400.gdf')
cg = ds.h.grids[0]
cube_slice = np.s_[:,:,:-5]

r = tvtk.XMLPolyDataReader(file_name='./data/Fieldline_surface_Slog_p30-0_A20r2_r60__B005_00400.vtp')
r.update()
surf_poly = r.output

fig = mlab.figure()

# Create a bfield tvtk field, in mT
bfield = mlab.pipeline.vector_field(cg['mag_field_x'][cube_slice] * 1e3,
                                    cg['mag_field_y'][cube_slice] * 1e3, 
                                    cg['mag_field_z'][cube_slice] * 1e3,
                                    name="Magnetic Field",figure=fig)
# Create a scalar field of the magntiude of the vector field
bmag = mlab.pipeline.extract_vector_norm(bfield, name="Field line Normals")
bfield.origin = (410,735,0)

vfield = mlab.pipeline.vector_field(cg['velocity_x'][cube_slice] / 1e3,
                                    cg['velocity_y'][cube_slice] / 1e3, 
                                    cg['velocity_z'][cube_slice] / 1e3,
                                    name="Velocity Field",figure=fig)
vmag = mlab.pipeline.extract_vector_norm(vfield, name="Velocity Mag")
vfield.origin = (410,735,0)
#==============================================================================
# Get GBand
#==============================================================================
data = fits.getdata('data/gband_image_00200.fits')[40:960,40:960]
data = data.astype('f8') #FITS is big endian, VTK says no.

# Create a x and y array for the fits data in the simulation *pixel* coords
dx = (cg['x'][1,0,0] - cg['x'][0,0,0])/1e5 #dx in km
pixel_scale =  50 / dx #3.3 simulation pixels to a ROSA pixel, one rosa pixel is ~50km
xmax = data.shape[1] * pixel_scale
ymax = data.shape[0] * pixel_scale

# Expand the GBand data so it has a vertical extent
profile = np.exp(-np.linspace(0,1,75))

data2 = data[...,None]/ data.max() * profile[None, None, :]

#==============================================================================
# Plotting
#==============================================================================
text_color = (1,1,1)
x,y,z = np.mgrid[0:xmax:1j*data.shape[1],0:ymax:1j*data.shape[0],-20:35:75j]
gband = mlab.pipeline.scalar_field(x,y,z, data2, name="GBand Data", figure=fig)
gband.origin = (-1400,-450,0)

# Create a bfield tvtk field, in mT
bfield = mlab.pipeline.vector_field(cg['mag_field_x'][cube_slice] * 1e3,
                                    cg['mag_field_y'][cube_slice] * 1e3, 
                                    cg['mag_field_z'][cube_slice] * 1e3,
                                    name="Magnetic Field",figure=fig)
# Create a scalar field of the magntiude of the vector field
bmag = mlab.pipeline.extract_vector_norm(bfield, name="Field line Normals")

vfield = mlab.pipeline.vector_field(cg['velocity_x'][cube_slice] / 1e3,
                                    cg['velocity_y'][cube_slice] / 1e3, 
                                    cg['velocity_z'][cube_slice] / 1e3,
                                    name="Velocity Field",figure=fig)
vmag = mlab.pipeline.extract_vector_norm(vfield, name="Velocity Mag")

# Magnetic field lines
slines = mlab.pipeline.streamline(bmag, linetype='tube',
                                  integration_direction='both', seed_resolution=6)
slines.stream_tracer.maximum_propagation = 500 #Make sure the lines hit the edge of the domain
slines.tube_filter.radius = 0.3
slines.parent.scalar_lut_manager.lut_mode = 'GnBu'
slines.parent.scalar_lut_manager.lut.scale = 'log10'
slines.seed.widget.theta_resolution = 9
slines.seed.widget.radius = 40
slines.seed.visible = False #Hide the seed widget
# Tweak to make the lower limit not zero for log scaling
slines.parent.scalar_lut_manager.data_range = slines.parent.scalar_lut_manager.data_range + 1e-5
# Add colour bar
cbar = mpf.add_colourbar(slines, [0.81, 0.5] ,[0.11,0.31], '', label_fstring='%#3.1e',
                  number_labels=5, orientation=1,lut_manager='scalar')
cbar_label = mpf.add_cbar_label(cbar,'Magnetic Field Strength\n               [mT] ')
cbar_label.property.color = text_color
slines.parent.scalar_lut_manager.label_text_property.color = (1,1,1)
#cbar_label.y_position = 0.45
cbar_label.x_position = 0.93

# Plot Surface
new_tube, surf_bar, surf_bar_label = mpf.draw_surface(surf_poly,'RdBu',lim=0.4,
                                                      position=[0.81, 0.1],
                                                      position2=[0.11,0.31])
mpf.change_surface_scalars(new_tube, surf_bar_label, 'vphi', lim=1.5)
new_tube.parent.scalar_lut_manager.label_text_property.color = (1,1,1)
surf_bar_label.property.color = text_color
#surf_bar_label.y_position = 0.05
surf_bar_label.x_position = 0.93

# Add GBand volume render
vol = mlab.pipeline.volume(gband)
vol.volume.mapper.blend_mode = 'maximum_intensity'

# Make a decent ctf and otf
ctf = ColorTransferFunction()
ctf.range = [0, 1]
ctf.add_rgb_point(1, 1., 1, 0.01)
ctf.add_rgb_point(0.85, 1., 0.8, 0.)
ctf.add_rgb_point(0.6, 0.9, 0.3, 0.)
ctf.add_rgb_point(0.4, 0.8, 0.0, 0.)
ctf.add_rgb_point(0., 0.01, 0., 0.)

otf = PiecewiseFunction()
otf.add_point(1., 1.)
otf.add_point(0.6, 0.9)
otf.add_point(0.2, 0.)
otf.add_point(0., 0.)

vol._volume_property.set_color(ctf)
vol._ctf = ctf
vol._otf = otf
vol._volume_property.set_scalar_opacity(otf)
vol.update_ctf = True

# Add The axes
axes, outline = mpf.add_axes(np.array(zip(ds.domain_left_edge,ds.domain_right_edge)).flatten()/1e8, obj=bfield)
axes.axes.property.color = text_color
axes._title_text_property.color = text_color
axes.label_text_property.color = text_color
outline.visible = False
axes.axes.y_axis_visibility = True
axes.axes.z_axis_visibility = False

# Tweak the figure and set the view
fig.scene.background = (0., 0., 0.)
mlab.view(-90.0, 75.0, 380.0, [ 70.0,  56.4,  61.5])
#fig.scene.anti_aliasing_frames = 20
#fig.scene.save('flux_surface_3d_with_GBandV_t400.png')
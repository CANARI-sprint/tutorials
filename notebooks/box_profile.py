# This python code computes the profile of the specified variable in a box defined by latitude and longitude boundaries and outputs it to a netcdf file.  This code will compute boxes go over the east/west boundary.

import numpy as np  # This package does matrix arithmetic
from netCDF4 import Dataset  # This package is used to read and write netcdf files
import glob         # This package allows us to list files
import sys          # This allows us to read in data behind the python script name when run from command line
import os           # This package is used to check if a file exists

# Get information used for computation:
inputs = sys.argv

# The inputs used to define the box computed:
ENS     = inputs[1]        # Ensemble member number
var     = inputs[2]        # Name of variable of which profile is being computed
region  = inputs[3]        # Region defines the subbasin specificed in the subbasins file (atlmsk, pacmsk, indmsk, socmsk or global)
imin    = float(inputs[4]) # longitude of the western boundary (must be between -180 and 180)
imax    = float(inputs[5]) # longitude of the eastern boundary (must be between -180 and 180)
jmin    = float(inputs[6]) # latitude of the southern boundary
jmax    = float(inputs[7]) # latitude of the northern boundary
outfile = inputs[8]        # filename where data will be saved

# Computing output file if it doesn't exist:
if not (os.path.isfile(outfile)):
    # Find all files needed for computation:
    # directory where data is stored:
    datadir   = ('/gws/nopw/j04/canari/shared/large-ensemble/priority/HIST2/' + ENS + '/')
    # meshmask information:
    meshmask  = '/gws/nopw/j04/canari/shared/large-ensemble/ocean/mesh_mask.nc' 
    # subbasins information:
    basinfile = '/gws/nopw/j04/canari/shared/large-ensemble/ocean/subbasins.nc'
    # List all files containing the variable used for the computation:
    infiles   = glob.glob((datadir + 'OCN/yearly/*/*_' + var + '.nc'))
    # Determine grid of data (t,u or v):
    Ogrid     = infiles[0].split('_')[-2].lower()
    # List all files containing ocean layer depth:
    gfiles    = glob.glob((datadir + 'OCN/yearly/*/*_e3' + Ogrid + '.nc'))

    # Read in data grid information from mesh_mask file:
    mmask = Dataset(meshmask,'r')
    lon   = mmask.variables[('glam' + Ogrid)][0,:,:]  # Note that the longitudes are all between -180 and 180
    lat   = mmask.variables[('gphi' + Ogrid)][0,:,:]
    tmask = mmask.variables[(Ogrid.lower() + 'mask')][0,:,:,:]
    # It is good practice to close netcdf files when you are done:  mmask.close(), however, we will make one more use of the meshmask file
    # Read in mask for basin:
    if region == 'global':
        bmask = tmask[0,:,:]
    else:
        basin = Dataset(basinfile,'r')
        bmask = basin.variables[region][:,:]
        basin.close()
    
    # Since we are averaging over a region, remove halo points by setting the mask to zero:
    tmask[:,:,0]  = 0
    tmask[:,:,-1] = 0
    
    # Mask out any area not in the desired region and compute the smallest region needed to read in to save time:
    if imin > imax:
        bmask[np.where(((lat < jmin) | (lat > jmax)) | ((lon < imin) & (lon > imax)))] = 0
    else:
        bmask[np.where(((lat < jmin) | (lat > jmax)) | ((lon < imin) | (lon > imax)))] = 0
    # Only read in data that's required, otherwise it slows down the computation:
    inds = np.asarray(np.where(bmask == 1))
    xmin = np.min(np.squeeze(inds[1,:]))
    xmax = np.max(inds[1,:])
    ymin = np.min(inds[0,:])
    ymax = np.max(inds[0,:])
    
    # Compute grid area of region  being averaged over:
    nk        = np.size(tmask,axis=0)
    tmask     = tmask[0,ymin:ymax+1,xmin:xmax+1]
    dx        = mmask.variables[('e1' + Ogrid.lower())][0,ymin:ymax+1,xmin:xmax+1]
    dy        = mmask.variables[('e2' + Ogrid.lower())][0,ymin:ymax+1,xmin:xmax+1]
    mmask.close()  # Last use of meshmask file, so closing file here
    area_box  = dx*dy*bmask[ymin:ymax+1,xmin:xmax+1]
    bmask_box = tmask*np.tile(bmask[ymin:ymax+1,xmin:xmax+1]*area_box,(nk,1,1))

    # Get time and depth information from file:
    ncid   = Dataset(infiles[0])
    cal    = ncid.variables['time_counter'].calendar
    units  = ncid.variables['time_counter'].units
    bounds = ncid.variables['time_counter'].bounds
    depth  = ncid.variables[('depth' + Ogrid)][:]
    ncid.close()
    
    # Loop through each file and each month to compute profile:
    nf = len(infiles)
    nt = nf*12
    tt = 0  # Time counter
    profile      = np.zeros((nt,nk,),'float')
    time_counter = np.zeros((nt,)   ,'float')
    time_bounds  = np.zeros((nt,2)  ,'float')

    for ff in range(0,nf):
        tdata = Dataset(infiles[ff],'r')
        gdata = Dataset(gfiles[ff] ,'r')
        for mm in range(0,12):
            print('computing month ' + str(tt+1) + ' of ' + str(nt))
            
            time_counter[tt] = tdata.variables['time_counter'][mm]
            time_bounds[tt]  = tdata.variables[bounds][mm,:]
            box_data         = tdata.variables[var][mm,:,ymin:ymax+1,xmin:xmax+1]
            dz_data          = gdata.variables[('e3' + Ogrid)][mm,:,ymin:ymax+1,xmin:xmax+1]
            
            profile[tt,:] = np.nansum(np.nansum(box_data*bmask_box*dz_data,axis=2),axis=1)/np.nansum(np.nansum(bmask_box*dz_data,axis=2),axis=1)
            tt = tt + 1
        tdata.close()
        gdata.close()
    
    # Save data to netcdf file:
    from netCDF4 import Dataset
    import cftime
    # Create file:    
    ncid = Dataset(outfile, 'w', format='NETCDF4')
    # dimensions:
    ncid.createDimension('time_counter',nt)
    ncid.createDimension('axis_nbounds',2)
    ncid.createDimension('deptht'      ,nk)
    # variables:
    ncid.createVariable(var           ,'f8' ,('time_counter','deptht',))
    ncid.createVariable('deptht'      ,'f8' ,('deptht',))
    ncid.createVariable('time_counter','f8' ,('time_counter',))
    ncid.createVariable(bounds        ,'f8' ,('time_counter','axis_nbounds',))
    # fill variables:
    ncid.variables['time_counter'][:]    = time_counter
    ncid.variables[bounds][:,:]          = time_bounds
    ncid.variables[('depth' + Ogrid)][:] = depth
    ncid.variables[var][:,:]             = profile
    # Add Calendar info:
    ncid.variables['time_counter'].calendar = cal
    ncid.variables['time_counter'].units    = units
    ncid.variables['time_counter'].bounds   = bounds
    # close:
    ncid.close()
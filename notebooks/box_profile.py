# This python code computes the profile of the specified variable in a box defined by latitude and longitude boundaries and outputs it to a netcdf file.  This code will compute boxes go over the east/west boundary.

import numpy as np  # This package does matrix arithmetic
import xarray as xr # This package is an easy way to work with netcdf data
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
    infiles = glob.glob((datadir + 'OCN/yearly/*/*_' + var + '.nc'))
    # Determine grid of data (t,u or v):
    Ogrid = infiles[0].split('_')[-2]
    
    # Read in grid information and determine region of the data needed to be read in:
    Ogrid = infiles[0].split('_')[-2]
    
    mmask = xr.open_mfdataset(meshmask)
    lon   = mmask[('glam' + Ogrid.lower())][0,:,:].to_numpy()  # Note that the longitudes are all between -180 and 180
    lat   = mmask[('gphi' + Ogrid.lower())][0,:,:].to_numpy()
    tmask = mmask[(Ogrid.lower() + 'mask')][0,:,:,:].to_numpy()
    basin = xr.open_mfdataset(basinfile)
    if region == 'global':
        bmask = tmask[0,:,:]
    else:
        bmask = basin[region].to_numpy()
    
    # Since we are only averaging over a region, remove halo points by setting the mask to zero:
    tmask[:,:,0] = 0
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
    dx        = mmask[('e1' + Ogrid.lower())][0,ymin:ymax+1,xmin:xmax+1].to_numpy()
    dy        = mmask[('e2' + Ogrid.lower())][0,ymin:ymax+1,xmin:xmax+1].to_numpy()
    area_box  = dx*dy*bmask[ymin:ymax+1,xmin:xmax+1]
    bmask_box = tmask*np.tile(bmask[ymin:ymax+1,xmin:xmax+1]*area_box,(nk,1,1))
    areaxy    = np.sum(np.sum(bmask_box,axis=2),axis=1)
    
    # Loop through each month and compute profile:
    Tdata = xr.open_mfdataset(infiles)
    nt = Tdata.sizes['time_counter']
    profile = np.zeros((nt,nk),'float')
    
    for tt in range(0,nt):
        print('computing month ' + str(tt+1) + ' of ' + str(nt))
        box_data = Tdata[var][tt,:,ymin:ymax+1,xmin:xmax+1].to_numpy()
        profile[tt,:] = np.nansum(np.nansum(box_data*bmask_box,axis=2),axis=1)/areaxy
    
    # Save data to netcdf file (I wasn't able to figure out how to do this using xarray):
    from netCDF4 import Dataset
    import cftime
    
    # Create file:    
    ncid = Dataset(outfile, 'w', format='NETCDF4')
    
    # dimensions:
    ncid.createDimension('time_counter',nt)
    ncid.createDimension('axis_nbounds',2)
    ncid.createDimension('deptht'      ,nk)
    
    # variables:
    ncid.createVariable(var     ,'f8' ,('time_counter','deptht',))
    ncid.createVariable('deptht','f8' ,('deptht',))
    
    # fill variables:
    ncid.variables['deptht'][:] = Tdata['deptht'].to_numpy()
    ncid.variables[var][:,:]    = profile
    
    # close:
    ncid.close()
    
    ## I tried to save the profile data using xarray since I wanted to keep the metadata (here in my failed attempt):
    #Tprofile = Tdata.isel(x=0,y=0)
    #Tprofile = Tprofile.drop_vars(['nav_lon','nav_lat','x','y','bounds_nav_lon','bounds_nav_lat','deptht_bounds'])
    #Tprofile[var][:,:] = profile
    #Tprofile.to_netcdf(outfile)
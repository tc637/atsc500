'''
    convert an LES netcdf file to a raw binary file

    example:  python3 write_vdf.py TABS output.nc
'''

import glob
from netCDF4 import Dataset
import numpy as np
import pdb
import argparse
import sys

linebreaks=argparse.RawTextHelpFormatter

def write_error(nc_in):
    namelist=[]
    for name,var in nc_in.variables.items():
        if len(var.shape) == 4:
            namelist.append(name)
    return namelist
            
descrip=globals()['__doc__']
parser = argparse.ArgumentParser(description=descrip,formatter_class=linebreaks)
parser.add_argument('varname',help='name of netcdf 3d variable')
parser.add_argument('ncfile',help='netcdf file with les data')
args=parser.parse_args()

meters2km=1.e-3
with Dataset(args.ncfile,'r') as nc_in:
    try:
        var_data=nc_in.variables[args.varname][0,...]
        #var_data=np.ascontiguousarray(var_data.T)
        print(var_data.shape)
        xvals=nc_in.variables['x'][:]*meters2km
        yvals=nc_in.variables['y'][:]*meters2km
        zvals=nc_in.variables['z'][:]*meters2km
        filenames=['xvals.txt','yvals.txt','zvals.txt']
        arrays=[xvals,yvals,zvals]
        for name,vals in zip(filenames,arrays):
            with open(name,'w') as outfile:
                [outfile.write('{:6.3f} '.format(item)) for item in vals[:-1]]
                outfile.write('{:6.3f}\n'.format(vals[-1]))
    except KeyError:
        print('variable names are: ',write_error(nc_in))
        sys.exit(1)
out_name='{}.bin'.format(args.varname)
print('writing an array of {}(x,y,z) shape {}x{}x{}'.format(args.varname,*var_data.shape))
fp=np.memmap(out_name, dtype=np.float32, mode='w+', shape=var_data.shape) 
fp[...]=var_data[...]
del fp
    

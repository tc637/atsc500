import glob
from netCDF4 import Dataset
import numpy as np

files=glob.glob('/Volumes/transcend/phil/gigales/*.nc')
xdim,ydim=100,100

for ncfile in files[:1]:
    with Dataset(ncfile,'r') as nc_in: 
        for name,var in nc_in.variables.items():
            for attr in var.ncattrs():
                print(name,var.__getattr__(attr))
                print('! ',getattr(var,attr))

# with Dataset('output.nc','w') as nc_out:
#     nc_out.createDimension('x',xdim)
#     nc_out.createDimension('y',xdim)
#     nc_out.createDimension('z',None)
#     the_dtype=np.float32
#     for the_var in variables:
#         nc_out.createVariable(varName,the_dtype,('z','y','x'))
    
        

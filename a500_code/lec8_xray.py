import glob
import xray
from matplotlib import pyplot as plt
import numpy as np
from collections import namedtuple
import textwrap

def sort_name(name):
    """
      sort the filenames so '10' sorts
      last by converting to integers
    """
    front, number, back = name.split('_')
    return int(number)


def dict_to_nt(the_dict, tupname):
    """
      convert a dictionary into a namedtuple
    """
    # first define the keys as attributes
    In_tup = namedtuple(tupname, the_dict.keys())
    # then read the key,value pairs in and assign to
    # attributes
    out_tuple = In_tup(**the_dict)
    return out_tuple

if __name__ == "__main__":

    the_files = glob.glob('mar*nc')
    the_files.sort(key=sort_name)

    #
    #  put the 10 ensembles together along a new "ens" dimension
    #  checkpoint the output fields for future runs
    #
    firstrun = False
    if firstrun:
        ds = xray.open_mfdataset(the_files, engine='netcdf4', concat_dim='ens')

        # dump the structure
        print(ds)
        #
        #  3-d ensemble average for temp
        #
        x = ds['x']
        y = ds['y']
        z = ds['z']
        temp = ds['TABS']
        mean_temp = temp[:, 0, :, :, :].mean(dim='ens')
        #
        # same for velocity
        #
        wvel = ds['W']
        mean_w = wvel[:, 0, :, :, :].mean(dim='ens')
        #
        # now look at the perturbation fields for one ensemble
        #
        wvelprime = wvel[0, 0, :, :, :] - mean_w
        Tprime = temp[0, 0, :, :, :] - mean_temp
        flux_prime = wvelprime * Tprime
        flux_profile = flux_prime.mean(dim='x').mean(dim='y')
        keep_dict = dict(flux_prof=flux_profile, flux_prime=flux_prime.values,
                         wvelprime=wvelprime.values, Tprime=Tprime.values, x=x, y=y, z=z)
        np.savez('dump.npz', **keep_dict)
        var_tup = dict_to_nt(keep_dict, 'vars')
    else:
        in_dict = np.load('dump.npz')
        var_tup = dict_to_nt(in_dict, 'vars')
        print(var_tup._fields)

    plt.close('all')
    plt.style.use('ggplot')
    fig1, ax1 = plt.subplots(1, 1)
    ax1.plot(var_tup.flux_prof, var_tup.z)
    ax1.set(ylim=[0, 1000], title='Ens 0: vertically averaged kinematic heat flux',
            ylabel='z (m)', xlabel='flux (K m/s)')

    fig2, ax2 = plt.subplots(1, 1)
    z200 = np.searchsorted(var_tup.z, 200)
    ax2.hist(var_tup.flux_prime[z200, :, :].flat)
    ax2.set(title='histogram of kinematic heat flux (K m/s) at z=200 m')

    fig3, ax3 = plt.subplots(1, 1)
    ax3.hist(var_tup.wvelprime[z200, :, :].flat)
    ax3.set(title="histogram of wvel' at 200 m")

    fig4, ax4 = plt.subplots(1, 1)
    ax4.hist(var_tup.Tprime[z200, :, :].flat)
    ax4.set(title="histogram ot T' at z=200 m")
    plt.show()

    hit = np.logical_and(var_tup.wvelprime > 0, var_tup.Tprime > 0)

    pos_buoyant = np.ones_like(var_tup.flux_prime, dtype=np.float32)
    #pos_buoyant[hit] = var_tup.flux_prime[hit]
    pos_buoyant[hit] = pos_buoyant[hit]*100.

    filenames = ['xvals.txt', 'yvals.txt', 'zvals.txt']
    arrays = [var_tup.x, var_tup.y, var_tup.z]
    for name, vals in zip(filenames, arrays):
        with open(name, 'w') as outfile:
            #
            # write all but the last without a newline
            #
            [outfile.write('{:6.3f} '.format(item)) for item in vals[:-1]]
            #
            # write the last value with a newline
            #
            outfile.write('{:6.3f}\n'.format(vals[-1]))

    varname = 'buoyancy'
    out_name = '{}.bin'.format(varname)
    rev_shape = pos_buoyant.shape[::-1]
    string_shape="{}x{}x{}".format(*rev_shape)
    print('writing an array of {} of shape x,y,z= {}'.format(varname,string_shape))
    fp = np.memmap(out_name, dtype=np.float32,
                   mode='w+', shape=pos_buoyant.shape)
    fp[...] = pos_buoyant[...]

    vars=dict(dim=string_shape,var='buoyancy')
    
    command=r"""
        vdfcreate  -xcoords xvals.txt -ycoords yvals.txt -zcoords zvals.txt \
           -gridtype stretched -dimension {dim:s} -vars3d {var:s} -numts 1 {var:s}.vdf

        raw2vdf -varname {var:s} -ts 0 {var:s}.vdf {var:s}.bin
    """
    out=textwrap.dedent(command.format_map(vars))
    print(out)

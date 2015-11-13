__version__="0.01"

import site
site.addsitedir('/Users/phil/repos/atsc500/a500_code')
import thermlib
from thermlib import thermfuncs as thf
from thermlib import thermconst as tc
from thermlib.readsound import readsound
import matplotlib.pyplot as plt
import os

def calcmixture(sounding):
    """
    given a dictionary with Temperature (K), wv (kg/kg), height (m), pressure (Pa)
    build a dictionary containing hmval (J/kg), wT (kg/kg), and thetae (K)
    """
    #calculate the moist static energy
    th=sounding['thetaK']; p=sounding['pkPa'];
    q =sounding['wvKgkg']; gz=sounding['heightM']*tc.g;
    
    r  = thf.r_q(q);
    t  = thf.t_thpr(th,p,r);
    tv = thf.tro_trtp(t,q,p);
    thv= thf.thv_tvp(tv,p)
    CPN= tc.CPD*(1.-q)+tc.CPV*q
    hl = t*CPN+gz      #liquid water static energy
    
    nk=1; mlev=50; num=140; smin=0.0; smax=1.0;
    mixture=thf.mix(hl[nk],q[nk],hl[mlev],q[mlev],p[mlev],gz[mlev],num,smin,smax)
    sm   =mixture["SM"];    # fraction of environmental air
    qm   =mixture["RM"];    # specific total water content
    hm   =mixture["HM"];    # liquid water potential temperature
    qlm  =mixture["RLM"];   # specific liquid water content
    throm=mixture["THROM"]; # virtual potential temperature including liquid water loading effect
    dens=mixture['DENS']
    #build a dictionary to hold the output
    outDict={'sm':sm,'hm':hm,'qm':qm,'qlm':qlm,'throm':throm,'throi':thv[mlev],'dens':dens}
    return outDict

def main():
    #input the sounding
    datapath=thermlib.__file__.split(os.sep)[:-1]
    soundfile = datapath.copy()
    soundfile.extend(['testdata','sound.dat'])
    print(soundfile)
    soundfile = os.sep.join(soundfile)
    soundDict=readsound(soundfile)
    mixout=calcmixture(soundDict)
    xvals=mixout["sm"]
    yvals=mixout["hm"]
    #make a plot
    plt.figure(1)
    plt.clf()
    plt.subplot(221)
    plt.plot(xvals,yvals*1.e-3,'r-')
    plt.xlabel("fraction of environmental air")
    plt.ylabel(r"$h_l\ (kJ/kg)$")
    plt.title ('mixture liquid water static energy')

    xvals=mixout["sm"]
    yvals=mixout["qm"]*1000.
    plt.subplot(222)
    plt.plot(xvals,yvals,'r-')
    plt.xlabel("fraction of environmental air")
    plt.ylabel("r_t (g/kg)")
    plt.title ('mixture total water mixing ratio')

    xvals=mixout["sm"]
    yvals=mixout["throm"]-mixout["throi"];
    plt.subplot(223)
    plt.plot(xvals,yvals,'r-')
    plt.xlabel("fraction of environmental air")
    plt.ylabel(r"$T_{mixture} - T_{environment}$")
    plt.title ('mixture - environment temperature difference')


    xvals=mixout["sm"]
    yvals=mixout["dens"]
    plt.subplot(224)
    plt.plot(xvals,yvals,'r-')
    plt.xlabel("fraction of environmental air")
    plt.ylabel("density kg/m3")
    plt.title ('mixture density')
    plt.suptitle('cloud environment mixtures at 1500 m',fontsize=18)

    plt.show()
    plt.savefig('mix.png',dpi=300)

if __name__ == "__main__":
    main()
    

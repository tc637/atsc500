"""
  this example reads in a souding and calculates
  the height of each pressure level by integrating
  the hydrostatic equation.  The result
"""

import numpy as N
from .thermconst import RD,g

def hydrostat(sound):
    """in: sounding dictionary with required keys
       out:
       given a sounding dictionary with pressure in Pa
       and Temperature in K, integrate the hydrostatic
       equation to get the height in meters
    """
    #no need to convert from kPa to Pa, because conversion
    #factor cancels between diffP and rho
    diffP=(sound["pkPa"][1:] - sound["pkPa"][:-1])
    rho=sound["pkPa"]/(RD*sound["tempK"])
    height=N.cumsum(-1.*diffP/(g*rho[1:]))
    #can only concatenate arrays
    height= N.concatenate((N.array([0.]),height))
    return height

if __name__== '__main__':
    from . import readsound
    soundDict=readsound.readsound("sound.dat")
    height=hydrostat(soundDict)
    print("height: ",height)



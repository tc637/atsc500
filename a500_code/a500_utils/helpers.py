"""
  helper function to turn a dictionary into a named tuple
  and check whether all arguments are scalar
"""
import numpy as np

from collections import namedtuple
def make_tuple(in_dict,tupname='values'):
    the_tup = namedtuple(tupname, in_dict.keys())
    the_tup = the_tup(**in_dict)
    return the_tup

def test_scalar(*args):
    """
      return true if every argument is a scalar
    """
    isscalar=True
    for item in args:
        isscalar = isscalar & np.isscalar(item)
    return isscalar

def testfuns():
    assert(test_scalar(1.,2.,3.))
    assert(not test_scalar([1.,2.],3.,4.))
    assert(not test_scalar([1.,2.],np.array(3.),4.))
    assert(test_scalar([1.,2.],np.array(3.),4.))
    
if __name__ == "__main__":
    testfuns()
    

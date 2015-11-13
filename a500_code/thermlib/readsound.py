"here is doc"

import numpy as np
import thermlib.thermfuncs as thf
import re
from thermlib.hydrostat import hydrostat


def readsound(soundfile):
    """
    in: text string specifying filename
    out: dictionary with sounding
    read an ascii sounding file named soundfile and return
    T (K), wv (kg/kg), p (kPa), height (m)
    into a dictionary with the keys:
    ['heightM', 'wvKgkg', 'pkPa', 'tempK']
    """
    
    sounding = open(soundfile,"r")
    #read in all the lines
    gulpIt=sounding.read()
    #gulpIt=gulpIt.replace('\n','xxx')

    #break sound.dat into four variables (T (K), wv (kg/kg), p (Pa), height (m)
    reBreak=re.compile(r'\n([A-Z]+)\n')  
    reVarname=re.compile('[A-Z]+')
    reBlanks=re.compile('\s+')
    
    variables=reBreak.split(gulpIt)
    
    varDict={}

    for count,line in enumerate(variables):
        if reVarname.match(line):
            theData=variables.pop(count+1)
            theData=theData.replace('\n',' ')
            theData=reBlanks.split(theData.strip())
            theData=[float(item) for item in theData]
            varDict[line]=theData

    sounding.close()

    #move the lists into a dictionary, converting into numeric arrays
    theDict={}
    theDict["thetaK"]=np.array(varDict['TH'])
    theDict["wvKgkg"]=np.array(varDict['QV'])
    theDict["pkPa"]=np.array(varDict['PL'])*0.001
    theDict["tempK"] = findTemp(theDict)
    theDict['heightM']=hydrostat(theDict)
    return theDict

def findTemp(soundDict):
    """in: sounding dictionary with required keys
       ['pkPa', 'thetaK'] for press (kPa), and theta (K)
       out: Numeric vector of temperatures (K)
    """
    #first check to make sure all dictionary vectors
    #have the same length
    #raise an exception if not
    theKeys=list(soundDict.keys())
    for key in theKeys:
        if len(soundDict[key]) != len(soundDict[theKeys[0]]):
               raise ValueError("trouble in findTheta:  soundDict arrays different sizes")
    tempVals=np.zeros(soundDict[theKeys[0]].shape[0],np.float)
    for i in range(tempVals.shape[0]):
        theta=soundDict["thetaK"][i]
        press=soundDict["pkPa"][i]
        tempVals[i]=thf.tda(theta,press)
    return tempVals
        
if __name__== '__main__':
    import thermlib, os
    datapath=thermlib.__file__.split(os.sep)[:-1]
    soundfile = datapath.copy()
    soundfile.extend(['testdata','sound.dat'])
    print(soundfile)
    soundfile = os.sep.join(soundfile)
    theSound=readsound(soundfile)
    print(theSound.keys())
    print(theSound)
    





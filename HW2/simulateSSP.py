#/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
import math

# longitudeES = some value
# latitudeES = some other value
# initialSSPLon = some value
# initialSSPLat = some value
# phi = some other value
# deltaTSec need this from simulateOrbit somehow
earthRotVelRadSec = 7.2921159e-5
def getSspLongLat(theta, r):
    pass
def getGamma(long, lat, theta, rn):
    pass

def convertXYZToLatLon(x,y,z, secsFromApogee):
    lat = math.degrees(math.acos( z / r) - initialSSPLat) # LAT in radians does NOT change as earth rotates
    lon = math.degrees(math.atan2(y, x) - initialSSPLon - earthRotVelRadSec*secsFromApogee) # LON in radians DOES change as earth rotates
    return lat, lon

def getCart3D(rn, thetaN, phi):
    XnewArr = []
    YnewArr = []
    ZnewArr = []
    for radius, angle in zip(rn, thetaN):
        c = radius * np.exp(complex(0, angle))
        Xold = np.real(c)
        Yold = np.imag(c)

        XnewArr.append(np.real(Xold * np.exp(complex(0, phi))))
        YnewArr.append(Yold)
        ZnewArr.append(np.imag(Xold * np.exp(complex(0, phi))))
    return XnewArr, YnewArr, ZnewArr

#/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
import math
import pdb


# longitudeES = some value
# latitudeES = some other value
# initialSSPLon = some value
# initialSSPLat = some value
# phi = some other value
# deltaTSec need this from simulateOrbit somehow
earthRotVelRadSec = 7.2921159e-5
pi2 = 2 * np.pi


def getCart3D(rn, thetaN, phi):
    XnewArr = []
    YnewArr = []
    ZnewArr = []
    for radius, angle in zip(rn, thetaN):
        c = radius * np.exp(angle * 1j)
        Xold = np.real(c)
        Yold = np.imag(c)
        # these are backwards? according to the help file, this is right.
        #HOwever, the math says x is the real part and z is the imaginary
        # I'm not sure what to do here, so I'll leave it like this for now
        # Things definitely don't work when this is "correct"
        ZnewArr.append(np.real(Xold * np.exp(phi * 1j)))
        YnewArr.append(Yold)
        XnewArr.append(np.imag(Xold * np.exp(phi * 1j)))
    return XnewArr, YnewArr, ZnewArr


def convertXYZToLatLon(x, y, z, secsFromApogee):
    r = math.sqrt(x * x + y * y + z * z)
    # LAT in rad does NOT change as earth rotates. [0, 360]
    lat = -1 * (math.acos(z / r) + math.radians(initialSSPLat)) + pi2  # ((math.degrees(math.acos(z / r)) + initialSSPLat) % 360) - 180
    # lat = math.degrees(lat)
    # LON in rad DOES change as earth rotates. [0 , 360]
    lon = (math.atan2(y, x) % pi2) - earthRotVelRadSec * secsFromApogee + math.radians(initialSSPLon)#(math.degrees(math.atan2(y, x))  + initialSSPLon - earthRotVelRadSec * secsFromApogee ) % 360
    return lat, lon


def calcGamma(Le, le, Ls, ls):
    cosGamma = math.sin(Ls) * math.sin(Le) + math.cos(Ls) * \
        math.cos(Le) * math.cos(ls - le)
    gamma = math.acos(cosGamma)
    return gamma


def calcElevationAngle(gamma, re, rs):
    denom = math.sqrt(1 + (re / rs)**2 - 2 * (re / rs) * math.cos(gamma))
    cosEl = math.sin(gamma) / denom
    El = math.degrees(math.acos(cosEl))
    return El


def getSSPRelativityToES(Le, le, Ls, ls):
    compass = ""
    # latitude ES > latitude sat
    if Le > Ls:
        compass += "S"
    else:
        compass += "N"
    if le > ls:
        compass += "E"
    else:
        compass += "W"
    return compass


def calcAzimuth(Le, le, Ls, ls, gamma):
    alpha = math.degrees(math.sin(math.fabs(le - ls)) * math.cos(Ls) / math.sin(gamma))
    compass = getSSPRelativityToES(Le, le, Ls, ls)
    print "compass", compass, "alpha", alpha
    if compass == "NE":
        return alpha
    elif compass == "SW":
        return alpha + 180
    elif compass == "SE":
        return 180 - alpha
    else:
        return 360 - alpha


def plotThisMotherfucker(x, y, title=""):
    ax = plt.plot(x, y, ms=10, alpha=1, color='b')
    plt.grid(True)
    plt.title(title)
    plt.show()

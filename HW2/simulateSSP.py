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


def getCart3D(rn, thetaN, phi):
    XnewArr = []
    YnewArr = []
    ZnewArr = []
    for radius, angle in zip(rn, thetaN):
        c = radius * np.exp(angle * 1j)
        Xold = np.real(c)
        Yold = np.imag(c)

        ZnewArr.append(np.real(Xold * np.exp(phi * 1j)))
        YnewArr.append(Yold)
        XnewArr.append(np.imag(Xold * np.exp(phi * 1j)))
    return XnewArr, YnewArr, ZnewArr


def convertXYZToLatLon(x, y, z, secsFromApogee):
    # LAT in radians does NOT change as earth rotates. [0, 360]
    r = math.sqrt(x*x + y*y + z*z);
    lat = (math.degrees(math.acos(z / r)) % 360)  + initialSSPLat
    # LON in radians DOES change as earth rotates. [-180 , 180]
    lon = (math.degrees(math.atan2(y, x)) % 360) - 180 + initialSSPLon - earthRotVelRadSec * secsFromApogee
    return lat, lon


def calcGamma(Le, le, Ls, ls):
    cosGamma = math.sin(Ls) * math.sin(Le) + math.cos(Ls) * \
        math.cos(Le) * math.cos(ls - le)
    gamma = math.acos(cosGamma)
    return gamma


def calcElevationAngle(gamma, re, rs):
    denom = math.sqrt(1 + (re / rs)**2 - 2 * (re / rs) * math.cos(gamma))
    cosEl = math.sin(gamma) / denom
    El = math.acos(cosEl)
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
    alpha = math.sin(math.fabs(le - ls)) * math.cos(Ls) / math.sin(gamma)
    compass = getSSPRelativityToES(Le, le, Ls, ls)
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

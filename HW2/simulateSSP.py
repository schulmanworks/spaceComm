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
earthRotVelRadSec = 7.2921159e-5 # rad/sec
pi2 = 2 * np.pi
initialSSPLat = 63.4  # degrees
initialSSPLon = 360-96.0  # degrees


def getCart3D(rn, thetaN, phi):
    XnewArr = []
    YnewArr = []
    ZnewArr = []
    for radius, theta in zip(rn, thetaN):
        print "radius", radius, "theta", theta
        Xold = radius * math.cos(theta)
        Yold = radius * math.sin(theta)
        # these are backwards? according to the help file, this is right.
        #HOwever, the math says x is the real part and z is the imaginary
        # I'm not sure what to do here, so I'll leave it like this for now
        # Things definitely don't work when this is "correct"
        # pdb.set_trace()
        ZnewArr.append(np.real(Xold * np.exp(phi * 1j)))
        YnewArr.append(Yold)
        XnewArr.append(np.imag(Xold * np.exp(phi * 1j)))
    return XnewArr, YnewArr, ZnewArr


def convertXYZToLatLon(x, y, z, secsFromApogee):
    r = math.sqrt(x * x + y * y + z * z)
    # LAT in rad does NOT change as earth rotates. [0, pi]
    lat = np.pi/2.0 - (math.acos(z / r)) #+ math.radians(initialSSPLat) +.57#+ np.pi # ((math.degrees(math.acos(z / r)) + initialSSPLat) % 360) - 180
    # lat = math.degrees(lat)
    # LON in rad DOES change as earth rotates. [0, 2pi]
    arctan = math.atan2(y, x)
    lon = (arctan - earthRotVelRadSec * secsFromApogee + math.radians(initialSSPLon))% pi2 #(math.degrees(math.atan2(y, x))  + initialSSPLon - earthRotVelRadSec * secsFromApogee ) % 360
    return lat, lon


def calcGamma(Le, le, Ls, ls):
    cosGamma = math.sin(Ls) * math.sin(Le) + math.cos(Ls) * math.cos(Le) * math.cos(ls - le)
    gamma = math.acos(cosGamma)
    return gamma


def calcElevationAngle(gamma, re, rs):
    denom = math.sqrt(1 + ((re / rs)**2) - 2 * (re / rs) * math.cos(gamma))
    cosEl = math.sin(gamma) / denom
    # print "elevation in rad", math.acos(cosEl)
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
        compass += "W"
    else:
        compass += "E"
    return compass


def calcAzimuth(Le, le, Ls, ls, gamma):
    sinalpha = math.sin(math.fabs(le - ls)) * math.cos(Ls) / math.sin(gamma)
    alpha = math.degrees(math.asin(sinalpha))
    compass = getSSPRelativityToES(Le, le, Ls, ls)
    # print "compass", compass, "alpha", alpha
    if compass == "NE":
        return alpha
    elif compass == "SW":
        return alpha + 180, alpha
    elif compass == "SE":
        return 180 - alpha, alpha
    else:
        return 360 - alpha, alpha


def plotThisMotherfucker(x, y, title="", specialPoints = None):
    ax = plt.plot(x, y, ms=10, alpha=1, color='b')
    if specialPoints != None:
        for point in specialPoints:
            plt.plot([point[0]], [point[1]], marker="x", color="red")
    plt.grid(True)
    plt.title(title)
    plt.show()

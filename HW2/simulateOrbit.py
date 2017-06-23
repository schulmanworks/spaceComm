#/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
import math
import pdb

import simulateSSP

r = 46983.0  # km MUST BE A FLOAT
theta = 0.0  # degrees
Vr = 0.0  # km/s
Vtheta = 2.74084  # km/s
G = 6.672e-20  # km^3 / kg*s^2
Mp = 5.974e24  # earth 5.974e24 #kg

deltaTSec = 1

rn = [r]  # km
thetaN = [theta]  # degrees
deltaRn = [Vr * deltaTSec]  # km
deltaThetaN = [Vtheta * deltaTSec / r]  # degrees / km

# hw2 new constants
Le = 0  # degrees
le = 0  # degrees
earthRadius = 6371  # km
phi = 63.4
simulateSSP.initialSSPLat = 63.4 # degrees
simulateSSP.initialSSPLon = -96 # degrees

def deltaRnPlus1(deltaRn, rn, deltaThetaN, G, Mp, deltaTSec):
    term1 = deltaRn
    term2 = (rn + 1 / 2 * deltaRn) * (deltaThetaN ** 2)
    term3 = (G * Mp * (deltaTSec ** 2)) / ((rn + 1 / 2 * deltaRn) ** 2)
    # pdb.set_trace()
    return term1 + term2 - term3


def deltaThetaNPlus1(deltaThetaN, deltaRn, rn):
    term1 = deltaThetaN
    term2 = (2 * deltaRn * deltaThetaN) / (rn + 1 / 2 * deltaRn)
    return term1 - term2


timeVector = np.arange(0, 9e4, deltaTSec)
for x in list(timeVector):  # 3.154e7
    rn.append(rn[-1] + deltaRn[-1])
    thetaN.append(thetaN[-1] + deltaThetaN[-1])
    tempDeltaRn = deltaRnPlus1(
        deltaRn[-1], rn[-1], deltaThetaN[-1], G, Mp, deltaTSec)
    tempThetaN = deltaThetaNPlus1(deltaThetaN[-1], deltaRn[-1], rn[-1])
    deltaRn.append(tempDeltaRn)
    deltaThetaN.append(tempThetaN)

# ax = plt.subplot(111, projection='polar')
# ax.plot(thetaN, rn)
# ax.grid(True)
# u = G * Mp
#
# Ra = max(rn)  # approx
# Rp = min(rn)  # approx
# e = (Ra - Rp) / (Ra + Rp)
#
# a = Ra / (1 + e)
# T = math.sqrt(4 * np.pi**2 * a**3 / u)
# m, s = divmod(T, 60)
# h, m = divmod(m, 60)
# print("e = %f and T = %f seconds" % (e, T))
# ax.set_title("Orbit r=%d theta=%d Vr=%d Vtheta=%.4f e=%.4f T=%d:%02d:%.2d" % (
#     r, theta, Vr, Vtheta, e, h, m, s), va='bottom')
# ax.set_rmax(Ra + 5000)
# ax.grid(True)
# plt.show()

rn = rn[:-1]
simulateSSP.plotThisMotherfucker(timeVector, rn, "rn")

thetaN = thetaN[:-1]
simulateSSP.plotThisMotherfucker(timeVector, thetaN, "thetaN")


xarr, yarr, zarr = simulateSSP.getCart3D(rn, thetaN, phi)
simulateSSP.plotThisMotherfucker(timeVector, xarr, "X values")
simulateSSP.plotThisMotherfucker(timeVector, yarr, "Y values")
simulateSSP.plotThisMotherfucker(timeVector, zarr, "Z values")

elevationAngles = []
azimuthAngles = []
lons = []
lats = []
i = 0
for x, y, z, satRadius in zip(xarr, yarr, zarr, rn):
    # print "i", i
    Ls, ls = simulateSSP.convertXYZToLatLon(x, y, z, deltaTSec * i)
    lons.append(ls)
    lats.append(Ls)
    gamma = simulateSSP.calcGamma(Le, le, Ls, ls)
    # horizon check
    # pdb.set_trace()
    if gamma <= math.acos(earthRadius / satRadius):
        El = simulateSSP.calcElevationAngle(gamma, earthRadius, satRadius)
        Az = simulateSSP.calcAzimuth(Le, le, Ls, ls, gamma)
        elevationAngles.append(El)
        azimuthAngles.append(Az)
    i += 1
simulateSSP.plotThisMotherfucker(timeVector, lons, "lons")
simulateSSP.plotThisMotherfucker(timeVector, lats, "lats")
simulateSSP.plotThisMotherfucker(azimuthAngles, elevationAngles, "Azimuth vs Elevation")

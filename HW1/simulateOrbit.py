#/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
import math
import pdb
# r = np.arange(0, 2, 0.01)
# theta = 2 * np.pi * r

r = 30000 # km
theta = 0 # degrees
Vr = 1 # km/s
Vtheta = 2 # km/s

G = 6.672e-20 # km^3 / kg*s^2
Mp = 5.974e24 #kg

deltaTSec = 1

rn = [r] # km
thetaN = [theta] # degrees
deltaRn = [Vr * deltaTSec] # km
deltaThetaN = [Vtheta * deltaTSec / r] # degrees / km


def deltaRnPlus1(deltaRn, rn, deltaThetaN, G, Mp, deltaTSec):
    term1 = deltaRn
    term2 = (rn + 1/2 * deltaRn) * (deltaThetaN ** 2)
    term3 =  (G * Mp * (deltaTSec ** 2))/((rn + 1/2 * deltaRn) ** 2)
    # pdb.set_trace()
    return term1 + term2 - term3

def deltaThetaNPlus1(deltaThetaN, deltaRn, rn):
    term1 = deltaThetaN
    term2 = (2 * deltaRn * deltaThetaN) / (rn + 1/2 * deltaRn)
    return term1 - term2

totalAngle = 0
for x in list(np.arange(0, 3.154e7, deltaTSec)):#3.154e7
    # print(i)
    # i += 1
    rn.append(rn[-1] + deltaRn[-1])
    thetaN.append(thetaN[-1] + deltaThetaN[-1])
    tempDeltaRn =  deltaRnPlus1(deltaRn[-1], rn[-1], deltaThetaN[-1], G, Mp, deltaTSec)
    tempThetaN = deltaThetaNPlus1(deltaThetaN[-1], deltaRn[-1], rn[-1])
    deltaRn.append(tempDeltaRn)
    deltaThetaN.append(tempThetaN)

    totalAngle += tempThetaN
    print(totalAngle, " ", tempThetaN)
    if totalAngle > 360:
        break
ax = plt.subplot(111, projection='polar')
ax.plot(thetaN, rn)
ax.grid(True)
u = G * Mp

Ra = max(np.absolute(rn)) # approx
Rp = min(np.absolute(rn)) # approx
e = (Ra - Rp) / (Ra + Rp)

a = Ra / (1 + e)
T = math.sqrt(4 * np.pi**2 * a**3 / u)
m,s = divmod(T, 60)
h,m = divmod(m, 60)
print("e = %f and T = %f seconds" % (e, T))
ax.set_title("Orbit r=%d theta=%d Vr=%d Vtheta=%d e=%f T=%d:%02d:%02d" % (r,theta,Vr,Vtheta,e,h,m,s), va='bottom')
ax.set_rmax(Ra + 5000)
plt.show()

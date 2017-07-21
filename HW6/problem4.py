#/usr/bin/python
import matplotlib.pyplot as plt
import numpy as np
import pdb

def calcAm(m, M=16, d=2):
    return (2 * m - 1 - M) * d
Ams = []
for x in range(15):
     Ams.append(calcAm(x+1, d=5))
print np.average(Ams)

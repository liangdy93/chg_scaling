import math
import numpy as np
import msd
import subprocess as sub
from scipy.optimize import minimize

para = [0.81069167, 0.05064066, 2.43190974, 0.06724219, 2.35213416]


# test if we can get msd

#msd1 = msd.msd(para)
#print(msd1)
#exit()

# optimize selected charge and lj parameter

test = minimize(msd.msd, para, method='nelder-mead',options={'xatol':1e-2,'disp':True})
print(test)



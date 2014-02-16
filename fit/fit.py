from __future__ import division
import numpy as np
import matplotlib.pyplot as plt

#def cn(n):
#   c = y*np.exp(-1j*2*n*np.pi*time/period)
#   return c.sum()/c.size
#
#def f(x, Nh):
#   f = np.array([2*cn(i)*np.exp(1j*2*i*np.pi*x/period) for i in range(1,Nh+1)])
#   return f.sum()
#
#time = np.arange(9,0,-1)
#y = np.array([19,19.5,20,21.4,22,23,25,25.1,25.5])
#
##time = np.arange(0,10)
#period = 0.01
#y2 = np.array([f(t,5).real for t in time])
#
#plt.plot(time, y)
#plt.plot(time, y2)
#plt.show()

x = np.arange(0,20)
y = x/np.pi
N = x.shape
c = np.fft.rfft(y)/N
print c

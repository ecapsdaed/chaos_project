import scipy.integrate as integrate
import matplotlib as mpl
from math import *
import matplotlib.pyplot as plt
import numpy as np
import random as ran
import multiprocessing as mp
import time

'''
  Global constants.
'''
X = 0
Y = 1

# Rectangle
xr, yr = 10, 10
xl, yl = 0, 0
# Starting position
xS, yS = 5, 5

# Chaos in Arnold
v = 1
A = 0.5
B = 0.25
C = 0.25 
# C = 0 results in periodic motion (very clear without mirror mapping).
# Large C results in chaos.
# Initial parameters
x0   = np.asarray( [4, 3.5, 0, xS, yS] ) #x1, x2, x3, x, y
t0   = 0
tEnd = 100
t    = np.linspace( t0, tEnd, num = tEnd+1 )


'''
  Mirror mapping
'''
# Inefficient, only for a rectangular area without obstacles.
# Need generalisation.
def mirrRec( m ):
  n = np.copy( m )
  for i in range( len( n ) ):
    if( n[i][X] ) > xr:
      n[i:][:,X] = 2*xr - n[i:][:,X]
    elif( n[i][X] ) < xl:
      n[i:][:,X] = 2*xl - n[i:][:,X]
    if( n[i][Y] ) > yr:
      n[i:][:,Y] = 2*yr - n[i:][:,Y]
    elif( n[i][Y] ) < yl:
      n[i:][:,Y] = 2*yl - n[i:][:,Y]
  return n

'''
  Deterministic chaos.
  Arnold equation.
'''
def detChaos( dxs, t ):
  dx1 = A*np.sin( dxs[2] ) + C*np.cos( dxs[1] )
  dx2 = B*np.sin( dxs[0] ) + A*np.cos( dxs[2] )
  dx3 = C*np.sin( dxs[1] ) + B*np.cos( dxs[0] )
  dx  = v*np.cos( dxs[2] )
  dy  = v*np.sin( dxs[2] )
  
  return np.asarray( [dx1, dx2, dx3, dx, dy] )

'''
  Random walk.
'''
# Inefficient.
def ranWalk():
  xyRan = np.zeros( (tEnd, 2), dtype = float )
  rng = np.random.default_rng()
  xyRan[0] = xS, yS
  for i in range( tEnd-1 ):
    rans = rng.uniform( 0.0, 2*np.pi )
    xyRan[i+1] = xyRan[i][X] + v*t[1]*np.cos( rans ), xyRan[i][Y] + v*t[1]*np.sin( rans )
  
  return np.copy( xyRan )

'''
  Run the simulation.
'''
def run():
  # Chaos
  f = integrate.odeint( detChaos, x0, t )
  # Random
  g = ranWalk()
  
  # Only the X and Y coordinates.
  xy = np.copy( f[:,[3,4]] )
  
  # Mirror map.
  test = mirrRec( xy )
  tist = mirrRec( g )
  
  plot( test, tist )


def plot( f, g ):
  figs = plt.figure()
  
  # Decay
  plt.plot( f[:,0], f[:,1], color = 'black', label = "Det")
  plt.plot( g[:,0], g[:,1], '--', color = 'black', label = "Ran")
  #plt.scatter( f[:,0], f[:,1], color = 'black', label = "Lim")
  
  plt.ylabel( 'y' )
  plt.xlabel( 'x' )
  axes = plt.gca()
  #axes.set_xlim([xl, xr])
  #axes.set_ylim([yl, yr])

  plt.legend( loc='best' )

  plt.show()
  
run()

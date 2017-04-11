#from cython.parallel import parallel, prange
#cimport openmp
#from libc.stdlib cimport malloc, free
import cython 
from cython.parallel import prange, parallel
import multiprocessing as mp
import numpy as np


cpdef C_np_generate_bonds(list coords):
    bonds = []
    NDIM = 3 # number of dimensions
    a = np.array(coords)
    a.shape = a.size / NDIM, NDIM

    for i  in  range(0, len(coords), 3): 
        
        point = np.array ([coords[i], coords[i+1], coords[i+2]])
        
        d = ((a-point)**2).sum(axis=1)  # compute distances
        ndx = d.argsort() # indirect sort 
        
        #'''
        for  index in ndx:
            if d[index] >= 2.84:
                break
        
            
            else:
                if d[index] == 0.0:
                    pass
                else:
                    pass
                    #print index, d[index]
                    #print point, a[index], d[index]
                    bonds.append(point[0])
                    bonds.append(point[1])
                    bonds.append(point[2])
                    bonds.append(a[index][0]) 
                    bonds.append(a[index][1])
                    bonds.append(a[index][2])
        #'''
    return bonds 
    
    



cpdef C_generate_bonds(list coords):
    
    #cdef double bonds[len(coords)]
    bonds = []
    cdef int i
    cdef int j
    cdef int num_threads
    #cdef double dist_2
    
    #with nogil, parallel(num_threads=4):
    #print coords
    for i in range (0, len(coords),3):
        
        for j in range (i+3, len(coords),3):
            
            if coords[i] - coords[j] >= 2.0  or coords[i+1] - coords[j+1] >= 2.0 or coords[i+2] - coords[j+2] >= 2.0:
                pass
                #print coords[i], coords[j]
            
            
            else:
                dist =  [coords[i]  - coords[j]  ,
                        coords[i+1] - coords[j+1],
                        coords[i+2] - coords[j+2]]
                #print dist
                dist2 = dist[0]**2 + dist[1]**2 + dist[2]**2

                if dist2 <= 2.89:
                    #print coords[i], coords[i+1], coords[i+2] ,coords[j] , coords[j+1], coords[j+2], dist2
                    bonds.append(coords[i])
                    bonds.append(coords[i+1])
                    bonds.append(coords[i+2])

                    bonds.append(coords[j])
                    bonds.append(coords[j+1])
                    bonds.append(coords[j+2])
    #print bonds
    return bonds


#from cython.parallel import parallel, prange
#cimport openmp
#from libc.stdlib cimport malloc, free
import cython 
from cython.parallel import prange, parallel
import multiprocessing as mp
import numpy as np

'''
#cpdef C_np_generate_bonds(list coords):
#    bonds = []
#    NDIM = 3 # number of dimensions
#    a = np.array(coords)
#    a.shape = a.size / NDIM, NDIM
#
#    for i  in  range(0, len(coords), 3): 
#        
#        point = np.array ([coords[i], coords[i+1], coords[i+2]])
#        
#        d = ((a-point)**2).sum(axis=1)  # compute distances
#        ndx = d.argsort() # indirect sort 
#        
#        #
#        for  index in ndx:
#            if d[index] >= 2.84:
#                break
#        
#            
#            else:
#                if d[index] == 0.0:
#                    pass
#                else:
#                    pass
#                    #print index, d[index]
#                    #print point, a[index], d[index]
#                    bonds.append(point[0])
#                    bonds.append(point[1])
#                    bonds.append(point[2])
#                    bonds.append(a[index][0]) 
#                    bonds.append(a[index][1])
#                    bonds.append(a[index][2])
#        #
#    return bonds 
#    
#cpdef C_generate_bonds2(list coords):
#    
#    #cdef double bonds[len(coords)]
#    bonds = []
#    cdef int i
#    cdef int j
#    cdef int num_threads
#
#
#
#    for i in range (0, len(coords),3):
#       
#        for j in range (i+3, len(coords),3):    
#            
#            
#            if coords[i] - coords[j] >= 2.0  or coords[i+1] - coords[j+1] >= 2.0 or coords[i+2] - coords[j+2] >= 2.0:
#                pass
#                #print coords[i], coords[j]
#            
#            
#            else:
#                dist =  [coords[i]  - coords[j]  ,
#                        coords[i+1] - coords[j+1],
#                        coords[i+2] - coords[j+2]]
#                #print dist
#                dist2 = dist[0]**2 + dist[1]**2 + dist[2]**2
#
#                if dist2 <= 2.89:
#                    #print coords[i], coords[i+1], coords[i+2] ,coords[j] , coords[j+1], coords[j+2], dist2
#                    bonds.append(coords[i])
#                    bonds.append(coords[i+1])
#                    bonds.append(coords[i+2])
#
#                    bonds.append(coords[j])
#                    bonds.append(coords[j+1])
#                    bonds.append(coords[j+2])
#    #print bonds
#    return bonds
#
#cpdef C_generate_bonds(list coords):
#    
#    #cdef double bonds[len(coords)]
#    bonds = []
#    cdef int i
#    cdef int j
#    cdef int num_threads
#
#
#
#    for i in range (0, len(coords),3):
#       
#        for j in range (i+3, len(coords),3):    
#            
#            if coords[i] - coords[j] >= 2.0  or coords[i+1] - coords[j+1] >= 2.0 or coords[i+2] - coords[j+2] >= 2.0:
#                pass
#                #print coords[i], coords[j]
#            
#            
#            else:
#                dist =  [coords[i]  - coords[j]  ,
#                        coords[i+1] - coords[j+1],
#                        coords[i+2] - coords[j+2]]
#                #print dist
#                dist2 = dist[0]**2 + dist[1]**2 + dist[2]**2
#
#                if dist2 <= 2.89:
#                    #print coords[i], coords[i+1], coords[i+2] ,coords[j] , coords[j+1], coords[j+2], dist2
#                    bonds.append(coords[i])
#                    bonds.append(coords[i+1])
#                    bonds.append(coords[i+2])
#
#                    bonds.append(coords[j])
#                    bonds.append(coords[j+1])
#                    bonds.append(coords[j+2])
#    #print bonds
#    return bonds
#
'''


cpdef C_generate_bonds3(atoms):
    
    #cdef double bonds[len(coords)]
    bonds       = []
    index_bonds = []
    arr1  = np.array([0,0,1])
    cdef int i
    cdef int j
    cdef int num_threads

    size =  len(atoms)
    
    if size >= 20:
        limit = 20
    else: 
        limit = size

    for i in range (0, size):
        
        if i + limit <= size:
            pass
        else:
            limit = limit-1
        
        for j in range (i+1, i+ limit):    
            if (atoms[i].pos[0] - atoms[j].pos[0] >= 2.0 or 
                atoms[i].pos[1] - atoms[j].pos[1] >= 2.0 or 
                atoms[i].pos[2] - atoms[j].pos[2] >= 2.0):
                pass
            
            else:
                v_dist =  [atoms[i].pos[0] - atoms[j].pos[0],
                           atoms[i].pos[1] - atoms[j].pos[1],
                           atoms[i].pos[2] - atoms[j].pos[2]]
                
                dist2 = v_dist[0]**2 + v_dist[1]**2 + v_dist[2]**2

                
                
                if dist2 <= ((atoms[i].cov_rad + atoms[j].cov_rad)**2) *1.1:
                #if dist2 <= 2.89:
                    
                    distance = dist2**0.5
                    midpoint = [(atoms[i].pos[0] + atoms[j].pos[0])/2.0,
                                (atoms[i].pos[1] + atoms[j].pos[1])/2.0,
                                (atoms[i].pos[2] + atoms[j].pos[2])/2.0]
                    
                    #arr2  = unit_vector(v_dist)
                    #angle = get_angle(arr1, arr2)
                    #vec_o = np.cross(arr1, arr2)
                    
                    angle = 0
                    vec_o = 0
                    
                    #index_bonds.append([i, j])
                    
                    bonds.append((atoms[i], distance , angle    , vec_o, midpoint))
                    bonds.append((atoms[j], distance , angle+180, vec_o, midpoint))

                    
                    #bonds.append(atoms[i].pos[0])
                    #bonds.append(atoms[i].pos[1])
                    #bonds.append(atoms[i].pos[2])
                    #
                    #bonds.append((atoms[i].pos[0] + atoms[j].pos[0])/2)
                    #bonds.append((atoms[i].pos[1] + atoms[j].pos[1])/2)
                    #bonds.append((atoms[i].pos[2] + atoms[j].pos[2])/2)
                    #
                    #
                    #bonds.append(atoms[j].pos[0])
                    #bonds.append(atoms[j].pos[1])
                    #bonds.append(atoms[j].pos[2])
                
                else:
                    pass
    #return #bonds#, index_bonds
    #print index_bonds
    return bonds
    #return index_bonds



def get_angle(vecA, vecB):
    """ Return the angle in degrees of two vectors.
    """
    vecA_u = unit_vector(vecA)
    vecB_u = unit_vector(vecB)
    return np.degrees(np.arccos(np.clip(np.dot(vecA_u, vecB_u), -1.0, 1.0)))

def unit_vector(vector):
    """ Returns the unit vector of the vector.
    """
    return vector / np.linalg.norm(vector)














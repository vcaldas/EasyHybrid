#from cython.parallel import parallel, prange
#cimport openmp
#from libc.stdlib cimport malloc, free
import cython 
#from cython.parallel import prange, parallel
import numpy as np


cpdef C_generate_bonds(atoms, _limit = 50):
    
    bonds       = []
    index_bonds = []
    arr1  = np.array([0,0,1])
    cdef int i
    cdef int j
    cdef int num_threads

    size =  len(atoms)
    
    if size >= _limit:
        limit = _limit
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

                    distance = dist2**0.5
                    midpoint = [(atoms[i].pos[0] + atoms[j].pos[0])/2.0,
                                (atoms[i].pos[1] + atoms[j].pos[1])/2.0,
                                (atoms[i].pos[2] + atoms[j].pos[2])/2.0]
                    
                    angle = 0
                    vec_o = 0
                    
                    index_bonds.append([i, j])
                    atoms[i].connected.append(atoms[j])
                    atoms[j].connected.append(atoms[i])
              
                else:
                    pass

    return index_bonds




cpdef generate_bond (item ):
    frame          = item[0]
    index_bonds    = item[1]
    show_hide_list = item[2]
    frame_bonds    = [] 

    for bond in index_bonds:
        
        if show_hide_list[bond[0]] and show_hide_list[bond[1]]:
            
            x1 = frame[(bond[0]*3)    ]
            y1 = frame[(bond[0]*3 + 1)]
            z1 = frame[(bond[0]*3 + 2)]
            x2 = frame[(bond[1]*3)    ]
            y2 = frame[(bond[1]*3 + 1)]
            z2 = frame[(bond[1]*3 + 2)]
            
            xm = (x1 + x2)/2.0
            ym = (y1 + y2)/2.0
            zm = (z1 + z2)/2.0
            
            frame_bonds.append(x1)
            frame_bonds.append(y1)
            frame_bonds.append(z1)
            
            frame_bonds.append(xm)
            frame_bonds.append(ym)
            frame_bonds.append(zm)
            
            frame_bonds.append(xm)
            frame_bonds.append(ym)
            frame_bonds.append(zm)
            
            frame_bonds.append(x2)
            frame_bonds.append(y2)
            frame_bonds.append(z2)

    frame_bonds = np.array(frame_bonds, dtype=np.float32)
    return frame_bonds





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














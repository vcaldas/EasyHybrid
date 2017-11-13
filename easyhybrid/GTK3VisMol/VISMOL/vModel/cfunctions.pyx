#from cython.parallel import parallel, prange
#cimport openmp
#from libc.stdlib cimport malloc, free
#import cython 
#from cython.parallel import prange, parallel
import numpy as np
#from cython.parallel import parallel, prange



def calculate_distance(atom_i, atoms):
    
    """ Function doc 
    if dist2 <= ((atoms[i].cov_rad + atoms[j].cov_rad)**2) *1.1:
    """
    cdef double dX
    cdef double dY
    cdef double dZ
    
    cdef double atom_ix   = atom_i.pos[0]
    cdef double atom_iy   = atom_i.pos[1]
    cdef double atom_iz   = atom_i.pos[2]
    cdef double cov_rad_i = atom_i.cov_rad
    cdef double cov_rad_j , cov_rad_ij_sqrt
    cdef double r_ij  
    indexes = []
    
    for atom_j in atoms:
        dX              = (atom_ix - atom_j.pos[0])**2
        dY              = (atom_iy - atom_j.pos[1])**2
        dZ              = (atom_iz - atom_j.pos[2])**2
        cov_rad_j       = atom_j.cov_rad
        cov_rad_ij_sqrt = ((cov_rad_i + cov_rad_j)**2)*1.5

        if (dX**2 > cov_rad_ij_sqrt or 
            dY**2 > cov_rad_ij_sqrt or 
            dZ**2 > cov_rad_ij_sqrt):
            pass
        else:
            r_ij = (dX**2 + dY**2 + dZ**2)
            if r_ij <= cov_rad_ij_sqrt:  
                
                j_index = atom_j.index-1
                i_index = atom_i.index-1
                
                atom_i.connected.append(j_index)
                atom_j.connected.append(i_index)
                indexes.append([i_index, j_index])
    
    return indexes
    
'''
cpdef C_generate_bonds_between_sectors(sector_atoms_1 = None, sector_atoms_2 = None):
    
    bonds        = []
    index_bonds  = []
    index_bonds2 = []

    arr1  = np.array([0,0,1])
    cdef int i
    cdef int j
    
    for atom1 in sector_atoms_1:
        for atom2 in sector_atoms_2:
            #print ('aqui!!!!', atom1.index ,atom2.index )
            if (atom1.pos[0] - atom2.pos[0] >= 2.0 or 
                atom1.pos[1] - atom2.pos[1] >= 2.0 or 
                atom1.pos[2] - atom2.pos[2] >= 2.0):
                pass
            
            else:
                v_dist =  [atom1.pos[0] - atom2.pos[0],
                           atom1.pos[1] - atom2.pos[1],
                           atom1.pos[2] - atom2.pos[2]]
                
                dist2 = v_dist[0]**2 + v_dist[1]**2 + v_dist[2]**2

                if dist2 <= ((atom1.cov_rad + atom2.cov_rad)**2) *1.1:
                    angle = 0
                    vec_o = 0
                    
                    index_bonds2.append([atom1.index -1, atom2.index -1])
                    index_bonds. append( atom1.index -1    )
                    index_bonds. append( atom2.index -1    )


                    atom1.connected.append(atom2)
                    atom2.connected.append(atom1)
              
                else:
                    pass
    return index_bonds, index_bonds2
#'''



'''
cpdef C_generate_bonds(atoms, _limit = 50):
    bonds        = []
    index_bonds  = []
    index_bonds2 = []

    #arr1  = np.array([0,0,1])
    cdef int i
    cdef int j
    #cdef int num_threads

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
                    
                    index_bonds2.append([atoms[i].index -1 , atoms[j].index - 1])
                    index_bonds .append( atoms[i].index -1 )
                    index_bonds .append( atoms[j].index -1 )
                    
                    atoms[i].connected.append(atoms[j])
                    atoms[j].connected.append(atoms[i])
              
                else:
                    pass

    return index_bonds, index_bonds2

#'''

#'''
cpdef C_generate_bonds(atoms):
    #bonds        = []
    #index_bonds  = []
    index_bonds2 = []

    cdef int i
    cdef int j
    cdef int size
    
    cdef double atom_ix
    cdef double atom_iy
    cdef double atom_iz
    cdef double cov_rad_i, cov_rad_j
    
    
    size =  len(atoms)
    
    for i in range (0, size-1):
        
        atom_ix   = atoms[i].pos[0]
        atom_iy   = atoms[i].pos[1]    
        atom_iz   = atoms[i].pos[2]
        cov_rad_i = atoms[i].cov_rad
        index_i   = atoms[i].index-1
        
        for j in range (i+1, size):    
            
            dX              = (atom_ix - atoms[j].pos[0])**2
            dY              = (atom_iy - atoms[j].pos[1])**2
            dZ              = (atom_iz - atoms[j].pos[2])**2
            
            cov_rad_j       = atoms[j].cov_rad
            cov_rad_ij_sqrt = ((cov_rad_i + cov_rad_j)**2)*1.2
            
            
            if (dX > cov_rad_ij_sqrt or 
                dY > cov_rad_ij_sqrt or 
                dZ > cov_rad_ij_sqrt):
                pass

            else:
                r_ij = (dX + dY + dZ)
                if r_ij <= cov_rad_ij_sqrt:
                    index_bonds2.append([index_i , atoms[j].index - 1])
                    #index_bonds .append( index_i           )
                    #index_bonds .append( atoms[j].index -1 )
                    atoms[i].connected.append(atoms[j])
                    atoms[j].connected.append(atoms[i])
                else:
                    pass

    return index_bonds2#, index_bonds

#'''

cpdef C_generate_bonds_between_sectors(atoms1, atoms2):
    #bonds        = []
    #index_bonds  = []
    index_bonds2 = []

    cdef int i
    cdef int j
    cdef int size1, size2
    
    cdef double atom_ix
    cdef double atom_iy
    cdef double atom_iz
    cdef double cov_rad_i, cov_rad_j
    
    
    size1 =  len(atoms1)
    size2 =  len(atoms2)

    for i in range (0, size1):
        
        atom_ix   = atoms1[i].pos[0]
        atom_iy   = atoms1[i].pos[1]    
        atom_iz   = atoms1[i].pos[2]
        cov_rad_i = atoms1[i].cov_rad
        index_i   = atoms1[i].index-1
        
        for j in range (0, size2):    
            
            dX              = (atom_ix - atoms2[j].pos[0])**2
            dY              = (atom_iy - atoms2[j].pos[1])**2
            dZ              = (atom_iz - atoms2[j].pos[2])**2
            
            cov_rad_j       = atoms2[j].cov_rad
            cov_rad_ij_sqrt = ((cov_rad_i + cov_rad_j)**2)*1.2
            
            
            if (dX > cov_rad_ij_sqrt or 
                dY > cov_rad_ij_sqrt or 
                dZ > cov_rad_ij_sqrt):
                pass

            else:
                r_ij = (dX + dY + dZ)
                if r_ij <= cov_rad_ij_sqrt:
                    index_bonds2.append([index_i , atoms2[j].index - 1])
                    #index_bonds .append( index_i           )
                    #index_bonds .append( atoms[j].index -1 )
                    atoms1[i].connected.append(atoms2[j])
                    atoms2[j].connected.append(atoms1[i])
                else:
                    pass

    return index_bonds2#, index_bonds





#'''
cpdef C_generate_bonds2(atoms):
    #bonds        = []
    #index_bonds  = []
    index_bonds2 = []

    cdef int i
    cdef int j
    cdef int size
    cdef int index_i

    cdef double atom_ix
    cdef double atom_iy
    cdef double atom_iz
    cdef double cov_rad_i, cov_rad_j
    
    cdef double r_ij
    cdef double dX
    cdef double dY
    cdef double dZ

    size =  len(atoms)
    
    for i in range (0, size-1):
        atom_ix   = atoms[i][3][0]
        atom_iy   = atoms[i][3][1]    
        atom_iz   = atoms[i][3][2]
        cov_rad_i = atoms[i][2]
        index_i   = atoms[i][0]
        
        for j in range (i+1, size):    
            
            dX              = (atom_ix - atoms[j][3][0])**2
            dY              = (atom_iy - atoms[j][3][1])**2
            dZ              = (atom_iz - atoms[j][3][2])**2
            
            cov_rad_j       = atoms[j][2]
            cov_rad_ij_sqrt = ((cov_rad_i + cov_rad_j)**2)*1.4
            
            
            if (dX > cov_rad_ij_sqrt or 
                dY > cov_rad_ij_sqrt or 
                dZ > cov_rad_ij_sqrt):
                pass

            else:
                r_ij = (dX + dY + dZ)
                if r_ij <= cov_rad_ij_sqrt:
                    index_bonds2.append([index_i , atoms[j][0]])
                    #index_bonds .append( index_i           )
                    #index_bonds .append( atoms[j].index -1 )
                    #atoms[i].connected.append(atoms[j])
                    #atoms[j].connected.append(atoms[i])
                else:
                    pass

    return index_bonds2#, index_bonds

#'''
cpdef C_generate_bonds_between_sectors2(atoms1, atoms2):

    index_bonds2 = []

    cdef int i
    cdef int j
    cdef int size1, size2
    cdef int index_i
    cdef double atom_ix
    cdef double atom_iy
    cdef double atom_iz
    cdef double cov_rad_i, cov_rad_j
    cdef double r_ij
    cdef double dX
    cdef double dY
    cdef double dZ
    
    
    size1 =  len(atoms1)
    size2 =  len(atoms2)

    for i in range (0, size1):   
        atom_ix   = atoms1[i][3][0]
        atom_iy   = atoms1[i][3][1]    
        atom_iz   = atoms1[i][3][2]
        cov_rad_i = atoms1[i][2]
        index_i   = atoms1[i][0]

        for j in range (0, size2):    

            dX              = (atom_ix - atoms2[j][3][0])**2
            dY              = (atom_iy - atoms2[j][3][1])**2
            dZ              = (atom_iz - atoms2[j][3][2])**2

            cov_rad_j       = atoms2[j][2]
            cov_rad_ij_sqrt = ((cov_rad_i + cov_rad_j)**2)*1.4
            
            if (dX > cov_rad_ij_sqrt or 
                dY > cov_rad_ij_sqrt or 
                dZ > cov_rad_ij_sqrt):
                pass

            else:
                
                r_ij = (dX + dY + dZ)
                
                if r_ij <= cov_rad_ij_sqrt:
                    index_bonds2.append([index_i , atoms2[j][0]])
                    
                    #index_bonds .append( index_i           )
                    #index_bonds .append( atoms[j].index -1 )
                    #atoms1[i].connected.append(atoms2[j])
                    #atoms2[j].connected.append(atoms1[i])
                else:
                    pass

    return index_bonds2#, index_bonds

'''
cpdef pairwise_grid_elements(atomic_grid):
    
    pair_of_sectors2 = []
    done             = []
    #-----------------------------------------------------------------
    grid_offset =  [
                   [ 1, 1, 1], # top level
                   [ 0, 1, 1], # top level
                   [-1, 1, 1], # top level
                   [-1, 0, 1], # top level
                   [ 0, 0, 1], # top level
                   [ 1, 0, 1], # top level
                   [-1,-1, 1], # top level
                   [ 0,-1, 1], # top level
                   [ 1,-1, 1], # top level
                   
                   #-------------------------
                   [ 1, 1, 0], # middle level 
                   [ 0, 1, 0], # middle level 
                   [-1, 0, 0], # middle level 
                   [-1, 1, 0], # middle level 
                  #[ 0, 0, 0], # middle level 
                   [ 1, 0, 0], # middle level 
                   [-1,-1, 0], # middle level 
                   [ 0,-1, 0], # middle level 
                   [ 1,-1, 0], # middle level 
                   #-------------------------
                   
                   [ 1, 1,-1], # ground level
                   [ 0, 1,-1], # ground level
                   [-1, 1,-1], # ground level
                   [-1, 0,-1], # ground level
                   [ 0, 0,-1], # ground level
                   [ 1, 0,-1], # ground level
                   [-1,-1,-1], # ground level
                   [ 0,-1,-1], # ground level
                   [ 1,-1,-1], # ground level
                   ]
    #-----------------------------------------------------------------

    for element in atomic_grid.keys():

        for offset_element in grid_offset:              

            element1  = (element[0]                  , element[1]                  , element[2]                  ) 
            element2  = (element[0]+offset_element[0], element[1]+offset_element[1], element[2]+offset_element[2]) 
            
            if [element1, element2] in done or [element2, element1] in done:
                pass                
            
            else: 
                if element2 in atomic_grid:                        
                    done.append([element1,
                                 element2])
                                                     
                    #pair_of_sectors2.append([atomic_grid[element1],
                    #                         atomic_grid[element2]])
    
    return pair_of_sectors2
'''






'''
cpdef C_generate_bonds2(atoms):
    bonds        = []
    index_bonds  = []
    index_bonds2 = []

    cdef int i
    cdef int j

    size =  len(atoms)
    for i in range (0, size-1):
        for j in range (i+1, size):    
            
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
                   
                    index_bonds2.append([atoms[i].index -1 , atoms[j].index - 1])
                    index_bonds .append( atoms[i].index -1 )
                    index_bonds .append( atoms[j].index -1 )

                    atoms[i].connected.append(atoms[j])
                    atoms[j].connected.append(atoms[i])
              
                else:
                    pass

    return index_bonds, index_bonds2








cpdef C_generate_bonds_by_sector(sector_atoms_1 = None, sector_atoms_2 = None):
    
    bonds       = []
    index_bonds = []
    index_bonds2 = []

    arr1  = np.array([0,0,1])
    cdef int i
    cdef int j
    cdef int num_threads
    
    if sector_atoms_2 is None:
        size =  len(sector_atoms_1)
        for i in range (0, size):    
            for j in range (i+1, size):    
                if (sector_atoms_1[i].pos[0] - sector_atoms_1[j].pos[0] >= 2.0 or 
                    sector_atoms_1[i].pos[1] - sector_atoms_1[j].pos[1] >= 2.0 or 
                    sector_atoms_1[i].pos[2] - sector_atoms_1[j].pos[2] >= 2.0):
                    pass
                
                else:
                    v_dist =  [sector_atoms_1[i].pos[0] - sector_atoms_1[j].pos[0],
                               sector_atoms_1[i].pos[1] - sector_atoms_1[j].pos[1],
                               sector_atoms_1[i].pos[2] - sector_atoms_1[j].pos[2]]
                    
                    dist2 = v_dist[0]**2 + v_dist[1]**2 + v_dist[2]**2

                    
                    
                    if dist2 <= ((sector_atoms_1[i].cov_rad + sector_atoms_1[j].cov_rad)**2) *1.1:

                        distance = dist2**0.5
                        midpoint = [(sector_atoms_1[i].pos[0] + sector_atoms_1[j].pos[0])/2.0,
                                    (sector_atoms_1[i].pos[1] + sector_atoms_1[j].pos[1])/2.0,
                                    (sector_atoms_1[i].pos[2] + sector_atoms_1[j].pos[2])/2.0]
                        
                        angle = 0
                        vec_o = 0
                        
                        #index_bonds2.append([i, j])
                        #index_bonds. append( i    )
                        #index_bonds. append( j    )
                        
                        index_bonds2.append([sector_atoms_1[i].index -1, sector_atoms_1[j].index -1])
                        index_bonds. append( sector_atoms_1[i].index -1    )
                        index_bonds. append( sector_atoms_1[j].index -1    )


                        sector_atoms_1[i].connected.append(sector_atoms_1[j])
                        sector_atoms_1[j].connected.append(sector_atoms_1[i])
                  
                    else:
                        pass

        return index_bonds, index_bonds2
    
    
    
    else:
        for atom1 in sector_atoms_1:
            for atom2 in sector_atoms_2:
                print ('aqui!!!!', atom1.index ,atom2.index )
                if (atom1.pos[0] - atom2.pos[0] >= 2.0 or 
                    atom1.pos[1] - atom2.pos[1] >= 2.0 or 
                    atom1.pos[2] - atom2.pos[2] >= 2.0):
                    pass
                
                else:
                    v_dist =  [atom1.pos[0] - atom2.pos[0],
                               atom1.pos[1] - atom2.pos[1],
                               atom1.pos[2] - atom2.pos[2]]
                    
                    dist2 = v_dist[0]**2 + v_dist[1]**2 + v_dist[2]**2

                    
                    
                    if dist2 <= ((atom1.cov_rad + atom2.cov_rad)**2) *1.1:

                        #distance = dist2**0.5
                        #midpoint = [(atom1.pos[0] + atom2.pos[0])/2.0,
                        #            (atom1.pos[1] + atom2.pos[1])/2.0,
                        #            (atom1.pos[2] + atom2.pos[2])/2.0]
                        #
                        angle = 0
                        vec_o = 0
                        
                        #index_bonds2.append([i, j])
                        #index_bonds. append( i    )
                        #index_bonds. append( j    )
                        
                        index_bonds2.append([atom1.index -1, atom2.index -1])
                        index_bonds. append( atom1.index -1    )
                        index_bonds. append( atom2.index -1    )


                        atom1.connected.append(atom2)
                        atom2.connected.append(atom1)
                  
                    else:
                        pass
        return index_bonds, index_bonds2


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



'''




'''
def calculate_distance(atom_i, atoms):
    
    """ Function doc     
    if dist2 <= ((atoms[i].cov_rad + atoms[j].cov_rad)**2) *1.1:
    """
    #bond_pairs = []
    cdef double dX
    cdef double dY
    cdef double dZ
    cdef double dist
    
    cdef double atom_ix   = atom_i.pos[0]
    cdef double atom_iy   = atom_i.pos[1]
    cdef double atom_iz   = atom_i.pos[2]
    cdef double cov_rad_i = atom_i.cov_rad
    cdef double cov_rad_j
    cdef double R_ij2  
    
    cdef int    atom_i_index = atom_i.index
    cdef int    atom_j_index

    for atom_j in atoms:
        
        dX        = atom_ix - atom_j.pos[0]
        dY        = atom_iy - atom_j.pos[1]
        dZ        = atom_iz - atom_j.pos[2]
        cov_rad_j = atom_j.cov_rad
        
        R_ij2 = (cov_rad_i + cov_rad_j)**2
        
        if (dX**2 > R_ij2 or 
            dY**2 > R_ij2 or 
            dZ**2 > R_ij2):
            pass
        
        else:
            dist = (dX**2 + dY**2 + dZ**2)
            if dist <= R_ij2:  
                atom_j_index = atom_j.index
                atom_i.connected.append(atom_j_index)
                atom_j.connected.append(atom_i_index)
                
                #bond_pairs.append(atom_i_index)
                #bond_pairs.append(atom_j_index)

    #print (bond_pairs)
    #return bond_pairs

#'''







'''
cpdef calculate_distances_from_atom_to_atoms(atom_i, atoms):
    cdef double dX
    cdef double dY
    cdef double dZ
    cdef double r_ij
    cdef int I, J
    cdef int i, j
    cdef double atom_ix   = atom_i[3][0]
    cdef double atom_iy   = atom_i[3][1]
    cdef double atom_iz   = atom_i[3][2]
    cdef double cov_rad_i = atom_i[2]
    cdef double cov_rad_j
    cdef double r_ij2  
    
    cdef int    atom_i_index = atom_i[0]
    cdef int    atom_j_index
    
    
    #with nogil, parallel(num_threads=8):
    
    indexes = []
    J       = len(atoms)
    with nogil, parallel(num_threads=8):
        for j in prange(J-1, schedule='dynamic'):
        
        #for atom_j in atoms:
        
            if atoms[j] == atom_i:
                pass 
            
            else:
                dX        = (atom_ix - atoms[j][3][0])**2
                dY        = (atom_iy - atoms[j][3][1])**2
                dZ        = (atom_iz - atoms[j][3][2])**2
                
                cov_rad_j = atoms[j][2]
                
                cov_rad_ij_sqrt = ((cov_rad_i + cov_rad_j)**2)*1.5
                
                if (dX > cov_rad_ij_sqrt or 
                    dY > cov_rad_ij_sqrt or 
                    dZ > cov_rad_ij_sqrt ):
                    pass
                
                else:
                    r_ij = (dX + dY + dZ)
                    if r_ij <= cov_rad_ij_sqrt:  
                        pass
                        #atom_j_index = atoms[j][0]
                        #indexes.append(atom_i_index)
                        #indexes.append(atom_j_index)
                        #atom_j_index = atom_j.index
                        #atom_i.connected.append(atom_j_index)
                        #atom_j.connected.append(atom_i_index)
    
    return indexes
'''



'''
cpdef calculate_distances_offset(atoms):
    bonds        = []
    index_bonds  = []
    index_bonds2 = []
    cdef int i
    cdef int j
    cdef int num_threads
    cdef int size
    
    size =  len(atoms)

    for i in range (0, size-1):       
        indexes = calculate_distances_from_atom_to_atoms(atoms[i], atoms[i+1:])
        index_bonds.append(indexes)

    return index_bonds
'''

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  VismolObject.py
#  
#  Copyright 2017 
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import numpy as np
import time
import os
import multiprocessing as mp

from multiprocessing import Pool



#import VISMOL.Model.cfunctions as cfunctions
#import VISMOL.Model.Chain as Chain
from VISMOL.vModel.Chain      import Chain
from VISMOL.vModel.Residue    import Residue
from VISMOL.vModel.cfunctions import C_generate_bonds, C_generate_bonds2, C_generate_bonds_between_sectors
#from VISMOL.glCore.VismolRepresentations import LineRepresetation

#----------------------------------------------------
from scipy.spatial import distance
#import scipy as scipy
#----------------------------------------------------

#import VISMOL.Model as model



class VismolObject:
    """ Class doc """
    
    def __init__ (self, 
                  name       = 'UNK', 
                  atoms      = [],
                  EMSession  = None, 
                  trajectory = None):
        
        """ Class initialiser """
        self.vismol_session = EMSession
        self.actived            = False
        self.editing            = False
        self.Type               = 'molecule'
        self.name               = name#self._get_name(name)

        # ------------- PDB size and cell ------------- 
        
        self.cell_max_x = None
        self.cell_max_y = None
        self.cell_max_z = None
        self.cell_min_x = None
        self.cell_min_y = None
        self.cell_min_z = None

        self.sector_size = 10 # (A) angtrons 
        self.sectors = {
                       # (0,0,0) : [atom1, atom2, ...] 
                       }
        #self.number_of_sectors = 0
        # ---------------------------------------------- 

        
        self.atoms              = atoms
        self.residues           = []
        self.chains             = {}
                                
        self.bonds              = []
        self.frames             = trajectory
        self.mass_center        = np.array([0.0, 0.0, 0.0])

        self.atom_unique_id_dic = {}
        self.index_bonds        = []
        self.index_bonds_rep    = []
        self.non_bonded_atoms   = None
		
		
        self._generate_chain_structure()
        self._generate_atom_unique_color_id()
        self._generate_bonds()
        self._generate_non_bonded_list()
        
        #self._generate_colors()
        
        """   L I N E S   """
        self.lines_actived       = True
        self.lines_show_list     = True
        #self.line_representation = LineRepresetation (visObj = self)
        
        
        #self.line_representation = LineRepresentation(self)
        #self.line_representation.update()

        """   D O T S   """
        self.dots_actived = False

        """   C I R C L E S   """
        self.circles_actived = False

        #self.flat_sphere_representation = FlatSphereRepresentation(self)
        
        '''
        self.dot_vao       = None
        self.dot_ind_vbo   = None
        self.dot_coord_vbo = None
        self.dot_col_vbo   = None
        '''

        print ('frames:     ', len(self.frames))
        print ('frame size: ', len(self.frames[0]))
        
        
        
        
        
        
        
        
        # OpenGL attributes
        self.dots_vao        = None
        self.lines_vao       = None
        self.circles_vao     = None
        self.dot_buffers     = None
        self.line_buffers    = None
        self.circles_buffers = None
        self.dot_indexes     = None
        
        self.selection_dots_vao      = None
        self.selection_dot_buffers   = None
        
        self.model_mat = np.identity(4, dtype=np.float32)
        self.trans_mat = np.identity(4, dtype=np.float32)
        self.target    = None
        self.unit_vec  = None
        self.distance  = None
        self.step      = None

        self.picking_dots_vao      = None
        self.picking_dot_buffers   = None

    def generate_dot_indexes(self):
        """ Function doc
        """
        self.dot_indexes = []
        for i in range(int(len(self.atoms))):
            self.dot_indexes.append(i)
        self.dot_indexes = np.array(self.dot_indexes, dtype=np.uint32)
    
    def _generate_chain_structure (self):
        """ Function doc """
        print ('\ngenerate_chain_structure starting')
        initial          = time.time()
        
        parser_resi  = None
        parser_resn  = None
        chains_m     = {}
        
        
        xyz_coords = []
        x_coords   = []
        y_coords   = []
        z_coords   = []
        
        sum_x   = 0
        sum_y   = 0
        sum_z   = 0
        frame   = []
        
        index   = 1
        
        for atom in self.atoms:
        
            #self.atoms[self.atoms.index(atom)].index   = index
            #self.atoms[self.atoms.index(atom)].atom_id = counter
            #print  (self.atoms[self.atoms.index(atom)].atom_id)
            atom.index   = index
            atom.atom_id = self.vismol_session.atom_id_counter
            atom.Vobject =  self
            if atom.chain in self.chains.keys():
                ch = self.chains[atom.chain]
                #print 'existe'
            
            else:
                ch = Chain(name = atom.chain, label = 'UNK')
                self.chains[atom.chain] = ch
                #print 'n existe'

            if atom.resi == parser_resi:# and at_res_n == parser_resn:
                atom.residue = ch.residues[-1]
                ch.residues[-1].atoms.append(atom)
                frame.append([atom.pos[0],atom.pos[1],atom.pos[2]])

            else:
                residue = Residue(name=atom.resn, index=atom.resi, chain=atom.chain)
                atom.residue     = residue
                residue.atoms.append(atom)
                
                ch.residues.append(residue)
                frame.append([atom.pos[0],atom.pos[1],atom.pos[2]])
                parser_resi  = atom.resi
                parser_resn  = atom.resn


            if atom.name == 'CA':
                ch.backbone.append(atom)

            self.vismol_session.atom_dic_id[self.vismol_session.atom_id_counter] = atom
            
            x_coords.append(atom.pos[0])
            y_coords.append(atom.pos[1])
            z_coords.append(atom.pos[2])
            
            xyz_coords.append(
                               (atom.pos[0],
                                atom.pos[1],
                                atom.pos[2])
                              )
            
            
            sum_x += atom.pos[0]
            sum_y += atom.pos[1]
            sum_z += atom.pos[2]
            index   +=1
            self.vismol_session.atom_id_counter +=1
        
        '''
        #-------------------------------------------------------------------------
        #print (xyz_coords)
        initial = time.time() 
        print ('generate_bonds euclidean')
        distances  = distance.cdist(xyz_coords, xyz_coords, 'euclidean')
        final = time.time() 
        print ('generate_bonds euclidean -  total time: ', final - initial, '\n')
        #-------------------------------------------------------------------------
        '''
        #print (distances[0])
        
        #-----------------------------------------------------------------
        self.cell_max_x = max(x_coords)   
        self.cell_max_y = max(y_coords)   
        self.cell_max_z = max(z_coords)   
        self.cell_min_x = min(x_coords)  
        self.cell_min_y = min(y_coords)  
        self.cell_min_z = min(z_coords)  
        
        nx_windows = int((self.cell_max_x - self.cell_min_x)/ self.sector_size) +1 
        ny_windows = int((self.cell_max_y - self.cell_min_y)/ self.sector_size) +1 
        nz_windows = int((self.cell_max_z - self.cell_min_z)/ self.sector_size) +1 

        for i in range(0, nx_windows):
            for j in range(0, ny_windows):
                for k in range(0, nz_windows):
                    self.sectors[(i,j,k)] = []
        
        print ('- - - - - - Sectors - - - - - - ')
        print ('Sectors size = ', self.sector_size)
        print ('cell_max_x =', self.cell_max_x )   
        print ('cell_max_y =', self.cell_max_y )   
        print ('cell_max_z =', self.cell_max_z )   
        print ('cell_min_x =', self.cell_min_x )  
        print ('cell_min_y =', self.cell_min_y )  
        print ('cell_min_z =', self.cell_min_z )  
        print ('nx_windows = ', nx_windows)
        print ('ny_windows = ', ny_windows)
        print ('nz_windows = ', nz_windows)
        print ('Number of sectors = ', len(self.sectors))


        for atom in self.atoms:
            a = int((atom.pos[0]  - self.cell_min_x) / self.sector_size)
            b = int((atom.pos[1]  - self.cell_min_y) / self.sector_size)
            c = int((atom.pos[2]  - self.cell_min_z) / self.sector_size)
            self.sectors[(a,b,c)].append(atom)
        #-----------------------------------------------------------------

        #self.frames.append(frame)
        total = len(self.atoms)
        self.list_atom_lines          = [True ]*total
        self.list_atom_ribbons        = [False]*total
        self.list_atom_dots           = [False]*total
        self.list_atom_sticks         = [False]*total
        self.list_atom_spheres        = [False]*total
        self.list_atom_surface        = [False]*total
        self.list_atom_ball_and_stick = [False]*total
        self.mass_center[0] = sum_x / total
        self.mass_center[1] = sum_y / total
        self.mass_center[2] = sum_z / total
        final = time.time() 
        print ('generate_chain_structure end -  total time: ', final - initial, '\n')
        return True

    def _get_name (self, name):
        """ Function doc """
        self.name  = os.path.basename(name)
        #self.name  = name.split('.')
        #self.name  = self.name[0]
    
    def _generate_bonds (self):
        """ Function doc """
        
        
        '''
        #print ('\ngenerate_bonds starting')
        initial          = time.time()
        #self.index_bonds        = []
        #self.index_bonds_pairs  = []
        self.index_bonds, self.index_bonds_pairs = C_generate_bonds(self.atoms)
        final = time.time() 
        print ('generate_bonds I end -  total time: ', final - initial, '\n')
        #'''
        #--------------------------------------------------------------------------------
        #'''
        
        sectors_arrond = [
                         [ 1, 1, 1], # level above
                         [ 0, 1, 1], # level above
                         [-1, 1, 1], # level above
                                     # level above
                         [-1, 0, 1], # level above
                         [ 0, 0, 1], # level above
                         [ 1, 0, 1], # level above
                                     # level above
                         [-1,-1, 1], # level above
                         [ 0,-1, 1], # level above
                         [ 1,-1, 1], # level above

                         #-------------------------
                         [ 1, 1, 0], # level ground
                         [ 0, 1, 0], # level ground
                         [-1, 0, 0], # level ground
                         [-1, 1, 0], # level ground

                        #[ 0, 0, 0], # level ground
                        
                         [ 1, 0, 0], # level ground
                         [-1,-1, 0], # level ground
                         [ 0,-1, 0], # level ground
                         [ 1,-1, 0], # level ground
                         #-------------------------
                         
                         [ 1, 1,-1], # level behind
                         [ 0, 1,-1], # level behind
                         [-1, 1,-1], # level behind
                         [-1, 0,-1], # level behind
                         [ 0, 0,-1], # level behind
                         [ 1, 0,-1], # level behind
                         [-1,-1,-1], # level behind
                         [ 0,-1,-1], # level behind
                         [ 1,-1,-1], # level behind

                         ]
        
        
        
        print ('\ngenerate_bonds  euclidian per sector starting')
        initial          = time.time()
        #self.compute_distances(self.atoms)
        for key in self.sectors:
            self.compute_distances(self.sectors[key])
        final = time.time() 
        print ('generate_bonds  euclidian per sector finished -  total time: ', final - initial, '\n')
        #index_bonds2 = []
        initial          = time.time()
        
        
        for key in self.sectors:
            distances = None
            for sector in sectors_arrond:
                if (key[0]+sector[0], 
                    key[1]+sector[1], 
                    key[2]+sector[2]) in self.sectors:
                        
                    self.compute_distances_between_sectors (self.sectors[key]   , 
                                                            self.sectors[(key[0]+sector[0],
                                                                          key[1]+sector[1],
                                                                          key[2]+sector[2])])
         
         
         
         
         
            
            ##  1 1 1
            #if (key[0]+1, key[1]+1, key[2]+1) in self.sectors:
            #    self.compute_distances_between_sectors (self.sectors[key]   , 
            #                                            self.sectors[(key[0]+1,key[1]+1,key[2]+1)])
            ##  0 1 1
            #if (key[0],key[1]+1,key[2]+1) in self.sectors:
            #    self.compute_distances_between_sectors (self.sectors[key]   , 
            #                                            self.sectors[(key[0],key[1]+1,key[2]+1)])
            ##  0 0 1
            #if (key[0],key[1],key[2]+1) in self.sectors:
            #    self.compute_distances_between_sectors (self.sectors[key]   , 
            #                                            self.sectors[(key[0],key[1],key[2]+1)])
            ##  1 0 1
            #if (key[0]+1, key[1], key[2]+1) in self.sectors:
            #    #print (key,(key[0], key[1]+1, key[2]))
            #    self.compute_distances_between_sectors (self.sectors[key]   , 
            #                                            self.sectors[ (key[0]+1 , key[1], key[2]+1) ])
            #
            ##  1 1 0
            #if (key[0]+1,key[1]+1,key[2]) in self.sectors:
            #    self.compute_distances_between_sectors (self.sectors[key]   , 
            #                                            self.sectors[(key[0]+1,key[1]+1,key[2])])
            ##  1 0 0
            #if (key[0]+1,key[1],key[2]) in self.sectors:
            #    self.compute_distances_between_sectors (self.sectors[key]   , 
            #                                            self.sectors[(key[0]+1,key[1],key[2])])
            ##  0 1 0
            #if (key[0],key[1]+1,key[2]) in self.sectors:
            #    self.compute_distances_between_sectors (self.sectors[key]   , 
            #                                            self.sectors[(key[0],key[1]+1,key[2])])
            #
#-----------#----------------------------------------------------------------------------------------------
            #
            ##  -1 -1 -1
            #if (key[0]-1,key[1]-1,key[2]-1) in self.sectors:
            #    self.compute_distances_between_sectors (self.sectors[key]   , 
            #                                            self.sectors[(key[0]-1,key[1]-1,key[2]-1)])
            #
            ##  0 -1 0
            #if (key[0],key[1]-1,key[2]) in self.sectors:
            #    self.compute_distances_between_sectors (self.sectors[key]   , 
            #                                            self.sectors[(key[0],key[1]-1,key[2])])
            #
            #
            ##  -1 0 0
            #if (key[0]-1,key[1],key[2]) in self.sectors:
            #    self.compute_distances_between_sectors (self.sectors[key]   , 
            #                                            self.sectors[(key[0]-1,key[1],key[2])])
            #
            ##  0 0 -1
            #if (key[0],key[1],key[2]-1) in self.sectors: 
            #    self.compute_distances_between_sectors (self.sectors[key]   , 
            #                                            self.sectors[(key[0],key[1],key[2]-1)])
            #
            ##  -1 -1 0
            #if (key[0]-1,key[1]-1,key[2]) in self.sectors:
            #    self.compute_distances_between_sectors (self.sectors[key]   , 
            #                                            self.sectors[(key[0]-1,key[1]-1,key[2])])
            #
            ##  0 -1 -1
            #if (key[0],key[1]-1,key[2]-1) in self.sectors:
            #    self.compute_distances_between_sectors (self.sectors[key]   , 
            #                                            self.sectors[(key[0],key[1]-1,key[2]-1)])
            #
            ##  -1 0 -1
            #if (key[0]-1,key[1],key[2]-1) in self.sectors:
            #    self.compute_distances_between_sectors (self.sectors[key]   , 
            #                                            self.sectors[(key[0]-1,key[1],key[2]-1)])

#---------------------------------------------------------------------------------------------------------
        
        final = time.time()    
        print ('_compute_bonds_scipy  between sectors total time: ', final - initial, '\n')
        #--------------------------------------------------------------------------------
        #'''

    
    
    def _generate_non_bonded_list (self):
        """ Function doc """
        self.non_bonded_atoms   =  []
        for atom in self.atoms:
            if atom.connected != []:
            #if atom.index -1 in self.index_bonds:
                pass
            else:
                self.non_bonded_atoms.append(atom.index -1)
        self.non_bonded_atoms = np.array(self.non_bonded_atoms, dtype=np.uint32)

    def _generate_atom_unique_color_id (self):
        self.color_indexes  = []
        self.colors         = []        
        self.vdw_dot_sizes  = []
        self.cov_dot_sizes  = []
#        self.atom_unique_id_dic     = {}

        """ Function doc """
        for atom in self.atoms:
            #-------------------------------------------------------
            #                     ID Colors
            #-------------------------------------------------------
            i = atom.atom_id
            r = (i & 0x000000FF) >>  0
            g = (i & 0x0000FF00) >>  8
            b = (i & 0x00FF0000) >> 16
           
            self.color_indexes.append(r/255.0)
            self.color_indexes.append(g/255.0)
            self.color_indexes.append(b/255.0)
            
            pickedID = r + g * 256 + b * 256*256
            #print (pickedID)
            self.vismol_session.atom_dic_id[pickedID] = atom
            
            #-------------------------------------------------------
            #                      Colors
            #-------------------------------------------------------
            self.colors.append(atom.color[0])        
            self.colors.append(atom.color[1])        
            self.colors.append(atom.color[2])   

            #-------------------------------------------------------
            #                      VdW list
            #-------------------------------------------------------
            self.vdw_dot_sizes.append(atom.vdw_rad)
            self.cov_dot_sizes.append(atom.cov_rad)

        self.color_indexes = np.array(self.color_indexes, dtype=np.float32)
        self.colors        = np.array(self.colors       , dtype=np.float32)    
        self.vdw_dot_sizes = np.array(self.vdw_dot_sizes, dtype=np.float32)
        self.cov_dot_sizes = np.array(self.cov_dot_sizes, dtype=np.float32)

    def _generate_colors  (self):
        """ Function doc """
        self.colors = []        
        for atom in self.atoms:
            #if atom.dots:
            #-------------------------------------------------------
            #                        D O T S
            #-------------------------------------------------------
            self.colors.append(atom.color[0])        
            self.colors.append(atom.color[1])        
            self.colors.append(atom.color[2])   
            #self.colors.append(atom.color[3])   

        self.colors  = np.array(self.colors, dtype=np.float32)
    
    def set_model_matrix(self, mat):
        """ Function doc
        """
        self.model_mat = np.copy(mat)
        return True
    
    def pos (self, frame = None):
        """ Function doc """

    

    def compute_distances (self, atoms):
        """ Function doc """
        
        xyz_coords = []

        for atom in atoms:
            xyz_coords.append(
                               (atom.pos[0],
                                atom.pos[1],
                                atom.pos[2])
                              )
        if xyz_coords == []:
            pass
        else:
            distances  = distance.cdist(xyz_coords, xyz_coords, 'euclidean')
            
            for i in range(0, len(xyz_coords)):
                 
                for j in range(i+1, len(xyz_coords)):
                    
                    if distances[i][j] <= ((atoms[i].cov_rad + atoms[j].cov_rad)*1.5):
                        #self.index_bonds2.append([atom1.index -1, atom2.index -1])
                        self.index_bonds. append( atoms[i].index -1    )
                        self.index_bonds. append( atoms[j].index -1    )
                        atoms[i].connected.append(atoms[j])
                        atoms[j].connected.append(atoms[i])


    def compute_distances_between_sectors (self, atoms1, atoms2):
        """ Function doc """
        xyz_coords1 = []
        xyz_coords2 = []

        for atom1 in atoms1:
            xyz_coords1.append(
                               (atom1.pos[0],
                                atom1.pos[1],
                                atom1.pos[2])
                              )

        for atom2 in atoms2:
            xyz_coords2.append(
                               (atom2.pos[0],
                                atom2.pos[1],
                                atom2.pos[2])
                              )        
        


        if xyz_coords1 == [] or xyz_coords2 == []:
            pass
        
        else:
            distances  = distance.cdist(xyz_coords1, xyz_coords2, 'euclidean')
            if distances.min() <= 3.0:
                for i in range(0, len(distances)):   
                    for j in  range(0, len(distances[i])):
                        #if distances[i][j] <=  1.5:   
                        #    index_bonds2.append([i,j])
                        if distances[i][j] <=  (atoms1[i].cov_rad + atoms2[j].cov_rad)*1.5:
                            #print (atoms1[i].index -1,atoms2[j].index -1,distances[i][j])
                            #self.index_bonds_pairs.append([atom1.index -1, atom2.index -1])
                            self.index_bonds. append( atoms1[i].index -1    )
                            self.index_bonds. append( atoms2[j].index -1    )
                            atoms1[i].connected.append(atoms2[j])
                            atoms2[j].connected.append(atoms1[i])












            #for i in range(0, len(xyz_coords1)):
            #     
            #    for j in range(i+1, len(xyz_coords2)):
            #        
            #        if distances[i][j] <= (((atoms1[i].cov_rad + atoms2[j].cov_rad)**2)**0.5)*1.5:
            #            #print (atoms1[i].index -1,atoms2[j].index -1,distances[i][j])
            #            #self.index_bonds_pairs.append([atom1.index -1, atom2.index -1])
            #            self.index_bonds. append( atoms1[i].index -1    )
            #            self.index_bonds. append( atoms2[j].index -1    )
            #            atoms1[i].connected.append(atoms2[j])
            #            atoms2[j].connected.append(atoms1[i])
            #

def C_generate_bonds2_parallel(atoms):
    index_bonds, index_bonds_pairs = C_generate_bonds2(self.atoms)
    return [index_bonds, index_bonds_pairs]
    

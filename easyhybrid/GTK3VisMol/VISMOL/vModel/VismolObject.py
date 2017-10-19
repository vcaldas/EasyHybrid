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

#import VISMOL.Model.cfunctions as cfunctions
#import VISMOL.Model.Chain as Chain
from VISMOL.vModel.Chain      import Chain
from VISMOL.vModel.Residue    import Residue
from VISMOL.vModel.cfunctions import C_generate_bonds
#from VISMOL.glCore.VismolRepresentations import LineRepresetation

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

        
        self.atoms              = atoms
        self.residues           = []
        self.chains             = {}
                                
        self.bonds              = []
        self.frames             = trajectory
        self.mass_center        = np.array([0.0, 0.0, 0.0])

        self.atom_unique_id_dic = {}
        self.index_bonds        = None
        self.index_bonds_rep    = None
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
            
            sum_x += atom.pos[0]
            sum_y += atom.pos[1]
            sum_z += atom.pos[2]
            index   +=1
            self.vismol_session.atom_id_counter +=1
            
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
        print ('\ngenerate_bonds starting')
        initial          = time.time()
        
        self.index_bonds, self.index_bonds_pairs = C_generate_bonds(self.atoms)
        
        #print (self.index_bonds)
        #print (self.index_bonds2)
        #print (np.array(self.index_bonds2, dtype=np.uint32))
        final = time.time() 
        #print ('generate_bonds end -  total time: ', final - initial, '\n')
        
        #self.index_bonds3 = []
        #for bond in self.index_bonds2:
        #    self.index_bonds3.append(bond[0])
        #    self.index_bonds3.append(bond[1])
        
        #print (np.array(self.index_bonds3, dtype=np.uint32))  
        
        
        final = time.time() 
        print ('generate_bonds II end -  total time: ', final - initial, '\n')
        
        
        
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
            print (pickedID)
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
        #self.bond_colors           = []
        #for bond in self.index_bonds:
        #    atom1    = self.atoms[bond[0]]
        #    atom2    = self.atoms[bond[1]]
        #    # checking if the selection is actived
        #    if  atom1.lines and atom2.lines:
        #        ## colors
        #        self.bond_colors.append(atom1.color[0])        
        #        self.bond_colors.append(atom1.color[1])        
        #        self.bond_colors.append(atom1.color[2])  
        #        
        #        self.bond_colors.append(atom1.color[0])        
        #        self.bond_colors.append(atom1.color[1])        
        #        self.bond_colors.append(atom1.color[2])
        #        
        #        self.bond_colors.append(atom2.color[0])        
        #        self.bond_colors.append(atom2.color[1])        
        #        self.bond_colors.append(atom2.color[2])
        #        
        #        self.bond_colors.append(atom2.color[0])        
        #        self.bond_colors.append(atom2.color[1])        
        #        self.bond_colors.append(atom2.color[2])
        #
        #self.bond_colors  = np.array(self.bond_colors, dtype=np.float32)
    
        
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
        
        
        
        

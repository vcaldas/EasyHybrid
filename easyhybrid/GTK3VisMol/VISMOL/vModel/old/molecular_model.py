#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  molecular_model.py
#  
#  Copyright 2016 Carlos Eduardo Sequeiros Borja <casebor@gmail.com>
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


#import cfunctions

import numpy as np
import time
import os
#from multiprocessing import Pool
try:
    import atom_types as at
    import cfunctions as cfunctions

except:
    import atom_types as at
    import cfunctions as cfunctions

import multiprocessing as mp



class FlatSphereRepresentation:
    """ Class doc """
    
    def __init__ (self, Vobject):
        """ Class initialiser """
        
        """  F L A T   S P H E R E S   """
        self.actived                  = False
        self.modified                 = False
        self.Vobject                  = Vobject
        #self.show_hide_atoms          = []
        
        self.trajectory               = []
        self.colors                   = []
        self.COMPILED_LIST_trajectory = []
        
    def _generate_trajectory (self):
        """ Function doc """
        self.trajectory               = []
        
        for frame in self.Vobject.frames:
            
            frame_coordinates = []
            
            for atom in self.Vobject.atoms:
                
                if atom.dots:                   
                    #----------------------------------
                    #           D O T S
                    #----------------------------------
                    x1 = frame[ ( (atom.index -1)*3     ) ]
                    y1 = frame[ ( (atom.index -1)*3 + 1 ) ]
                    z1 = frame[ ( (atom.index -1)*3 + 2 ) ]                
                    
                    frame_coordinates.append(x1)
                    frame_coordinates.append(y1)
                    frame_coordinates.append(z1)
 
            frame_coordinates = np.array (frame_coordinates , dtype=np.float32)  
            self.trajectory.append(frame_coordinates) 

    def _generate_colors  (self):
        """ Function doc """
        
        self.colors = []        
        
        for atom in self.Vobject.atoms:
            if atom.dots:                   
                #-------------------------------------------------------
                #                        D O T S
                #-------------------------------------------------------
                self.colors.append(atom.color[0])        
                self.colors.append(atom.color[1])        
                self.colors.append(atom.color[2])   
                #self.colors.append(atom.color[3])   
        self.colors  = np.array(self.colors, dtype=np.float32)

    def update (self, selection = None):
        """ Function doc """
        print ('\nFlatSphereRepresentation starting')
        initial          = time.time()
        
        self._generate_trajectory()
        self._generate_colors()
        
        final = time.time() 
        print ('FlatSphereRepresentation end -  total time: ', final - initial, '\n')

class LineRepresentation:
    """ Class doc """
    
    def __init__ (self, Vobject):
        """ Class initialiser """
        
        """   L I N E S   """
        self.actived                  = True
        self.modified                 = False
        self.Vobject                  = Vobject
        #self.show_hide_atoms          = []
        
        self.trajectory_bonds         = []
        self.color_bonds              = []
        self.COMPILED_LIST_trajectory = []
        
    
    def generate_bond_colors (self):
        
        """ Function doc """
        self.line_color_bonds             = []

        for bond in self.Vobject.index_bonds:
            atom1    = self.Vobject.atoms[bond[0]]
            atom2    = self.Vobject.atoms[bond[1]]
            
            if atom1.lines and atom2.lines:
                self.line_color_bonds.append(atom1.color[0])        
                self.line_color_bonds.append(atom1.color[1])        
                self.line_color_bonds.append(atom1.color[2])  
                
                self.line_color_bonds.append(atom1.color[0])        
                self.line_color_bonds.append(atom1.color[1])        
                self.line_color_bonds.append(atom1.color[2])
                
                self.line_color_bonds.append(atom2.color[0])        
                self.line_color_bonds.append(atom2.color[1])        
                self.line_color_bonds.append(atom2.color[2])
                
                self.line_color_bonds.append(atom2.color[0])        
                self.line_color_bonds.append(atom2.color[1])        
                self.line_color_bonds.append(atom2.color[2])
        
        self.color_bonds  = np.array(self.line_color_bonds, dtype=np.float32)
    
    def generate_trajectory_line_representation (self):
        
        """ Function doc """
        #return None
        print ('\ngenerate_trajectory_bonds starting')
        initial     = time.time()
        
        n_processor      = mp.cpu_count()
        pool             = mp.Pool(n_processor)
        
        pool_list = [] 
        
        show_hide_list = []
        for atom in self.Vobject.atoms:
            show_hide_list.append(atom.lines)
        
        for frame in self.Vobject.frames:
            pool_list.append([frame, self.Vobject.index_bonds, show_hide_list] )
        
        self.trajectory_bonds = pool.map(cfunctions.generate_bond, pool_list)

        
        final = time.time() 
        
        print ('ngenerate_trajectory_bonds finished -  total time: ', final - initial, '\n')
    

    def update(self):
        """ Function doc """
        self.generate_bond_colors()
        self.generate_trajectory_line_representation()


class VismolObject:
    """ Class doc """
    
    def __init__ (self, atoms = [] , label = None, EMSession = None, trajectory = None):
        """ Class initialiser """
        self.EMSession = EMSession
        self.actived   = False       
        self.Type      = 'molecule'
        
        if label:
            label = os.path.basename(label)
            self.label = self._get_label(label)
            self.name  = self._get_label(label)
        else:
            self.label = 'unkown'
            self.name  = 'unkown'

        
        self.atoms              = atoms
        self.residues           = []
        self.chains             = {}
                                
        self.bonds              = []
        self.frames             = trajectory
        self.mass_center        = np.array([0.0, 0.0, 0.0])

        self.atom_unique_id_dic = {}
        self.index_bonds        = None
       
        self._generate_chain_structure()
        self._generate_atom_unique_color_id()
        self._generate_bonds()
        #self._generate_colors()
        
        """   L I N E S   """
        self.line_representation = LineRepresentation(self)
        self.line_representation.update()

        """   F L A T   S P H E R E   """
        self.flat_sphere_representation = FlatSphereRepresentation(self)

        
        print ('frames:     ', len(self.frames))
        print ('frame size: ', len(self.frames[0]))

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
            atom.atom_id = self.EMSession.atom_id_counter
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

            self.EMSession.atom_dic_id[self.EMSession.atom_id_counter] = atom
            
            sum_x += atom.pos[0]
            sum_y += atom.pos[1]
            sum_z += atom.pos[2]
            index   +=1
            self.EMSession.atom_id_counter +=1
            
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

    def _get_label (self, label):
        """ Function doc """
        #print( 'label:', label)
        self.label  = label.split('.')
        self.label  = self.label[0]
    
    def _generate_bonds (self):
        """ Function doc """
        print ('\ngenerate_bonds starting')
        initial          = time.time()
        self.index_bonds = cfunctions.C_generate_bonds(self.atoms)
        final = time.time() 
        print ('generate_bonds end -  total time: ', final - initial, '\n')

    def _generate_atom_unique_color_id (self):
        self.coordinates_color_ids  = []        
#        self.atom_unique_id_dic     = {}

        """ Function doc """
        for atom in self.atoms:
            i = atom.atom_id
            r = (i & 0x000000FF) >>  0
            g = (i & 0x0000FF00) >>  8
            b = (i & 0x00FF0000) >> 16
           
            self.coordinates_color_ids.append(r/255.0)
            self.coordinates_color_ids.append(g/255.0)
            self.coordinates_color_ids.append(b/255.0)
            
            pickedID = r + g * 256 + b * 256*256
            print (pickedID)
            self.EMSession.atom_dic_id[pickedID] = atom
            #self.atom_unique_id_dic[pickedID] = atom
        self.coordinates_color_ids = np.array(self.coordinates_color_ids, dtype=np.float32)
        
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
    
        
        self.coordinates_colors = []        
        for atom in self.atoms:
            #if atom.dots:
            #-------------------------------------------------------
            #                        D O T S
            #-------------------------------------------------------
            self.coordinates_colors.append(atom.color[0])        
            self.coordinates_colors.append(atom.color[1])        
            self.coordinates_colors.append(atom.color[2])   
            #self.coordinates_colors.append(atom.color[3])   

        self.coordinates_colors  = np.array(self.coordinates_colors, dtype=np.float32)
    

class Chain:
    """ Class doc """
    
    def __init__ (self, name=None, residues=None, label=None):
        """ Class initialiser """
        #self.residues = {}
        self.residues = []
        
        self.backbone = []
        self.name     = ''
        #self.label    = None
class Residue:
    """ Class doc """
    
    def __init__ (self, atoms=None, 
                        name='UNK', 
                        index=None,
                        chain=None):
        """ Class initialiser """
        self.atoms = []
        self.resi  = index
        self.resn  = name
        self.chain = chain
        
class Atom:
    """ Class doc """
    
    def __init__ (self, name         ='Xx',
                        index        =None, 
                        symbol       ='X', 
                        pos          = None, 
                        resi         = None, 
                        resn         = None, 
                        chain        = '', 
                        atom_id      = 0, 
                        residue      = None,
                        #Vobject_id   = None, 
                        #Vobject_name = '', 
                        Vobject      = None):
        """ Class initialiser """
        
        if pos is None:
            pos = np.array([0.0, 0.0, 0.0])
        
        self.pos          = pos                   # - coordinates of the first frame
        self.index        = index                 # 
        self.name         = name                  #
        self.symbol       = symbol                #
        self.resi         = resi                  #
        self.resn         = resn                  #
        self.chain        = chain                 #
        #self.Vobject_id   = Vobject_id            #
        #self.Vobject_name = Vobject_name          #
        self.Vobject      = Vobject
        self.residue      = residue                                
        
        self.atom_id      = atom_id               # An unique number

        self.color        = at.get_color    (name)
        self.color.append(0.0)  
	     
        self.col_rgb      = at.get_color_rgb(name)
        self.radius       = at.get_radius   (name)
        self.vdw_rad      = at.get_vdw_rad  (name)
        self.cov_rad      = at.get_cov_rad  (name)
        self.ball_radius  = at.get_ball_rad (name)

        self.lines          = True
        self.dots           = False
        self.ribbons        = False
        self.ball_and_stick = False
        self.sticks         = False
        self.spheres        = False
        self.surface        = False
        
        
        self.connected      = []



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

#from multiprocessing import Pool
import GLarea.atom_types as at
import GLarea.cfunctions as cfunctions
import multiprocessing




class Vobject:
    """ Class doc """
    
    def __init__ (self, chains=None, bonds=None, mass_center=None, label = None):
        """ Class initialiser """
        #print( 'label:', label)
        self.actived           = True       
        
        """   D O T S   """
        self.show_dots         = False
        self.GL_list_dots      = []    # GL list -  GPU compiled 
        self.modified_dots     = False
        #self.list_atom_dots    = []    # <-- True/False lista containg all atoms 
        
        """   L I N E S   """
        self.show_lines        = True
        self.list_lines        = []
        self.modified_lines    = False

        #self.list_atom_lines   = []    # <-- True/False lista containg all atoms 
        
        """   R I B B O N S   """
        self.show_ribbons      = False
        self.list_ribbons      = []
        self.modified_ribbons  = False

        #self.list_atom_ribbons = []    # <-- True/False lista containg all atoms 
        
        """   S T I C K S   """
        self.show_sticks       = False
        self.list_sticks       = []
        self.modified_sticks   = False

        #self.list_atom_sticks  = []   # <-- True/False lista containg all atoms 
        
        """   S P H E R E S   """
        self.show_spheres      = False
        self.list_spheres      = []
        self.modified_spheres  = False

        #self.list_atom_spheres = []   # <-- True/False lista containg all atoms 
        
        """   S U R F A C E   """
        self.show_surface      = False
        self.list_surface      = []
        self.modified_surface  = False

        #self.list_atom_surface = []
        
        """   B A L L  A N D  S T I C K   """   
        self.show_ball_and_stick      = False
        self.list_ball_and_stick      = []
        self.modified_ball_and_stick  = False

        #self.list_atom_ball_and_stick = []



        self.Type  = 'molecule'
        
        
      
        
        if label:
            self.label = self._get_label(label)
            self.name = self._get_label(label)
        else:
            self.label = 'unkown'
            self.name  = 'unkown'

        
        
        
        self.chains       = {}

        self.bonds        = []
        self.index_bonds  = []

        self.mass_center  = np.array([0.0, 0.0, 0.0])

        self.frames       = []
        self.frame_energy = [] 
        
        self.atoms        = []
        self.residues     = []

        #self.coords       = []
        pass  

    

    
    def generate_chain_structure (self, counter = 0, atom_dic_id = None):
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
            atom.atom_id = counter
            
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


            if atom_dic_id is not None:
                atom_dic_id[counter] = atom

            sum_x += atom.pos[0]
            sum_y += atom.pos[1]
            sum_z += atom.pos[2]
            index   +=1
            counter +=1
            
        self.frames.append(frame)
        total = len(self.atoms)
        self.list_atom_lines          = [True] *total
        self.list_atom_ribbons        = [False]*total
        self.list_atom_dots           = [False]*total
        self.list_atom_sticks         = [False]*total
        self.list_atom_spheres        = [False]*total
        self.list_atom_surface        = [False]*total
        self.list_atom_ball_and_stick = [False]*total


        self.mass_center[0] = sum_x / total
        self.mass_center[1] = sum_y / total
        self.mass_center[2] = sum_z / total
        #print ('generate_chain_structure -> label:', self.label, self.name)
        final = time.time() 
        print ('generate_chain_structure end -  total time: ', final - initial, '\n')
        return atom_dic_id

    def _get_label (self, label):
        """ Function doc """
        #print( 'label:', label)
        self.label  = label.split('.')
        self.label  = self.label[0]
        #print( 'label:', self.label)

    def generate_atom_list (self):
        """ Function doc """
        bonds = []
        NDIM = 3 # number of dimensions

        a = np.array(self.coords)
        a.shape = a.size / NDIM, NDIM
        for i  in  range(0, len(self.coords), 3): 
            point = np.array ([self.coords[i], self.coords[i+1], self.coords[i+2]])
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
                        bonds.append(point[0])
                        bonds.append(point[1])
                        bonds.append(point[2])
                        bonds.append(a[index][0]) 
                        bonds.append(a[index][1])
                        bonds.append(a[index][2])
            #'''
        return bonds 

    #'''
    def generate_bonds (self):
        """ Function doc """
        print ('\ngenerate_bonds starting')
        initial          = time.time()
        self.index_bonds = cfunctions.C_generate_bonds3 (self.atoms)
        final = time.time() 
        print ('generate_bonds end -  total time: ', final - initial, '\n')

        self.generate_trajectory_bonds()
        self.generate_trajectory_coordinates()
    '''
    def generate_bonds (self):
        """ Function doc """
        print ('start')
        initial = time.time()
        #self.bonds = self.generete_atom_list()
        #self.bonds = cfunctions.C_generate_bonds (self.coords)
        #self.bonds, self.index_bonds = cfunctions.C_generate_bonds3 (self.atoms)
        for chain in self.chains:
            for residue in self.chains[chain].residues:
                
        self.index_bonds = cfunctions.C_generate_bonds3 (self.atoms)
        #self.bonds = cfunctions.C_np_generate_bonds (self.coords)
        #self.bonds = self.distances_from_point()
        print ('end')
        final = time.time() 
        print (final - initial)
    #'''

    
    def generate_trajectory_bonds (self):
        """ Function doc """
        self.trajectory_bonds = []
        self.bonds_trajectory_colors = []
        for bond in self.index_bonds:
            atom1    = self.atoms[bond[0]]
            atom2    = self.atoms[bond[1]]
            # checking if the selection is actived
            if  atom1.lines and atom2.lines:
                coord1   = self.frames[0][bond[0]]
                coord2   = self.frames[0][bond[1]]
                
                midcoord = [
                           (coord1[0] + coord2[0])/2,	   
                           (coord1[1] + coord2[1])/2,
                           (coord1[2] + coord2[2])/2,
                           ]
                
                self.trajectory_bonds.append(float(coord1[0]))
                self.trajectory_bonds.append(float(coord1[1]))
                self.trajectory_bonds.append(float(coord1[2]))
                
                self.trajectory_bonds.append(float(midcoord[0]))
                self.trajectory_bonds.append(float(midcoord[1]))
                self.trajectory_bonds.append(float(midcoord[2]))
                
                self.trajectory_bonds.append(float(midcoord[0]))
                self.trajectory_bonds.append(float(midcoord[1]))
                self.trajectory_bonds.append(float(midcoord[2]))
                
                self.trajectory_bonds.append(float(coord2[0]))
                self.trajectory_bonds.append(float(coord2[1]))
                self.trajectory_bonds.append(float(coord2[2]))
                
                
                
                
                self.bonds_trajectory_colors.append(atom1.color[0])        
                self.bonds_trajectory_colors.append(atom1.color[1])        
                self.bonds_trajectory_colors.append(atom1.color[2])  
                
                self.bonds_trajectory_colors.append(atom1.color[0])        
                self.bonds_trajectory_colors.append(atom1.color[1])        
                self.bonds_trajectory_colors.append(atom1.color[2])
                
                self.bonds_trajectory_colors.append(atom2.color[0])        
                self.bonds_trajectory_colors.append(atom2.color[1])        
                self.bonds_trajectory_colors.append(atom2.color[2])
                
                self.bonds_trajectory_colors.append(atom2.color[0])        
                self.bonds_trajectory_colors.append(atom2.color[1])        
                self.bonds_trajectory_colors.append(atom2.color[2])
                
                #midcoord = [
                #        (coord1[0] + coord2[0])/2,	   
                #        (coord1[1] + coord2[1])/2,
                #        (coord1[2] + coord2[2])/2,
                #        ]
                #
                #glPushMatrix()		
                #glPushName(atom1.atom_id) 
                #glColor3f(atom1.color[0], 
                #          atom1.color[1], 
                #      atom1.color[2])
                #
                #
                #glBegin(GL_LINES)
                #glVertex3f(coord1[0],coord1[1],coord1[2])
                #glVertex3f(midcoord[0],midcoord[1],midcoord[2])
                #glEnd()
                #glPopName()
                #glPopMatrix()
                #
                #
                #glPushMatrix()		
                #glPushName(atom2.atom_id) 
                #glColor3f (atom2.color[0], 
                #           atom2.color[1], 
                #       atom2.color[2])
                #
                #glBegin(GL_LINES)
                #glVertex3f(midcoord[0],midcoord[1],midcoord[2])
                #glVertex3f(coord2[0],coord2[1],coord2[2])
                #
                #glEnd()
                #glPopName()
                #glPopMatrix()

                
        self.trajectory_bonds       = np.array(self.trajectory_bonds,        dtype=np.float32)
        self.bonds_trajectory_colors= np.array(self.bonds_trajectory_colors, dtype=np.float32)
        #self.VBOID    = GLuint(1)

    def generate_trajectory_coordinates (self):
        """ Function doc """
        self.trajectory_coordinates  = []        
        self.trajectory_colors       = []        
        self.unique_colors_colors_id = [] 
        self.atom_unique_id_dic      = {}
        
        for atom in self.atoms:
            #if atom.dots:
            #-------------------------------------------------------
            #                        D O T S
            #-------------------------------------------------------
            coord1   = self.frames[0][atom.index-1]
            self.trajectory_coordinates.append(float(coord1[0]))
            self.trajectory_coordinates.append(float(coord1[1]))
            self.trajectory_coordinates.append(float(coord1[2]))
            
            self.trajectory_colors.append(atom.color[0])        
            self.trajectory_colors.append(atom.color[1])        
            self.trajectory_colors.append(atom.color[2])        
            
            i = atom.atom_id
            r = (i & 0x000000FF) >>  0
            g = (i & 0x0000FF00) >>  8
            b = (i & 0x00FF0000) >> 16
            
            
            self.unique_colors_colors_id.append(r/255.0)
            self.unique_colors_colors_id.append(g/255.0)
            self.unique_colors_colors_id.append(b/255.0)
            
            pickedID = r + g * 256 + b * 256*256
            self.atom_unique_id_dic[pickedID] = atom
            
        self.trajectory_coordinates  = np.array(self.trajectory_coordinates , dtype=np.float32)
        self.trajectory_colors       = np.array(self.trajectory_colors      , dtype=np.float32)
        self.unique_colors_colors_id = np.array(self.unique_colors_colors_id, dtype=np.float32)

        #self.VBOID    = GLuint(1)


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



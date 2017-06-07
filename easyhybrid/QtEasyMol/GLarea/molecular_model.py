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



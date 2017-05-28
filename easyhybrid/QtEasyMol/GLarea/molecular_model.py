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

from multiprocessing import Pool
import GLarea.atom_types as at
import GLarea.cfunctions as cfunctions




class Vobject:
    """ Class doc """
    
    def __init__ (self, chains=None, bonds=None, mass_center=None):
        """ Class initialiser """
        
        self.actived      = True       
        
        self.show_dots    = True
        self.list_dots    = []
        
        self.show_lines   = True
        self.list_lines   = []
        
        self.show_ribbons = False
        self.list_ribbons = []
        
        self.show_sticks  = False
        self.list_sticks  = []

        self.show_spheres = False
        self.list_spheres = []
        
        self.show_ball_and_stick = False
        self.list_ball_and_stick = []
        
        self.show_surface = False
        self.list_surface = []
        
        self.Type  = 'molecule'
        self.label = 'unkown'


        self.chains       = {}

        self.bonds        = []
        self.index_bonds  = []

        self.mass_center  = np.array([0.0, 0.0, 0.0])

        self.frames       = []
        self.atoms        = []
        self.residues     = []

        self.coords       = []
        pass  


    def generete_atom_list (self):
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

    
    def generate_bonds (self):
        """ Function doc """
        print ('start')
        initial = time.time()
        #self.bonds = self.generete_atom_list()
        #self.bonds = cfunctions.C_generate_bonds (self.coords)
        self.bonds, self.index_bonds = cfunctions.C_generate_bonds3 (self.atoms)
        #self.bonds = cfunctions.C_np_generate_bonds (self.coords)
        #self.bonds = self.distances_from_point()
        print ('end')
        final = time.time() 
        print (final - initial)



class Chain:
    """ Class doc """
    
    def __init__ (self, name=None, residues=None, label=None):
        """ Class initialiser """
        self.residues = {}
        self.backbone = []
        self.name     = ''
        self.label    = None

        
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
    
    def __init__ (self, name='Xx', index=None, symbol='X', pos=None, resi = None, chain = '', atom_id = 0, Vobject_id = None):
        """ Class initialiser """
        
        if pos is None:
            pos = np.array([0.0, 0.0, 0.0])
        
        self.pos     = pos
        self.index   = index
        self.name    = name
        self.symbol  = symbol
        self.resi    = resi 
        self.chain   = chain

        self.Vobject_id = Vobject_id
        self.atom_id = atom_id

        self.color       = at.get_color(name)
        self.col_rgb     = at.get_color_rgb(name)
        self.radius      = at.get_radius(name)
        self.vdw_rad     = at.get_vdw_rad(name)
        self.cov_rad     = at.get_cov_rad(name)
        self.ball_radius = at.get_ball_rad(name)


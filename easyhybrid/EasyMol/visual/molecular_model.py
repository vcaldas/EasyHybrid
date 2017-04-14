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


import pyximport; pyximport.install()
import cfunctions

import numpy as np
import time

from multiprocessing import Pool
import atom_types as at




class MolObject:
    """ Class doc """
    
    def __init__ (self, chains=None, bonds=None, mass_center=None):
        """ Class initialiser """
        
        self.actived      = True       
        
        self.show_dots    = False
        self.list_dots    = []
        
        self.show_lines   = True
        self.list_lines   = []
        
        self.show_ribbons = False
        self.list_ribbons = []
        
        self.show_sticks  = False
        self.list_sticks  = []

        self.show_spheres = False
        self.list_spheres = []
        
        self.show_surface = False
        self.list_surface = []
        
        self.Type    = 'molecule'
        self.label   = 'unkown'
        
        
        self.chains       = {}
        self.bonds        = []
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
        print 'start'
        initial = time.time()
        #self.bonds = self.generete_atom_list()
        #self.bonds = cfunctions.C_generate_bonds (self.coords)
        self.bonds = cfunctions.C_generate_bonds3 (self.atoms)
        #self.bonds = cfunctions.C_np_generate_bonds (self.coords)
        #self.bonds = self.distances_from_point()
        print 'end'
        #print self.bonds
        final = time.time() 
        print final - initial

        #print 'BEGINS TO CALCULATE DISTANCES'
        #arr1 = np.array([0, 0, 1])
        #for i in range(len(atoms)-1):
        #    if i+25>=len(atoms):
        #        limit = len(atoms)
        #
        #
        #
        #else:
        #    limit = i+25
        #for j in range(i+1, limit):
        #    if get_euclidean(atoms[i].pos, atoms[j].pos) <= (atoms[i].cov_rad + atoms[j].cov_rad):
        #    arr2 = unit_vector(atoms[j].pos - atoms[i].pos)
        #    mid_point = (atoms[i].pos+atoms[j].pos)/2
        #    angle = get_angle(arr1, arr2)
        #    vec_o = np.cross(arr1, arr2)
        #    length = get_euclidean(atoms[i].pos, atoms[j].pos)/2
        #    bond = (atoms[i], length, angle, vec_o, mid_point)
        #    bond2 = (atoms[j], length, angle+180, vec_o, mid_point)
        #    bonds_list.append(bond)
        #    bonds_list.append(bond2)
        #print 'ENDS!'
        #return bonds_list


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
    
    def __init__ (self, name='Xx', index=None, symbol='X', pos=None, resi = None, chain = ''):
        """ Class initialiser """
        
        if pos is None:
            pos = np.array([0.0, 0.0, 0.0])
        
        self.pos     = pos
        self.index   = index
        self.name    = name
        self.symbol  = symbol
        self.resi    = resi 
        self.chain   = chain
        
        self.color       = at.get_color(name)
        self.col_rgb     = at.get_color_rgb(name)
        self.radius      = at.get_radius(name)
        self.vdw_rad     = at.get_vdw_rad(name)
        self.cov_rad     = at.get_cov_rad(name)
        self.ball_radius = at.get_ball_rad(name)



'''
class Frame:
    """ Class doc """
    
    def __init__ (self, chains=None, bonds=None, mass_center=None):
        """ Class initialiser """
	if chains is None:
	    chains = {}
	if bonds is None:
	    bonds = []
	if mass_center is None:
	    mass_center = np.array([0.0, 0.0, 0.0])
        self.chains      = chains
        self.bonds       = bonds
        self.ribbons     = []
        self.mass_center = mass_center
	self.atoms       = []
    
    def load_bonds(self):
	"""
	"""
	import operations
	self.bonds = operations.generate_bonds(self.atoms)
    
    def load_ribbons(self):
	"""
	"""
	import operations
	for chain in self.chains.values():
	    ribs = operations.generate_ribbons(chain.backbone)
	    self.ribbons += ribs

'''

'''
class Chain:
    """ Class doc """
    
    def __init__ (self, name='A', residues=None, frame=None):
        """ Class initialiser """
	if residues is None:
	    residues = {}
        self.residues = residues
        self.name     = name
	self.frame    = frame
	self.backbone = []
'''

'''
class Residue:
    """ Class doc """
    
    def __init__ (self, atoms=None, name='UNK', index=None, chain=None):
        """ Class initialiser """
	if atoms is None:
	    atoms = {}
        self.atoms = atoms
        self.name  = name
        self.index = index
        self.chain = chain
'''

'''
class Atom:
    """ Class doc """
    
    def __init__ (self, name='Xx', index=None, symbol='X', pos=None, residue=None):
        """ Class initialiser """
	import atom_types as at
	if pos is None:
	    pos = np.array([0.0, 0.0, 0.0])
        self.pos     = pos
        self.index   = index
        self.name    = name
        self.symbol  = symbol
	self.residue = residue
        
	self.color       = at.get_color(name)
	self.col_rgb     = at.get_color_rgb(name)
	self.radius      = at.get_radius(name)
	self.vdw_rad     = at.get_vdw_rad(name)
	self.cov_rad     = at.get_cov_rad(name)
	self.ball_radius = at.get_ball_rad(name)
	self.sphere      = False
	self.ball        = False
        self.vdw         = False
        self.pretty_vdw  = False
        self.dot         = False
        self.dot_surface = False
        self.surface     = False
        self.wires       = False
        #self.lines   = False
'''

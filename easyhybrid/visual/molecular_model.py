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

import numpy as np

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
        self.mass_center = mass_center

class Chain:
    """ Class doc """
    
    def __init__ (self, name='A', residues=None, frame=None):
        """ Class initialiser """
	if residues is None:
	    residues = {}
        self.residues = residues
        self.name     = name
	self.frame    = frame

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
	self.dots_surf = None
        
	self.color   = at.get_color(name)
	self.col_rgb = at.get_color_rgb(name)
	self.radius  = at.get_radius(name)
	self.vdw_rad = at.get_vdw(name)
	self.cov_rad = at.get_cov_rad(name)
	self.sphere  = False
        self.stick   = False
        self.vdw     = False
        self.lines   = False
        self.surface = False
        self.dots    = False

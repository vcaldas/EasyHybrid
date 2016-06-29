#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  dataobject.py
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


class Atom:
    """
    """
    def __init__(self, bonded_atoms=[], pos=(0.0, 0.0, 0.0), name='X', color=[0.07, 0.50, 0.70], sphere=False):
	"""
	"""
	self.bonded_atoms = bonded_atoms
	self.pos = pos
	self.name = name
	self.color = color
	self.sphere = sphere

class Residue:
    """
    """
    def __init__(self, atoms=[], name='XXX'):
	self.atoms = atoms
	self.name = name

class Chain:
    """
    """
    def __init__(self, residues=[], name='A'):
	self.residues = residues
	self.name = name

class DataObject:
    """
    """
    


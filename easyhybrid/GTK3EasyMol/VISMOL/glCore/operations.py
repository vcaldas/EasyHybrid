#!/usr/bin/env python33
# -*- coding: utf-8 -*-
#
#  operations.py
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
import math

def generate_bonds(atoms):
    """ Make calculations for the bonds, this part of the code must be more efficient.
    """
    bonds_list = []
    print('BEGINS TO CALCULATE DISTANCES')
    arr1 = np.array([0, 1, 0])
    for i in range(len(atoms)-1):
        if i+25 >= int(len(atoms)):
            limit = int(len(atoms))
        else:
            limit = i+25
        for j in range(i+1, limit):
            if get_euclidean(atoms[i].pos, atoms[j].pos) <= (atoms[i].cov_rad + atoms[j].cov_rad):
                arr2 = unit_vector(atoms[j].pos - atoms[i].pos)
                mid_point = (atoms[i].pos+atoms[j].pos)/2
                angle = get_angle(arr1, arr2)
                vec_o = np.cross(arr1, arr2)
                length = get_euclidean(atoms[i].pos, atoms[j].pos)/2
                bond = (atoms[i], length, angle, vec_o, mid_point)
                bond2 = (atoms[j], length, angle+180, vec_o, mid_point)
                bonds_list.append(bond)
                bonds_list.append(bond2)
    print('ENDS!')
    return bonds_list

def generate_ribbons(backbone):
    """ Calculates the distances and angles for the ribbon representation.
    """
    arr1 = np.array([0, 1, 0])
    ribbon_list = []
    for i in range(int(len(backbone))-1):
        arr2 = unit_vector(backbone[i+1].pos - backbone[i].pos)
        angle = get_angle(arr1, arr2)
        vec_o = np.cross(arr1, arr2)
        length = get_euclidean(backbone[i].pos, backbone[i+1].pos)
        temp = (backbone[i], length, angle, vec_o)
        ribbon_list.append(temp)
    #ribbon_list.append((backbone[-1], 0, 0, [0,0,0]))
    return ribbon_list

def get_mass_center(atoms):
    """ Returns the mass center of a molecule.
    """
    mass_c = np.zeros(3)
    for atom in atoms:
        mass_c += atom.pos
    mass_c /= int(len(atoms))
    return mass_c

def get_euclidean(pa, pb):
    """ Returns the distance between two points in R3
    """
    import math
    if int(len(pa)) == 1:
        pa = [pa[0], 0.0, 0.0]
    if int(len(pa)) == 2:
        pa = [pa[0], pa[1], 0.0]
    if int(len(pb)) == 1:
        pb = [pb[0], 0.0, 0.0]
    if int(len(pb)) == 2:
        pb = [pb[0], pb[1], 0.0]
    return math.sqrt((pb[0]-pa[0])**2 + (pb[1]-pa[1])**2 + (pb[2]-pa[2])**2)

def unit_vector(vector):
    """ Returns the unit vector of the vector.
    """
    return vector / np.linalg.norm(vector)

def get_angle(vecA, vecB):
    """ Return the angle in degrees of two vectors.
    """
    vecA_u = unit_vector(vecA)
    vecB_u = unit_vector(vecB)
    return np.degrees(np.arccos(np.clip(np.dot(vecA_u, vecB_u), -1.0, 1.0)))
















#!/usr/bin/env python
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

sin_phi = np.array([0.309017,0.587785,0.809017,0.951057,1.0])
#sin_phi = np.array([17.705370,33.677614,46.353259,54.491524,57.295780])
cos_phi = np.array([0.951057,0.809017,0.587785,0.309017,0.0])
#cos_phi = np.array([54.491524,46.353259,33.677614,17.705370,0.0])

sin_teta = np.array([0.0,0.866025,0.866025,0.0,-0.866025,-0.866025,0.5,1.0,0.5,-0.5,-1.0,-0.5,0.0,0.642788,0.984808,0.866025,0.342020,-0.342020,-0.866025,-0.984808,-0.642788,0.258819,0.707107,0.965926,0.965926,0.707107,0.258819,-0.258819,-0.707107,-0.965926,-0.965926,-0.707107,-0.258819,0.0,0.406737,0.743145,0.951057,0.994522,0.866025,0.587785,0.207912,-0.207912,-0.587785,-0.866025,-0.994522,-0.951057,-0.743145,-0.406737])
#sin_teta = np.array([0.0,49.619601,49.619601,0.0,-49.619601,-49.619601,28.647890,57.295780,28.647890,-28.647890,-57.295780,-28.647890,0.0,36.829017,56.425328,49.619601,19.596311,-19.596311,-49.619601,-56.425328,-36.829017,14.829239,40.514234,55.343473,55.343473,40.514234,14.829239,-14.829239,-40.514234,-55.343473,-55.343473,-40.514234,-14.829239,0.0,23.304293,42.579062,54.491524,56.981907,49.619601,33.677614,11.912462,-11.912462,-33.677614,-49.619601,-56.981907,-54.491524,-42.579062,-23.304293])
cos_teta = np.array([1.0,0.5,-0.5,-1.0,-0.5,0.5,0.866025,0.0,-0.866025,-0.866025,0.0,0.866025,1.0,0.766044,0.173648,-0.5,-0.939693,-0.939693,-0.5,0.173648,0.766044,0.965926,0.707107,0.258819,-0.258819,-0.707107,-0.965926,-0.965926,-0.707107,-0.258819,0.258819,0.707107,0.965926,1.0,0.913545,0.669131,0.309017,-0.104528,-0.5,-0.809017,-0.978148,-0.978148,-0.809017,-0.5,-0.104528,0.309017,0.669131,0.913545])
#cos_teta = np.array([57.295780,28.647890,-28.647890,-57.295780,-28.647890,28.647890,49.619601,0.0,-49.619601,-49.619601,0.0,49.619601,57.295780,43.891114,9.949308,-28.647890,-53.840421,-53.840421,-28.647890,9.949308,43.891114,55.343473,40.514234,14.829239,-14.829239,-40.514234,-55.343473,-55.343473,-40.514234,-14.829239,14.829239,40.514234,55.343473,57.295780,52.342299,38.338360,17.705370,-5.989040,-28.647890,-46.353259,-56.043729,-56.043729,-46.353259,-28.647890,-5.989040,17.705370,38.338360,52.342299])

def get_surf_dots(atom):
    """
    """
    dots = []
    r = atom.radius
    x, y, z = atom.pos[0], atom.pos[1], atom.pos[2]
    point = [x, y+r, z]
    point2 = [x, y-r, z]
    dots.append(point)
    dots.append(point2)
    for i in range(6):
	point = [x+r*sin_phi[0]*sin_teta[i], y+r*cos_phi[0], z+r*sin_phi[0]*cos_teta[i]]
	point2 = [point[0], y-r*cos_phi[0], point[2]]
	dots.append(point)
	dots.append(point2)
    for i in range(6, 12):
	point = [x+r*sin_phi[1]*sin_teta[i], y+r*cos_phi[1], z+r*sin_phi[1]*cos_teta[i]]
	point2 = [point[0], y-r*cos_phi[1], point[2]]
	dots.append(point)
	dots.append(point2)
    for i in range(12, 21):
	point = [x+r*sin_phi[2]*sin_teta[i], y+r*cos_phi[2], z+r*sin_phi[2]*cos_teta[i]]
	point2 = [point[0], y-r*cos_phi[2], point[2]]
	dots.append(point)
	dots.append(point2)
    for i in range(21, 33):
	point = [x+r*sin_phi[3]*sin_teta[i], y+r*cos_phi[3], z+r*sin_phi[3]*cos_teta[i]]
	point2 = [point[0], y-r*cos_phi[3], point[2]]
	dots.append(point)
	dots.append(point2)
    for i in range(33, 48):
	point = [x+r*sin_teta[i], y, z+r*cos_teta[i]]
	dots.append(point)
    return dots

def get_bonds(atom_matrix, rad_matrix):
    """
    """
    x_pos = atom_matrix[:,0]
    y_pos = atom_matrix[:,1]
    z_pos = atom_matrix[:,2]
    dim = len(x_pos)
    x_matrix1 = x_matrix2 = y_matrix1 = y_matrix2 = z_matrix1 = z_matrix2 = cov_rad_matrix1 = cov_rad_matrix2 = x_pow = y_pow = z_pow = cov_dist_pow_matrix = np.zeros((dim, dim))
    x_matrix1[:] = x_pos
    x_matrix2[:] = x_matrix1.T
    y_matrix1[:] = y_pos
    y_matrix2[:] = y_matrix1.T
    z_matrix1[:] = z_pos
    z_matrix2[:] = z_matrix1.T
    cov_rad_matrix1[:] = rad_matrix
    cov_rad_matrix2[:] = cov_rad_matrix1.T
    #np.savetxt('x_mat1.txt', x_matrix1, fmt='%.3f')
    #np.savetxt('x_mat2.txt', x_matrix2, fmt='%.3f')
    dist_x = np.triu(x_matrix1-x_matrix2)
    dist_y = np.triu(y_matrix1-y_matrix2)
    dist_z = np.triu(z_matrix1-z_matrix2)
    cov_dist_matrix = np.triu(cov_rad_matrix1+cov_rad_matrix2)
    #np.savetxt('x_dist.txt', dist_x, fmt='%.3f')
    #print 'entra'
    for i in range(1, dim):
	diag_x = dist_x.diagonal(offset=i)
	diag_y = dist_y.diagonal(offset=i)
	diag_z = dist_z.diagonal(offset=i)
	#print i, '<-- aca estamos'
	diag_cov = cov_dist_matrix.diagonal(offset=i)
	diag_x = diag_x*diag_x.T
	diag_y = diag_y*diag_y.T
	diag_z = diag_z*diag_z.T
	diag_cov = diag_cov*diag_cov.T
	x_pow += np.diag(diag_x, k=i)
	y_pow += np.diag(diag_y, k=i)
	z_pow += np.diag(diag_z, k=i)
	cov_dist_pow_matrix += np.diag(diag_cov, k=i)
    #print 'sale'
    #np.savetxt('x_square.txt', x_pow, fmt='%.3f')
    pow_matrix = x_pow + y_pow + z_pow

#def get_bonds(atom_matrix, rad_matrix):
    #"""
    #"""
    #x_pos = atom_matrix[:,0]
    #y_pos = atom_matrix[:,1]
    #z_pos = atom_matrix[:,2]
    #dim = len(x_pos)
    #x_matrix1 = np.zeros((dim, dim))
    #x_matrix2 = np.zeros((dim, dim))
    #y_matrix1 = np.zeros((dim, dim))
    #y_matrix2 = np.zeros((dim, dim))
    #z_matrix1 = np.zeros((dim, dim))
    #z_matrix2 = np.zeros((dim, dim))
    #cov_rad_matrix1 = np.zeros((dim, dim))
    #cov_rad_matrix2 = np.zeros((dim, dim))
    #x_pow = np.zeros((dim, dim))
    #y_pow = np.zeros((dim, dim))
    #z_pow = np.zeros((dim, dim))
    #cov_dist_pow_matrix = np.zeros((dim, dim))
    #x_matrix1[:] = x_pos
    #x_matrix2[:] = x_matrix1.T
    #y_matrix1[:] = y_pos
    #y_matrix2[:] = y_matrix1.T
    #z_matrix1[:] = z_pos
    #z_matrix2[:] = z_matrix1.T
    #cov_rad_matrix1[:] = rad_matrix
    #cov_rad_matrix2[:] = cov_rad_matrix1.T
    ##np.savetxt('x_mat1.txt', x_matrix1, fmt='%.3f')
    ##np.savetxt('x_mat2.txt', x_matrix2, fmt='%.3f')
    #dist_x = np.triu(x_matrix1-x_matrix2)
    #dist_y = np.triu(y_matrix1-y_matrix2)
    #dist_z = np.triu(z_matrix1-z_matrix2)
    #cov_dist_matrix = np.triu(cov_rad_matrix1+cov_rad_matrix2)
    ##np.savetxt('x_dist.txt', dist_x, fmt='%.3f')
    #for i in range(1, dim):
	#diag_x = dist_x.diagonal(offset=i)
	#diag_y = dist_y.diagonal(offset=i)
	#diag_z = dist_z.diagonal(offset=i)
	#diag_cov = cov_dist_matrix.diagonal(offset=i)
	#diag_x = diag_x*diag_x.T
	#diag_y = diag_y*diag_y.T
	#diag_z = diag_z*diag_z.T
	#diag_cov = diag_cov*diag_cov
	#x_pow = x_pow+np.diag(diag_x, k=i)
	#y_pow = y_pow+np.diag(diag_y, k=i)
	#z_pow = z_pow+np.diag(diag_z, k=i)
	#cov_dist_pow_matrix = cov_dist_pow_matrix+np.diag(diag_cov, k=i)
    ##np.savetxt('x_square.txt', x_pow, fmt='%.3f')
    #pow_matrix = x_pow + y_pow + z_pow

def generate_bonds(atoms):
    """ Make calculations for the bonds, this part of the code must be more efficient.
    """
    bonds_list = []
    #print 'BEGINS TO CALCULATE DISTANCES'
    #arr1 = np.array([0, 0, 1])
    #for i in range(len(atoms)-1):
	#for j in range(i+1, len(atoms)):
	    #if get_euclidean(atoms[i].pos, atoms[j].pos) <= (atoms[i].cov_rad + atoms[j].cov_rad):
		#arr2 = unit_vector(atoms[j].pos - atoms[i].pos)
		#angle = get_angle(arr1, arr2)
		#vec_o = np.cross(arr1, arr2)
		#length = get_euclidean(atoms[i].pos, atoms[j].pos)
		#bond = (atoms[i], length, angle, vec_o)
		#bonds_list.append(bond)
    #print 'ENDS!'
    print 'BEGINS TO CALCULATE DISTANCES'
    arr1 = np.array([0, 0, 1])
    for i in range(len(atoms)-1):
	if i+20>=len(atoms):
	    limit = len(atoms)
	else:
	    limit = i+20
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
    print 'ENDS!'
    return bonds_list

def generate_ribbons(backbone):
    """ Calculates the distances and angles for the ribbon representation.
    """
    arr1 = np.array([0, 0, 1])
    ribbon_list = []
    for i in range(len(backbone)-1):
	arr2 = unit_vector(backbone[i+1].pos - backbone[i].pos)
	angle = get_angle(arr1, arr2)
	vec_o = np.cross(arr1, arr2)
	length = get_euclidean(backbone[i].pos, backbone[i+1].pos)
	temp = (backbone[i], length, angle, vec_o)
	ribbon_list.append(temp)
    ribbon_list.append((backbone[-1], 0, 0, [0,0,0]))
    return ribbon_list

def get_mass_center(atoms):
    """ Returns the mass center of a molecule.
    """
    mass_c = np.zeros(3)
    for atom in atoms:
	mass_c += atom.pos
    mass_c /= len(atoms)
    return mass_c

def get_euclidean(pa, pb):
    """ Returns the distance between two points in R3
    """
    import math
    if len(pa) == 1:
	pa = [pa[0], 0, 0]
    if len(pa) == 2:
	pa = [pa[0], pa[1], 0]
    if len(pb) == 1:
	pb = [pb[0], 0, 0]
    if len(pb) == 2:
	pb = [pb[0], pb[1], 0]
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
















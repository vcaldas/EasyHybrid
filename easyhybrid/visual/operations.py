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

def get_bonds(atom_matrix):
    """
    """
    x_pos = atom_matrix[:,0]
    y_pos = atom_matrix[:,1]
    z_pos = atom_matrix[:,2]
    dim = len(x_pos)
    x_matrix1 = np.zeros((dim, dim))
    x_matrix2 = np.zeros((dim, dim))
    y_matrix1 = np.zeros((dim, dim))
    y_matrix2 = np.zeros((dim, dim))
    z_matrix1 = np.zeros((dim, dim))
    z_matrix2 = np.zeros((dim, dim))
    x_matrix1[:] = x_pos
    x_matrix2[:] = x_matrix1.T
    y_matrix1[:] = y_pos
    y_matrix2[:] = y_matrix1.T
    z_matrix1[:] = z_pos
    z_matrix2[:] = z_matrix1.T
    #print x_matrix1, '<-- matriz X1'
    #print x_matrix2, '<-- matriz X2'
    dist_x = np.triu(x_matrix1-x_matrix2)
    dist_y = np.triu(y_matrix1-y_matrix2)
    dist_z = np.triu(z_matrix1-z_matrix2)
    print dist_x, '<-- dist en x'
























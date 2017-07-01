#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  shapes.py
#  
#  Copyright 2016 Carlos Eduardo Sequeiros Borja <casebor@gmail.com>
#  
#  This program is free software, you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY, without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program, if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import numpy as np
import math, copy
import VISMOL.glCore.sphere_data as sphd
import VISMOL.glCore.cylinder_data as cyd
import VISMOL.glCore.matrix_operations as mop

def get_cube(center, r):
    """ Generates the vertex of a cube for using the 
        GL_TRIANGLES_STRIP option in opengl.
        
        Keyword arguments:
        center -- The center of the cube
        r -- Distance of the center to the walls
    """
    assert(len(center)==3)
    assert(r>0)
    vertices = []
    vertices += [center[0]-r, center[1]+r, center[2]+r]
    vertices += [center[0]-r, center[1]+r, center[2]-r]
    vertices += [center[0]+r, center[1]+r, center[2]-r]
    vertices += [center[0]-r, center[1]-r, center[2]-r]
    vertices += [center[0]+r, center[1]-r, center[2]-r]
    vertices += [center[0]+r, center[1]-r, center[2]+r]
    vertices += [center[0]+r, center[1]+r, center[2]-r]
    vertices += [center[0]+r, center[1]+r, center[2]+r]
    vertices += [center[0]-r, center[1]+r, center[2]+r]
    vertices += [center[0]+r, center[1]-r, center[2]+r]
    vertices += [center[0]-r, center[1]-r, center[2]+r]
    vertices += [center[0]-r, center[1]-r, center[2]-r]
    vertices += [center[0]-r, center[1]+r, center[2]+r]
    vertices += [center[0]-r, center[1]+r, center[2]-r]
    vertices = np.array(vertices,dtype=np.float32)
    return vertices

def get_icosahedron(radius):
    """ A radius circumscribed to it has the radius:
            rad = (edge/4)*sqrt(10+2*sqrt(5))
        Fixed value of sqrt(10+2*sqrt(5)) to 3.804226065180614
        Then one edge of the icosahedron is equal to '2b'
        and the distance of the center to one edge is 'a'.
        Now we can get all the vertices with the form:
            {[+-a,+-b,0.0],[0.0,+-a,+-b],[+-a,0.0,+-b]}
    """
    assert(radius>0.0)
    val = 3.804226065180614
    b = 2*radius/val
    a = math.sqrt(radius*radius-b*b)
    vertices = np.array([ 0,  a,  b,
                          0,  a, -b,
                          0, -a,  b,
                          0, -a, -b,
                         -b,  0,  a,
                          b,  0,  a,
                         -b,  0, -a,
                          b,  0, -a,
                         -a,  b,  0,
                         -a, -b,  0,
                          a,  b,  0,
                          a, -b,  0],dtype=np.float32)
    triangles = np.array([ 0, 4, 5, 0, 5,10, 0,10, 1, 0, 1, 8,
                           0, 8, 4, 3, 6, 7, 3, 6, 9, 3, 9, 2,
                           3, 2,11, 3,11, 7, 4, 2, 5, 5,11,10,
                           1,10, 7, 1, 6, 8, 8, 9, 4, 7, 6, 1,
                           6, 9, 8, 2, 4, 9, 2,11, 5,10,11, 7],dtype=np.uint32)
    return vertices, triangles

def get_sphere(pos, rad, color, level='level_1'):
    """ Function doc
    """
    vertices = copy.copy(sphd.sphere_vertices[level])
    indices = copy.copy(sphd.sphere_triangles[level])
    colors = np.array(color*len(vertices),dtype=np.float32)
    for i in range(int(len(vertices)/3)):
        vertices[i*3:(i+1)*3] = (vertices[i*3:(i+1)*3] * rad) + pos
    return vertices, indices, colors

def get_cylinder(pos, color, angle, vec_dir, length, stacks, radius=0.5, level='level_0'):
    """ Function doc
    """
    assert(stacks>1)
    assert(length>0.0)
    assert(angle>=0.0)
    verts = copy.copy(cyd.cylinder_vertices[level])
    verts2 = copy.copy(cyd.cylinder_vertices2[level])
    inds = copy.copy(cyd.cylinder_triangles[level])
    vertices = np.array([],dtype=np.float32)
    normals = np.array([],dtype=np.float32)
    indices = np.array([],dtype=np.uint16)
    colors = np.array(color*int(len(verts)/3)*stacks,dtype=np.float32)
    to_add_pos = length/float(stacks-1)
    rot_mat = mop.my_glRotatef(np.identity(4, dtype=np.float32), angle, vec_dir)[:3,:3]
    to_add_ind = int(len(inds))/6
    verts *= radius
    verts2 *= radius
    zeros = np.zeros(int(len(verts)),dtype=np.float32)
    for i in range(stacks):
        if i%2==0:
            vertices = np.append(vertices, verts)
        else:
            vertices = np.append(vertices, verts2)
        normals = np.append(normals, zeros)
        for j in range(1, int(len(verts)), 3):
            vertices[j+i*int(len(verts))] += i*to_add_pos
            normals[j+i*int(len(verts))] += i*to_add_pos
            # Rotation of points and Translation at the end
            x, y, z = vertices[j+i*len(verts)-1:j+i*int(len(verts))+2]
            vertices[j+i*int(len(verts))-1] = x*rot_mat[0,0] + y*rot_mat[0,1] + z*rot_mat[0,2] + pos[0]
            vertices[j+i*int(len(verts))] = x*rot_mat[1,0] + y*rot_mat[1,1] + z*rot_mat[1,2] + pos[1]
            vertices[j+i*int(len(verts))+1] = x*rot_mat[2,0] + y*rot_mat[2,1] + z*rot_mat[2,2] + pos[2]
            # Rotation of normals and Translation at the end
            x, y, z = normals[j+i*len(verts)-1:j+i*len(verts)+2]
            normals[j+i*int(len(verts))-1] = x*rot_mat[0,0] + y*rot_mat[0,1] + z*rot_mat[0,2] + pos[0]
            normals[j+i*int(len(verts))] = x*rot_mat[1,0] + y*rot_mat[1,1] + z*rot_mat[1,2] + pos[1]
            normals[j+i*int(len(verts))+1] = x*rot_mat[2,0] + y*rot_mat[2,1] + z*rot_mat[2,2] + pos[2]
        if i>0:
            indices = np.append(indices, inds)
            for k in range(int(len(inds))):
                indices[k+(i-1)*int(len(inds))] += (i-1)*to_add_ind
    return vertices, indices, colors, normals























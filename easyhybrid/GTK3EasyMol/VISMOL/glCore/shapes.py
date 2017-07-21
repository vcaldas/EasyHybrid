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
import ctypes
from OpenGL import GL

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

def make_gl_dots(program, atom_list, bckgrnd_color=[0.0,0.0,0.0,1.0]):
    """ Function doc
    """
    coords = []
    colors = []
    dot_sizes = []
    for atom in atom_list:
        coords = np.hstack((coords, atom.pos))
        colors = np.hstack((colors, atom.color))
        dot_sizes.append(atom.vdw_rad)
    coords = np.array(coords, dtype=np.float32)
    colors = np.array(colors, dtype=np.float32)
    dot_sizes = np.array(dot_sizes, dtype=np.float32)
    dot_qtty = int(len(coords)/3)
    bckgrnd_color = [bckgrnd_color[0],bckgrnd_color[1],
                     bckgrnd_color[2],bckgrnd_color[3]]*dot_qtty
    bckgrnd_color = np.array(bckgrnd_color, dtype=np.float32)
    
    indexes = []
    for i in range(dot_qtty):
        indexes.append(i)
    indexes = np.array(indexes,dtype=np.uint16)
    
    vao = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vao)
    
    ind_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.itemsize*int(len(indexes)), indexes, GL.GL_DYNAMIC_DRAW)
    
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*int(len(coords)), coords, GL.GL_STATIC_DRAW)
    att_position = GL.glGetAttribLocation(program, 'vert_coord')
    GL.glEnableVertexAttribArray(att_position)
    GL.glVertexAttribPointer(att_position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*int(len(colors)), colors, GL.GL_STATIC_DRAW)
    att_colors = GL.glGetAttribLocation(program, 'vert_color')
    GL.glEnableVertexAttribArray(att_colors)
    GL.glVertexAttribPointer(att_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    dot_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, dot_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, dot_sizes.itemsize*len(dot_sizes), dot_sizes, GL.GL_STATIC_DRAW)
    att_size = GL.glGetAttribLocation(program, 'vert_dot_size')
    GL.glEnableVertexAttribArray(att_size)
    GL.glVertexAttribPointer(att_size, 1, GL.GL_FLOAT, GL.GL_FALSE, dot_sizes.itemsize, ctypes.c_void_p(0))
    
    bckgrnd_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, bckgrnd_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, bckgrnd_color.itemsize*len(bckgrnd_color), bckgrnd_color, GL.GL_STATIC_DRAW)
    att_bck_color = GL.glGetAttribLocation(program, 'bckgrnd_color')
    GL.glEnableVertexAttribArray(att_bck_color)
    GL.glVertexAttribPointer(att_bck_color, 4, GL.GL_FLOAT, GL.GL_FALSE, 4*bckgrnd_color.itemsize, ctypes.c_void_p(0))
    
    #vao_list.append(vao)
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(att_position)
    GL.glDisableVertexAttribArray(att_colors)
    GL.glDisableVertexAttribArray(att_size)
    GL.glDisableVertexAttribArray(att_bck_color)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
    
    return vao, (ind_vbo, coord_vbo, col_vbo)

def make_gl_lines(program, bond_list, atom_list):
    """ Function doc
    """
    coords = []
    colors = []
    for bond in bond_list:
        coords = np.hstack((coords, atom_list[bond[0]].pos))
        coords = np.hstack((coords, atom_list[bond[1]].pos))
        colors = np.hstack((colors, atom_list[bond[0]].color))
        colors = np.hstack((colors, atom_list[bond[1]].color))
    
    coords = np.array(coords, dtype=np.float32)
    colors = np.array(colors, dtype=np.float32)
    
    indexes = []
    for i in range(int(len(coords)/3)):
        indexes.append(i)
    indexes = np.array(indexes,dtype=np.uint16)
    
    vao = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vao)
    
    ind_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.itemsize*int(len(indexes)), indexes, GL.GL_DYNAMIC_DRAW)
    
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*int(len(coords)), coords, GL.GL_STATIC_DRAW)
    att_position = GL.glGetAttribLocation(program, 'vert_coord')
    GL.glEnableVertexAttribArray(att_position)
    GL.glVertexAttribPointer(att_position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*int(len(colors)), colors, GL.GL_STATIC_DRAW)
    att_colors = GL.glGetAttribLocation(program, 'vert_color')
    GL.glEnableVertexAttribArray(att_colors)
    GL.glVertexAttribPointer(att_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    #vao_list.append(vao)
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(att_position)
    GL.glDisableVertexAttribArray(att_colors)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
    
    return vao, (ind_vbo, coord_vbo, col_vbo)


def _make_gl_dots(program, vismol_object = None, bckgrnd_color= [0.0,0.0,0.0,1.0]):
    """ Function doc
    """
    #coords       = []
    #colors       = []
    #dot_sizes    = []
    #bckgrnd_color=[0.0,0.0,0.0,1.0]
    #
    #for atom in atom_list:
    #    coords = np.hstack((coords, atom.pos))
    #    colors = np.hstack((colors, atom.color))
    #    dot_sizes.append(atom.vdw_rad)
    #
    #coords = np.array(coords, dtype=np.float32)
    #colors = np.array(colors, dtype=np.float32)
    
    
    #dot_sizes = np.array(dot_sizes, dtype=np.float32)
    
    #coords
    colors    = vismol_object.colors
    dot_sizes = vismol_object.vdw_dot_sizes
    coords    = vismol_object.frames[0]
    
    dot_qtty = int(len(coords)/3)
    bckgrnd_color = [bckgrnd_color[0],bckgrnd_color[1],
                     bckgrnd_color[2],bckgrnd_color[3]]*dot_qtty
    bckgrnd_color = np.array(bckgrnd_color, dtype=np.float32)
    
    indexes = []
    for i in range(dot_qtty):
        indexes.append(i)
    indexes = np.array(indexes,dtype=np.uint16)
    
    vao = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vao)
    
    ind_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.itemsize*int(len(indexes)), indexes, GL.GL_DYNAMIC_DRAW)
    
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*int(len(coords)), coords, GL.GL_STATIC_DRAW)
    att_position = GL.glGetAttribLocation(program, 'vert_coord')
    GL.glEnableVertexAttribArray(att_position)
    GL.glVertexAttribPointer(att_position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*int(len(colors)), colors, GL.GL_STATIC_DRAW)
    att_colors = GL.glGetAttribLocation(program, 'vert_color')
    GL.glEnableVertexAttribArray(att_colors)
    GL.glVertexAttribPointer(att_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    dot_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, dot_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, dot_sizes.itemsize*len(dot_sizes), dot_sizes, GL.GL_STATIC_DRAW)
    att_size = GL.glGetAttribLocation(program, 'vert_dot_size')
    GL.glEnableVertexAttribArray(att_size)
    GL.glVertexAttribPointer(att_size, 1, GL.GL_FLOAT, GL.GL_FALSE, dot_sizes.itemsize, ctypes.c_void_p(0))
    
    bckgrnd_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, bckgrnd_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, bckgrnd_color.itemsize*len(bckgrnd_color), bckgrnd_color, GL.GL_STATIC_DRAW)
    att_bck_color = GL.glGetAttribLocation(program, 'bckgrnd_color')
    GL.glEnableVertexAttribArray(att_bck_color)
    GL.glVertexAttribPointer(att_bck_color, 4, GL.GL_FLOAT, GL.GL_FALSE, 4*bckgrnd_color.itemsize, ctypes.c_void_p(0))
    
    #vao_list.append(vao)
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(att_position)
    GL.glDisableVertexAttribArray(att_colors)
    GL.glDisableVertexAttribArray(att_size)
    GL.glDisableVertexAttribArray(att_bck_color)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
    
    vismol_object.dots_vao      = vao
    vismol_object.dot_buffers   = (ind_vbo, coord_vbo, col_vbo)
    #vismol_object.dot_vao       = vao      
    #vismol_object.dot_ind_vbo   = ind_vbo  
    #vismol_object.dot_coord_vbo = coord_vbo
    #vismol_object.dot_col_vbo   = col_vbo  
    return True




def _make_gl_lines(program, vismol_object = None):
    """ Function doc
    """
    #coords = []
    #colors = []
    #
    ##for bond in vismol_object.index_bonds[0]:
    #
    #for bond in vismol_object.index_bonds:
    ###for bond in bond_list:
    #    coords = np.hstack((coords, vismol_object.atoms[bond[0]].pos))
    #    coords = np.hstack((coords, vismol_object.atoms[bond[1]].pos))
    #    colors = np.hstack((colors, vismol_object.atoms[bond[0]].color))
    #    colors = np.hstack((colors, vismol_object.atoms[bond[1]].color))
    #
    #coords = np.array(coords, dtype=np.float32)
    #colors = np.array(colors, dtype=np.float32)
    
    #coords = vismol_object.frames[0]
    #colors = vismol_object.colors
    
    
    #indexes = []
    #for i in range(int(len(coords)/3)):
    #    indexes.append(i)
    #indexes = np.array(indexes,dtype=np.uint16)
    
    indexes = np.array(vismol_object.index_bonds,dtype=np.uint16)
    coords  = vismol_object.frames[0]
    colors  = vismol_object.colors
    
    vao = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vao)
    
    ind_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.itemsize*int(len(indexes)), indexes, GL.GL_DYNAMIC_DRAW)
    
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*int(len(coords)), coords, GL.GL_STATIC_DRAW)
    att_position = GL.glGetAttribLocation(program, 'vert_coord')
    GL.glEnableVertexAttribArray(att_position)
    GL.glVertexAttribPointer(att_position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*int(len(colors)), colors, GL.GL_STATIC_DRAW)
    att_colors = GL.glGetAttribLocation(program, 'vert_color')
    GL.glEnableVertexAttribArray(att_colors)
    GL.glVertexAttribPointer(att_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    #vao_list.append(vao)
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(att_position)
    GL.glDisableVertexAttribArray(att_colors)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
    
    
    vismol_object.lines_vao      = vao
    vismol_object.line_buffers   = (ind_vbo, coord_vbo, col_vbo)
    #return vao, (ind_vbo, coord_vbo, col_vbo)






    
    
    #return vao, (ind_vbo, coord_vbo, col_vbo)





    #def make_gl_dot_sphere(self, program, atom_list, vao_list):
        #""" Function doc
        #"""
        #for atom in atom_list:
            #vertices, indexes, colors = shapes.get_sphere(atom.pos, atom.cov_rad, atom.color, level='level_2')
            #vao = GL.glGenVertexArrays(1)
            #GL.glBindVertexArray(vao)
            #atom.vertices = int(len(vertices)/3)
            
            #vert_vbo = GL.glGenBuffers(1)
            #GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vert_vbo)
            #GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.itemsize*int(len(vertices)), vertices, GL.GL_STATIC_DRAW)
            
            #att_position = GL.glGetAttribLocation(program, 'coordinate')
            #GL.glEnableVertexAttribArray(att_position)
            #GL.glVertexAttribPointer(att_position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*vertices.itemsize, ctypes.c_void_p(0))
            
            #col_vbo = GL.glGenBuffers(1)
            #GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
            #GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*int(len(colors)), colors, GL.GL_STATIC_DRAW)
            
            #att_colors = GL.glGetAttribLocation(program, 'vert_color')
            #GL.glEnableVertexAttribArray(att_colors)
            #GL.glVertexAttribPointer(att_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
            
            #vao_list.append(vao)
            #GL.glBindVertexArray(0)
            #GL.glDisableVertexAttribArray(att_position)
            #GL.glDisableVertexAttribArray(att_colors)
            #GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
            #GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
    
    #def make_gl_sphere(self, program, atom_list, vao_list, covalent=True):
        #""" Function doc
        #"""
        #for atom in atom_list:
            #if covalent:
                #vertices, indexes, colors = shapes.get_sphere(atom.pos, atom.cov_rad, atom.color, level='level_2')
            #else:
                #vertices, indexes, colors = shapes.get_sphere(atom.pos, atom.ball_radius, atom.color, level='level_2')
            #centers = [atom.pos[0],atom.pos[1],atom.pos[2]]*int(len(indexes))
            #centers = np.array(centers,dtype=np.float32)
            #vao = GL.glGenVertexArrays(1)
            #GL.glBindVertexArray(vao)
            #atom.triangles = int(len(indexes))
            
            #ind_vbo = GL.glGenBuffers(1)
            #GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
            #GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.itemsize*int(len(indexes)), indexes, GL.GL_STATIC_DRAW)
        
            #vert_vbo = GL.glGenBuffers(1)
            #GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vert_vbo)
            #GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.itemsize*int(len(vertices)), vertices, GL.GL_STATIC_DRAW)
            
            #att_position = GL.glGetAttribLocation(program, 'coordinate')
            #GL.glEnableVertexAttribArray(att_position)
            #GL.glVertexAttribPointer(att_position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*vertices.itemsize, ctypes.c_void_p(0))
        
            #center_vbo = GL.glGenBuffers(1)
            #GL.glBindBuffer(GL.GL_ARRAY_BUFFER, center_vbo)
            #GL.glBufferData(GL.GL_ARRAY_BUFFER, centers.itemsize*int(len(centers)), centers, GL.GL_STATIC_DRAW)
            
            #att_center = GL.glGetAttribLocation(program, 'center')
            #GL.glEnableVertexAttribArray(att_center)
            #GL.glVertexAttribPointer(att_center, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*centers.itemsize, ctypes.c_void_p(0))
            
            #col_vbo = GL.glGenBuffers(1)
            #GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
            #GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*int(len(colors)), colors, GL.GL_STATIC_DRAW)
            
            #att_colors = GL.glGetAttribLocation(program, 'vert_color')
            #GL.glEnableVertexAttribArray(att_colors)
            #GL.glVertexAttribPointer(att_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
            
            #vao_list.append(vao)
            #GL.glBindVertexArray(0)
            #GL.glDisableVertexAttribArray(att_position)
            #GL.glDisableVertexAttribArray(att_colors)
            #GL.glDisableVertexAttribArray(att_center)
            #GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
            #GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
    
    #def make_gl_cylinder(self, program, bond_list, vao_list, ribbon=True):
        #""" Function doc
        #"""
        #for bond in bond_list:
            #if ribbon:
                #vertices, indexes, colors, normals = shapes.get_cylinder(bond[0].pos,bond[0].color,bond[2],bond[3],bond[1],10,radius=0.2,level='level_6')
                #self.ribbon_indexes = int(len(indexes))
            #else:
                #vertices, indexes, colors, normals = shapes.get_cylinder(bond[0].pos,bond[0].color,bond[2],bond[3],bond[1],10,radius=0.1,level='level_6')
                #self.stick_indexes = int(len(indexes))
            #vao = GL.glGenVertexArrays(1)
            #GL.glBindVertexArray(vao)
            
            #ind_vbo = GL.glGenBuffers(1)
            #GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
            #GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.itemsize*int(len(indexes)), indexes, GL.GL_STATIC_DRAW)
            
            #vert_vbo = GL.glGenBuffers(1)
            #GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vert_vbo)
            #GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.itemsize*int(len(vertices)), vertices, GL.GL_STATIC_DRAW)
            
            #att_position = GL.glGetAttribLocation(program, 'coordinate')
            #GL.glEnableVertexAttribArray(att_position)
            #GL.glVertexAttribPointer(att_position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*vertices.itemsize, ctypes.c_void_p(0))
            
            #center_vbo = GL.glGenBuffers(1)
            #GL.glBindBuffer(GL.GL_ARRAY_BUFFER, center_vbo)
            #GL.glBufferData(GL.GL_ARRAY_BUFFER, normals.itemsize*int(len(normals)), normals, GL.GL_STATIC_DRAW)
            
            #att_center = GL.glGetAttribLocation(program, 'center')
            #GL.glEnableVertexAttribArray(att_center)
            #GL.glVertexAttribPointer(att_center, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*normals.itemsize, ctypes.c_void_p(0))
            
            #col_vbo = GL.glGenBuffers(1)
            #GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
            #GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*int(len(colors)), colors, GL.GL_STATIC_DRAW)
            
            #att_colors = GL.glGetAttribLocation(program, 'vert_color')
            #GL.glEnableVertexAttribArray(att_colors)
            #GL.glVertexAttribPointer(att_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
            
            #vao_list.append(vao)
            #GL.glBindVertexArray(0)
            #GL.glDisableVertexAttribArray(att_position)
            #GL.glDisableVertexAttribArray(att_colors)
            #GL.glDisableVertexAttribArray(att_center)
            #GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
            #GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
    













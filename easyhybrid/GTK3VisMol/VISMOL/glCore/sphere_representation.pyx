#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  sphere_representation.pyx
#  
#  Copyright 2018 Carlos Eduardo Sequeiros Borja <casebor@gmail.com>
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

import cython
import numpy as np
cimport numpy as np
import ctypes, time
from OpenGL import GL
import VISMOL.glCore.sphere_data as sphd

class SphereRepresentation:
    """ Class doc """
    
    def __init__(self, vismol_object = None, level = 'level_0'):
        """ Class initialiser """
        self.vismol_object = vismol_object
        self.level = level
        self.number_of_frames = 0
        self.coords = None
        self.colors = None
        self.centers = None
        self.indexes = None
    
    def _make_gl_spheres(self, program):
        """ Function doc """
        init = time.time()
        qtty = int(len(self.vismol_object.atoms))
        nucleus = [0.0, 0.0, 0.0]*qtty
        colores = [0.0, 0.0, 0.0]*qtty
        cdef Py_ssize_t a, i
        coords = sphd.sphere_vertices[self.level]*qtty
        centers = sphd.sphere_vertices[self.level]*qtty
        colors = sphd.sphere_vertices[self.level]*qtty
        indexes = np.array(sphd.sphere_triangles[self.level]*qtty, dtype=np.uint32)
        elems = int(len(sphd.sphere_vertices[self.level])/3)
        offset = int(len(sphd.sphere_vertices[self.level]))
        inds_e = int(len(sphd.sphere_triangles[self.level]))
        for a,atom in enumerate(self.vismol_object.atoms):
            colors[a*offset:(a+1)*offset] = [atom.color[0],atom.color[1],atom.color[2]]*elems
            centers[a*offset:(a+1)*offset] = [atom.pos[0],atom.pos[1],atom.pos[2]]*elems
            for i in range(elems):
                coords[a*offset+i*3] *= atom.radius
                coords[a*offset+i*3+1] *= atom.radius
                coords[a*offset+i*3+2] *= atom.radius
                coords[a*offset+i*3] += atom.pos[0]
                coords[a*offset+i*3+1] += atom.pos[1]
                coords[a*offset+i*3+2] += atom.pos[2]
            indexes[a*inds_e:(a+1)*inds_e] += a*elems
        end = time.time()
        print('Time used creating nucleus, vertices and colors:', end-init)
        self.coords = np.array(coords, dtype=np.float32)
        self.centers = np.array(centers, dtype=np.float32)
        self.colors = np.array(colors, dtype=np.float32)
        self.indexes = indexes
        
        #init = time.time()
        #qtty = int(len(self.vismol_object.atoms))
        #nucleus = [0.0, 0.0, 0.0]*qtty
        #colores = [0.0, 0.0, 0.0]*qtty
        #cdef Py_ssize_t a, i, j
        #for a,atom in enumerate(self.vismol_object.atoms):
            #nucleus[a*3] = atom.pos[0]
            #nucleus[a*3+1] = atom.pos[1]
            #nucleus[a*3+2] = atom.pos[2]
            #colores[a*3] = atom.color[0]
            #colores[a*3+1] = atom.color[1]
            #colores[a*3+2] = atom.color[2]
        #end = time.time()
        #print('Time used creating nucleus and colors:', end-init)
        #init = time.time()
        #for i,atom in enumerate(self.vismol_object.atoms):
            #crds = np.copy(sphd.sphere_vertices[self.level])
            #inds = np.copy(sphd.sphere_triangles[self.level])
            #offset = int(len(crds)/3)
            #cols = np.array(colores[i*3:(i+1)*3]*offset, dtype=np.float32)
            #cnts = np.array(nucleus[i*3:(i+1)*3]*offset, dtype=np.float32)
            #for j in range(offset):
                #crds[j*3] = crds[j*3]*atom.radius + nucleus[i*3]
                #crds[j*3+1] = crds[j*3+1]*atom.radius + nucleus[i*3+1]
                #crds[j*3+2] = crds[j*3+2]*atom.radius + nucleus[i*3+2]
            #inds += i*offset
            #self.coords = np.concatenate((self.coords, crds))
            #self.centers = np.concatenate((self.centers, cnts))
            #self.colors = np.concatenate((self.colors, cols))
            #self.indexes = np.concatenate((self.indexes, inds))
        #end = time.time()
        #print('Time used creating vertices and calculating:', end-init)
        
        #self.coords = np.array(coords, dtype=np.float32)
        #self.centers = np.array(centers, dtype=np.float32)
        #self.colors = np.array(colors, dtype=np.float32)
        #self.indexes = np.array(indexes, dtype=np.uint32)
        
        vertex_array_object = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vertex_array_object)
        
        ind_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, self.indexes.itemsize*int(len(self.indexes)), self.indexes, GL.GL_DYNAMIC_DRAW)
        
        coord_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.coords.itemsize*len(self.coords), self.coords, GL.GL_STATIC_DRAW)
        gl_coord = GL.glGetAttribLocation(program, 'vert_coord')
        GL.glEnableVertexAttribArray(gl_coord)
        GL.glVertexAttribPointer(gl_coord, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*self.coords.itemsize, ctypes.c_void_p(0))
        
        centr_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, centr_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.centers.itemsize*len(self.centers), self.centers, GL.GL_STATIC_DRAW)
        gl_center = GL.glGetAttribLocation(program, 'vert_centr')
        GL.glEnableVertexAttribArray(gl_center)
        GL.glVertexAttribPointer(gl_center, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*self.centers.itemsize, ctypes.c_void_p(0))
        
        col_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.colors.itemsize*len(self.colors), self.colors, GL.GL_STATIC_DRAW)
        gl_colors = GL.glGetAttribLocation(program, 'vert_color')
        GL.glEnableVertexAttribArray(gl_colors)
        GL.glVertexAttribPointer(gl_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*self.colors.itemsize, ctypes.c_void_p(0))
        
        GL.glBindVertexArray(0)
        GL.glDisableVertexAttribArray(gl_coord)
        GL.glDisableVertexAttribArray(gl_center)
        GL.glDisableVertexAttribArray(gl_colors)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        self.spheres_vao = vertex_array_object
        self.spheres_buffers = (ind_vbo, coord_vbo, col_vbo)
        self.triangles = int(len(self.indexes))
        return True
    

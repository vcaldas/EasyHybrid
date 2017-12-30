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



class SphereRepresentation:
    """ Class doc """
    
    def __init__ (self, vismol_object = None,  level = 'level_0'):
        """ Class initialiser """
        self.vismol_object = vismol_object
        self.level = level
        #self.vertices = []
        #self.triangles  = []
        
        #self.sphere_vertices       = sphd.sphere_vertices [level]
        #self.sphere_triangles      = sphd.sphere_triangles[level]
        #self.number_of_vertices    = len(self.sphere_vertices)
        
        self.number_of_frames      = 0

    #def build_sphere_frames_from_coordinates_frames (self, frames = []):    
        #""" Function doc """
        
        #for coords in frames:
            #full_sphere_vertices  = []          
            
            #for i in range(0,len(coords),3):
                
                #for vertice in self.sphere_vertices:
                    
                    #full_sphere_vertices.append(vertice+coords[i])
                    #full_sphere_vertices.append(vertice+coords[i+1])
                    #full_sphere_vertices.append(vertice+coords[i+2])
            
            #full_sphere_vertices = np.array(full_sphere_vertices ,dtype=np.float32)
            #self.sphere_vertices_frames.append(full_sphere_vertices)
            #self.number_of_frames += 1
    
    
    #def build_sphere_triangles (self, natoms):    
        #number_of_vertices   = len(self.sphere_triangles)
        #self.full_sphere_triangles = []
        #for i in range(natoms):
            #for index in self.sphere_triangles:
                #self.full_sphere_triangles.append(index+i*number_of_vertices)
        
        #self.full_sphere_triangles = np.array(self.full_sphere_triangles,dtype=np.uint32)            
    
    #def set_sphere_level (self, level ):
        #""" Function doc """
        #self.sphere_vertices       = sphd.sphere_vertices [level]
        #self.sphere_triangles      = sphd.sphere_triangles[level]
        #self.number_of_vertices    = len(sphere_vertices)



    #def _make_gl_true_spheres (self, shader_program):
        #""" Function doc """
        ##'''
        ##-------------------------------------------------------------------------------
        ##                               simpleSphere
        ##------------------------------------------------------------------------------- 
        #natoms = int(len(self.vismol_object.atoms))

        ##if self.sphere_vertices_frames == []:
        ##    self.build_sphere_frames_from_coordinates_frames (self.vismol_object.frames)
        ##
        ##if self.number_of_vertices == []:
        ##    self.build_sphere_triangles (natoms)
        
        
        ##self.sphere_vertices       = sphd.sphere_vertices [level]
        ##self.sphere_triangles      = sphd.sphere_triangles[level]
        
        
        
        
        #colors    = self.vismol_object.colors
        ##coords    = self.sphere_vertices_frames[0]
        ##indexes   = np.array(self.full_sphere_triangles,dtype=np.uint32) 
        
        
        #coords    = sphd.sphere_vertices ['level_1']
        #indexes   = sphd.sphere_triangles['level_1']
        #colors    = [0.,1.,1.]*int(len(coords))
        #colors    = np.array(colors, dtype=np.float32)

        
        #self.coords  = coords
        #self.indexes = indexes
        
        #vao = GL.glGenVertexArrays(1)
        #GL.glBindVertexArray(vao)
        #ind_vbo = GL.glGenBuffers(1)
        
        #GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
        #GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.itemsize*int(len(indexes)), indexes, GL.GL_DYNAMIC_DRAW)
        
        #coord_vbo = GL.glGenBuffers(1)
        #GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
        #GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*int(len(coords)), coords, GL.GL_STATIC_DRAW)
        #att_position = GL.glGetAttribLocation(shader_program, 'vert_coord')
        #GL.glEnableVertexAttribArray(att_position)
        #GL.glVertexAttribPointer(att_position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
        
        ##ol_vbo = None
        #col_vbo = GL.glGenBuffers(1)
        #GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
        #GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*int(len(colors)), colors, GL.GL_STATIC_DRAW)
        #att_colors = GL.glGetAttribLocation(shader_program, 'vert_color')
        #GL.glEnableVertexAttribArray(att_colors)
        #GL.glVertexAttribPointer(att_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
        
        ##vao_list.append(vao)
        #GL.glBindVertexArray(0)
        #GL.glDisableVertexAttribArray(att_position)
        #GL.glDisableVertexAttribArray(att_colors)
        #GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        #GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
        
        #self.spheres_vao             = vao
        #self.spheres_buffers         = (ind_vbo, coord_vbo, col_vbo)
        
        ##vismol_object.lines_vao      = vao
        ##vismol_object.line_buffers   = (ind_vbo, coord_vbo, col_vbo)
        #return True
    
    def _make_gl_true_spheres(self, program):
        """ Function doc """
        qtty = int(len(self.vismol_object.atoms))
        nucleus = [0.0, 0.0 ,0.0]*qtty
        colores = [0.0, 0.0, 0.0]*qtty
        for a,atom in enumerate(self.vismol_object.atoms):
            nucleus[a*3:(a+1)*3] = atom.pos[0:3]
            colores[a*3:(a+1)*3] = atom.color[0:3]
        coords = np.array([], dtype=np.float32)
        centers = np.array([], dtype=np.float32)
        colors = np.array([], dtype=np.float32)
        indexes = np.array([], dtype=np.uint32)
        for i,atom in enumerate(self.vismol_object.atoms):
            crds = np.copy(sphd.sphere_vertices[self.level])
            inds = np.copy(sphd.sphere_triangles[self.level])
            offset = int(len(crds)/3)
            cols = np.array(colores[i*3:(i+1)*3]*offset, dtype=np.float32)
            cnts = np.array(nucleus[i*3:(i+1)*3]*offset, dtype=np.float32)
            for j in range(offset):
                crds[j*3] = crds[j*3]*atom.radius + nucleus[i*3]
                crds[j*3+1] = crds[j*3+1]*atom.radius + nucleus[i*3+1]
                crds[j*3+2] = crds[j*3+2]*atom.radius + nucleus[i*3+2]
            inds += i*offset
            coords = np.concatenate((coords, crds))
            centers = np.concatenate((centers, cnts))
            colors = np.concatenate((colors, cols))
            indexes = np.concatenate((indexes, inds))
        
        self.coords = np.array(coords, dtype=np.float32)
        self.centers = np.array(centers, dtype=np.float32)
        self.colors = np.array(colors, dtype=np.float32)
        self.indexes = np.array(indexes, dtype=np.uint32)
        
        vertex_array_object = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vertex_array_object)
        
        ind_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.itemsize*int(len(indexes)), indexes, GL.GL_DYNAMIC_DRAW)
        
        coord_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*len(coords), coords, GL.GL_STATIC_DRAW)
        gl_coord = GL.glGetAttribLocation(program, 'vert_coord')
        GL.glEnableVertexAttribArray(gl_coord)
        GL.glVertexAttribPointer(gl_coord, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
        
        centr_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, centr_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, centers.itemsize*len(centers), centers, GL.GL_STATIC_DRAW)
        gl_center = GL.glGetAttribLocation(program, 'vert_centr')
        GL.glEnableVertexAttribArray(gl_center)
        GL.glVertexAttribPointer(gl_center, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*centers.itemsize, ctypes.c_void_p(0))
        
        col_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*len(colors), colors, GL.GL_STATIC_DRAW)
        gl_colors = GL.glGetAttribLocation(program, 'vert_color')
        GL.glEnableVertexAttribArray(gl_colors)
        GL.glVertexAttribPointer(gl_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
        
        GL.glBindVertexArray(0)
        GL.glDisableVertexAttribArray(gl_coord)
        GL.glDisableVertexAttribArray(gl_center)
        GL.glDisableVertexAttribArray(gl_colors)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        
        self.spheres_vao = vertex_array_object
        self.spheres_buffers = (ind_vbo, coord_vbo, col_vbo)
        self.triangles = int(len(indexes))
        return True
    











def _make_gl_circles(program, vismol_object = None):
    """ Function doc
    """
    colors = vismol_object.colors
    coords = vismol_object.frames[0]
    dot_qtty = int(len(coords)/3)
    radios = [0.3] * dot_qtty
    radios = np.array(radios, dtype=np.float32)
    indexes = []
    for i in range(dot_qtty):
        indexes.append(i)
    indexes = np.array(indexes, dtype=np.uint32)
    
    vao = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vao)
    
    ind_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.itemsize*int(len(indexes)), indexes, GL.GL_DYNAMIC_DRAW)
    
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*len(coords), coords, GL.GL_STATIC_DRAW)
    gl_coord = GL.glGetAttribLocation(program, 'vert_coord')
    GL.glEnableVertexAttribArray(gl_coord)
    GL.glVertexAttribPointer(gl_coord, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*len(colors), colors, GL.GL_STATIC_DRAW)
    gl_color = GL.glGetAttribLocation(program, 'vert_color')
    GL.glEnableVertexAttribArray(gl_color)
    GL.glVertexAttribPointer(gl_color, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    rad_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, rad_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, radios.itemsize*len(radios), radios, GL.GL_STATIC_DRAW)
    gl_rad = GL.glGetAttribLocation(program, 'vert_rad')
    GL.glEnableVertexAttribArray(gl_rad)
    GL.glVertexAttribPointer(gl_rad, 1, GL.GL_FLOAT, GL.GL_FALSE, colors.itemsize, ctypes.c_void_p(0))
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(gl_coord)
    GL.glDisableVertexAttribArray(gl_color)
    GL.glDisableVertexAttribArray(gl_rad)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    
    vismol_object.circles_vao = vao
    vismol_object.circles_buffers = (ind_vbo, coord_vbo, col_vbo)
    return True

def _make_gl_non_bonded(program, vismol_object = None):
    """ Function doc
    """
    indexes = np.array(vismol_object.non_bonded_atoms, dtype=np.uint32)
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
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(att_position)
    GL.glDisableVertexAttribArray(att_colors)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
    
    vismol_object.non_bonded_vao = vao
    vismol_object.non_bonded_buffers = (ind_vbo, coord_vbo, col_vbo)
    return True

def _make_gl_cylinders(program, vismol_object = None):
    """ Function doc
    """
    indexes = np.array(vismol_object.index_bonds,dtype=np.uint32)
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
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(att_position)
    GL.glDisableVertexAttribArray(att_colors)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
    
    vismol_object.cylinders_vao = vao
    vismol_object.cylinders_buffers = (ind_vbo, coord_vbo, col_vbo)
    return True

def _make_gl_dots_surface(program, vismol_object = None):
    """ Function doc
    """
    colors = vismol_object.colors
    coords = vismol_object.frames[0]
    indexes = np.array(vismol_object.dot_indexes,dtype=np.uint32)
    
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
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(att_position)
    GL.glDisableVertexAttribArray(att_colors)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
    
    vismol_object.dots_surface_vao = vao
    vismol_object.dots_surface_buffers = (ind_vbo, coord_vbo, col_vbo)
    return True

def _make_gl_spheres(program, vismol_object = None):
    """ Function doc
    """
    colors  = vismol_object.colors
    coords  = vismol_object.frames[0]
    indexes = np.array(vismol_object.dot_indexes,dtype=np.uint32)
    
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
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(att_position)
    GL.glDisableVertexAttribArray(att_colors)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
    
    vismol_object.spheres_vao = vao
    vismol_object.spheres_buffers = (ind_vbo, coord_vbo, col_vbo)
    return True

def _make_gl_true_spheres (program, vismol_object = None, level = 'level_0'):
    """ Function doc """
    #'''
    #-------------------------------------------------------------------------------
    #                               simpleSphere
    #------------------------------------------------------------------------------- 

    #dot_sizes = vismol_object.vdw_dot_sizes
    #coords    = vismol_object.frames[0]
    #colors    = [0.,1.,1.]*int(len(coords)/3)
    #colors    = np.array(colors, dtype=np.float32)
    natoms    = int(len(coords)/3)
    colors    = vismol_object.colors

    sphere_vertices       = sphd.sphere_vertices [level]
    sphere_triangles      = sphd.sphere_triangles[level]
    number_of_vertices    = len(sphere_vertices)
    
    full_sphere_vertices  = []
    full_sphere_triangles = []

    for coords in vismol_object.frames:
        for i in range(0,len(coords),3):
            for vertice in sphere_vertices:
                full_sphere_vertices.append(vertice+coords[i])
                full_sphere_vertices.append(vertice+coords[i+1])
                full_sphere_vertices.append(vertice+coords[i+2])


    for i in range(natoms):
        for index in sphere_triangles:
            full_sphere_triangles.append(index+i*number_of_vertices)

        

    coords  = np.array(full_sphere_vertices ,dtype=np.float32)
    indexes = np.array(full_sphere_triangles,dtype=np.uint32)
    #print (full_sphere_vertices)
    indexes = full_sphere_triangles

    
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
    return True

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
    #indexes = vismol_object.non_bonded_atoms
    
    #indexes = []
    #indexes = vismol_object.non_bonded_atoms
    #for i in range(dot_qtty):
        #indexes.append(i)
    indexes = np.array(vismol_object.dot_indexes,dtype=np.uint32)
    
    #try:
    #    indexes = np.array(indexes,dtype=np.uint32)
    #except:
    #    pass
        
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

def _make_gl_selection_dots(program, vismol_object = None):
    """ Function doc
    """

    dot_sizes = vismol_object.vdw_dot_sizes
    coords    = vismol_object.frames[0]
    colors    = [0.,1.,1.]*int(len(coords)/3)
    colors    = np.array(colors, dtype=np.float32)
   
    dot_qtty = int(len(coords)/3)
    
    #bckgrnd_color = [bckgrnd_color[0],bckgrnd_color[1],
    #                 bckgrnd_color[2],bckgrnd_color[3]]*dot_qtty
    bckgrnd_color = [0,0,0]
    bckgrnd_color = np.array(bckgrnd_color, dtype=np.float32)
    
    indexes = []
    for i in range(dot_qtty):
        indexes.append(i)
    indexes = np.array(indexes,dtype=np.uint32)
    
    vao = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vao)
    
    ind_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.itemsize*int(len(indexes)), indexes, GL.GL_DYNAMIC_DRAW)
    
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
    
    vismol_object.selection_dots_vao      = vao
    vismol_object.selection_dot_buffers   = (ind_vbo, coord_vbo, col_vbo)
    return True

def _make_gl_picking_dots(program, vismol_object = None, bckgrnd_color= [0.0,0.0,0.0,1.0]):
    """ Function doc
    """
    colors    = vismol_object.color_indexes
    #dot_sizes = vismol_object.vdw_dot_sizes
    
    coords    = vismol_object.frames[0]
    
    #dot_sizes = vismol_object.vdw_dot_sizes
    
    dot_qtty      = int(len(coords)/3)
    
    #bckgrnd_color = [bckgrnd_color[0],bckgrnd_color[1],
    #                 bckgrnd_color[2],bckgrnd_color[3]]*dot_qtty
    #bckgrnd_color = np.array(bckgrnd_color, dtype=np.float32)
    
    indexes = []
    for i in range(dot_qtty):
        indexes.append(i)
    indexes = np.array(indexes,dtype=np.uint32)
    
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
    
    #dot_vbo = GL.glGenBuffers(1)
    #GL.glBindBuffer(GL.GL_ARRAY_BUFFER, dot_vbo)
    #GL.glBufferData(GL.GL_ARRAY_BUFFER, dot_sizes.itemsize*len(dot_sizes), dot_sizes, GL.GL_STATIC_DRAW)
    #att_size = GL.glGetAttribLocation(program, 'vert_dot_size')
    #GL.glEnableVertexAttribArray(att_size)
    #GL.glVertexAttribPointer(att_size, 1, GL.GL_FLOAT, GL.GL_FALSE, dot_sizes.itemsize, ctypes.c_void_p(0))
    #
    #bckgrnd_vbo = GL.glGenBuffers(1)
    #GL.glBindBuffer(GL.GL_ARRAY_BUFFER, bckgrnd_vbo)
    #GL.glBufferData(GL.GL_ARRAY_BUFFER, bckgrnd_color.itemsize*len(bckgrnd_color), bckgrnd_color, GL.GL_STATIC_DRAW)
    #att_bck_color = GL.glGetAttribLocation(program, 'bckgrnd_color')
    #GL.glEnableVertexAttribArray(att_bck_color)
    #GL.glVertexAttribPointer(att_bck_color, 4, GL.GL_FLOAT, GL.GL_FALSE, 4*bckgrnd_color.itemsize, ctypes.c_void_p(0))
    
    
    
    #vao_list.append(vao)
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(att_position)
    GL.glDisableVertexAttribArray(att_colors)
    #GL.glDisableVertexAttribArray(att_size)
    #GL.glDisableVertexAttribArray(att_bck_color)

    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
    
    vismol_object.picking_dots_vao      = vao
    vismol_object.picking_dot_buffers   = (ind_vbo, coord_vbo, col_vbo)
    return True


#def _make_gl_nb_lines(program, vismol_object = None):
    #""" Function doc
    #"""   
    #indexes = np.array(vismol_object.non_bonded_atoms,dtype=np.uint32)
    #coords  = vismol_object.frames[0]
    #colors  = vismol_object.colors
    
    #vao = GL.glGenVertexArrays(1)
    #GL.glBindVertexArray(vao)
    
    #ind_vbo = GL.glGenBuffers(1)
    #GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    #GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.itemsize*int(len(indexes)), indexes, GL.GL_DYNAMIC_DRAW)
    
    #coord_vbo = GL.glGenBuffers(1)
    #GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    #GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*int(len(coords)), coords, GL.GL_STATIC_DRAW)
    #att_position = GL.glGetAttribLocation(program, 'vert_coord')
    #GL.glEnableVertexAttribArray(att_position)
    #GL.glVertexAttribPointer(att_position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    #col_vbo = GL.glGenBuffers(1)
    #GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    #GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*int(len(colors)), colors, GL.GL_STATIC_DRAW)
    #att_colors = GL.glGetAttribLocation(program, 'vert_color')
    #GL.glEnableVertexAttribArray(att_colors)
    #GL.glVertexAttribPointer(att_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    ##vao_list.append(vao)
    #GL.glBindVertexArray(0)
    #GL.glDisableVertexAttribArray(att_position)
    #GL.glDisableVertexAttribArray(att_colors)
    #GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    #GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
    
    
    #vismol_object.lines_vao      = vao
    #vismol_object.line_buffers   = (ind_vbo, coord_vbo, col_vbo)
    ##return vao, (ind_vbo, coord_vbo, col_vbo)


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
    #indexes = np.array(indexes,dtype=np.uint32)
    
    indexes = np.array(vismol_object.index_bonds,dtype=np.uint32)
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

def _make_gl_ribbon_lines(program, vismol_object = None):
    """ Function doc
    """  
    indexes = np.array(vismol_object.ribbons_Calpha_indexes_rep,dtype=np.uint32)
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
    
    
    vismol_object.ribbons_vao      = vao
    vismol_object.ribbons_buffers  = (ind_vbo, coord_vbo, col_vbo)




def change_vbo_indexes (ind_vbo = None, indexes = []):
    """ Function doc """
    indexes = np.array(indexes,dtype=np.uint32)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.itemsize*int(len(indexes)), indexes, GL.GL_DYNAMIC_DRAW)


def change_vbo_colors  (col_vbo = None, colors = [], program = None):
    """ Function doc """
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*int(len(colors)), colors, GL.GL_STATIC_DRAW)
    att_colors = GL.glGetAttribLocation(program, 'vert_color')
    GL.glEnableVertexAttribArray(att_colors)
    GL.glVertexAttribPointer(att_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))





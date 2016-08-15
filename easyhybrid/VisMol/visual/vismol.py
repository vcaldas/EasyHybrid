#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  VisMol.py
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

import math
import numpy as np
import ctypes
import glcamera as cam
import matrix_operations as mop
import shapes
import sphere_data as sph_d
import vismol_shaders as vm_shader

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import OpenGL
from OpenGL import GL
from OpenGL.GL import shaders

class MyGLProgram(Gtk.GLArea):
    """ Object that contains the GLArea from GTK3+.
        It needs a vertex and shader to be created, maybe later I'll
        add a function to change the shaders.
    """
    
    def __init__(self, data=None, vertex=None, fragment=None, geometry=None, width=640, height=420):
        """ Constructor of the class, needs two String objects,
            the vertex and fragment shaders.
            
            Keyword arguments:
            vertex -- The vertex shader to be used (REQUIRED)
            fragment -- The fragment shader to be used (REQUIRED)
            
            Returns:
            A MyGLProgram object.
        """
        super(MyGLProgram, self).__init__()
        self.connect("realize", self.initialize)
        self.connect("render", self.render)
        self.connect("resize", self.reshape)
        self.connect("key-press-event", self.key_press)
        self.connect("button-press-event", self.mouse_pressed)
        self.connect("button-release-event", self.mouse_released)
        self.connect("motion-notify-event", self.mouse_motion)
        self.connect("scroll-event", self.mouse_scroll)
        self.set_size_request(width, height)
        self.grab_focus()
        self.set_events( self.get_events() | Gdk.EventMask.SCROLL_MASK
                       | Gdk.EventMask.BUTTON_PRESS_MASK | Gdk.EventMask.BUTTON_RELEASE_MASK
                       | Gdk.EventMask.POINTER_MOTION_MASK | Gdk.EventMask.POINTER_MOTION_HINT_MASK
                       | Gdk.EventMask.KEY_PRESS_MASK | Gdk.EventMask.KEY_RELEASE_MASK )
        self.vertex_shader = vertex
        self.fragment_shader = fragment
        self.geometry_shader = geometry
        self.data = data
        
    def initialize(self, widget):
        """ Enables the buffers and other charasteristics of the OpenGL context.
            sets the initial projection and view matrix
            
            self.flag -- Needed to only create one OpenGL program, otherwise a bunch of
                         programs will be created and use system resources. If the OpenGL
                         program will be changed change this value to True
        """
        if self.get_error()!=None:
            print self.get_error().args
            print self.get_error().code
            print self.get_error().domain
            print self.get_error().message
            Gtk.main_quit()
        self.model_mat = np.identity(4, dtype=np.float32)
        self.normal_mat = np.identity(3, dtype=np.float32)
        self.glcamera = cam.GLCamera()
        self.set_has_depth_buffer(True)
        self.set_has_alpha(True)
        self.frame_i = 0
        aloc = self.get_allocation()
        w = np.float32(aloc.width)
        h = np.float32(aloc.height)
        self.shader_flag = True
        self.test = False
        self.scroll = 0.3
        self.glcamera.field_of_view = 25.0
        self.glcamera.z_near = 0.1
        self.glcamera.z_far = 15
        self.glcamera.viewport_aspect_ratio = float(w)/h
        self.right = float(w)/h
        self.left = -self.right
        self.top = 1
        self.bottom = -1
        self.mouse_x = self.mouse_y = 0
        self.mouse_rotate = self.mouse_zoom = self.mouse_pan = False
        self.bckgrnd_color = np.array([0.0,0.0,0.0,1.0],dtype=np.float32)
        #self.bckgrnd_color = np.array([1.0,1.0,1.0,1.0],dtype=np.float32)
        self.light_position = np.array([2.5,2.5,3.0],dtype=np.float32)
        self.light_color = np.array([1.0,1.0,1.0,1.0],dtype=np.float32)
        self.light_ambient_coef = 0.5
        self.light_shininess = 5.5
        self.light_intensity = np.array([0.6,0.6,0.6],dtype=np.float32)
        self.light_specular_color = np.array([1.0,1.0,1.0],dtype=np.float32)
        self.LINES = self.SPHERES = self.DOTS = self.DOTS_SURFACE = False
        self.VDW = self.PRETTY_VDW = self.RIBBON = self.BALL_STICK = False
    
    def reshape(self, widget, width, height):
        """ Resizing function, takes the widht and height of the widget
            and modifies the view in the camera acording to the new values
        
            Keyword arguments:
            widget -- The widget that is performing resizing
            width -- Actual width of the window
            height -- Actual height of the window
        """
        self.left = -float(width)/height
        self.right = -self.left
        self.width = width
        self.height = height
        self.center_x = width/2
        self.center_y = height/2
        self.glcamera.viewport_aspect_ratio = float(width)/height
        self.queue_draw()
        return True
    
    def load_shaders(self, vertex=None, fragment=None, geometry=None):
        """ Here the shaders are loaded and compiled to an OpenGL program. By default
            the constructor shaders will be used, if you want to change the shaders
            use this function. The flag is used to create only one OpenGL program.
            
            Keyword arguments:
            vertex -- The vertex shader to be used
            fragment -- The fragment shader to be used
        """
        my_vertex_shader = self.create_shader(self.vertex_shader, GL.GL_VERTEX_SHADER)
        #my_geometry_shader = self.create_shader(self.geometry_shader, GL.GL_GEOMETRY_SHADER)
        my_fragment_shader = self.create_shader(self.fragment_shader, GL.GL_FRAGMENT_SHADER)
        self.program = GL.glCreateProgram()
        GL.glAttachShader(self.program, my_vertex_shader)
        #GL.glAttachShader(self.program, my_geometry_shader)
        GL.glAttachShader(self.program, my_fragment_shader)
        GL.glLinkProgram(self.program)
        print 'OpenGL version: ',GL.glGetString(GL.GL_VERSION)
        try:
            print 'OpenGL major version: ',GL.glGetDoublev(GL.GL_MAJOR_VERSION)
            print 'OpenGL minor version: ',GL.glGetDoublev(GL.GL_MINOR_VERSION)
        except:
            print 'OpenGL major version not found'
        self.load_data()
        self.shader_flag = False
        
    def create_shader(self, shader_prog, shader_type):
        """ Creates, links to a source, compiles and returns a shader.
            
            Keyword arguments:
            shader -- The shader text to use
            shader_type -- The OpenGL enum type of shader, it can be:
                           GL.GL_VERTEX_SHADER, GL.GL_GEOMETRY_SHADER or GL.GL_FRAGMENT_SHADER
            
            Returns:
            A shader object identifier or pops out an error
        """
        shader = GL.glCreateShader(shader_type)
        GL.glShaderSource(shader, shader_prog)
        GL.glCompileShader(shader)
        if GL.glGetShaderiv(shader, GL.GL_COMPILE_STATUS) != GL.GL_TRUE:
            print "Error compiling the shader: ", shader_type
            raise RuntimeError(GL.glGetShaderInfoLog(shader))
        return shader
    
    def render(self, area, context):
        """ This is the function that will be called everytime the window
            needs to be re-drawed.
        """
        if self.data is not None:
            if self.shader_flag:
                self.load_shaders()
            GL.glClearColor(self.bckgrnd_color[0],self.bckgrnd_color[1],
                            self.bckgrnd_color[2],self.bckgrnd_color[3])
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
            
            GL.glUseProgram(self.program)
            
            self.load_matrices()
            self.load_lights()
            
            if self.SPHERES:
                self.draw_spheres()
            if self.BALL_STICK:
                self.draw_ball_stick()
            if self.RIBBON:
                self.draw_ribbons()
            
            GL.glUseProgram(0)
        else:
            GL.glClearColor(self.bckgrnd_color[0],self.bckgrnd_color[1],
                            self.bckgrnd_color[2],self.bckgrnd_color[3])
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
    
    def load_matrices(self):
        """ Load the matrices to OpenGL.
            
            model_mat -- transformation matrix for the objects rendered
            view_mat -- transformation matrix for the camera used
            projection_mat -- matrix for the space to be visualized in the scene
        """
        model = GL.glGetUniformLocation(self.program, 'model_mat')
        GL.glUniformMatrix4fv(model, 1, GL.GL_FALSE, self.model_mat)
        view = GL.glGetUniformLocation(self.program, 'view_mat')
        GL.glUniformMatrix4fv(view, 1, GL.GL_FALSE, self.glcamera.get_view_matrix())
        proj = GL.glGetUniformLocation(self.program, 'projection_mat')
        GL.glUniformMatrix4fv(proj, 1, GL.GL_FALSE, self.glcamera.get_projection_matrix())
        norm = GL.glGetUniformLocation(self.program, 'normal_mat')
        GL.glUniformMatrix3fv(norm, 1, GL.GL_FALSE, self.normal_mat)
        return True
    
    def load_lights(self):
        """ Function doc
        """
        #light_pos = GL.glGetUniformLocation(self.program, 'sun_light.v_direction')
        #GL.glUniform3fv(light_pos, 1, self.light_position)
        #light_col = GL.glGetUniformLocation(self.program, 'sun_light.v_color')
        #GL.glUniform3fv(light_col, 1, self.light_color)
        #amb_coef = GL.glGetUniformLocation(self.program, 'sun_light.ambient_intensity')
        #GL.glUniform1fv(amb_coef, 1, self.light_ambient_coef)
        light_pos = GL.glGetUniformLocation(self.program, 'my_light.position')
        GL.glUniform3fv(light_pos, 1, self.light_position)
        light_col = GL.glGetUniformLocation(self.program, 'my_light.color')
        GL.glUniform3fv(light_col, 1, self.light_color)
        amb_coef = GL.glGetUniformLocation(self.program, 'my_light.ambient_coef')
        GL.glUniform1fv(amb_coef, 1, self.light_ambient_coef)
        shiny = GL.glGetUniformLocation(self.program, 'my_light.shininess')
        GL.glUniform1fv(shiny, 1, self.light_shininess)
        intensity = GL.glGetUniformLocation(self.program, 'my_light.intensity')
        GL.glUniform3fv(intensity, 1, self.light_intensity)
        spec_col = GL.glGetUniformLocation(self.program, 'my_light.specular_color')
        GL.glUniform3fv(spec_col, 1, self.light_specular_color)
        cam_pos = GL.glGetUniformLocation(self.program, 'cam_pos')
        GL.glUniform3fv(cam_pos, 1, self.glcamera.get_position())
        return True
    
    def load_data(self, data=None):
        """ In this function you load the data to be displayed. Because of
            using the flag the program loads the data just once. Here you
            bind the coordinates data to the buffer array.
        """
        assert(self.data is not None or data is not None)
        if data is not None:
            self.data = data
        self.dot_list         = []
        self.vdw_list         = []
        self.ball_stick_list  = []
        self.ball_stick_vao   = []
        self.bond_stick_vao   = []
        self.ribbons_vao      = []
        self.bonds_list       = []
        self.wires_list       = []
        self.sphere_list      = []
        self.spheres_vao      = []
        self.pretty_vdw_list  = []
        self.dot_surface_list = []
        for chain in self.data[self.frame_i].chains.values():
            for residue in chain.residues.values():
                for atom in residue.atoms.values():
                    if atom.dot:
                        self.dot_list.append(atom)
                    if atom.vdw:
                        self.vdw_list.append(atom)
                    if atom.ball:
                        self.ball_stick_list.append(atom)
                    if atom.wires:
                        self.wires_list.append(atom)
                    if atom.sphere:
                        self.sphere_list.append(atom)
                    if atom.pretty_vdw:
                        self.pretty_vdw_list.append(atom)
                    if atom.dot_surface:
                        self.dot_surface_list.append(atom)
        
        for atom in self.sphere_list:
            vertices, indexes, colors = shapes.get_sphere(atom.pos, atom.cov_rad, atom.color, level='level_2')
            centers = [atom.pos[0],atom.pos[1],atom.pos[2]]*len(indexes)
            centers = np.array(centers,dtype=np.float32)
            vao = GL.glGenVertexArrays(1)
            GL.glBindVertexArray(vao)
            atom.vertices = len(vertices)
            atom.triangles = len(indexes)
        
            vert_vbo = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vert_vbo)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.itemsize*len(vertices), vertices, GL.GL_STATIC_DRAW)
            
            ind_vbo = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
            GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.itemsize*len(indexes), indexes, GL.GL_STATIC_DRAW)
            
            att_position = GL.glGetAttribLocation(self.program, 'coordinate')
            GL.glEnableVertexAttribArray(att_position)
            GL.glVertexAttribPointer(att_position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*vertices.itemsize, ctypes.c_void_p(0))
        
            center_vbo = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, center_vbo)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, centers.itemsize*len(centers), centers, GL.GL_STATIC_DRAW)
            
            att_center = GL.glGetAttribLocation(self.program, 'center')
            GL.glEnableVertexAttribArray(att_center)
            GL.glVertexAttribPointer(att_center, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*centers.itemsize, ctypes.c_void_p(0))
            
            col_vbo = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*len(colors), colors, GL.GL_STATIC_DRAW)
            
            att_colors = GL.glGetAttribLocation(self.program, 'vert_color')
            GL.glEnableVertexAttribArray(att_colors)
            GL.glVertexAttribPointer(att_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
            
            self.spheres_vao.append(vao)
            GL.glBindVertexArray(0)
            GL.glDisableVertexAttribArray(att_position)
            GL.glDisableVertexAttribArray(att_colors)
            GL.glDisableVertexAttribArray(att_center)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
            GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
        
        for atom in self.ball_stick_list:
            vertices, indexes, colors = shapes.get_sphere(atom.pos, atom.ball_radius, atom.color, level='level_2')
            centers = [atom.pos[0],atom.pos[1],atom.pos[2]]*len(indexes)
            centers = np.array(centers,dtype=np.float32)
            vao = GL.glGenVertexArrays(1)
            GL.glBindVertexArray(vao)
            atom.vertices = len(vertices)
            atom.triangles = len(indexes)
            vert_vbo = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vert_vbo)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.itemsize*len(vertices), vertices, GL.GL_STATIC_DRAW)
            
            ind_vbo = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
            GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.itemsize*len(indexes), indexes, GL.GL_STATIC_DRAW)
            
            att_position = GL.glGetAttribLocation(self.program, 'coordinate')
            GL.glEnableVertexAttribArray(att_position)
            GL.glVertexAttribPointer(att_position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*vertices.itemsize, ctypes.c_void_p(0))
            
            center_vbo = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, center_vbo)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, centers.itemsize*len(centers), centers, GL.GL_STATIC_DRAW)
            
            att_center = GL.glGetAttribLocation(self.program, 'center')
            GL.glEnableVertexAttribArray(att_center)
            GL.glVertexAttribPointer(att_center, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*centers.itemsize, ctypes.c_void_p(0))
            
            col_vbo = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*len(colors), colors, GL.GL_STATIC_DRAW)
            
            att_colors = GL.glGetAttribLocation(self.program, 'vert_color')
            GL.glEnableVertexAttribArray(att_colors)
            GL.glVertexAttribPointer(att_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
            
            self.ball_stick_vao.append(vao)
            GL.glBindVertexArray(0)
            GL.glDisableVertexAttribArray(att_position)
            GL.glDisableVertexAttribArray(att_colors)
            GL.glDisableVertexAttribArray(att_center)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
            GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
        
        for bond in self.data[0].bonds:
            vertices, indexes, colors, normals = shapes.get_cylinder(bond[0].pos,bond[0].color,bond[2],bond[3],bond[1],5,radius=0.1,level='level_3')
            vao = GL.glGenVertexArrays(1)
            GL.glBindVertexArray(vao)
            vert_vbo = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vert_vbo)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.itemsize*len(vertices), vertices, GL.GL_STATIC_DRAW)
            
            ind_vbo = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
            GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.itemsize*len(indexes), indexes, GL.GL_STATIC_DRAW)
            
            att_position = GL.glGetAttribLocation(self.program, 'coordinate')
            GL.glEnableVertexAttribArray(att_position)
            GL.glVertexAttribPointer(att_position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*vertices.itemsize, ctypes.c_void_p(0))
            
            center_vbo = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, center_vbo)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, normals.itemsize*len(normals), normals, GL.GL_STATIC_DRAW)
            
            att_center = GL.glGetAttribLocation(self.program, 'center')
            GL.glEnableVertexAttribArray(att_center)
            GL.glVertexAttribPointer(att_center, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*normals.itemsize, ctypes.c_void_p(0))
            
            col_vbo = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*len(colors), colors, GL.GL_STATIC_DRAW)
            
            att_colors = GL.glGetAttribLocation(self.program, 'vert_color')
            GL.glEnableVertexAttribArray(att_colors)
            GL.glVertexAttribPointer(att_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
            
            self.bond_stick_vao.append(vao)
            GL.glBindVertexArray(0)
            GL.glDisableVertexAttribArray(att_position)
            GL.glDisableVertexAttribArray(att_colors)
            GL.glDisableVertexAttribArray(att_center)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
            GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
        
        for rib in self.data[0].ribbons:
            vertices, indexes, colors, normals = shapes.get_cylinder(rib[0].pos,rib[0].color,rib[2],rib[3],rib[1],5,radius=0.2,level='level_4')
            vao = GL.glGenVertexArrays(1)
            GL.glBindVertexArray(vao)
            vert_vbo = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vert_vbo)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.itemsize*len(vertices), vertices, GL.GL_STATIC_DRAW)
            
            ind_vbo = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
            GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.itemsize*len(indexes), indexes, GL.GL_STATIC_DRAW)
            
            att_position = GL.glGetAttribLocation(self.program, 'coordinate')
            GL.glEnableVertexAttribArray(att_position)
            GL.glVertexAttribPointer(att_position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*vertices.itemsize, ctypes.c_void_p(0))
            
            center_vbo = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, center_vbo)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, normals.itemsize*len(normals), normals, GL.GL_STATIC_DRAW)
            
            att_center = GL.glGetAttribLocation(self.program, 'center')
            GL.glEnableVertexAttribArray(att_center)
            GL.glVertexAttribPointer(att_center, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*normals.itemsize, ctypes.c_void_p(0))
            
            col_vbo = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*len(colors), colors, GL.GL_STATIC_DRAW)
            
            att_colors = GL.glGetAttribLocation(self.program, 'vert_color')
            GL.glEnableVertexAttribArray(att_colors)
            GL.glVertexAttribPointer(att_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
            
            self.ribbons_vao.append(vao)
            GL.glBindVertexArray(0)
            GL.glDisableVertexAttribArray(att_position)
            GL.glDisableVertexAttribArray(att_colors)
            GL.glDisableVertexAttribArray(att_center)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
            GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
        
    def draw_spheres(self):
        """ Function doc
        """
        assert(len(self.spheres_vao)>0)
        for i,atom in enumerate(self.sphere_list):
            GL.glBindVertexArray(self.spheres_vao[i])
            GL.glDrawElements(GL.GL_TRIANGLES, atom.triangles, GL.GL_UNSIGNED_SHORT, None)
            GL.glBindVertexArray(0)
    
    def draw_ball_stick(self):
        """ Function doc
        """
        assert(len(self.ball_stick_vao)>0)
        for i,atom in enumerate(self.ball_stick_list):
            GL.glBindVertexArray(self.ball_stick_vao[i])
            GL.glDrawElements(GL.GL_TRIANGLES, atom.triangles, GL.GL_UNSIGNED_SHORT, None)
            GL.glBindVertexArray(0)
        for i,bond in enumerate(self.bond_stick_vao):
            GL.glBindVertexArray(self.bond_stick_vao[i])
            GL.glDrawElements(GL.GL_TRIANGLES, 144, GL.GL_UNSIGNED_SHORT, None)
            GL.glBindVertexArray(0)
    
    def draw_ribbons(self):
        """ Function doc
        """
        assert(len(self.ribbons_vao)>0)
        for i,bond in enumerate(self.ribbons_vao):
            GL.glBindVertexArray(self.ribbons_vao[i])
            GL.glDrawElements(GL.GL_TRIANGLES, 168, GL.GL_UNSIGNED_SHORT, None)
            GL.glBindVertexArray(0)
        
    
    def key_press(self, widget, event):
        """ The mouse_button function serves, as the names states, to catch
            events in the keyboard, e.g. letter 'l' pressed, 'backslash'
            pressed. Note that there is a difference between 'A' and 'a'.
            Here I use a specific handler for each key pressed after
            discarding the CONTROL, ALT and SHIFT keys pressed (usefull
            for customized actions) and maintained, i.e. it's the same as
            using Ctrl+Z to undo an action.
        """
        k_name = Gdk.keyval_name(event.keyval)
        func = getattr(self, 'pressed_' + k_name, None)
        #print k_name, 'key Pressed'
        if func:
            func()
        return True
    
    def pressed_Escape(self):
        print 'Exit!'
        Gtk.main_quit()
    
    def pressed_s(self):
        self.SPHERES = not self.SPHERES
        self.queue_draw()
    
    def pressed_b(self):
        self.BALL_STICK = not self.BALL_STICK
        self.queue_draw()
    
    def pressed_r(self):
        self.RIBBON = not self.RIBBON
        self.queue_draw()
    
    def pressed_l(self):
        self.color = np.array([ 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0,
                                0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0,
                                0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0,
                                0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0,
                                1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0,
                                0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0,
                                0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0,
                                0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0,
                                1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0,
                                0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0,
                                0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0,
                                0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0,
                                1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0,
                                0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0,
                                0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0,
                                0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0,
                                1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0,
                                0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0,
                                0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0,
                                0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0,
                                1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0,
                                0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0,
                                0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0,
                                0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0,
                                1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0,
                                0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0,
                                0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0,
                                0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0,
                                1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0,
                                0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0,
                                0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0,
                                0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0,
                                1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0,
                                0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0,
                                0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0,
                                0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0,
                                1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0,
                                0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0,
                                0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0,
                                0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0,
                                0.0, 0.0, 1.0, 0.0, 1.0, 0.0],dtype=np.float32)
        
        self.queue_draw()
        print 'Load data'
    
    def mouse_pressed(self, widget, event):
        left   = event.button==1 and event.type==Gdk.EventType.BUTTON_PRESS
        middle = event.button==2 and event.type==Gdk.EventType.BUTTON_PRESS
        right  = event.button==3 and event.type==Gdk.EventType.BUTTON_PRESS
        self.mouse_rotate = left and not (middle or right)
        self.mouse_zoom   = right and not (middle or left)
        self.mouse_pan    = middle and not (right or left)
        x = self.mouse_x = event.x
        y = self.mouse_y = event.y
        self.drag_pos_x, self.drag_pos_y, self.drag_pos_z = self.pos(x, y)
    
    def mouse_released(self, widget, event):
        pass
        self.mouse_rotate = self.mouse_zoom = self.mouse_pan = False
    
    def mouse_motion(self, widget, event):
        x = event.x
        y = event.y
        state = event.state
        dx = x - self.mouse_x
        dy = y - self.mouse_y
        if (dx==0 and dy==0):
            return
        self.mouse_x, self.mouse_y = x, y
        changed = False
        #GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        if self.mouse_rotate:
            angle = math.sqrt(dx**2+dy**2)/float(self.width+1)*180.0
            self.model_mat = mop.my_glRotatef(self.model_mat, angle, [-dy, -dx, 0])
            self.update_normal_mat()
            changed = True
        elif self.mouse_pan:
            px, py, pz = self.pos(x, y)
            pan_matrix = mop.my_glTranslatef(np.identity(4,dtype=np.float32),
                [(px-self.drag_pos_x)*self.glcamera.z_far/10, 
                 (py-self.drag_pos_y)*self.glcamera.z_far/10, 
                 (pz-self.drag_pos_z)*self.glcamera.z_far/10])
            self.model_mat = mop.my_glMultiplyMatricesf(self.model_mat, pan_matrix)
            self.update_normal_mat()
            self.drag_pos_x = px
            self.drag_pos_y = py
            self.drag_pos_z = pz
            changed = True
        elif self.mouse_zoom:
            delta = (((self.glcamera.z_far-self.glcamera.z_near)/2)+self.glcamera.z_near)/200
            direction = mop.my_glForwardVectorAbs(self.glcamera.get_view_matrix())
            #self.model_mat = mop.my_glTranslatef(self.model_mat, -dy*delta*direction)
            self.glcamera.move_position(dy*delta*direction)
            changed = True
        if changed:
            self.queue_draw()
        
    def mouse_scroll(self, widget, event):
        if event.direction == Gdk.ScrollDirection.UP:
            self.glcamera.z_near -= self.scroll
            self.glcamera.z_far += self.scroll
        if event.direction == Gdk.ScrollDirection.DOWN:
            self.glcamera.z_near += self.scroll
            self.glcamera.z_far -= self.scroll
        if self.glcamera.z_near < 0:
            self.glcamera.z_near = 0.001
        if self.glcamera.z_far < self.glcamera.z_near:
            self.glcamera.z_near -= self.scroll
            self.glcamera.z_far = self.glcamera.z_near + 0.05
        self.queue_draw()
    
    def update_normal_mat(self):
        """ Function doc
        """
        modelview = mop.my_glMultiplyMatricesf(self.glcamera.get_view_matrix(), self.model_mat)
        normal_mat = np.matrix(modelview[:3,:3]).I.T
        self.normal_mat = np.array(normal_mat)
        #model = np.matrix(self.model_mat[:3,:3]).I.T
        #self.normal_mat = np.array(model)
    
    def pos(self, x, y):
        """
        Use the ortho projection and viewport information
        to map from mouse co-ordinates back into world
        co-ordinates
        """
        px = x/float(self.width)
        py = y/float(self.height)
        px = self.left + px*(self.right-self.left)
        py = self.top + py*(self.bottom-self.top)
        pz = self.glcamera.z_near
        return px, py, pz
    

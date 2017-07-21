#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  gtk3.py
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
import VISMOL.glCore.glcamera as cam
import VISMOL.glCore.matrix_operations as mop
import VISMOL.glCore.shapes as shapes
import VISMOL.glCore.sphere_data as sph_d
import VISMOL.glCore.vismol_shaders as vm_shader
import VISMOL.glCore.glaxis as glaxis

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import OpenGL
from OpenGL import GLU
from OpenGL import GL
from OpenGL.GL import shaders


class GLMenu:
    """ Class doc """
    def __init__ (self, glWidget):
        """ Class initialiser """
        xml = '''
<?xml version="1.0" encoding="UTF-8"?>
<!-- Generated with glade 3.18.3 -->
<interface>
  <requires lib="gtk+" version="3.12"/>
  <object class="GtkMenu" id="menu1">
    <property name="visible">True</property>
    <property name="can_focus">False</property>
    <child>
      <object class="GtkMenuItem" id="menuitem1">
        <property name="visible">True</property>
        <property name="can_focus">False</property>
        <property name="label" translatable="yes">menuitem1</property>
        <property name="use_underline">True</property>
        <signal name="button-release-event" handler="menuItem_function" swapped="no"/>
      </object>
    </child>
    <child>
      <object class="GtkMenuItem" id="menuitem2">
        <property name="visible">True</property>
        <property name="can_focus">False</property>
        <property name="label" translatable="yes">menuitem2</property>
        <property name="use_underline">True</property>
        <child type="submenu">
          <object class="GtkMenu" id="menu2">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <child>
              <object class="GtkMenuItem" id="menuitem5">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">menuitem5</property>
                <property name="use_underline">True</property>
                <signal name="button-release-event" handler="menuItem_function" swapped="no"/>
              </object>
            </child>
          </object>
        </child>
      </object>
    </child>
    <child>
      <object class="GtkMenuItem" id="menuitem3">
        <property name="visible">True</property>
        <property name="can_focus">False</property>
        <property name="label" translatable="yes">menuitem3</property>
        <property name="use_underline">True</property>
        <child type="submenu">
          <object class="GtkMenu" id="menu3">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <child>
              <object class="GtkMenuItem" id="menuitem4">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">menuitem4</property>
                <property name="use_underline">True</property>
                <signal name="button-release-event" handler="menuItem_function" swapped="no"/>
              </object>
            </child>
          </object>
        </child>
      </object>
    </child>
    <child>
      <object class="GtkMenuItem" id="menuitem6">
        <property name="visible">True</property>
        <property name="can_focus">False</property>
        <property name="label" translatable="yes">menuitem6</property>
        <property name="use_underline">True</property>
        <signal name="button-release-event" handler="menuItem_function" swapped="no"/>
      </object>
    </child>
    <child>
      <object class="GtkMenuItem" id="menuitem7">
        <property name="visible">True</property>
        <property name="can_focus">False</property>
        <property name="label" translatable="yes">menuitem7</property>
        <property name="use_underline">True</property>
        <signal name="button-release-event" handler="menuItem_function" swapped="no"/>
      </object>
    </child>
    <child>
      <object class="GtkMenuItem" id="menuitem8">
        <property name="visible">True</property>
        <property name="can_focus">False</property>
        <property name="label" translatable="yes">menuitem8</property>
        <property name="use_underline">True</property>
        <signal name="button-release-event" handler="menuItem_function" swapped="no"/>
      </object>
    </child>
    <child>
      <object class="GtkMenuItem" id="menuitem9">
        <property name="visible">True</property>
        <property name="can_focus">False</property>
        <property name="label" translatable="yes">El Diablo</property>
        <property name="use_underline">True</property>
        <signal name="button-release-event" handler="menuItem_function" swapped="no"/>
      </object>
    </child>
  </object>
</interface>
        '''

        self.builder = Gtk.Builder()
        self.builder.add_from_string(xml)
        self.builder.connect_signals(self)
        self.glWidget = glWidget
    
    def open_gl_menu (self, event = None):
        """ Function doc """
        
        # Check if right mouse button was preseed
        if event.button == 3:
        #self.popup.popup(None, None, None, None, event.button, event.time)
        #return True # event has been handled        
            widget = self.builder.get_object('menu1')
            widget.popup(None, None, None, None, event.button, event.time)        
            pass
    def menuItem_function (self, widget, data):
        """ Function doc """
        #print ('Charlitos, seu lindo')
        if widget == self.builder.get_object('menuitem1'):
            self.glWidget.test_hide()
        
        if widget == self.builder.get_object('menuitem4'):
            self.glWidget.test_show()
        
        if widget == self.builder.get_object('menuitem5'):
        
            print ('Charlitos, el diablo')
        
        if widget == self.builder.get_object('menuitem6'):
            print ('Charlitos, el locotto del Andes')
        
        if widget == self.builder.get_object('menuitem7'):
            print ('Charlitos, seu lindo2')
        
        if widget == self.builder.get_object('menuitem8'):
            print ('Charlitos, seu lindo3')
        
        if widget == self.builder.get_object('menuitem9'):
            print ('Charlitos, seu lindo4')
            
class GtkGLWidget(Gtk.GLArea):
    """ Object that contains the GLArea from GTK3+.
        It needs a vertex and shader to be created, maybe later I'll
        add a function to change the shaders.
    """
    
    def __init__(self, vismolSession = None, width=640, height=420):
        """ Constructor of the class, needs two String objects,
            the vertex and fragment shaders.
            
            Keyword arguments:
            vertex -- The vertex shader to be used (REQUIRED)
            fragment -- The fragment shader to be used (REQUIRED)
            
            Returns:
            A MyGLProgram object.
        """
        super(GtkGLWidget, self).__init__()
        self.connect("realize", self.initialize)
        self.connect("render", self.render)
        self.connect("resize", self.reshape)
        self.connect("key-press-event", self.key_pressed)
        self.connect("key-release-event", self.key_released)
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
        
        self.vismolSession = vismolSession 
        
        self.glMenu = GLMenu(self)
        
        self.data = None
        
    
    def initialize(self, widget):
        """ Enables the buffers and other charasteristics of the OpenGL context.
            sets the initial projection and view matrix
            
            self.flag -- Needed to only create one OpenGL program, otherwise a bunch of
                         programs will be created and use system resources. If the OpenGL
                         program will be changed change this value to True
        """
        if self.get_error()!=None:
            print(self.get_error().args)
            print(self.get_error().code)
            print(self.get_error().domain)
            print(self.get_error().message)
            Gtk.main_quit()
        aloc = self.get_allocation()
        w = np.float32(aloc.width)
        h = np.float32(aloc.height)
        self.model_mat = np.identity(4, dtype=np.float32)
        self.normal_mat = np.identity(3, dtype=np.float32)
        self.glcamera = cam.GLCamera(25.0, 0.1, 5.8, float(w/h), np.array([0,0,3],dtype=np.float32), 3.8, 5.8)
        self.axis = glaxis.GLAxis()
        self.set_has_depth_buffer(True)
        self.set_has_alpha(True)
        self.frame = 0
        self.shader_flag = True
        self.modified_data = False
        self.modified_view = False
        self.scroll = 0.3
        self.right = float(w)/h
        self.left = -self.right
        self.top = 1
        self.bottom = -1
        self.mouse_x = 0
        self.mouse_y = 0
        self.mouse_rotate = False
        self.mouse_zoom = False
        self.mouse_pan = False
        self.bckgrnd_color = [0.0,0.0,0.0,1.0]
        #self.bckgrnd_color = [1.0,1.0,1.0,1.0]
        self.light_position = np.array([2.5,2.5,3.0],dtype=np.float32)
        self.light_color = np.array([1.0,1.0,1.0,1.0],dtype=np.float32)
        self.light_ambient_coef = 0.5
        self.light_shininess = 5.5
        self.light_intensity = np.array([0.6,0.6,0.6],dtype=np.float32)
        self.light_specular_color = np.array([1.0,1.0,1.0],dtype=np.float32)
        self.dragging = False
        self.LINES = False
        self.SPHERES = False
        self.DOTS = False
        self.DOTS_SURFACE = False
        self.VDW = False
        self.CRYSTAL = False
        self.RIBBON = False
        self.BALL_STICK = False
        self.SHOW_AXIS = True
        self.zero_reference_point = np.array([0.0, 0.0, 0.0],dtype=np.float32)
        self.dist_cam_zrp = np.linalg.norm(self.glcamera.get_position()-self.zero_reference_point)
        self.ctrl = False
        self.shift = False
        #GL.glEnable(GL_LINE_SMOOTH)
        #GL.glEnable(GL_MULTISAMPLE)
    
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
        self.glcamera.set_projection_matrix(mop.my_glPerspectivef(self.glcamera.field_of_view,
             self.glcamera.viewport_aspect_ratio, self.glcamera.z_near, self.glcamera.z_far))
        self.queue_draw()
        return True
    
    def create_gl_programs(self):
        """ Function doc
        """
        self.dots_program = self.load_shaders(vm_shader.vertex_shader_dots, vm_shader.fragment_shader_dots)
        self.lines_program = self.load_shaders(vm_shader.vertex_shader_lines, vm_shader.fragment_shader_lines, vm_shader.geometry_shader_lines)
    
    def load_shaders(self, vertex, fragment, geometry=None):
        """ Here the shaders are loaded and compiled to an OpenGL program. By default
            the constructor shaders will be used, if you want to change the shaders
            use this function. The flag is used to create only one OpenGL program.
            
            Keyword arguments:
            vertex -- The vertex shader to be used
            fragment -- The fragment shader to be used
        """
        my_vertex_shader = self.create_shader(vertex, GL.GL_VERTEX_SHADER)
        my_fragment_shader = self.create_shader(fragment, GL.GL_FRAGMENT_SHADER)
        if geometry is not None:
            my_geometry_shader = self.create_shader(geometry, GL.GL_GEOMETRY_SHADER)
        program = GL.glCreateProgram()
        GL.glAttachShader(program, my_vertex_shader)
        GL.glAttachShader(program, my_fragment_shader)
        if geometry is not None:
            GL.glAttachShader(program, my_geometry_shader)
        GL.glLinkProgram(program)
        print('OpenGL version: ',GL.glGetString(GL.GL_VERSION))
        try:
            print('OpenGL major version: ',GL.glGetDoublev(GL.GL_MAJOR_VERSION))
            print('OpenGL minor version: ',GL.glGetDoublev(GL.GL_MINOR_VERSION))
        except:
            print('OpenGL major version not found')
        return program
        
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
            print("Error compiling the shader: ", shader_type)
            raise RuntimeError(GL.glGetShaderInfoLog(shader))
        return shader
    
    def render(self, area, context):
        """ This is the function that will be called everytime the window
            needs to be re-drawed.
        """
        if self.shader_flag:
            print ('create_gl_programs')
            self.create_gl_programs()
            self.axis.initialize_gl()
            self.shader_flag = False
            print ('create_gl_programs done')
        
        GL.glClearColor(self.bckgrnd_color[0],self.bckgrnd_color[1],
                        self.bckgrnd_color[2],self.bckgrnd_color[3])
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        
        for visObj in self.vismolSession.vismol_objects:
            if visObj.actived:
                
                if visObj.lines_actived:
                
                    if visObj.lines_vao is None:
                        shapes._make_gl_lines(self.lines_program, vismol_object = visObj)
                    else:
                        GL.glEnable(GL.GL_DEPTH_TEST)                        
                        GL.glUseProgram(self.lines_program)
                        GL.glLineWidth(60/abs(self.dist_cam_zrp))
                        self.load_matrices(self.lines_program, visObj.model_mat, visObj.normal_mat)
                        self._draw_lines(visObj = visObj)
                        GL.glUseProgram(0)
                        GL.glDisable(GL.GL_DEPTH_TEST)
                
                if visObj.dots_actived:
                    pass
                    
                    #if visObj.dots_vao is None:
                    #    #print ('_make_gl_dots')
                    #    shapes._make_gl_dots (self.dots_program,  vismol_object = visObj)
                    #else:
                    #    GL.glEnable(GL.GL_DEPTH_TEST)
                    #    GL.glUseProgram(self.dots_program)
                    #    GL.glEnable(GL.GL_VERTEX_PROGRAM_POINT_SIZE)
                    #    self.load_matrices(self.dots_program, visObj.model_mat, visObj.normal_mat)
                    #    self.load_dot_params(self.dots_program)
                    #    self._draw_dots(visObj = visObj)
                    #    GL.glDisable(GL.GL_VERTEX_PROGRAM_POINT_SIZE)
                    #    GL.glUseProgram(0)
                    #    GL.glDisable(GL.GL_DEPTH_TEST)
        
        if self.SHOW_AXIS:
            GL.glEnable(GL.GL_DEPTH_TEST)
            GL.glUseProgram(self.axis.gl_axis_program)
            self.axis.load_params()
            self.draw_axis(True)
            GL.glUseProgram(0)
            GL.glUseProgram(self.axis.gl_lines_program)
            GL.glLineWidth(5)
            self.axis.load_lines_params()
            self.draw_axis(False)
            GL.glUseProgram(0)
            GL.glDisable(GL.GL_DEPTH_TEST)
    
    
    
    
    def old_render(self, area, context):
        """ This is the function that will be called everytime the window
            needs to be re-drawed.
        """
        #self.data = True
        if self.shader_flag:
            self.create_gl_programs()
            self.axis.initialize_gl()
            self.shader_flag = False
        
        
        
        
        if self.data is not None:
            if self.modified_data:
                #self.delete_vaos()
                self._load_data()
            GL.glClearColor(self.bckgrnd_color[0],self.bckgrnd_color[1],
                            self.bckgrnd_color[2],self.bckgrnd_color[3])
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
            
            for visObj in self.vismolSession.vismol_objects:
                
                if visObj.lines_actived:
                    GL.glEnable(GL.GL_DEPTH_TEST)
                    GL.glUseProgram(self.lines_program)
                    GL.glLineWidth(60/abs(self.dist_cam_zrp))
                    self.load_matrices(self.lines_program, visObj.model_mat, visObj.normal_mat)
                    self._draw_lines(visObj = visObj)
                    GL.glUseProgram(0)
                    GL.glDisable(GL.GL_DEPTH_TEST)
                
                #if visObj.dots_actived:
                #    GL.glEnable(GL.GL_DEPTH_TEST)
                #    GL.glUseProgram(self.dots_program)
                #    GL.glEnable(GL.GL_VERTEX_PROGRAM_POINT_SIZE)
                #    self.load_matrices(self.dots_program, visObj.model_mat, visObj.normal_mat)
                #    self.load_dot_params(self.dots_program)
                #    self.draw_dots()
                #    GL.glDisable(GL.GL_VERTEX_PROGRAM_POINT_SIZE)
                #    GL.glUseProgram(0)
                #    GL.glDisable(GL.GL_DEPTH_TEST)
                
                
                #if self.LINES:
                #    GL.glEnable(GL.GL_DEPTH_TEST)
                #    GL.glUseProgram(self.lines_program)
                #    GL.glLineWidth(60/abs(self.dist_cam_zrp))
                #    self.load_matrices(self.lines_program, visObj.model_mat, visObj.normal_mat)
                #    self.draw_lines()
                #    GL.glUseProgram(0)
                #    GL.glDisable(GL.GL_DEPTH_TEST)
                #if self.DOTS:
                #    GL.glEnable(GL.GL_DEPTH_TEST)
                #    GL.glUseProgram(self.dots_program)
                #    GL.glEnable(GL.GL_VERTEX_PROGRAM_POINT_SIZE)
                #    self.load_matrices(self.dots_program, visObj.model_mat, visObj.normal_mat)
                #    self.load_dot_params(self.dots_program)
                #    self.draw_dots()
                #    GL.glDisable(GL.GL_VERTEX_PROGRAM_POINT_SIZE)
                #    GL.glUseProgram(0)
                #    GL.glDisable(GL.GL_DEPTH_TEST)
            
        
        else:
            GL.glClearColor(self.bckgrnd_color[0],self.bckgrnd_color[1],
                            self.bckgrnd_color[2],self.bckgrnd_color[3])
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        
        if self.SHOW_AXIS:
            GL.glUseProgram(self.axis.gl_axis_program)
            self.axis.load_params()
            self.draw_axis(True)
            GL.glUseProgram(0)
            GL.glUseProgram(self.axis.gl_lines_program)
            GL.glLineWidth(5)
            self.axis.load_lines_params()
            self.draw_axis(False)
            GL.glUseProgram(0)
    
    def load_matrices(self, program, model_mat, normal_mat):
        """ Load the matrices to OpenGL.
            
            model_mat -- transformation matrix for the objects rendered
            view_mat -- transformation matrix for the camera used
            projection_mat -- matrix for the space to be visualized in the scene
        """
        model = GL.glGetUniformLocation(program, 'model_mat')
        GL.glUniformMatrix4fv(model, 1, GL.GL_FALSE, model_mat)
        view = GL.glGetUniformLocation(program, 'view_mat')
        GL.glUniformMatrix4fv(view, 1, GL.GL_FALSE, self.glcamera.view_matrix)
        proj = GL.glGetUniformLocation(program, 'projection_mat')
        GL.glUniformMatrix4fv(proj, 1, GL.GL_FALSE, self.glcamera.projection_matrix)
        norm = GL.glGetUniformLocation(program, 'normal_mat')
        GL.glUniformMatrix3fv(norm, 1, GL.GL_FALSE, normal_mat)
        fog_s = GL.glGetUniformLocation(program, 'fog_start')
        GL.glUniform1fv(fog_s, 1, self.glcamera.fog_start)
        fog_e = GL.glGetUniformLocation(program, 'fog_end')
        GL.glUniform1fv(fog_e, 1, self.glcamera.fog_end)
        fog_c = GL.glGetUniformLocation(program, 'fog_color')
        GL.glUniform4fv(fog_c, 1, self.bckgrnd_color)
        return True
    
    def load_lights(self, program):
        """ Function doc
        """
        light_pos = GL.glGetUniformLocation(program, 'my_light.position')
        GL.glUniform3fv(light_pos, 1, self.light_position)
        light_col = GL.glGetUniformLocation(program, 'my_light.color')
        GL.glUniform3fv(light_col, 1, self.light_color)
        amb_coef = GL.glGetUniformLocation(program, 'my_light.ambient_coef')
        GL.glUniform1fv(amb_coef, 1, self.light_ambient_coef)
        shiny = GL.glGetUniformLocation(program, 'my_light.shininess')
        GL.glUniform1fv(shiny, 1, self.light_shininess)
        intensity = GL.glGetUniformLocation(program, 'my_light.intensity')
        GL.glUniform3fv(intensity, 1, self.light_intensity)
        spec_col = GL.glGetUniformLocation(program, 'my_light.specular_color')
        GL.glUniform3fv(spec_col, 1, self.light_specular_color)
        cam_pos = GL.glGetUniformLocation(program, 'cam_pos')
        GL.glUniform3fv(cam_pos, 1, self.glcamera.get_position())
        return True
    
    def load_dot_params(self, program):
        """ Function doc
        """
        # Extern line
        linewidth = float(80/abs(self.dist_cam_zrp))
        if linewidth > 3.73:
            linewidth = 3.73
        # Intern line
        antialias = float(80/abs(self.dist_cam_zrp))
        if antialias > 3.73:
            antialias = 3.73
        # Dot size factor
        dot_factor = float(500/abs(self.dist_cam_zrp))
        if dot_factor > 150.0:
            dot_factor = 150.0
        uni_vext_linewidth = GL.glGetUniformLocation(program, 'vert_ext_linewidth')
        GL.glUniform1fv(uni_vext_linewidth, 1, linewidth)
        uni_vint_antialias = GL.glGetUniformLocation(program, 'vert_int_antialias')
        GL.glUniform1fv(uni_vint_antialias, 1, antialias)
        uni_dot_size = GL.glGetUniformLocation(program, 'vert_dot_factor')
        GL.glUniform1fv(uni_dot_size, 1, dot_factor)
        return True
    
    def _load_data(self):
        """ In this function you load the data to be displayed. Because of
            using the flag the program loads the data just once. Here you
            bind the coordinates data to the buffer array.
        """
        for visObj in self.vismolSession.vismol_objects:
            shapes._make_gl_dots (self.dots_program,  vismol_object = visObj)
            shapes._make_gl_lines(self.lines_program, vismol_object = visObj)
            
            #visObj.dots_vao,  visObj.dot_buffers   = shapes.make_gl_dots(self.dots_program, visObj.atoms)
            #visObj.lines_vao, visObj.line_buffers  = shapes._make_gl_lines(self.lines_program, visObj.index_bonds, visObj.atoms)
            #visObj.lines_vao, visObj.line_buffers  = shapes._make_gl_lines(self.lines_program, vismol_object = visObj)

        self.modified_data = False
    
    def draw_dots(self):
        """ Function doc
        """
        for visObj in self.vismolSession.vismol_objects:
            if visObj.dots_vao is not None:
                GL.glBindVertexArray(visObj.dots_vao)
                if self.modified_view:
                    pass
                    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, visObj.dot_buffers[0])
                    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, visObj.dot_indexes.itemsize*int(len(visObj.dot_indexes)), visObj.dot_indexes, GL.GL_DYNAMIC_DRAW)
                    GL.glDrawElements(GL.GL_POINTS, int(len(visObj.dot_indexes)), GL.GL_UNSIGNED_SHORT, None)
                    GL.glBindVertexArray(0)
                    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
                    self.modified_view = False
                else:
                    GL.glDrawElements(GL.GL_POINTS, int(len(visObj.dot_indexes)), GL.GL_UNSIGNED_SHORT, None)
                GL.glBindVertexArray(0)
    

    def _draw_dots(self, visObj = None):
        """ Function doc
        """

        if visObj.dots_vao is not None:
            GL.glBindVertexArray(visObj.dots_vao)
            
            if self.modified_view:
                pass
            #    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, visObj.dot_buffers[0])
            #    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, visObj.dot_indexes.itemsize*int(len(visObj.dot_indexes)), visObj.dot_indexes, GL.GL_DYNAMIC_DRAW)
            #    GL.glDrawElements(GL.GL_POINTS, int(len(visObj.dot_indexes)), GL.GL_UNSIGNED_SHORT, None)
            #    GL.glBindVertexArray(0)
            #    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
            #    self.modified_view = False
            else:
                GL.glBindBuffer(GL.GL_ARRAY_BUFFER, visObj.dot_buffers[0])
                GL.glBufferData(GL.GL_ARRAY_BUFFER, visObj.frames[self.frame].itemsize*int(len(visObj.frames[self.frame])), 
                                visObj.frames[self.frame], 
                                GL.GL_STATIC_DRAW)   
                GL.glDrawElements(GL.GL_POINTS, int(len(visObj.index_bonds)), GL.GL_UNSIGNED_SHORT, None)
        GL.glBindVertexArray(0)



    def _draw_lines(self, visObj = None):
        """ Function doc
        """
        if visObj.lines_vao is not None:
            GL.glBindVertexArray(visObj.lines_vao)
            if self.modified_view:
                pass
                #GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, visObj.line_buffers[0])
                #GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, visObj.line_indexes.itemsize*int(len(visObj.line_indexes)), visObj.line_indexes, GL.GL_DYNAMIC_DRAW)
                #GL.glDrawElements(GL.GL_LINES, int(len(visObj.line_indexes)), GL.GL_UNSIGNED_SHORT, None)
                #GL.glBindVertexArray(0)
                #GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
                #self.modified_data = False
                
                #- - - - -  SHOW HIDE - - - - -
                #id self.modified_show:
                    #GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, visObj.line_buffers[0])
                    #GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, visObj.line_indexes.itemsize*int(len(visObj.line_indexes)), visObj.line_indexes, GL.GL_DYNAMIC_DRAW)
                    #GL.glDrawElements(GL.GL_LINES, int(len(visObj.line_indexes)), GL.GL_UNSIGNED_SHORT, None)
                    #GL.glBindVertexArray(0)
                    #GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
                    #self.modified_data = False
                
                # - - - - - COLOR - - - - -
                #if self.modified_color:
                    #GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, visObj.line_buffers[2])
                    #GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, visObj.line_indexes.itemsize*int(len(visObj.line_indexes)), visObj.line_indexes, GL.GL_DYNAMIC_DRAW)
                    #GL.glDrawElements(GL.GL_LINES, int(len(visObj.line_indexes)), GL.GL_UNSIGNED_SHORT, None)
                    #GL.glBindVertexArray(0)
                    #GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
                    #self.modified_data = False
           
            else:
                #coord_vbo = GL.glGenBuffers(1)
                GL.glBindBuffer(GL.GL_ARRAY_BUFFER, visObj.line_buffers[1])
                GL.glBufferData(GL.GL_ARRAY_BUFFER, visObj.frames[self.frame].itemsize*int(len(visObj.frames[self.frame])), 
                                visObj.frames[self.frame], 
                                GL.GL_STATIC_DRAW)              
                GL.glDrawElements(GL.GL_LINES, int(len(visObj.index_bonds)*2), GL.GL_UNSIGNED_SHORT, None)
        GL.glBindVertexArray(0)

            
        #for visObj in self.vismolSession.vismol_objects:
        #    if visObj.lines_vao is not None:
        #        GL.glBindVertexArray(visObj.lines_vao)
        #        if self.modified_view:
        #            pass
        #            #GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, visObj.line_buffers[0])
        #            #GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, visObj.line_indexes.itemsize*int(len(visObj.line_indexes)), visObj.line_indexes, GL.GL_DYNAMIC_DRAW)
        #            #GL.glDrawElements(GL.GL_LINES, int(len(visObj.line_indexes)), GL.GL_UNSIGNED_SHORT, None)
        #            #GL.glBindVertexArray(0)
        #            #GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
        #            #self.modified_data = False
        #        else:
        #            GL.glDrawElements(GL.GL_LINES, int(len(visObj.index_bonds)*2), GL.GL_UNSIGNED_SHORT, None)
        #assert(len(self.lines_vao)>0)
        #GL.glBindVertexArray(self.lines_vao[0])
        #GL.glDrawArrays(GL.GL_LINES, 0, len(self.vismolSession.vismol_objects[0].index_bonds)*2)
        #GL.glBindVertexArray(0)
    
    def make_lines (self, vismol_object):
        """ Function doc """
        shapes._make_gl_lines(self.lines_program, vismol_object = vismol_object)
    
    def draw_lines(self):
        """ Function doc
        """
        for visObj in self.vismolSession.vismol_objects:
            if visObj.lines_vao is not None:
                GL.glBindVertexArray(visObj.lines_vao)
                if self.modified_view:
                    pass
                    #GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, visObj.line_buffers[0])
                    #GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, visObj.line_indexes.itemsize*int(len(visObj.line_indexes)), visObj.line_indexes, GL.GL_DYNAMIC_DRAW)
                    #GL.glDrawElements(GL.GL_LINES, int(len(visObj.line_indexes)), GL.GL_UNSIGNED_SHORT, None)
                    #GL.glBindVertexArray(0)
                    #GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
                    #self.modified_data = False
                else:
                    GL.glDrawElements(GL.GL_LINES, int(len(visObj.index_bonds)*2), GL.GL_UNSIGNED_SHORT, None)
        GL.glBindVertexArray(0)
        #assert(len(self.lines_vao)>0)
        #GL.glBindVertexArray(self.lines_vao[0])
        #GL.glDrawArrays(GL.GL_LINES, 0, len(self.vismolSession.vismol_objects[0].index_bonds)*2)
        #GL.glBindVertexArray(0)
    
    def draw_axis(self, flag):
        """ Function doc
        """
        if flag:
            GL.glBindVertexArray(self.axis.x_vao)
            GL.glDrawElements(GL.GL_TRIANGLES, len(self.axis.axis_indexes), GL.GL_UNSIGNED_SHORT, None)
            GL.glBindVertexArray(0)
            GL.glBindVertexArray(self.axis.y_vao)
            GL.glDrawElements(GL.GL_TRIANGLES, len(self.axis.axis_indexes), GL.GL_UNSIGNED_SHORT, None)
            GL.glBindVertexArray(0)
            GL.glBindVertexArray(self.axis.z_vao)
            GL.glDrawElements(GL.GL_TRIANGLES, len(self.axis.axis_indexes), GL.GL_UNSIGNED_SHORT, None)
            GL.glBindVertexArray(0)
        else:
            GL.glBindVertexArray(self.axis.lines_vao)
            GL.glDrawArrays(GL.GL_LINES, 0, len(self.axis.lines_vertices))
            GL.glBindVertexArray(0)
    
    def draw_dots_surface(self):
        """ Function doc
        """
        assert(len(self.dots_surf_vao)>0)
        GL.glPointSize(2)
        for i,atom in enumerate(self.dot_surface_list):
            GL.glBindVertexArray(self.dots_surf_vao[i])
            GL.glDrawArrays(GL.GL_POINTS, 0, atom.vertices)
            GL.glBindVertexArray(0)
        GL.glPointSize(2)
    
    def draw_spheres(self):
        """ Function doc
        """
        assert(len(self.spheres_vao)>0)
        for i,atom in enumerate(self.sphere_list):
            GL.glBindVertexArray(self.spheres_vao[i])
            GL.glDrawElements(GL.GL_TRIANGLES, atom.triangles, GL.GL_UNSIGNED_SHORT, None)
            GL.glBindVertexArray(0)
    
    def draw_crystal(self):
        """ Function doc
        """
        assert(len(self.crystal_list)>0)
        GL.glEnable(GL.GL_DEPTH_TEST)
        #GL.glDepthFunc(GL.GL_EQUAL)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_SRC_ALPHA)
        GL.glEnable(GL.GL_CULL_FACE)
        for i,atom in enumerate(self.crystal_list):
            GL.glBindVertexArray(self.outer_cryst_vao[i])
            GL.glDrawElements(GL.GL_TRIANGLES, atom.triangles, GL.GL_UNSIGNED_SHORT, None)
            GL.glBindVertexArray(0)
        #GL.glDepthFunc(GL.GL_LESS)
        GL.glDisable(GL.GL_BLEND)
        GL.glDisable(GL.GL_CULL_FACE)
    
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
            GL.glDrawElements(GL.GL_TRIANGLES, self.stick_indexes, GL.GL_UNSIGNED_SHORT, None)
            GL.glBindVertexArray(0)
    
    def draw_ribbons(self):
        """ Function doc
        """
        assert(len(self.ribbons_vao)>0)
        for i,bond in enumerate(self.ribbons_vao):
            GL.glBindVertexArray(self.ribbons_vao[i])
            GL.glDrawElements(GL.GL_TRIANGLES, self.ribbon_indexes, GL.GL_UNSIGNED_SHORT, None)
            GL.glBindVertexArray(0)
    
    def key_pressed(self, widget, event):
        """ The mouse_button function serves, as the names states, to catch
            events in the keyboard, e.g. letter 'l' pressed, 'backslash'
            pressed. Note that there is a difference between 'A' and 'a'.
            Here I use a specific handler for each key pressed after
            discarding the CONTROL, ALT and SHIFT keys pressed (usefull
            for customized actions) and maintained, i.e. it's the same as
            using Ctrl+Z to undo an action.
        """
        k_name = Gdk.keyval_name(event.keyval)
        func = getattr(self, '_pressed_' + k_name, None)
        print(k_name, 'key Pressed')
        if func:
            func()
        return True
    
    def key_released(self, widget, event):
        """ Used to indicates a key has been released.
        """
        k_name = Gdk.keyval_name(event.keyval)
        func = getattr(self, '_released_' + k_name, None)
        print(k_name, 'key released')
        if func:
            func()
        
        if k_name == 'Right':
            self.frame +=1
            print (self.frame)
        if k_name == 'Left':
            self.frame -=1
            print (self.frame)
        self.queue_draw()
        return True
    
    def _pressed_Control_L(self):
        """ Function doc
        """
        self.ctrl = True
        return True
    
    def _released_Control_L(self):
        """ Function doc
        """
        self.ctrl = False
        return True
    
    def delete_vaos(self):
        """ Function doc
        """
        # Ball-Stick representation
        if len(self.ball_stick_vao)>0:
            GL.glDeleteVertexArrays(int(len(self.ball_stick_vao)), self.ball_stick_vao)
            GL.glDeleteVertexArrays(int(len(self.bond_stick_vao)), self.bond_stick_vao)
            self.ball_stick_vao = []
            self.bond_stick_vao = []
        # Ribbon representation
        if len(self.ribbons_vao)>0:
            GL.glDeleteVertexArrays(int(len(self.ribbons_vao)), self.ribbons_vao)
            self.ribbons_vao = []
        # Covalent radius representation
        if len(self.spheres_vao)>0:
            GL.glDeleteVertexArrays(int(len(self.spheres_vao)), self.spheres_vao)
            self.spheres_vao = []
        # Dots representation
        if len(self.dots_surf_vao)>0:
            GL.glDeleteVertexArrays(int(len(self.dots_surf_vao)), self.dots_surf_vao)
            self.dots_surf_vao = []
        # Dotted surface representation
        if len(self.dots_vao)>0:
            GL.glDeleteVertexArrays(int(len(self.dots_vao)), self.dots_vao)
            self.dots_vao = []
        # Lines representation
        if len(self.lines_vao)>0:
            GL.glDeleteVertexArrays(int(len(self.lines_vao)), self.lines_vao)
            self.lines_vao = []
        # Van der Waals representation
        if len(self.vdw_vao)>0:
            GL.glDeleteVertexArrays(int(len(self.vdw_vao)), self.vdw_vao)
            self.vdw_vao = []
        # Transparent Representataion
        if len(self.inner_cryst_vao)>0:
            GL.glDeleteVertexArrays(int(len(self.inner_cryst_vao)), self.inner_cryst_vao)
            GL.glDeleteVertexArrays(int(len(self.bond_cryst_vao)), self.bond_cryst_vao)
            GL.glDeleteVertexArrays(int(len(self.outer_cryst_vao)), self.outer_cryst_vao)
            self.inner_cryst_vao = []
            self.bond_cryst_vao = []
            self.outer_cryst_vao = []
    
    def mouse_pressed(self, widget, event):
        left   = event.button==1 and event.type==Gdk.EventType.BUTTON_PRESS
        middle = event.button==2 and event.type==Gdk.EventType.BUTTON_PRESS
        right  = event.button==3 and event.type==Gdk.EventType.BUTTON_PRESS
        self.mouse_rotate = left   and not (middle or right)
        self.mouse_zoom   = right  and not (middle or left)
        self.mouse_pan    = middle and not (right  or left)
        x = self.mouse_x = event.x
        y = self.mouse_y = event.y
        self.drag_pos_x, self.drag_pos_y, self.drag_pos_z = self.pos(x, y)
        self.dragging = False
    
        
        if event.button == 1 and event.type == Gdk.EventType.BUTTON_PRESS:
            pass
            #print ('event.button == 1')
            #nearest, hits = self.pick(x, self.get_allocation().height-1-y, self.pick_radius[0], self.pick_radius[1], event)
            #selected = self.select(event, nearest, hits)
            #if selected is not None:
            #    self.center_on_atom(selected.pos)
            #    self.zero_reference_point = selected.pos
            #    self.target_point = selected.pos
        if event.button == 2 and event.type == Gdk.EventType.BUTTON_PRESS:
            pass
            #print ('event.button == 2')
            #self.dist_cam_zpr = op.get_euclidean(self.zero_reference_point, self.get_cam_pos())
        if event.button == 3 and event.type == Gdk.EventType.BUTTON_PRESS:
            pass
            #print ('event.button == 3')
            #self.pos_mouse = [x, y]
    
    
    def mouse_released(self, widget, event):
        pass
        self.mouse_rotate = self.mouse_zoom = self.mouse_pan = False
        if event.button==3:
            if self.dragging:
                self.dragging = False
            else:
                self.glMenu.open_gl_menu(event = event)
        if event.button==1:
            if self.dragging:
                self.dragging = False
            else:
                print('funcao de selecao')
                
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
        if self.mouse_rotate:
            angle = math.sqrt(dx**2+dy**2)/float(self.width+1)*180.0
            for visObj in self.vismolSession.vismol_objects:
                if self.ctrl:
                    if abs(dx) >= abs(dy):
                        if (y-self.height/2) < 0:
                            visObj.model_mat = mop.my_glRotatef(visObj.model_mat, angle, [0, 0, dx])
                        else:
                            visObj.model_mat = mop.my_glRotatef(visObj.model_mat, angle, [0, 0, -dx])
                    else:
                        if (x-self.width/2) < 0:
                            visObj.model_mat = mop.my_glRotatef(visObj.model_mat, angle, [0, 0, -dy])
                        else:
                            visObj.model_mat = mop.my_glRotatef(visObj.model_mat, angle, [0, 0, dy])
                else:
                    visObj.model_mat = mop.my_glRotatef(visObj.model_mat, angle, [-dy, -dx, 0])
                visObj.normal_mat = self.update_normal_mat(visObj.model_mat)
            
            self.axis.model_mat = mop.my_glTranslatef(self.axis.model_mat, -self.axis.zrp)
            if self.ctrl:
                if abs(dx) >= abs(dy):
                    if (y-self.height/2) < 0:
                        self.axis.model_mat = mop.my_glRotatef(self.axis.model_mat, angle, [0, 0, dx])
                    else:
                        self.axis.model_mat = mop.my_glRotatef(self.axis.model_mat, angle, [0, 0, -dx])
                else:
                    if (x-self.width/2) < 0:
                        self.axis.model_mat = mop.my_glRotatef(self.axis.model_mat, angle, [0, 0, -dy])
                    else:
                        self.axis.model_mat = mop.my_glRotatef(self.axis.model_mat, angle, [0, 0, dy])
            else:
                self.axis.model_mat = mop.my_glRotatef(self.axis.model_mat, angle, [dy, dx, 0])
            self.axis.normal_mat = self.update_normal_mat(self.axis.model_mat)
            self.axis.model_mat = mop.my_glTranslatef(self.axis.model_mat, self.axis.zrp)
            
            changed = True
        elif self.mouse_pan:
            px, py, pz = self.pos(x, y)
            pan_matrix = mop.my_glTranslatef(np.identity(4,dtype=np.float32),
                [(px-self.drag_pos_x)*self.glcamera.z_far/10, 
                 (py-self.drag_pos_y)*self.glcamera.z_far/10, 
                 (pz-self.drag_pos_z)*self.glcamera.z_far/10])
            for visObj in self.vismolSession.vismol_objects:
                visObj.model_mat = mop.my_glMultiplyMatricesf(visObj.model_mat, pan_matrix)
                visObj.normal_mat = self.update_normal_mat(visObj.model_mat)
            self.drag_pos_x = px
            self.drag_pos_y = py
            self.drag_pos_z = pz
            changed = True
        elif self.mouse_zoom:
            delta = (((self.glcamera.z_far-self.glcamera.z_near)/2)+self.glcamera.z_near)/200
            move_z = dy * delta
            self.glcamera.set_view_matrix(mop.my_glTranslatef(self.glcamera.view_matrix, [0.0, 0.0, move_z]))
            
            self.glcamera.z_near += -move_z
            self.glcamera.z_far += -move_z
            self.glcamera.fog_start += -move_z
            self.glcamera.fog_end += -move_z
            if self.glcamera.z_near >= 0.1:
                self.glcamera.set_projection_matrix(mop.my_glPerspectivef(self.glcamera.field_of_view, 
                        self.glcamera.viewport_aspect_ratio, self.glcamera.z_near, self.glcamera.z_far))
            else:
                self.glcamera.set_projection_matrix(mop.my_glPerspectivef(self.glcamera.field_of_view, 
                        self.glcamera.viewport_aspect_ratio, 0.1, self.glcamera.z_far))
            self.dist_cam_zrp += -move_z
            changed = True
        self.dragging = True
        if changed:
            self.queue_draw()
        
    def mouse_scroll(self, widget, event):
        """ Function doc
        """
        if self.ctrl:
            for visObj in self.vismolSession.vismol_objects:
                if event.direction == Gdk.ScrollDirection.UP:
                    visObj.model_mat = mop.my_glTranslatef(visObj.model_mat, [0.0, 0.0, -self.scroll])
                if event.direction == Gdk.ScrollDirection.DOWN:
                    visObj.model_mat = mop.my_glTranslatef(visObj.model_mat, [0.0, 0.0, self.scroll])
        else:
            if event.direction == Gdk.ScrollDirection.UP:
                self.glcamera.z_near -= self.scroll
                self.glcamera.z_far += self.scroll
                self.glcamera.fog_start += self.scroll
                self.glcamera.fog_end += self.scroll
            if event.direction == Gdk.ScrollDirection.DOWN:
                self.glcamera.z_near += self.scroll
                self.glcamera.z_far -= self.scroll
                self.glcamera.fog_start -= self.scroll
                self.glcamera.fog_end -= self.scroll
            if self.glcamera.z_near < 0:
                self.glcamera.z_near = 0.001
            if self.glcamera.z_far < self.glcamera.z_near:
                self.glcamera.z_near -= self.scroll
                self.glcamera.z_far = self.glcamera.z_near + 0.05
                self.glcamera.fog_start = self.glcamera.z_near + 0.05
                self.glcamera.fog_end = self.glcamera.z_near + 2.05
        self.glcamera.set_projection_matrix(mop.my_glPerspectivef(self.glcamera.field_of_view, 
                        self.glcamera.viewport_aspect_ratio, self.glcamera.z_near, self.glcamera.z_far))
        self.queue_draw()
    
    def update_normal_mat(self, model_mat):
        """ Function doc
        """
        #modelview = mop.my_glMultiplyMatricesf(self.glcamera.get_view_matrix(), self.model_mat)
        modelview = mop.my_glMultiplyMatricesf(self.glcamera.view_matrix, model_mat)
        normal_mat = np.matrix(modelview[:3,:3]).I.T
        #self.normal_mat = np.array(normal_mat)
        return np.array(normal_mat)
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
    
    def test_gl(self):
        """ Function doc
        """
        print("Test function init")
        #self.data = self.vismolSession
        #for visObj in self.vismolSession.vismol_objects:
        #    visObj.generate_dot_indexes()
        #self.modified_data = True
        #self._load_data()
        #self.DOTS = not self.DOTS
        #self.LINES = not self.LINES
        #self.queue_draw()
        print("Test function OK")
        return True
    
    def test_hide(self):
        """ Function doc
        """
        self.modified_view = True
        for visObj in self.vismolSession.vismol_objects:
            visObj.dot_indexes = np.array([1,3,5,7,9], dtype=np.uint16)
        self.queue_draw()
        print("hiding")
        
    def test_show(self):
        """ Function doc
        """
        self.modified_view = True
        for visObj in self.vismolSession.vismol_objects:
            visObj.dot_indexes = np.array([0,1,2,3,4,5,6,7,8,9], dtype=np.uint16)
        self.queue_draw()
        print("showing")

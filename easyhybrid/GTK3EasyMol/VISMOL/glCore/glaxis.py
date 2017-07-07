#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  glaxis.py
#  
#  Copyright 2017 Carlos Eduardo Sequeiros Borja <casebor@gmail.com>
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

import ctypes
import numpy as np
import VISMOL.glCore.matrix_operations as mop

import OpenGL
from OpenGL import GL
from OpenGL.GL import shaders

class GLAxis:
    """ Class doc
    """
    
    def __init__ (self):
        """ Class initialiser
        """
        self.axis_vertices = {'x_axis' : np.array(
        [-0.85000000, -0.85000000,  0.00000000,
         -0.85000000, -0.86464466, -0.03535534,
         -0.85000000, -0.90000000, -0.05000000,
         -0.85000000, -0.93535534, -0.03535534,
         -0.85000000, -0.95000000,  0.00000000,
         -0.85000000, -0.93535534,  0.03535534,
         -0.85000000, -0.90000000,  0.05000000,
         -0.85000000, -0.86464466,  0.03535534,
         -0.77500000, -0.90000000,  0.00000000], dtype=np.float32),
         'y_axis' : np.array(
        [-0.90000000, -0.85000000, -0.05000000,
         -0.86464466, -0.85000000, -0.03535534,
         -0.85000000, -0.85000000,  0.00000000,
         -0.86464466, -0.85000000,  0.03535534,
         -0.90000000, -0.85000000,  0.05000000,
         -0.93535534, -0.85000000,  0.03535534,
         -0.95000000, -0.85000000,  0.00000000,
         -0.93535534, -0.85000000, -0.03535534,
         -0.90000000, -0.77500000,  0.00000000], dtype=np.float32),
        'z_axis' : np.array(
        [-0.90000000, -0.85000000, -0.05000000,
         -0.86464466, -0.86464466, -0.05000000,
         -0.85000000, -0.90000000, -0.05000000,
         -0.86464466, -0.93535534, -0.05000000,
         -0.90000000, -0.95000000, -0.05000000,
         -0.93535534, -0.93535534, -0.05000000,
         -0.95000000, -0.90000000, -0.05000000,
         -0.93535534, -0.86464466, -0.05000000,
         -0.90000000, -0.90000000, -0.12500000], dtype=np.float32)}
        self.axis_indexes = np.array([0, 1, 8, 1, 2, 8, 2, 3, 8, 3, 4, 8,
                                      4, 5, 8, 5, 6, 8, 6, 7, 8, 7, 0, 8], dtype=np.uint16)
        self.axis_centers = {'x_axis' : [0.0, 0.0, 0.0],
                             'y_axis' : [0.0, 0.0, 0.0],
                             'z_axis' : [0.0, 0.0, 0.0]}
        self.axis_colors = {'x_axis' : [1.0, 0.0, 0.0],
                            'y_axis' : [0.0, 1.0, 0.0],
                            'z_axis' : [0.0, 0.0, 1.0]}
        self.model_mat = np.identity(4, dtype=np.float32)
        self.normal_mat = np.identity(3, dtype=np.float32)
        self.gl_axis_program = None
        self.x_vao = None
        self.y_vao = None
        self.z_vao = None
        self.vertex_shader_axis = """
#version 330

uniform mat4 model_mat;
uniform mat3 normal_mat;

in vec3 vert_coord;
in vec3 vert_center;
in vec3 vert_color;

out vec3 frag_coord;
out vec3 frag_color;
out vec3 frag_normal;

void main(){
    vec3 coord = vec3(model_mat * vec4(vert_coord, 1.0));
    gl_Position = vec4(coord, 1.0);
    frag_coord = -coord;
    frag_normal = normalize(normal_mat * (vert_coord - vert_center));
    frag_color = vert_color;
}
"""
        self.fragment_shader_axis = """
#version 330

struct Light {
   vec3 position;
   vec3 color;
   vec3 intensity;
   vec3 specular_color;
   float ambient_coef;
   float shininess;
};

uniform Light my_light;
uniform mat4 model_mat;
uniform mat3 normal_mat;

in vec3 frag_coord;
in vec3 frag_color;
in vec3 frag_normal;

out vec4 final_color;

void main(){
    vec3 normal = normalize(frag_normal);
    vec3 vert_to_light = normalize(my_light.position-frag_coord);
    vec3 vert_to_cam = normalize(frag_coord);
    
    // Ambient Component
    vec3 ambient = my_light.ambient_coef * frag_color * my_light.intensity;
    
    // Diffuse component
    float diffuse_coef = max(0.0, dot(normal, vert_to_light));
    vec3 diffuse = diffuse_coef * frag_color * my_light.intensity;
    
    // Specular component
    float specular_coef = 0.0;
    if (diffuse_coef > 0.0)
        specular_coef = pow(max(0.0, dot(vert_to_cam, reflect(-vert_to_light, normal))), my_light.shininess);
    vec3 specular = specular_coef * my_light.intensity;
    specular = specular * (vec3(1) - diffuse);
    
    final_color = vec4(ambient + diffuse + specular, 1.0);
}
"""
        self.zrp = np.array([-0.9, -0.9, 0.0],dtype=np.float32)
        self.light_position = np.array([2.5,2.5,3.0],dtype=np.float32)
        self.light_color = np.array([1.0,1.0,1.0,1.0],dtype=np.float32)
        self.light_intensity = np.array([0.6,0.6,0.6],dtype=np.float32)
        self.light_specular_color = np.array([1.0,1.0,1.0],dtype=np.float32)
        self.light_ambient_coef = 0.5
        self.light_shininess = 5.5
    
    def make_vaos(self):
        """ Function doc
        """
        self.x_vao = self._get_vao('x_axis')
        self.y_vao = self._get_vao('y_axis')
        self.z_vao = self._get_vao('z_axis')
        return True
        
    def make_axis_program(self):
        """ Function doc
        """
        v_shader = GL.glCreateShader(GL.GL_VERTEX_SHADER)
        GL.glShaderSource(v_shader, self.vertex_shader_axis)
        GL.glCompileShader(v_shader)
        f_shader = GL.glCreateShader(GL.GL_FRAGMENT_SHADER)
        GL.glShaderSource(f_shader, self.fragment_shader_axis)
        GL.glCompileShader(f_shader)
        self.gl_axis_program = GL.glCreateProgram()
        GL.glAttachShader(self.gl_axis_program, v_shader)
        GL.glAttachShader(self.gl_axis_program, f_shader)
        GL.glLinkProgram(self.gl_axis_program)
        return True
        
    def _get_vao(self, axis):
        """ Function doc
        """
        centers = self.axis_centers[axis] * int(len(self.axis_vertices[axis]))
        centers = np.array(centers, dtype=np.float32)
        colors = self.axis_colors[axis] * int(len(self.axis_vertices[axis]))
        colors = np.array(colors, dtype=np.float32)
        
        vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vao)
        
        ind_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, self.axis_indexes.itemsize*int(len(self.axis_indexes)), self.axis_indexes, GL.GL_STATIC_DRAW)
    
        vert_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vert_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.axis_vertices[axis].itemsize*int(len(self.axis_vertices[axis])), self.axis_vertices[axis], GL.GL_STATIC_DRAW)
        
        att_position = GL.glGetAttribLocation(self.gl_axis_program, 'vert_coord')
        GL.glEnableVertexAttribArray(att_position)
        GL.glVertexAttribPointer(att_position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*self.axis_vertices[axis].itemsize, ctypes.c_void_p(0))
    
        center_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, center_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, centers.itemsize*int(len(centers)), centers, GL.GL_STATIC_DRAW)
        
        att_center = GL.glGetAttribLocation(self.gl_axis_program, 'vert_center')
        GL.glEnableVertexAttribArray(att_center)
        GL.glVertexAttribPointer(att_center, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*centers.itemsize, ctypes.c_void_p(0))
        
        col_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*int(len(colors)), colors, GL.GL_STATIC_DRAW)
        
        att_colors = GL.glGetAttribLocation(self.gl_axis_program, 'vert_color')
        GL.glEnableVertexAttribArray(att_colors)
        GL.glVertexAttribPointer(att_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
        
        GL.glBindVertexArray(0)
        GL.glDisableVertexAttribArray(att_position)
        GL.glDisableVertexAttribArray(att_colors)
        GL.glDisableVertexAttribArray(att_center)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
        
        return vao
    
    def load_params(self):
        """ Function doc
        """
        model = GL.glGetUniformLocation(self.gl_axis_program, 'model_mat')
        GL.glUniformMatrix4fv(model, 1, GL.GL_FALSE, self.model_mat)
        norm = GL.glGetUniformLocation(self.gl_axis_program, 'normal_mat')
        GL.glUniformMatrix3fv(norm, 1, GL.GL_FALSE, self.normal_mat)
        light_pos = GL.glGetUniformLocation(self.gl_axis_program, 'my_light.position')
        GL.glUniform3fv(light_pos, 1, self.light_position)
        light_col = GL.glGetUniformLocation(self.gl_axis_program, 'my_light.color')
        GL.glUniform3fv(light_col, 1, self.light_color)
        amb_coef = GL.glGetUniformLocation(self.gl_axis_program, 'my_light.ambient_coef')
        GL.glUniform1fv(amb_coef, 1, self.light_ambient_coef)
        shiny = GL.glGetUniformLocation(self.gl_axis_program, 'my_light.shininess')
        GL.glUniform1fv(shiny, 1, self.light_shininess)
        intensity = GL.glGetUniformLocation(self.gl_axis_program, 'my_light.intensity')
        GL.glUniform3fv(intensity, 1, self.light_intensity)
        spec_col = GL.glGetUniformLocation(self.gl_axis_program, 'my_light.specular_color')
        GL.glUniform3fv(spec_col, 1, self.light_specular_color)
    
    

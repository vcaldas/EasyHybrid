#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  glcamera.py
#  
#  Copyright 2016 Labio <labio@labio-XPS-8300>
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
import VISMOL.glCore.matrix_operations as mop
import VISMOL.glCore.operations as op

class GLCamera():
    """ The GLCamera object creates a "camera" to be used in OpenGL.
        It automatically creates a viewing and projection matrices with the
        values defined in the constructor.
    """
    
    def __init__ (self, fov=30.0, var=(4.0/3.0), pos=np.array([0,0,10],dtype=np.float32), zrp=np.array([0,0,0],dtype=np.float32)):
        """ Depending of the distance from the camera position to a defined
            reference point, it creates different clipping planes (this function
            could be improved, but will work for now).
            
            Input parameters:
             + fov = Specifies the field of view angle, in degrees, in the y direction.
             + var = Specifies the aspect ratio that determines the field of
                     view in the x direction. The aspect ratio is the ratio
                     of x (width) to y (height).
             + pos = The position in world coordinates of the camera.
             + zrp = The zero reference point defined for rotation functions.
            
            Automatically generates:
             + z_near = Specifies the distance from the viewer to the near
                        clipping plane (always positive).
             + z_far = Specifies the distance from the viewer to the far
                       clipping plane (always positive).
             + fog_start = Specifies the beggining of the fog effect (always
                           positive and lower than z_far).
             + fog_end = Specifies the end of the fog effect (always positive
                         and preferable equal to z_far).
             + view_matrix = The viewing matrix used in the render by shaders.
             + projection_matrix = The projection matrix used in the render
                                   by shaders.
        """
        self.field_of_view = np.float32(fov)
        self.viewport_aspect_ratio = np.float32(var)
        self.zero_reference_point = np.array(zrp, dtype=np.float32)
        self.max_vertical_angle = 85.0  # must be less than 90 to avoid gimbal lock
        self.horizontal_angle = 0.0
        self.vertical_angle = 0.0
        self.min_znear = 0.1
        self.min_zfar = 2.5
        dist = op.get_euclidean(pos, zrp)
        if dist < 10.0:
            self.z_near = dist - 3.0
            self.z_far = dist + 3.0
        elif dist < 20.0:
            self.z_near = dist - 6.0
            self.z_far = dist + 6.0
        elif dist < 40.0:
            self.z_near = dist - 9.0
            self.z_far = dist + 9.0
        elif dist < 80.0:
            self.z_near = dist - 12.0
            self.z_far = dist + 12.0
        else:
            self.z_near = dist - 15.0
            self.z_far = dist + 15.0
        self.fog_end = self.z_far
        self.fog_start = self.fog_end - self.min_zfar
        self.view_matrix = self._get_view_matrix(pos)
        self.projection_matrix = self._get_projection_matrix()
    
    def _get_view_matrix(self, position):
        """ Function doc
        """
        trans = mop.my_glTranslatef(np.identity(4,dtype=np.float32), -position)
        orient = mop.my_glRotatef(np.identity(4,dtype=np.float32), self.vertical_angle, [1,0,0])
        orient = mop.my_glRotatef(orient, self.horizontal_angle, [0,1,0])
        view = mop.my_glMultiplyMatricesf(trans, orient)
        return view
    
    def _get_projection_matrix(self):
        """ Function doc
        """
        assert(self.field_of_view>0.0 and self.field_of_view<180.0)
        assert(self.z_near>0.0)
        assert(self.z_near<self.z_far)
        assert(self.viewport_aspect_ratio>0.0)
        return mop.my_glPerspectivef(self.field_of_view,self.viewport_aspect_ratio,self.z_near,self.z_far)
    
    def get_position(self):
        """ Returns the x, y, z position of the camera in 
            absolute coordinates.
        """
        return mop.get_xyz_coords(self.view_matrix)
    
    def _normalize_angles(self):
        """ Function doc
        """
        self.horizontal_angle = self.horizontal_angle % 360.0
        if self.horizontal_angle<0:
            self.horizontal_angle += 360.0
        if self.vertical_angle>self.max_vertical_angle:
            self.vertical_angle = self.max_vertical_angle
        elif self.vertical_angle<-self.max_vertical_angle:
            self.vertical_angle = -self.max_vertical_angle
    
    def add_orientation_angles(self, h_angle, v_angle):
        """ Function doc
        """
        self.horizontal_angle += h_angle
        self.vertical_angle += v_angle
        self._normalize_angles()
        return True
    
    def look_at(self, target):
        """ Function doc
        """
        pos = self.get_position()
        assert(position[0]!=target[0] and
               position[1]!=target[1] and
               position[2]!=target[2])
        direction = op.unit_vector(target - position)
        self.vertical_angle = -math.asin(direction[1])*180/math.pi
        self.horizontal_angle = -(math.atan2(-direction[0], -direction[2])*180/math.pi)
        self._normalize_angles()
        return True
    
    def get_proj_view_matrix(self):
        """ Function doc
        """
        return mop.my_glMultiplyMatricesf(self.get_projection_matrix(), self.get_view_matrix())
    
    def set_view_matrix(self, new_view_matrix):
        """ Function doc
        """
        self.view_matrix = new_view_matrix
    
    def set_projection_matrix(self, new_proj_matrix):
        """ Function doc
        """
        self.projection_matrix = new_proj_matrix
    
    def update_projection(self):
        """ Function doc
        """
        self.projection_matrix = mop.my_glPerspectivef(self.field_of_view, self.viewport_aspect_ratio, self.z_near, self.z_far)
        return True
    
    def update_fog(self):
        """ Function doc
        """
        self.fog_end = self.z_far
        self.fog_start = self.fog_end - self.min_zfar
        return True
    
    def print_parms(self):
        """ Function doc
        """
        print("######## GLCAMERA PARAMETERS ########")
        print("<= z_near    =>",self.z_near)
        print("<= z_far     =>",self.z_far)
        print("<= fog_start =>",self.fog_start)
        print("<= fog_end   =>",self.fog_end)
        print("<= position  =>",self.get_position())
        print("######## GLCAMERA PARAMETERS ########")
    
    def print_matrices(self):
        """ Function doc """
        print("######## GLCAMERA MATRICES ########")
        print("<= view_matrix =>", self.view_matrix)
        print("<= projection_matrix =>", self.projection_matrix)
        print("######## GLCAMERA MATRICES ########")
    
    

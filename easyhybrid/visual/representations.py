#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  representations.py
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

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from atom_types import get_color


gl_settings = {'sphere_scale':0.15, 'sphere_res':15, 'pretty_res':20}
cylinder = gluNewQuadric()

def init_gl(fog_start, fog_end, fovy, width, height, z_near, z_far):
    """ Inside the realize function, you should put all you OpenGL
	initialization code, e.g. set the projection matrix,
	the modelview matrix, position of the camera.
    """
    # All OpenGL initialization code goes here
    glMaterialfv(GL_FRONT,GL_AMBIENT, (.7,.7,.7,1.))
    glMaterialfv(GL_FRONT,GL_DIFFUSE, (.8,.8,.8,1.))
    glMaterialfv(GL_FRONT,GL_SPECULAR,(1.,1.,1.,1.))
    glMaterialfv(GL_FRONT,GL_SHININESS,100.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_NORMALIZE)
    glEnable(GL_COLOR_MATERIAL)
    # FOG
    glEnable(GL_FOG)
    glFogi(GL_FOG_MODE, GL_LINEAR)
    glFogf(GL_FOG_START, fog_start)
    glFogf(GL_FOG_END, fog_end)
    glFogfv(GL_FOG_COLOR, [0,0,0])
    glFogfv(GL_FOG_DENSITY, 1)
    glEnable(GL_POINT_SMOOTH)
    # light
    light_0_position = [ 1.0,  1.0, 1.0, 0.0]
    light_1_position = [ 1.0, -1.0, 1.0, 0.0]
    light_2_position = [-1.0, -1.0, 1.0, 0.0]
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glShadeModel(GL_SMOOTH)
    glLightfv(GL_LIGHT0, GL_POSITION, light_0_position)
    glLightfv(GL_LIGHT1, GL_POSITION, light_1_position)
    glLightfv(GL_LIGHT2, GL_POSITION, light_2_position)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT2)
    glEnable(GL_LIGHTING)
    glEnable(GL_DEPTH_TEST)
    #  Antialiased lines
    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
    # Initialize view
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovy, float(width)/float(height), z_near, z_far)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 10, 0, 0, 0, 0, 1, 0)

def draw_bond_line(atom1, atom2):
    """ Draw the bonds. Make use of the imported function
	atom_types.get_color(name).
    """
    glDisable(GL_LIGHT0)
    glDisable(GL_LIGHT1)
    glDisable(GL_LIGHT2)
    glDisable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glPushName(atom1.index)
    glColor3f(atom1.color[0], atom1.color[1], atom1.color[2])
    glLineWidth(3)
    glBegin(GL_LINES)
    glVertex3f(atom1.pos[0], atom1.pos[1], atom1.pos[2])
    glVertex3f(atom2.pos[0], atom2.pos[1], atom2.pos[2])
    glEnd()
    glPopName()
    glPopMatrix()

def draw_dot(atom, point):
    """
    """
    glDisable(GL_LIGHT0)
    glDisable(GL_LIGHT1)
    glDisable(GL_LIGHT2)
    glDisable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    #glPushName(atom.index)
    glColor3f(atom.color[0], atom.color[1], atom.color[2])
    glPointSize(2)
    glBegin(GL_POINTS)
    glVertex3f(point[0], point[1], point[2])
    glEnd()
    glPopName()
    glPopMatrix()

def draw_point(atom):
    """
    """
    glDisable(GL_LIGHT0)
    glDisable(GL_LIGHT1)
    glDisable(GL_LIGHT2)
    glDisable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glPushName(atom.index)
    glColor3f(atom.color[0], atom.color[1], atom.color[2])
    glPointSize(3)
    glBegin(GL_POINTS)
    glVertex3f(atom.pos[0], atom.pos[1], atom.pos[2])
    glEnd()
    glPopName()
    glPopMatrix()

def draw_ball(atom):
    """ Graphs a sphere for the given coordinates. Make use of the
	imported function atom_types.get_color(name).
    """
    # Enables the GL_LIGHT0 variable
    glEnable(GL_LIGHT0)
    # Enables lightin three dimensions, i guess
    glEnable(GL_LIGHTING)
    # Enables tha surface colors in 3D, i guess
    glEnable(GL_COLOR_MATERIAL)
    # Enables profundity effect, i guess
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(atom.pos[0], atom.pos[1], atom.pos[2])
    glPushName(atom.index)
    glColor3f(atom.color[0], atom.color[1], atom.color[2])
    glutSolidSphere(atom.radius/1.5, gl_settings['sphere_res'], gl_settings['sphere_res'])
    #quad = gluNewQuadric()
    #gluSphere(quad, atom_size/1.5, gl_settings['sphere_res'], gl_settings['sphere_res'])
    glPopName()
    glPopMatrix()
    glFlush()

def draw_sp(atom):
    """ Graphs a sphere for the given coordinates. Make use of the
	imported function atom_types.get_color(name).
    """
    # Enables the GL_LIGHT0 variable
    glEnable(GL_LIGHT0)
    # Enables lightin three dimensions, i guess
    glEnable(GL_LIGHTING)
    # Enables tha surface colors in 3D, i guess
    glEnable(GL_COLOR_MATERIAL)
    # Enables profundity effect, i guess
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(atom.pos[0], atom.pos[1], atom.pos[2])
    glPushName(atom.index)
    glColor3f(atom.color[0], atom.color[1], atom.color[2])
    #glutSolidSphere(atom.radius, gl_settings['sphere_res'], gl_settings['sphere_res'])
    glutWireSphere(atom.radius, gl_settings['sphere_res'], gl_settings['sphere_res'])
    glPopName()
    glPopMatrix()
    glFlush()

def draw_pretty_vdw(atom):
    """ Graphs a sphere for the given coordinates. Make use of the
	imported function atom_types.get_color(name).
    """
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    #glBlendFunc(GL_SRC_ALPHA, GL_DST_ALPHA)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(atom.pos[0], atom.pos[1], atom.pos[2])
    glPushName(atom.index)
    glColor4ub(atom.col_rgb[0], atom.col_rgb[1], atom.col_rgb[2], 60)
    glutSolidSphere(atom.vdw_rad, gl_settings['sphere_res'], gl_settings['sphere_res'])
    glPopName()
    glPopMatrix()
    glFlush()
    glDisable(GL_BLEND)

def draw_vdw(atom):
    """ Graphs a sphere for the given coordinates. Make use of the
	imported function atom_types.get_color(name).
    """
    # Enables the GL_LIGHT0 variable
    glEnable(GL_LIGHT0)
    # Enables lightin three dimensions, i guess
    glEnable(GL_LIGHTING)
    # Enables tha surface colors in 3D, i guess
    glEnable(GL_COLOR_MATERIAL)
    # Enables profundity effect, i guess
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(atom.pos[0], atom.pos[1], atom.pos[2])
    glPushName(atom.index)
    glColor3f(atom.col_rgb[0], atom.col_rgb[1], atom.col_rgb[2])
    glutSolidSphere(atom.vdw_rad, gl_settings['sphere_res'], gl_settings['sphere_res'])
    glPopName()
    glPopMatrix()
    glFlush()

def draw_bond_stick(atom, length, angle, vec_o):
    """ Draw the bonds. Make use of the imported function
	atom_types.get_color(name).
    """
    # The matris is by default looking at (0,0,1)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    gluQuadricNormals(cylinder, GLU_SMOOTH)
    gluQuadricTexture(cylinder, GL_TRUE)
    glPushMatrix()
    glPushName(atom.index)
    glColor3f(atom.color[0], atom.color[1], atom.color[2])
    glTranslatef(atom.pos[0], atom.pos[1], atom.pos[2])
    glRotatef(angle, vec_o[0], vec_o[1], vec_o[2])
    gluCylinder(cylinder, 0.1, 0.1, length, 10, 10)
    glPopName()
    glPopMatrix()

def change_light_properties(gl_ambient=None, gl_diffuse=None, gl_specular=None, gl_position=None):
    """ Function doc
    """
    if gl_ambient is None:
	gl_ambient  = [0.,0.,0.,1.]
    if gl_diffuse is None:
	gl_diffuse  = [1.,1.,1.,1.]
    if gl_specular is None:
	gl_specular = [1.,1.,1.,1.]
    if gl_position is None:
	gl_position = [1.,1.,1.,0.]
    
    glLightfv(GL_LIGHT0,GL_AMBIENT, (gl_ambient[0],
				     gl_ambient[1],
				     gl_ambient[2],
				     gl_ambient[3]))
    
    glLightfv(GL_LIGHT0,GL_DIFFUSE, (gl_diffuse[0],
				     gl_diffuse[1],
				     gl_diffuse[2],
				     gl_diffuse[3]))
    
    glLightfv(GL_LIGHT0,GL_SPECULAR,(gl_specular[0],
				     gl_specular[1],
				     gl_specular[2],
				     gl_specular[3]))
   
    glLightfv(GL_LIGHT0,GL_POSITION,(gl_position[0],
				     gl_position[1],
				     gl_position[2],
				     gl_position[3]))
    
    glMaterialfv(GL_FRONT, GL_AMBIENT, (.7,.7,.7,1.))
    glMaterialfv(GL_FRONT, GL_DIFFUSE, (.8,.8,.8,1.))
    glMaterialfv(GL_FRONT, GL_SPECULAR, (1.,1.,1.,1.))
    glMaterialfv(GL_FRONT, GL_SHININESS, 100.0)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_FOG)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)
    glEnable(GL_COLOR_MATERIAL)



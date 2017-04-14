#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  gldrawarea.py
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

import pygtk
pygtk.require('2.0')
import gtk
import gtk.gdk as gdk
import gtk.gtkgl
import gtk.gdkgl
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math

import representations as rep
import operations as op
import time


class GLCanvas(gtk.gtkgl.DrawingArea):
    
    data   = None
    fovy   = 50.0
    aspect = 0.0
    z_near = 1.0
    z_far  = 10.0
    fog_start = z_far - 1.5
    fog_end = z_far
    width  = 640
    height = 420
    top    = 1.0
    bottom = -1.0
    left   = -10.0
    right  = 10
    selected_atoms = [None]*4
    mouse_x = mouse_y = 0
    dist_cam_zpr = frame_i = 0
    scroll = 1
    pick_radius = [10, 10]
    pos_mouse = [None, None]
    gl_backgrd = [0.0, 0.0, 0.0, 0.0]
    zero_reference_point = target_point = np.array([0, 0, 0])
    mouse_rotate = mouse_pan = mouse_zoom = dragging = False
    LINES = DOTS_SURFACE = DOTS = BALL_STICK = VDW = PRETTY_VDW = RIBBON = SPHERES = WIRES = SELECTION = MODIFIED = False
    
    #base_LineWidth = 2  /(z_far/50) # melhor esse criterio para o tamanho das linhas e pontos
    #base_PointSize = 3  /(z_far/50) #
    #
    #LineWidth = base_LineWidth      #
    #PointSize = base_PointSize      #
    LineWidth = 2
    PointSize = 3
    
    def __init__(self, EasyMolSession=None, width=640, height=420):
	""" Constructor of the GLCanvas object. Here you can change the
	    default parameters for the size, change the names of the
	    connection functions, modify OpenGL configurations.
	"""
	try:
	    glconfig = gtk.gdkgl.Config(mode = (gtk.gdkgl.MODE_RGB | gtk.gdkgl.MODE_DOUBLE | gtk.gdkgl.MODE_DEPTH))
	except gtk.gdkgl.NoMatches:
	    glconfig = gtk.gdkgl.Config(mode = (gtk.gdkgl.MODE_RGB | gtk.gdkgl.MODE_DEPTH))
	gtk.gtkgl.DrawingArea.__init__(self, glconfig)
	self.set_size_request(width, height)
	
	
	
	self.EMSession = EasyMolSession
	#self.data   = data
	
	
	self.width  = width
	self.height = height
	self.connect_after('realize', self.initialize)
	self.connect('configure_event', self.reshape_wind)
	self.connect('expose_event', self.my_draw)
	self.connect('button_press_event', self.mouse_pressed)
        self.connect('button_release_event', self.mouse_released)
        self.connect('motion_notify_event', self.mouse_motion)
        self.connect('scroll_event', self.mouse_scroll)
        self.connect('key_press_event', self.key_press)
	# Set the events masks
	self.set_events(self.get_events() |
            gdk.BUTTON_PRESS_MASK | gdk.BUTTON_RELEASE_MASK |
            gdk.POINTER_MOTION_MASK | gdk.POINTER_MOTION_HINT_MASK |
            gdk.KEY_PRESS_MASK | gdk.KEY_RELEASE_MASK)
	# If you want to cath keyboard events use this two lines
	self.set_flags(gtk.HAS_FOCUS | gtk.CAN_FOCUS)
	self.grab_focus()
    
    def initialize(self, widget):
	""" Load the molecule if is any data and initialize the widget.
	"""
	assert(widget == self)
	glutInit()
	self.create_gl_lists()
	self.load_mol()
        self.gl_initialize()
	return True
    
    def create_gl_lists(self):
	"""
	"""
	#self.gl_ball_stick_list = self.gl_point_list = self.gl_lines_list = self.gl_pretty_vdw_list = self.gl_ribbon_list =  self.gl_sphere_list = self.gl_vdw_list = self.gl_wires_list = None
    
    def open_gl_ctx(self):
	""" Open the OpenGL context.
	"""
	# Get OpenGL context
	gl_context  = gtk.gtkgl.widget_get_gl_context(self)
	# Get actual OpenGL surface
	gl_drawable = gtk.gtkgl.widget_get_gl_drawable(self)
	if not gl_drawable.gl_begin(gl_context):
	    return None, None
	return gl_context, gl_drawable
    
    def close_gl_ctx(self, gl_context, gl_drawable):
	""" Close the OpenGL context to avoid errors.
	"""
	if gl_drawable.is_double_buffered():
	    gl_drawable.swap_buffers()
	else:
	    glFlush()
	gl_drawable.gl_end()
	del gl_context
	del gl_drawable
	return True
    
    def gl_initialize(self):
	""" Initializes all the parameters for the OpenGL context. Is in 
	    another module to keep OpenGL commands separated from the gtk
	    commands.
	"""
	rep.init_gl(self.fog_start, self.fog_end, self.fovy, self.width, self.height, self.z_near, self.z_far)
	return True
    
    def reshape_wind(self, widget, event):
	""" Avoids error when resizing the window.
	"""
	assert(self == widget)
	gl_context, gl_drawable = self.open_gl_ctx()
	x, y, width, height = self.get_allocation()
	glViewport(0, 0, width, height)
	self.left = -float(width)/float(height)
	self.right = -self.left
	self.width = width
	self.height = height
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(self.fovy, float(width)/float(height), self.z_near, self.z_far)
	glMatrixMode(GL_MODELVIEW)
	self.close_gl_ctx(gl_context, gl_drawable)
	self.queue_draw()
	return True
    
    def my_draw(self, widget, event):
	""" This can actually be one function alone and not call
	    another function to make the drawing, but to keep the
	    code more readable I decided to separate them.
	"""
	assert(self == widget)
	gl_context, gl_drawable = self.open_gl_ctx()
	glMatrixMode(GL_MODELVIEW)
	self.draw()
	self.close_gl_ctx(gl_context, gl_drawable)
	return True
    
    def load_mol(self, data=None):
        """ Loads the data (if is any) or replace it if new data is given.
            This is the core of the representations, and need to be more
            efficient.
        """
        
        glDisable(GL_LIGHT0)
        glDisable(GL_LIGHT1)
        glDisable(GL_LIGHT2)
        glDisable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_DEPTH_TEST)
        #glPushName(atom.index)

        
        
        #self.dot_list         = []
        #self.vdw_list         = []
        #self.ball_list        = []
        #self.bonds_list       = []
        #self.wires_list       = []
        #self.sphere_list      = []
        #self.pretty_vdw_list  = []
        #self.dot_surface_list = []
        n = 1
        for Vobject in self.EMSession.Vobjects:
            #print Vobject.label
            
            if Vobject.actived:
                for chain in  Vobject.chains:
                    
                    
                    #'''
                    for res in Vobject.chains[chain].residues:
                        for atom in Vobject.chains[chain].residues[res].atoms:
                            glPushMatrix()
                            
                            glPushName(atom.index)
                            
                            glColor3f(atom.color[0], atom.color[1], atom.color[2])
                            glPointSize(self.PointSize*atom.vdw_rad)
                            glBegin(GL_POINTS)
                            glVertex3f(float(atom.pos[0]),float( atom.pos[1]),float( atom.pos[2]))
                            glEnd()
                            glPopName()
                            glPopMatrix()
                            #print atom.name, atom.pos
                    #'''
                    
                   
                    color = 1.0/n
                    
                    #'''
                    for i in range(0, len(Vobject.chains[chain].backbone) -1):
                        
                        ATOM1 = Vobject.chains[chain].backbone[i]
                        ATOM2 = Vobject.chains[chain].backbone[i+1]
                        
                        glEnable(GL_COLOR_MATERIAL)
                        glEnable(GL_DEPTH_TEST)
                        glPushMatrix()
                        
                        
                        glColor3f(1,  color, 2*color)
                        
                        glLineWidth(self.LineWidth*3)
                        #print Vobject.bonds[i],Vobject.bonds[i+1],Vobject.bonds[i+2], Vobject.bonds[i+3],Vobject.bonds[i+4],Vobject.bonds[i+5]
                        glBegin(GL_LINES)
                        
                        glVertex3f(ATOM1.pos[0],ATOM1.pos[1],ATOM1.pos[2])
                        glVertex3f(ATOM2.pos[0],ATOM2.pos[1],ATOM2.pos[2])
                        
                        glEnd()
                        glPopName()
                        glPopMatrix()
                        
                        #color += 0.001
                    #'''
            
                
                #initial = time.time()
                for bond in Vobject.bonds:
                    #glPushMatrix()
                    #glDisable(GL_LIGHT0)
                    #glDisable(GL_LIGHT1)
                    #glDisable(GL_LIGHT2)
                    #glDisable(GL_LIGHTING)
                    glEnable(GL_COLOR_MATERIAL)
                    glEnable(GL_DEPTH_TEST)
                    glPushMatrix()
                    #glPushName(bond[0])
                    
                    #glColor3f(0, 1, 1)
                    
                    glColor3f(Vobject.atoms[bond[0]].color[0], 
                              Vobject.atoms[bond[0]].color[1], 
                              Vobject.atoms[bond[0]].color[2])
                    
                    glLineWidth(self.LineWidth)
                    
                    #glBegin(GL_LINES)
                    glBegin(GL_LINE_STRIP)
                    glVertex3f(Vobject.atoms[bond[0]].pos[0], 
                               Vobject.atoms[bond[0]].pos[1], 
                               Vobject.atoms[bond[0]].pos[2])
                    
                    
                    glVertex3f((Vobject.atoms[bond[0]].pos[0] + Vobject.atoms[bond[1]].pos[0])/2, 
                               (Vobject.atoms[bond[0]].pos[1] + Vobject.atoms[bond[1]].pos[1])/2, 
                               (Vobject.atoms[bond[0]].pos[2] + Vobject.atoms[bond[1]].pos[2])/2)                    

                    
                    glColor3f(Vobject.atoms[bond[1]].color[0], 
                              Vobject.atoms[bond[1]].color[1], 
                              Vobject.atoms[bond[1]].color[2])
                    
                    glVertex3f((Vobject.atoms[bond[0]].pos[0] + Vobject.atoms[bond[1]].pos[0])/2, 
                               (Vobject.atoms[bond[0]].pos[1] + Vobject.atoms[bond[1]].pos[1])/2, 
                               (Vobject.atoms[bond[0]].pos[2] + Vobject.atoms[bond[1]].pos[2])/2) 

                    glVertex3f(Vobject.atoms[bond[1]].pos[0], 
                               Vobject.atoms[bond[1]].pos[1], 
                               Vobject.atoms[bond[1]].pos[2])                    
                    
                    glEnd()
                    glPopName()
                    glPopMatrix()
                #final = time.time() 
                #print final - initial

            else:
                pass
            n += 1

    
    def draw(self, frame = -1):
        """ Defines wich type of representations will be displayed
        """
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glClearColor(self.gl_backgrd[0],self.gl_backgrd[1],self.gl_backgrd[2],self.gl_backgrd[3])
        
	for i,atom in enumerate(self.selected_atoms):
	    if atom is not None:
		glPushMatrix()
		glPushName(atom.index)
		glColor3f(0, 1, 1)
		glPointSize(7)
		glBegin(GL_POINTS)
		glVertex3f(float(atom.pos[0]),float( atom.pos[1]),float( atom.pos[2]))
		glEnd()
		glPopName()
		glPopMatrix()
	
        #if self.SELECTION:
            #for i,atom in enumerate(self.selected_atoms):
                #if atom is not None:
                    #rep.draw_selected(atom, i+2)
        
        for Vobject in self.EMSession.Vobjects:
            
            if Vobject.actived:   
                
                if Vobject.show_dots    :
                    glCallList(Vobject.list_dots[frame], GL_COMPILE)
                
                if Vobject.show_lines   :
                    glCallList(Vobject.list_lines[frame], GL_COMPILE)
                
                if Vobject.show_ribbons :
                    glCallList(Vobject.list_ribbons[frame], GL_COMPILE)
                
                if Vobject.show_sticks  :
                    glCallList(Vobject.list_sticks[frame], GL_COMPILE)

                if Vobject.show_spheres :
                    glCallList(Vobject.list_spheres[frame], GL_COMPILE)

                if Vobject.show_surface :
                    glCallList(Vobject.list_surface[frame], GL_COMPILE)

	
                     
        #if self.DOTS_SURFACE:
        #    glCallList(self.gl_points_list[self.frame_i], GL_COMPILE)
        #if self.DOTS:
        #    glCallList(self.gl_point_list[self.frame_i], GL_COMPILE)
        #if self.BALL_STICK:
        #    glCallList(self.gl_ball_stick_list[self.frame_i], GL_COMPILE)
        #if self.WIRES:
        #    glCallList(self.gl_wires_list[self.frame_i], GL_COMPILE)
        #if self.LINES:
        #    glCallList(self.gl_lines_list[self.frame_i])
        #if self.VDW:
        #    glCallList(self.gl_vdw_list[self.frame_i], GL_COMPILE)
        #if self.PRETTY_VDW:
        #    glCallList(self.gl_pretty_vdw_list[self.frame_i], GL_COMPILE)
        #if self.RIBBON:
        #    glCallList(self.gl_ribbon_list[self.frame_i], GL_COMPILE)
        #if self.SPHERES:
        #    glCallList(self.gl_sphere_list[self.frame_i], GL_COMPILE)

        #self.load_mol()
    
    
    
    def draw_to_pick(self, frame=-1):
	""" Drawing method only to select atoms.
	"""
	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
	glClearColor(self.gl_backgrd[0],self.gl_backgrd[1],self.gl_backgrd[2],self.gl_backgrd[3])
	#if self.SELECTION:
            #for i,atom in enumerate(self.selected_atoms):
                #if atom is not None:
                    #rep.draw_selected(atom, i+2)
        
        for Vobject in self.EMSession.Vobjects:           
            
            if Vobject.actived:   
                
                #if Vobject.show_dots    :
                    #glCallList(Vobject.list_dots[frame], GL_COMPILE)
                
                if Vobject.show_lines   :
                    glCallList(Vobject.list_lines[frame], GL_COMPILE)
                
                #if Vobject.show_ribbons :
                    #glCallList(Vobject.list_ribbons[frame], GL_COMPILE)
                
                #if Vobject.show_sticks  :
                    #glCallList(Vobject.list_sticks[frame], GL_COMPILE)

                #if Vobject.show_spheres :
                    #glCallList(Vobject.list_spheres[frame], GL_COMPILE)

                #if Vobject.show_surface :
                    #glCallList(Vobject.list_surface[frame], GL_COMPILE)
		    
	#glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
	#glClearColor(self.gl_backgrd[0],self.gl_backgrd[1],self.gl_backgrd[2],self.gl_backgrd[3])
	#if self.DOTS_SURFACE:
	    #glCallList(self.gl_points_list[self.frame_i], GL_COMPILE)
	#if self.DOTS:
	    #glCallList(self.gl_point_list[self.frame_i], GL_COMPILE)
	#if self.BALL_STICK:
	    #glCallList(self.gl_ball_stick_list[self.frame_i], GL_COMPILE)
	#if self.WIRES:
	    #glCallList(self.gl_wires_list[self.frame_i], GL_COMPILE)
	#if self.LINES:
	    #glCallList(self.gl_lines_list[self.frame_i])
	#if self.VDW:
	    #glCallList(self.gl_vdw_list[self.frame_i], GL_COMPILE)
	#if self.PRETTY_VDW:
	    #glCallList(self.gl_pretty_vdw_list[self.frame_i], GL_COMPILE)
	#if self.RIBBON:
	    #glCallList(self.gl_ribbon_list[self.frame_i], GL_COMPILE)
	#if self.SPHERES:
	    #glCallList(self.gl_sphere_list[self.frame_i], GL_COMPILE)
    
    def center_on_atom(self, atom_pos):
        """ Only change the center of viewpoint of the camera.
	    It does not change (yet) the position of the camera.
	    
	    atom_pos is a vector containing the XYZ coordinates
	    of the selected atom.
        """
        if op.get_euclidean(self.target_point, atom_pos) != 0:
            cam_pos = self.get_cam_pos()
            glMatrixMode(GL_MODELVIEW)
            modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
            up = modelview[:3, 1]
            zrp = self.zero_reference_point
            dist = op.get_euclidean(zrp, atom_pos)
            vec_dir = op.unit_vector([atom_pos[0]-zrp[0], atom_pos[1]-zrp[1], atom_pos[2]-zrp[2]])
            add_z = (self.z_far - self.z_near)/2
            dist_z = op.get_euclidean(cam_pos, zrp)
            if dist_z < add_z:
                add_z = dist_z - 0.1
            cycles = 15
            to_add = float(dist/cycles)
            
            for i in range(1, cycles):
                aum = i*to_add
                pto = [zrp[0]+vec_dir[0]*aum, zrp[1]+vec_dir[1]*aum, zrp[2]+vec_dir[2]*aum]
                self.z_far = dist_z + add_z
                self.z_near = dist_z - add_z
                self.fog_start = self.z_far - 1.5
                self.fog_end = self.z_far
                dist_z = op.get_euclidean(cam_pos, pto)
                
                x, y, width, height = self.get_allocation()
                
                glMatrixMode(GL_PROJECTION)
                glLoadIdentity()
                gluPerspective(self.fovy, float(width)/float(height), self.z_near, self.z_far)
                
                glFogf(GL_FOG_START, self.fog_start)
                glFogf(GL_FOG_END, self.fog_end)
                
                glMatrixMode(GL_MODELVIEW)
                glLoadIdentity()
                gluLookAt(cam_pos[0], cam_pos[1], cam_pos[2],
                              pto[0], pto[1]    , pto[2],
                              up[0] , up[1]     , up[2])
                self.window.invalidate_rect(self.allocation, False)
                self.window.process_updates(False)
        
            if dist%0.1 > 0:
                dist_z = op.get_euclidean(cam_pos, atom_pos)
                self.z_far = dist_z + add_z
                self.z_near = dist_z - add_z

                self.fog_start = self.z_far - 1.5

                self.fog_end = self.z_far
                x, y, width, height = self.get_allocation()

                glMatrixMode(GL_PROJECTION)
                glLoadIdentity()
                gluPerspective(self.fovy, float(width)/float(height), self.z_near, self.z_far)
                glFogf(GL_FOG_START, self.fog_start)
                glFogf(GL_FOG_END, self.fog_end)
                glMatrixMode(GL_MODELVIEW)
                glLoadIdentity()
                gluLookAt(cam_pos[0], cam_pos[1], cam_pos[2], atom_pos[0], atom_pos[1], atom_pos[2], up[0], up[1], up[2])
                self.queue_draw()
    
    def key_press(self, widget, event):
	""" The mouse_button function serves, as the names states, to catch
	    events in the keyboard, e.g. letter 'l' pressed, 'backslash'
	    pressed. Note that there is a difference between 'A' and 'a'.
	    Here I use a specific handler for each key pressed after
	    discarding the CONTROL, ALT and SHIFT keys pressed (usefull
	    for customized actions) and maintained, i.e. it's the same as
	    using Ctrl+Z to undo an action.
	"""
	k_name = gdk.keyval_name(event.keyval)
	if event.state & gdk.CONTROL_MASK:
	    print 'Ctrl pressed'
	elif event.state & gdk.MOD1_MASK:
	    print 'Alt pressed'
	elif event.state & gdk.SHIFT_MASK:
	    print 'Shift pressed'
	else:
	    func = getattr(self, 'pressed_' + k_name, None)
	    print k_name, 'key Pressed'
	    if func:
		func()
	return True
    
    def pressed_Escape(self):
	""" Quit the program.
	"""
	print 'Quitting'
	quit()
    
    def pressed_q(self):
	""" Move frames.
	"""
	for i in range(len(self.data)):
	    self.frame_i = i
	    self.update_draw_view()
    
    def pressed_1(self):
	""" Changes color to white.
	"""
	color = [1.0, 1.0, 1.0, 0.0]
	self.change_background(color)
    
    def pressed_2(self):
	""" Changes color to white.
	"""
	color = [0.486275, 0.988235, 0.0, 0.0]
	self.change_background(color)
    
    def pressed_b(self):
	""" Turn on/off Ball-Stick representation.
	"""
	self.BALL_STICK = not self.BALL_STICK
	self.draw_ball_stick()
	self.queue_draw()
	return True
    
    def pressed_d(self):
	""" Turn on/off Dots representation.
	"""
	self.DOTS = not self.DOTS
	self.draw_dots()
	self.queue_draw()
	return True
    
    def pressed_l(self):
	""" Turn on/off Lines representation.
	"""
	self.LINES = not self.LINES
	self.draw_lines()
	self.queue_draw()
	return True
    
    def pressed_p(self):
	""" Turn on/off the Pretty VDW representation.
	"""
	self.PRETTY_VDW = not self.PRETTY_VDW
	self.draw_pretty_vdw()
	self.queue_draw()
	return True
    
    def pressed_r(self):
	""" Turn on/off the Ribbon representation.
	"""
	self.RIBBON = not self.RIBBON
	self.draw_ribbon()
	self.queue_draw()
	return True
    
    def pressed_s(self):
	""" Turn on/off the Sphere representation.
	"""
	self.SPHERES = not self.SPHERES
	self.draw_spheres()
	self.queue_draw()
	return True
    
    def pressed_v(self):
	""" Turn on/off the Van-Der-Waals representation.
	"""
	self.VDW = not self.VDW
	self.draw_vdw()
	self.queue_draw()
	return True
    
    def pressed_w(self):
	""" Turn on/off the Wires representation.
	"""
	self.WIRES = not self.WIRES
	self.draw_wires()
	self.queue_draw()
	return True
    
    def draw_ball_stick(self):
	""" Draws all the elements for Ball-Stick representation.
	"""
	#print 'Ball-Stick Representation'
	if self.gl_ball_stick_list == None or self.MODIFIED:
	    self.gl_ball_stick_list = []
	    for i in range(len(self.data)):
		self.frame_i = i
		self.load_mol()
		gl_bs_li = glGenLists(1)
		glNewList(gl_bs_li, GL_COMPILE)
		for atom in self.ball_list:
		    rep.draw_ball(atom)
		for bond in self.data[self.frame_i].bonds:
		    rep.draw_bond_stick(bond[0], bond[1], bond[2], bond[3])
		glEndList()
		self.gl_ball_stick_list.append(gl_bs_li)
	return True
    
    def draw_dots(self, Vobject):
        """ Change the representation to Dots.
        """
        #print 'Dots Representation'
        # Center dots representations of the atoms
        
        gl_pt_li = glGenLists(1)
        glNewList(gl_pt_li, GL_COMPILE)
        
        
        if Vobject.actived:
            for chain in  Vobject.chains:
                for res in Vobject.chains[chain].residues:
                    for atom in Vobject.chains[chain].residues[res].atoms:
                        glPushMatrix()
                        glPushName(atom.index)
                        glColor3f(atom.color[0], atom.color[1], atom.color[2])
                        glPointSize(self.PointSize*atom.vdw_rad)
                        glBegin(GL_POINTS)
                        glVertex3f(float(atom.pos[0]),float( atom.pos[1]),float( atom.pos[2]))
                        glEnd()
                        glPopName()
                        glPopMatrix()
                        #print atom.name, atom.pos
        
        glEndList()
        Vobject.list_dots.append(gl_pt_li)
        
        #if self.gl_point_list == None or self.MODIFIED:
        #    self.gl_point_list = []
        #    for i in range(len(self.data)):
        #	self.frame_i = i
        #	self.load_mol()
        #	gl_pt_li = glGenLists(1)
        #	
        #	glNewList(gl_pt_li, GL_COMPILE)
        #	for atom in self.dot_list:
        #	    rep.draw_point(atom)
        #	glEndList()
        #	
        #	self.gl_point_list.append(gl_pt_li)
        #    
        #return True
    
    def draw_lines(self, Vobject):
        """ Change the representation to lines.
            It is the default representation.
        """
        gl_ln_li = glGenLists(1)
        glNewList(gl_ln_li, GL_COMPILE)
        
        for bond in Vobject.bonds:
	    
	    glDisable(GL_LIGHT0)
	    glDisable(GL_LIGHT1)
	    glDisable(GL_LIGHT2)
	    glDisable(GL_LIGHTING)
	    glEnable(GL_COLOR_MATERIAL)
	    glEnable(GL_DEPTH_TEST)
	    glPushMatrix()
	    glPushName(bond[0].index)
	    glColor3f(bond[0].color[0], bond[0].color[1], bond[0].color[2])
	    glLineWidth(3)
	    glBegin(GL_LINES)
	    glVertex3f(bond[0].pos[0], bond[0].pos[1], bond[0].pos[2])
	    glVertex3f(bond[4][0], bond[4][1], bond[4][2])
	    glEnd()
	    glPopName()
	    glPopMatrix()
	    
	    
            #glPushMatrix()
            #glDisable(GL_LIGHT0)
            #glDisable(GL_LIGHT1)
            #glDisable(GL_LIGHT2)
            #glDisable(GL_LIGHTING)
            #glEnable(GL_COLOR_MATERIAL)
            #glEnable(GL_DEPTH_TEST)
            #glPushMatrix()
	    #print type(bond[0]), bond[0]
            #glPushName(bond[0].index)
            
            ##glColor3f(0, 1, 1)
            
            #glColor3f(Vobject.atoms[bond[0]].color[0], 
                      #Vobject.atoms[bond[0]].color[1], 
                      #Vobject.atoms[bond[0]].color[2])
            
            #glLineWidth(self.LineWidth)
            
            ##glBegin(GL_LINES)
            #glBegin(GL_LINE_STRIP)
            #glVertex3f(Vobject.atoms[bond[0]].pos[0], 
                       #Vobject.atoms[bond[0]].pos[1], 
                       #Vobject.atoms[bond[0]].pos[2])
            
            
            #glVertex3f((Vobject.atoms[bond[0]].pos[0] + Vobject.atoms[bond[1]].pos[0])/2, 
                       #(Vobject.atoms[bond[0]].pos[1] + Vobject.atoms[bond[1]].pos[1])/2, 
                       #(Vobject.atoms[bond[0]].pos[2] + Vobject.atoms[bond[1]].pos[2])/2)                    

            ##glPopName()
            ##glPushName(bond[1])
            
            #glColor3f(Vobject.atoms[bond[1]].color[0], 
                      #Vobject.atoms[bond[1]].color[1], 
                      #Vobject.atoms[bond[1]].color[2])
            
            #glVertex3f((Vobject.atoms[bond[0]].pos[0] + Vobject.atoms[bond[1]].pos[0])/2, 
                       #(Vobject.atoms[bond[0]].pos[1] + Vobject.atoms[bond[1]].pos[1])/2, 
                       #(Vobject.atoms[bond[0]].pos[2] + Vobject.atoms[bond[1]].pos[2])/2) 

            #glVertex3f(Vobject.atoms[bond[1]].pos[0], 
                       #Vobject.atoms[bond[1]].pos[1], 
                       #Vobject.atoms[bond[1]].pos[2])                    
            
            #glEnd()
            #glPopName()
            #glPopMatrix() 
        
        
        #for res in Vobject.chains[chain].residues:
        #    for atom in Vobject.chains[chain].residues[res].atoms:
        #        glPushMatrix()
        #        
        #        glPushName(atom.index)
        #        
        #        glColor3f(atom.color[0], atom.color[1], atom.color[2])
        #        glPointSize(self.PointSize*atom.vdw_rad)
        #        glBegin(GL_POINTS)
        #        glVertex3f(float(atom.pos[0]),float( atom.pos[1]),float( atom.pos[2]))
        #        glEnd()
        #        glPopName()
        #        glPopMatrix()
        #        #print atom.name, atom.pos

        glEndList()
        Vobject.list_lines.append(gl_ln_li)
        
    
        '''
        if self.gl_lines_list == None or self.MODIFIED:
            self.gl_lines_list = []
            for frame in self.data:
            gl_ln_li = glGenLists(1)
            glNewList(gl_ln_li, GL_COMPILE)
            for bond in frame.bonds:
                rep.draw_bond_line(bond[0], bond[4])
            glEndList()
            
            self.gl_lines_list.append(gl_ln_li)
        #'''
        
        return True
    
    def draw_pretty_vdw(self):
	""" Change the representation to Pretty VDW.
	"""
	#print 'Pretty Van-Der-Waals Representation'
	# Ball representation.
	if self.gl_pretty_vdw_list == None or self.MODIFIED:
	    self.gl_pretty_vdw_list = []
	    for i in range(len(self.data)):
		self.frame_i = i
		self.load_mol()
		gl_p_vdw_li = glGenLists(1)
		glNewList(gl_p_vdw_li, GL_COMPILE)
		for atom in self.ball_list:
		    rep.draw_ball(atom)
		    # Makes the bonds representations in sticks format
		for bond in self.data[self.frame_i].bonds:
		    rep.draw_bond_stick(bond[0], bond[1], bond[2], bond[3])
		    # Makes the pretty van-der-walls representation of the atoms. The
		    # difference between vdw is that this representation is transparent.
		for atom in self.pretty_vdw_list:
		    rep.draw_pretty_vdw(atom)
		glEndList()
		self.gl_pretty_vdw_list.append(gl_p_vdw_li)
	return True
    
    def draw_ribbon(self, Vobject):
        """ Change the representation to Ribbon.
        """
        #print 'Ribbon Representation'
        # Makes the ribbon representations

        gl_rb_li = glGenLists(1)
        glNewList(gl_rb_li, GL_COMPILE)
        
        if Vobject.actived:
            for chain in  Vobject.chains:
                for i in range(0, len(Vobject.chains[chain].backbone) -1):
                    
                    ATOM1 = Vobject.chains[chain].backbone[i]
                    ATOM2 = Vobject.chains[chain].backbone[i+1]
                    
                    glEnable(GL_COLOR_MATERIAL)
                    glEnable(GL_DEPTH_TEST)
                    glPushMatrix()
                    
                    
                    glColor3f(ATOM1.color[0],ATOM1.color[1], ATOM1.color[1])
                    
                    glLineWidth(self.LineWidth*3)
                    #print Vobject.bonds[i],Vobject.bonds[i+1],Vobject.bonds[i+2], Vobject.bonds[i+3],Vobject.bonds[i+4],Vobject.bonds[i+5]
                    glBegin(GL_LINES)
                    
                    glVertex3f(ATOM1.pos[0],ATOM1.pos[1],ATOM1.pos[2])
                    glVertex3f(ATOM2.pos[0],ATOM2.pos[1],ATOM2.pos[2])
                    
                    glEnd()
                    glPopName()
                    glPopMatrix()

        glEndList()
        #self.gl_ribbon_list.append(gl_rb_li)   
        Vobject.list_ribbons.append(gl_rb_li)
         
        #if self.gl_ribbon_list == None or self.MODIFIED:
        #    self.gl_ribbon_list = []
        #    for frame in self.data:
        #	gl_rb_li = glGenLists(1)
        #	glNewList(gl_rb_li, GL_COMPILE)
        #	for ribbon in frame.ribbons:
        #	    rep.draw_ribbon(ribbon[0], ribbon[1], ribbon[2], ribbon[3])
        #	glEndList()
        #	self.gl_ribbon_list.append(gl_rb_li)
	
    
    
    
    
    def draw_spheres(self):
	""" Change the representation to Spheres.
	"""
	#print 'Spheres Representation'
	# Sphere representation of the atoms, the difference between the ball
	# representation is that sphere uses the covalent radius and ball the
	# atomic radius.
	if self.gl_sphere_list == None or self.MODIFIED:
	    self.gl_sphere_list = []
	    for i in range(len(self.data)):
		self.frame_i = i
		self.load_mol()
		gl_sp_li = glGenLists(1)
		glNewList(gl_sp_li, GL_COMPILE)
		for atom in self.sphere_list:
		    rep.draw_sphere(atom)
		glEndList()
		self.gl_sphere_list.append(gl_sp_li)
	return True
    
    def draw_vdw(self):
	""" Change the representation to Van-Der-Waals.
	"""
	#print 'Van-Der-Waals Representation'
	# Makes the van-der-walls representation of the atoms.
	if self.gl_vdw_list == None or self.MODIFIED:
	    self.gl_vdw_list = []
	    for i in range(len(self.data)):
		self.frame_i = i
		self.load_mol()
		gl_vdw_li = glGenLists(1)
		glNewList(gl_vdw_li, GL_COMPILE)
		for atom in self.vdw_list:
		    rep.draw_vdw(atom)
		glEndList()
		self.gl_vdw_list.append(gl_vdw_li)
	return True
    
    def draw_wires(self):
	""" Change the representation to Wires.
	"""
	#print 'Wired Representation'
	# Wires representation.
	if self.gl_wires_list == None or self.MODIFIED:
	    self.gl_wires_list = []
	    for i in range(len(self.data)):
		self.frame_i = i
		self.load_mol()
		gl_wr_li = glGenLists(1)
		glNewList(gl_wr_li, GL_COMPILE)
		for atom in self.wires_list:
		    rep.draw_wire_sphere(atom)
		# Makes the bonds representations in wired sticks format
		for bond in self.data[self.frame_i].bonds:
		    rep.draw_bond_wired_stick(bond[0], bond[1], bond[2], bond[3])
		glEndList()
		self.gl_wires_list.append(gl_wr_li)
	return True
    
    def update_draw_view(self):
	""" Redraws the representations with new data.
	"""
	# Experimental, ONLY WORKS if all the atoms are numbered the same in all frames
	for i in range(len(self.selected_atoms)):
	    if self.selected_atoms[i] is not None:
		self.selected_atoms[i] = self.data[self.frame_i].atoms[self.selected_atoms[i].index-1]
	# Experimental, ONLY WORKS if all the atoms are numbered the same in all frames
	reps = ['dots_surf', 'dots', 'vdw', 'pretty_vdw', 'ribbon', 'spheres', 'wires', 'ball_stick', 'lines']
	for rep in reps:
	    func = getattr(self, 'draw_' + rep, None)
	    if func:
		func()
	    self.window.invalidate_rect(self.allocation, False)
	    self.window.process_updates(False)
    
    def turn_off_reps(self):
	""" Hyde Everything
	"""
	self.DOTS_SURFACE = self.DOTS = self.LINES = self.VDW = self.PRETTY_VDW = self.RIBBON = self.SPHERES = self.WIRES = self.BALL_STICK = self.LINES = False
    
    def change_background(self, color):
	""" Changes the color of the background.
	    The color variable is an array of four elements 
	    corresponding to Red, Green, Blue and Alpha values
	    in the 0.0-1.0 range.
	"""
	self.gl_backgrd = color
	glFogfv(GL_FOG_COLOR, color[:3])
	self.draw()
	self.queue_draw()
    
    @classmethod
    def event_masked(cls, event, mask):
        return (event.state & mask) == mask
    
    @classmethod
    def _button_check(cls, event, button, mask):
        if event.button == button:
            return (event.type == gdk.BUTTON_PRESS)                    
        return cls.event_masked(event, mask) 
    
    @classmethod
    def get_left_button_down(cls, event):
        return cls._button_check(event, 1, gdk.BUTTON1_MASK)
    
    @classmethod
    def get_middle_button_down(cls, event):
        return cls._button_check(event, 2, gdk.BUTTON2_MASK)
    
    @classmethod
    def get_right_button_down(cls, event):
        return cls._button_check(event, 3, gdk.BUTTON3_MASK)
    
    def mouse_pressed(self, widget, event):
	""" The mouse_button function serves, as the names states, to catch
	    mouse buttons events when pressed.
	"""
	left   = self.get_left_button_down(event)
        middle = self.get_middle_button_down(event)
        right  = self.get_right_button_down(event)
        self.mouse_rotate = left and not (middle or right)
        self.mouse_zoom   = right and not (middle or left)
        self.mouse_pan    = middle and not (right or left)
        x = self.mouse_x = event.x
        y = self.mouse_y = event.y
        self.drag_pos_x, self.drag_pos_y, self.drag_pos_z = self.pos(x, y)
        if event.button == 1 and event.type == gtk.gdk._2BUTTON_PRESS:
            nearest, hits = self.pick(x, self.get_allocation().height-1-y, self.pick_radius[0], self.pick_radius[1], event)
            selected = self.select(event, nearest, hits)
	    if selected is not None:
		self.center_on_atom(selected.pos)
		self.zero_reference_point = selected.pos
		self.target_point = selected.pos
        if event.button == 2 and event.type == gtk.gdk.BUTTON_PRESS:
	    self.dist_cam_zpr = op.get_euclidean(self.zero_reference_point, self.get_cam_pos())
	if event.button == 1 and event.type == gtk.gdk.BUTTON_PRESS:
	    self.pos_mouse = [x, y]
    
    def mouse_released(self, widget, event):
	""" The mouse_released function serves, as the names states, to catch
	    mouse buttons events when released.
	"""
	self.mouse_rotate = self.mouse_pan = self.mouse_zoom = False
	x = self.mouse_x = event.x
        y = self.mouse_y = event.y
        self.drag_pos_x, self.drag_pos_y, self.drag_pos_z = self.pos(x, y)
	if event.button == 1 and event.type == gtk.gdk.BUTTON_RELEASE:
	    if math.fabs(self.pos_mouse[0]-x) <= self.pick_radius[0] and math.fabs(self.pos_mouse[1]-y) <= self.pick_radius[1]:
		nearest, hits = self.pick(x, self.get_allocation().height-1-y, self.pick_radius[0], self.pick_radius[1], event)
		selected = self.select(event, nearest, hits)
		if selected is None:
		    self.selected_atoms = [None]*len(self.selected_atoms)
		else:
		    if selected not in self.selected_atoms:
			for i in range(len(self.selected_atoms)):
			    if self.selected_atoms[i] == None:
				self.selected_atoms[i] = selected
				selected = None
				break
			if selected is not None:
			    self.selected_atoms[len(self.selected_atoms)-1] = selected
		    else:
			for i in range(len(self.selected_atoms)):
			    if self.selected_atoms[i] == selected:
				self.selected_atoms[i] = None
		self.queue_draw()
	    else:
		self.pos_mouse = [None, None]
	if event.button == 2 and event.type == gtk.gdk.BUTTON_RELEASE:
	    if self.dragging:
		glMatrixMode(GL_MODELVIEW)
		modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
		dir_vec = modelview[:3, 2]
		cam_pos = self.get_cam_pos()
		dir_vec *= -self.dist_cam_zpr
		new_zpr = cam_pos + dir_vec
		self.zero_reference_point = np.array([new_zpr[0], new_zpr[1], new_zpr[2]])
		self.dragging = False
	    else:
		nearest, hits = self.pick(x, self.get_allocation().height-1-y, self.pick_radius[0], self.pick_radius[1], event)
		selected = self.select(event,nearest,hits)
		if selected is not None:
		    self.center_on_atom(selected.pos)
		    self.zero_reference_point = selected.pos
		    self.target_point = selected.pos
    
    def mouse_motion(self, widget, event):
        """ The mouse_motion function serves, as the names states, to perform
        actions when the mouse is in movement.
        """
        assert(widget==self)
        if event.is_hint:
            x, y, state = event.window.get_pointer()
        else:
            x = event.x
            y = event.y
            state = event.state

        dx = x - self.mouse_x
        dy = y - self.mouse_y
        if (dx==0 and dy==0):
            return
        self.mouse_x, self.mouse_y = x, y
        changed = False
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        
        if self.mouse_zoom:
            x, y, width, height = self.get_allocation()
            ax, ay, az = 0, 0, dy
            modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
            #self.line_width_refresh()



            delta = ((self.z_far-self.z_near)/2)+ self.z_near
            delta = delta/200
            glLoadIdentity()
            inv = np.matrix(glGetDoublev(GL_MODELVIEW_MATRIX)).I
            bx = (inv[0,0]*ax + inv[1,0]*ay + inv[2,0]*az)/(1/(delta))
            by = (inv[0,1]*ax + inv[1,1]*ay + inv[2,1]*az)/(1/(delta))
            bz = (inv[0,2]*ax + inv[1,2]*ay + inv[2,2]*az)/(1/(delta))
            self.apply_trans(glTranslatef, bx, by, bz)
            glMultMatrixd(modelview)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            self.z_near += -bz
            self.z_far += -bz
            self.fog_start += -bz
            self.fog_end += -bz

            
            
            #print self.LineWidth, self.PointSize, self.z_far
            #self.LineWidth = self.base_LineWidth/ (self.z_far/10)#(math.log10(self.z_far))
            #self.PointSize = self.base_PointSize/ (self.z_far/10)#(math.log10(self.z_far))
            
            
            # aqui tem que ser colocar a funcao que altera a grossura das linhas e pontos
            
            
            #print self.LineWidth
            
            #LineWidth = self.LineWidth
            #PointSize = self.PointSize
            
            #
            #LineWidth = LineWidth/self.z_far
            #PointSize = PointSize/self.z_far
            #
            #if LineWidth <=1:
            #    LineWidth = 1
            #
            #
            #
            #else:
            #    self.LineWidth = LineWidth 
            #    self.PointSize = PointSize 

            if self.z_near >= 0.1:
                gluPerspective(self.fovy, float(width)/float(height), self.z_near, self.z_far)
            else: 
                gluPerspective(self.fovy, float(width)/float(height), 0.1, self.z_far)
            
            glFogf(GL_FOG_START, self.fog_start)
            glFogf(GL_FOG_END, self.fog_end)
            glMatrixMode(GL_MODELVIEW)
            changed = True
        
        elif self.mouse_rotate:
            ax, ay, az = dy, dx, 0.0
            viewport = glGetIntegerv(GL_VIEWPORT)
            angle = math.sqrt(ax**2+ay**2+az**2)/float(viewport[2]+1)*180.0
            inv = np.matrix(glGetDoublev(GL_MODELVIEW_MATRIX)).I
            bx = (inv[0,0]*ax + inv[1,0]*ay + inv[2,0]*az)
            by = (inv[0,1]*ax + inv[1,1]*ay + inv[2,1]*az)
            bz = (inv[0,2]*ax + inv[1,2]*ay + inv[2,2]*az)
            self.apply_trans(glRotatef, angle, bx, by, bz)
            changed = True
        
        
        elif self.mouse_pan:
            px, py, pz = self.pos(x, y)
            modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
            glLoadIdentity()
            glTranslatef((px-self.drag_pos_x)*(self.z_far)/10, 
                 (py-self.drag_pos_y)*(self.z_far)/10, 
                 (pz-self.drag_pos_z)*(self.z_far)/10)
            glMultMatrixd(modelview)
            x = self.zero_reference_point[0]
            y = self.zero_reference_point[1]
            z = self.zero_reference_point[2]
            self.drag_pos_x = px
            self.drag_pos_y = py
            self.drag_pos_z = pz
            changed = True
        if changed:
            self.queue_draw()
        if state & gtk.gdk.BUTTON2_MASK:
            self.dragging = True
    
    def mouse_scroll(self, widget, event):
	""" Change the z_near and z_far values (moves the fog)
	"""
	if event.direction == gdk.SCROLL_UP:
            self.z_near -= self.scroll
            self.z_far += self.scroll
            self.fog_start += self.scroll
            self.fog_end += self.scroll
        if event.direction == gdk.SCROLL_DOWN:
            if self.z_near >= self.z_far:
                pass
            else:
                self.z_near += self.scroll
                self.z_far -= self.scroll
                self.fog_start -= self.scroll
                self.fog_end -= self.scroll
	x, y, width, height = self.get_allocation()
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	if self.z_near >= 0.1:
	    gluPerspective(self.fovy, float(width)/float(height), self.z_near, self.z_far)
	else: 
	    gluPerspective(self.fovy, float(width)/float(height), 0.1, self.z_far)
	glFogf(GL_FOG_START, self.fog_start)
	glFogf(GL_FOG_END, self.fog_end)
	glMatrixMode(GL_MODELVIEW)
	self.queue_draw()
    
    def pos(self, x, y):
        """
        Use the ortho projection and viewport information
        to map from mouse co-ordinates back into world
        co-ordinates
        """  
        viewport = glGetIntegerv(GL_VIEWPORT)
        px = float(x-viewport[0])/float(viewport[2])
        py = float(y-viewport[1])/float(viewport[3])       
        px = self.left + px*(self.right-self.left)
        py = self.top + py*(self.bottom-self.top)
        pz = self.z_near
        return px, py, pz
    
    def apply_trans(self, func, *args):
	"""
	"""
        glTranslatef(*self.zero_reference_point)
        func(*args)
        glTranslatef(*map(lambda x:-x, self.zero_reference_point))
    
    def pick(self, x, y, dx, dy, event):
	"""
	"""
        buf = glSelectBuffer(256)
        glRenderMode(GL_SELECT)
        glInitNames()
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        viewport = glGetIntegerv(GL_VIEWPORT)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        glLoadIdentity()
        gluPickMatrix(x, y, dx, dy, viewport)
        glMultMatrixd(projection)        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        self.draw_to_pick()
        glPopMatrix()
        hits = glRenderMode(GL_RENDER)
        nearest = []
        min_z = None
	for hit in hits:
            if (len(hit.names) > 0) and ((min_z is None) or (hit.near < min_z)):
                min_z = hit.near
                nearest = hit.names
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        return nearest, hits
    
    def select(self, event, nearest, hits):
	"""
	"""
	picked = None
        if nearest != []:
	    picked = self.EMSession.Vobjects[0].atoms[nearest[0]-1]
	    coords = self.EMSession.Vobjects[0].atoms[nearest[0]-1].pos
	    #print coords
        #if nearest != []:
	    #for chain in self.data[self.frame_i].chains.values():
		#for residue in chain.residues.values():
		    #for atom in residue.atoms.values():
			#if atom.index == nearest[0]:
			    #picked = atom
			    #break
	return picked
    
    def get_cam_pos(self):
	""" Returns the position of the camera in XYZ coordinates
	    The type of data returned is 'numpy.ndarray'.
	"""
	modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
	crd_xyz = -1 * np.mat(modelview[:3,:3]) * np.mat(modelview[3,:3]).T
	return crd_xyz.A1
    
    #""" Following are the functions to use with glade-gtk.
    #"""
    
    def switch_ball_stick(self, button):
	""" Turn on/off Ball-Stick representation.
	"""
	self.BALL_STICK = not self.BALL_STICK
	self.draw_ball_stick()
	self.queue_draw()
	return True
    
    
    def switch_dots(self, button):
	""" Turn on/off Dots representation.
	"""
	self.DOTS = not self.DOTS
	self.draw_dots()
	self.queue_draw()
	return True
    
    def switch_lines(self, button):
	""" Turn on/off Lines representation.
	"""
	self.LINES = not self.LINES
	self.draw_lines()
	self.queue_draw()
	return True
    
    def switch_pretty_vdw(self, button):
	""" Turn on/off the Pretty VDW representation.
	"""
	self.PRETTY_VDW = not self.PRETTY_VDW
	self.draw_pretty_vdw()
	self.queue_draw()
	return True
    
    def switch_ribbon(self, button):
	""" Turn on/off the Ribbon representation.
	"""
	self.RIBBON = not self.RIBBON
	self.draw_ribbon()
	self.queue_draw()
	return True
    
    def switch_spheres(self, button):
	""" Turn on/off the Sphere representation.
	"""
	self.SPHERES = not self.SPHERES
	self.draw_spheres()
	self.queue_draw()
	return True
    
    def switch_vdw(self, button):
	""" Turn on/off the Van-Der-Waals representation.
	"""
	self.VDW = not self.VDW
	self.draw_vdw()
	self.queue_draw()
	return True
    
    def switch_wires(self, button):
	""" Turn on/off the Wires representation.
	"""
	self.WIRES = not self.WIRES
	self.draw_wires()
	self.queue_draw()
	return True

        
    def generate_surface_test (self):
        """ Function doc """

        surface = [
                   #[  0.56112162422,    10.29360903,     0   ],
                   #[  2.02227064637,   10.603929468,    0    ],
                   #[  4.49459344735,   9.5053416863,    0    ],
                   #[  5.80008748262,   8.4243655892,    0    ],
                   #[  7.8697253231 ,  7.75986127056,   0     ],
                   #[  9.34815209509,   5.7109257643,    0    ],
                   #[  10.1177228958,   3.9451337612,    0    ],
                   #[  10.6006971632,   1.7451099816,    0    ],
                   #[  10.2387397788,   0.2077071833,     0   ],
                   #[  10.1813999315,   -1.561218007,     0   ],
                   #[  9.21484179241,   -3.664385038,     1   ],
                   #[  8.66549927515,   -5.022363810,     1   ],
                   #[  7.49358448115,   -6.903588222,     1   ],
                   #[  5.81352917129,   -8.508878332,     1   ],
                   #[  4.24071451349,   -9.080951442,     1   ],
                   #[  2.3014577022 ,  -9.2395996562,    1    ],
                   #[  -0.1517795788,     -9.1778179,       1 ],
                   #[  -1.8539619610,    -9.56429855,      1  ],
                   #[  -3.7174257720,    -8.72935936,      1  ],
                   #[  -5.9452525877,    -7.34955361,      1  ],
                   #[  -7.5258568825,    -5.57086664,     2   ],
                   #[  -8.0395263889,    -4.09175540,     2   ],
                   #[  -8.6188189088,    -2.73967977,      2  ],
                   #[  -9.7827543079,    -0.71310154,       2 ],
                   #[  -9.7465131417,   1.6513020468,    2    ],
                   #[  -9.5028783997,    2.844255762,     2   ],
                   #[  -8.7837164631,    5.390271147,     2   ],
                   #[  -6.9431403139,    6.549195262,    2    ],
                   #[  -5.9525131595,   8.5286712999,    2    ],
                   #[  -4.3280729107,    9.021868684,     2   ],
                   #[  -2.2277852522,    10.23483576,     3   ],
                   #[  -0.2344258441,     10.5566287,      3  ],
                   #[  1.80115800173,   10.346756093,    3    ],
                   #[  3.18506300747,   9.7331312156,    3    ],
                   #[  5.22791612914,   8.7142844885,    3    ],
                   #[  7.4431989849 ,  7.55311803462,   3     ],
                   #[  8.53854430041,   6.1804551645,    3    ],
                   #[  9.53782578795,   5.2275171051,   3     ],
                   #[  9.77893926239,   2.8616439771,    3    ],
                   #[  10.8650810839,   1.4616642056,    3    ],
                   #[  10.1191077732,   -1.069588363,     4   ],
                   #[  9.72905199633,   -3.075864955,     4   ],
                   #[  8.76775315386,   -5.179769157,     4   ],
                   #[  8.30233896971,   -5.888737711,     4   ],
                   #[  5.8875399484 ,  -7.6875851233,    4    ],
                   #[  4.39683136778,   -8.128691943,    4    ],
                   #[  2.48017865605,   -8.945724057,    4    ],
                   #[  0.30546632935,    -9.02659613,      4  ],
                   #[  -1.5456825844,    -9.35660715,      4  ],
                   #[  -2.8524426772,    -9.25107829,      4  ],
                   #[  -5.1498071856,    -7.53682677,      5  ],
                   #[  -6.4498538918,    -6.61277041,      5  ],
                   #[  -8.2651979295,    -4.80983321,      5  ],
                   #[  -9.1824693729,    -3.16326691,      5  ],
                   #[  -9.5871124691,   -0.948526857,      5  ],
                   #[  -9.0201865214,    1.043579317,     5   ],
                   #[  -8.8972980653,    2.387565465,     5   ],
                   #[  -8.9829708310,    4.634309863,     5   ],
                   #[  -7.3212896993,    6.429248888,     5   ],
                   #[  -6.4611426082,    7.344736341,     5   ],
                   #[  -4.9376679091,    9.236904310,     6   ],
                   #[  -3.3131476062,    9.951161133,    6    ],
                   #[  -1.4876637786,    10.37029879,     6   ],
                   #[  1.2341465214 ,  10.076578737 ,  6      ],
                   #[  2.91869182998,   10.642604944,    6    ],
                   #[  5.07036395782,   9.8935282163,    6    ],
                   #[  6.44965791757,   8.7091606610,    6    ],
                   #[  7.43231292635,   7.5419545847,    6    ],
                   #[  9.19336664064,   5.4307287863,    6    ],
                   #[  9.56819417104,   3.7128642631,    6    ],
                   #[  10.6591813194,   2.3635710125,   7     ],
                   #[  10.9207535463,   -0.337620129,      7  ],
                   #[  9.73219200441,   -2.514914359,    7    ],
                   #[  9.74527893107,   -3.989861743,     7   ],
                   #[  8.13399739442,   -5.492420217,     7   ],
                   #[  6.6406020975 ,  -7.4613217331,    7    ],
                   #[  5.42260196522,   -8.311440343,     7   ],
                   #[  3.93672204252,   -9.347283779,     7   ],
                   #[  1.14460257012,   -9.411338891,    7    ],
                   #[  -0.0865952660,    -9.05543673,      7  ],
                   #[  -2.6081877513,   -9.129973364,     8   ],
                   #[  -4.6623071802,    -8.06964971,      8  ],
                   #[  -6.1578566331,    -6.90819250,      8  ],
                   #[  -7.2606184588,    -5.66635833,      8  ],
                   #[  -7.9742778950,    -4.13820033,      8  ],
                   #[  -9.2051094511,    -2.37294959,      8  ],
                   #[  -9.6968691084,    0.192932183,      8  ],
                   #[  -9.5049554953,   1.6634513937,    8    ],
                   #[  -8.8366145321,    3.899040276,     8   ],
                   #[  -8.2862763193,    5.573870668,    8    ],
                   #[  -7.0543242207,    6.927253704,     9   ],
                   #[  -5.4070247808,    8.945754533,     9   ],
                   #[  -4.2486683139,    9.295524008,     9   ],
                   #[  -1.9785892862,    10.30888630,     9   ],
                   #[  0.09227762821,     10.7598662,    9    ],
                   #[  1.67719495469,   10.044774183,    9    ],
                   #[  4.19739771567,   9.7035545302,    9    ],
                   #[  6.04196214401,   8.5532430472,   9     ],
                   #[  7.64441750841,   7.4848164018,    9    ],
                   #[  8.83984313731,   6.0691523079,    9    ],
                   #[  9.8984585106 ,  4.70735394881,   10    ],
                   #[  9.9386286782 ,  2.36745079461,   10    ],
                   #[  10.3684592595,   0.6560495372,     10  ],
                   #[  10.0899436829,   -1.181851021,     10  ],
                   #[  9.58230445812,   -3.233474036,     10  ],
                   #[  8.84399959836,   -4.980355959,     10  ],
                   #[  7.86553299971,   -6.914423598,     10  ],
                   #[  5.67803139825,   -7.799637742,     10  ],
                   #[  4.32034229584,   -8.833003039,     10  ],
                   #[  2.59508726376,   -8.884337708,     10  ],
                   #[  0.21980142235,   -9.226642685,     11  ],
                   #[  -2.0282501266,    -9.27550550,     11  ],
                   #[  -3.2433127600,    -8.98842435,      11 ],
                   #[  -4.9037571565,   -7.288851677,     11  ],
                   #[  -6.4609874236,    -6.17267691,      11 ],
                   #[  -8.4516274943,    -4.39486490,      11 ],
                   #[  -8.4831540809,    -3.47019996,      11 ],
                   #[  -9.2162854746,    -0.66528386,       11],
                   #[  -9.6828756409,    0.482390778,      11 ],
                   #[  -9.4755060800,    3.092594308,     11  ],
                   #[  -8.2803133993,    4.849766824,     12  ],
                   #[  -7.0713744014,    6.264646330,    12   ],
                   #[  -5.8309659248,   8.3673200456,    12   ],
                   #[  -5.0101004296,    8.642111171,     12  ],
                   #[  -2.4844867718,    10.32952979,     12  ],
                   #[  -1.3230129526,   10.777300711,    12   ],
                   #[  1.01384684063,   10.426981073,    12   ],
                   #[  3.32283025587,   9.9825056410,    12   ],
                   #[  5.39780352975,   9.7868741316,    12   ],
                   #[  6.2898543453 ,  8.83281467396,   12    ],
                   #[  7.81858500704,   6.9767747567,    13   ],
                   #[  8.81979487616,   5.5029287490,    13   ],
                   #[  10.30520895  , 3.97178844086 ,  13     ],
                   #[  10.5459675664,   1.8175442884,    13   ],
                   #[  10.6808380672,   -0.571060322,      13 ],
                   #[  9.68863210273,   -2.406483033,    13   ],
                   #[  9.69402920292,   -4.514109605,    13   ],
                   #[  8.44851884845,   -5.885621400,     13  ],
                   #[  7.03262379633,   -7.040866613,     13  ],
                   #[  5.3329554124 ,  -8.4097172869,    13   ],
                   #[  2.71528723324,   -9.314873974,     14  ],
                   #[  1.13213511061,   -8.999095901,     14  ],
                   #[  -0.3073033671,     -9.3462547,       14],
                   #[  -2.9511299671,    -9.11277580,     14  ],
                   #[  -4.0880691474,    -7.96646611,      14 ],
                   #[  -6.5610887094,    -7.24112915,      14 ],
                   #[  -7.4063177385,   -5.592700123,     14  ],
                   #[  -8.2618950412,    -4.28136274,      14 ],
                   #[  -9.3230991524,    -1.76074181,      14 ],
                   #[  -9.2414800735,    0.414009238,      14 ],
                   #[  -9.4720985309,    2.416416814,     15  ],
                   #[  -8.7560924002,    3.610856973,     15  ],
                   #[  -7.8680104325,    5.463410460,     15  ],
                   #[  -6.6241323823,    7.171451813,     15  ],
                   #[  -5.7053536463,    8.337462296,     15  ],
                   #[  -3.9736829620,    9.687398445,     15  ],
                   #[  -1.4093201510,    10.40823541,     15  ],
        [ 0.0 , 10.0 , 0 ],
        [ 1.98669330795 , 9.80066577841 , 0 ],
        [ 3.89418342309 , 9.21060994003 , 0 ],
        [ 5.64642473395 , 8.2533561491 , 0 ],
        [ 7.173560909 , 6.96706709347 , 0 ],
        [ 8.41470984808 , 5.40302305868 , 0 ],
        [ 9.32039085967 , 3.62357754477 , 0 ],
        [ 9.85449729988 , 1.699671429 , 0 ],
        [ 9.99573603042 , -0.291995223013 , 0 ],
        [ 9.73847630878 , -2.27202094693 , 0 ],
        [ 9.09297426826 , -4.16146836547 , 1 ],
        [ 8.0849640382 , -5.88501117255 , 1 ],
        [ 6.75463180551 , -7.37393715541 , 1 ],
        [ 5.15501371821 , -8.56888753369 , 1 ],
        [ 3.34988150156 , -9.42222340669 , 1 ],
        [ 1.4112000806 , -9.899924966 , 1 ],
        [ -0.583741434276 , -9.98294775795 , 1 ],
        [ -2.55541102027 , -9.66798192579 , 1 ],
        [ -4.42520443295 , -8.96758416334 , 1 ],
        [ -6.11857890943 , -7.90967711914 , 1 ],
        [ -7.56802495308 , -6.53643620864 , 2 ],
        [ -8.71575772414 , -4.90260821341 , 2 ],
        [ -9.5160207389 , -3.07332869978 , 2 ],
        [ -9.93691003633 , -1.12152526935 , 2 ],
        [ -9.96164608836 , 0.874989834394 , 2 ],
        [ -9.58924274663 , 2.83662185463 , 2 ],
        [ -8.8345465572 , 4.685166713 , 2 ],
        [ -7.72764487556 , 6.34692875943 , 2 ],
        [ -6.31266637872 , 7.7556587851 , 2 ],
        [ -4.64602179414 , 8.85519516941 , 2 ],
        [ -2.79415498199 , 9.6017028665 , 3 ],
        [ -0.830894028175 , 9.96542097023 , 3 ],
        [ 1.1654920485 , 9.93184918758 , 3 ],
        [ 3.11541363513 , 9.50232591959 , 3 ],
        [ 4.94113351139 , 8.6939749035 , 3 ],
        [ 6.56986598719 , 7.53902254343 , 3 ],
        [ 7.93667863849 , 6.08351314532 , 3 ],
        [ 8.98708095812 , 4.38547327574 , 3 ],
        [ 9.67919672031 , 2.51259842582 , 3 ],
        [ 9.98543345375 , 0.539554205626 , 3 ],
        [ 9.89358246623 , -1.45500033809 , 4 ],
        [ 9.4073055668 , -3.39154860984 , 4 ],
        [ 8.54598908088 , -5.19288654117 , 4 ],
        [ 7.34397097874 , -6.7872004732 , 4 ],
        [ 5.84917192892 , -8.11093014062 , 4 ],
        [ 4.12118485242 , -9.11130261885 , 4 ],
        [ 2.228899141 , -9.74843621404 , 4 ],
        [ 0.247754254534 , -9.99693042035 , 4 ],
        [ -1.74326781223 , -9.84687855794 , 4 ],
        [ -3.66479129252 , -9.30426272105 , 4 ],
        [ -5.44021110889 , -8.39071529076 , 5 ],
        [ -6.99874687594 , -7.14265652027 , 5 ],
        [ -8.27826469086 , -5.60984257427 , 5 ],
        [ -9.22775421613 , -3.85338190772 , 5 ],
        [ -9.80936230066 , -1.94329906455 , 5 ],
        [ -9.99990206551 , 0.0442569798805 , 5 ],
        [ -9.79177729151 , 2.03004863819 , 5 ],
        [ -9.19328525665 , 3.93490866348 , 5 ],
        [ -8.22828594969 , 5.68289629768 , 5 ],
        [ -6.93525084777 , 7.20432478991 , 5 ],
        [ -5.36572918 , 8.43853958732 , 6 ],
        [ -3.58229282237 , 9.33633644075 , 6 ],
        [ -1.65604175448 , 9.86192302279 , 6 ],
        [ 0.336230472211 , 9.99434585501 , 6 ],
        [ 2.31509825102 , 9.72832565697 , 6 ],
        [ 4.20167036827 , 9.0744678145 , 6 ],
        [ 5.92073514707 , 8.0588395764 , 6 ],
        [ 7.40375889952 , 6.72193083553 , 6 ],
        [ 8.59161814856 , 5.11703992453 , 6 ],
        [ 9.43695669444 , 3.30814877949 , 6 ],
        [ 9.90607355695 , 1.36737218208 , 7 ],
        [ 9.98026652716 , -0.627917229241 , 7 ],
        [ 9.65657776549 , -2.59817356214 , 7 ],
        [ 8.94791172141 , -4.46484891412 , 7 ],
        [ 7.88252067375 , -6.15352482955 , 7 ],
        [ 6.50287840157 , -7.59687912859 , 7 ],
        [ 4.86398688854 , -8.73736983011 , 7 ],
        [ 3.03118356746 , -9.52952916887 , 7 ],
        [ 1.07753652299 , -9.94177625184 , 7 ],
        [ -0.919068502277 , -9.95767608873 , 7 ],
        [ -2.87903316665 , -9.57659480323 , 8 ],
        [ -4.72421986398 , -8.81372490362 , 8 ],
        [ -6.38106682348 , -7.69947960542 , 8 ],
        [ -7.78352078534 , -6.27828035246 , 8 ],
        [ -8.87567033582 , -4.60678587411 , 8 ],
        [ -9.6139749188 , -2.75163338052 , 8 ],
        [ -9.96900066042 , -0.786781947318 , 8 ],
        [ -9.92659380471 , 1.20943599928 , 8 ],
        [ -9.48844497918 , 3.15743754919 , 8 ],
        [ -8.67202179486 , 4.97956202788 , 8 ],
        [ -7.50987246772 , 6.60316708244 , 9 ],
        [ -6.04832822406 , 7.96352470292 , 9 ],
        [ -4.34565622072 , 9.00640172385 , 9 ],
        [ -2.46973661737 , 9.69022192939 , 9 ],
        [ -0.495356408784 , 9.98772356587 , 9 ],
        [ 1.49877209663 , 9.88704618187 , 9 ],
        [ 3.4331492882 , 9.39220346697 , 9 ],
        [ 5.23065765158 , 8.52292323865 , 9 ],
        [ 6.81963620068 , 7.31386095645 , 9 ],
        [ 8.13673737507 , 5.81321811814 , 9 ],
        [ 9.12945250728 , 4.08082061813 , 10 ],
        [ 9.75820517767 , 2.18573367785 , 10 ],
        [ 9.99792900143 , 0.203508433317 , 10 ],
        [ 9.83906694619 , -1.78683005025 , 10 ],
        [ 9.28795234077 , -3.70593325838 , 10 ],
        [ 8.36655638536 , -5.47729260224 , 10 ],
        [ 7.11161222906 , -7.03028957465 , 10 ],
        [ 5.57315053518 , -8.30301108709 , 10 ],
        [ 3.81250491655 , -9.24471774914 , 10 ],
        [ 1.89986675795 , -9.81786668793 , 10 ],
        [ -0.088513092904 , -9.99960826395 , 11 ],
        [ -2.07336420607 , -9.78269701407 , 11 ],
        [ -3.97555683121 , -9.17578050532 , 11 ],
        [ -5.7192565511 , -8.20305458367 , 11 ],
        [ -7.23494756044 , -6.90329876202 , 11 ],
        [ -8.46220404175 , -5.32833020333 , 11 ],
        [ -9.35209915195 , -3.54093793396 , 11 ],
        [ -9.86915558121 , -1.61237964324 , 11 ],
        [ -9.99275992137 , 0.380459135698 , 11 ],
        [ -9.71798445744 , 2.35813020951 , 11 ],
        [ -9.05578362007 , 4.24179007337 , 12 ],
        [ -8.03255726694 , 5.95634315275 , 12 ],
        [ -6.68909820378 , 7.43343562696 , 12 ],
        [ -5.07896590391 , 8.61418048029 , 12 ],
        [ -3.26635126105 , 9.45150514148 , 12 ],
        [ -1.32351750098 , 9.91202811863 , 12 ],
        [ 0.672080725255 , 9.97738981391 , 12 ],
        [ 2.64088521384 , 9.64498446278 , 12 ],
        [ 4.50440594275 , 8.92806401763 , 12 ],
        [ 6.1883502212 , 7.85520983423 , 12 ],
        [ 7.6255845048 , 6.46919322329 , 13 ],
        [ 8.75881079811 , 4.82527029325 , 13 ],
        [ 9.54285094493 , 2.98897906364 , 13 ],
        [ 9.94644773878 , 1.03352667104 , 13 ],
        [ 9.95351104912 , -0.963129168458 , 13 ],
        [ 9.56375928405 , -2.92138808734 , 13 ],
        [ 8.79273061651 , -4.76318048215 , 13 ],
        [ 7.67116352636 , -6.41507990222 , 13 ],
        [ 6.24377135416 , -7.81123033055 , 13 ],
        [ 4.56745972144 , -8.89597165536 , 13 ],
        [ 2.70905788308 , -9.62605866314 , 14 ],
        [ 0.742654455844 , -9.97238508879 , 14 ],
        [ -1.25335626096 , -9.92114399064 , 14 ],
        [ -3.19939961884 , -9.47437818957 , 14 ],
        [ -5.01789301021 , -8.6498988282 , 14 ],
        [ -6.63633884213 , -7.48057529689 , 14 ],
        [ -7.9902147866 , -6.01302483481 , 14 ],
        [ -9.0255460821 , -4.30575404777 , 14 ],
        [ -9.70105733707 , -2.42682643443 , 14 ],
        [ -9.98981804947 , -0.451148909445 , 14 ],
        [ -9.88031624093 , 1.54251449888 , 15 ],
        [ -9.376917403 , 3.47468272181 , 15 ],
        [ -8.49969045879 , 5.26832630963 , 15 ],
        [ -7.28360767832 , 6.85193835264 , 15 ],
        [ -5.77715044446 , 8.16238523608 , 15 ],
        [ -4.04037645323 , 9.14742357805 , 15 ],
        [ -2.14252540296 , 9.76778300832 , 15 ],
                   
                   ]
        
        
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_DEPTH_TEST)
        glMaterialfv(GL_FRONT,GL_AMBIENT, (.7,.7,.7,1.))
        glMaterialfv(GL_FRONT,GL_DIFFUSE, (.8,.8,.8,1.))
        glMaterialfv(GL_FRONT,GL_SPECULAR,(1.,1.,1.,1.))
        glMaterialfv(GL_FRONT,GL_SHININESS,100.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_NORMALIZE)
        glEnable(GL_COLOR_MATERIAL)
        
        
        for i in range(0, len(surface)):
            

            glPushMatrix()
    
            glColor3f(0.0, 
                      0.0, 
                      1.0)
            
            glLineWidth(1)

            #glBegin(GL_POINTS)
            #glBegin(GL_LINES)
            #glBegin(GL_LINE_STRIP)
            #glBegin(GL_TRIANGLE_STRIP)
            glBegin(GL_TRIANGLE_FAN)
            #glBegin(GL_LINE_LOOP)
            
            glVertex3f(surface[i][0], 
                       surface[i][1], 
                       surface[i][2])
            
            
            for j in range(0,len(surface)):
                
                dist =  [surface[i][0] - surface[j][0],
                         surface[i][1] - surface[j][1],
                         surface[i][2] - surface[j][2]]
                
                dist2 = dist[0]**2 + dist[1]**2 + dist[2]**2                

                if dist2 <= 20.0 and dist2 >= 16.0:
                    #glColor3f(j/100, 
                    #          i/100, 
                    #          j/100)
                    glVertex3f(surface[j][0], 
                               surface[j][1], 
                               surface[j][2])               
            glEnd()
            glPopName()
            glPopMatrix()
    
    
    
    

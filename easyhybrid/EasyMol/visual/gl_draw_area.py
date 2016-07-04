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

class GLCanvas(gtk.gtkgl.DrawingArea):
    
    data   = None
    fovy   = 30.0
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
    DOTS_SURFACE = DOTS = BALL_STICK = LINES = VDW = PRETTY_VDW = RIBBON = SPHERES = WIRES = SELECTION = MODIFIED = False
    
    def __init__(self, data=None, width=640, height=420):
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
	self.data   = data
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
	self.gl_points_list = self.gl_point_list = self.gl_ball_list = self.gl_stick_list = \
	self.gl_wires_list = self.gl_wired_stick_list = self.gl_lines_list = self.gl_vdw_list = \
	self.gl_pretty_vdw_list = self.gl_ribbon_list = self.gl_sphere_list = None
    
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
	self.dot_list         = []
	self.vdw_list         = []
	self.ball_list        = []
	self.bonds_list       = []
	self.wires_list       = []
	self.sphere_list      = []
	self.pretty_vdw_list  = []
	self.dot_surface_list = []
	if data is None and self.data is None:
	    print 'No data to load'
	else:
	    if data is not None:
		for chain in data[self.frame_i].chains.values():
		    for residue in chain.residues.values():
			for atom in residue.atoms.values():
			    if atom.dot:
				self.dot_list.append(atom)
			    if atom.vdw:
				self.vdw_list.append(atom)
			    if atom.ball:
				self.ball_list.append(atom)
			    if atom.wires:
				self.wires_list.append(atom)
			    if atom.sphere:
				self.sphere_list.append(atom)
			    if atom.pretty_vdw:
				self.pretty_vdw_list.append(atom)
			    if atom.dot_surface:
				self.dot_surface_list.append(atom)
	    else:
		for chain in self.data[self.frame_i].chains.values():
		    for residue in chain.residues.values():
			for atom in residue.atoms.values():
			    if atom.dot:
				self.dot_list.append(atom)
			    if atom.vdw:
				self.vdw_list.append(atom)
			    if atom.ball:
				self.ball_list.append(atom)
			    if atom.wires:
				self.wires_list.append(atom)
			    if atom.sphere:
				self.sphere_list.append(atom)
			    if atom.pretty_vdw:
				self.pretty_vdw_list.append(atom)
			    if atom.dot_surface:
				self.dot_surface_list.append(atom)
	    
	    # Surface dots representation of the atoms
	    for atom in self.dot_surface_list:
		atom.dots_surf = op.get_surf_dots(atom)
	    self.gl_points_list = glGenLists(1)
	    glNewList(self.gl_points_list, GL_COMPILE)
	    for atom in self.dot_surface_list:
		for point in atom.dots_surf:
		    rep.draw_dot(atom, point)
	    glEndList()
	    ## Center dots representations of the atoms
	    #self.gl_point_list = glGenLists(1)
	    #glNewList(self.gl_point_list, GL_COMPILE)
	    #for atom in self.dot_list:
		#rep.draw_point(atom)
	    #glEndList()
	    ## Sphere representation of the atoms, the difference between the ball
	    ## representation is that sphere uses the covalent radius and ball the
	    ## atomic radius.
	    #self.gl_sphere_list = glGenLists(1)
	    #glNewList(self.gl_sphere_list, GL_COMPILE)
	    #for atom in self.sphere_list:
		#rep.draw_sphere(atom)
	    #glEndList()
	    ## Ball representation.
	    #self.gl_ball_list = glGenLists(1)
	    #glNewList(self.gl_ball_list, GL_COMPILE)
	    #for atom in self.ball_list:
		#rep.draw_ball(atom)
	    #glEndList()
	    ## Wires representation.
	    #self.gl_wires_list = glGenLists(1)
	    #glNewList(self.gl_wires_list, GL_COMPILE)
	    #for atom in self.wires_list:
		#rep.draw_wire_sphere(atom)
	    #glEndList()
	    ## Makes the van-der-walls representation of the atoms.
	    #self.gl_vdw_list = glGenLists(1)
	    #glNewList(self.gl_vdw_list, GL_COMPILE)
	    #for atom in self.vdw_list:
		#rep.draw_vdw(atom)
	    #glEndList()
	    ## Makes the pretty van-der-walls representation of the atoms. The
	    ## difference between vdw is that this representation is transparent.
	    #self.gl_pretty_vdw_list = glGenLists(1)
	    #glNewList(self.gl_pretty_vdw_list, GL_COMPILE)
	    #for atom in self.pretty_vdw_list:
		#rep.draw_pretty_vdw(atom)
	    #glEndList()
	    ## Makes the ribbon representations
	    #self.gl_ribbon_list = glGenLists(1)
	    #glNewList(self.gl_ribbon_list, GL_COMPILE)
	    #for ribbon in self.data.ribbons:
		#rep.draw_ribbon(ribbon[0], ribbon[1], ribbon[2], ribbon[3])
	    #glEndList()
	    ## Makes the bonds representations in sticks format
	    #self.gl_stick_list = glGenLists(1)
	    #glNewList(self.gl_stick_list, GL_COMPILE)
	    #for bond in self.data.bonds:
		#rep.draw_bond_stick(bond[0], bond[1], bond[2], bond[3])
	    #glEndList()
	    ## Makes the bonds representations in wired sticks format
	    #self.gl_wired_stick_list = glGenLists(1)
	    #glNewList(self.gl_wired_stick_list, GL_COMPILE)
	    #for bond in self.data.bonds:
		#rep.draw_bond_wired_stick(bond[0], bond[1], bond[2], bond[3])
	    #glEndList()
    
    def draw(self):
	""" Defines wich type of representations will be displayed
	"""
	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
	glClearColor(self.gl_backgrd[0],self.gl_backgrd[1],self.gl_backgrd[2],self.gl_backgrd[3])
	#if self.SELECTION:
	for i,atom in enumerate(self.selected_atoms):
	    if atom is not None:
		rep.draw_selected(atom, i+2)
	if self.DOTS_SURFACE:
	    glCallList(self.gl_points_list, GL_COMPILE)
	if self.DOTS:
	    glCallList(self.gl_point_list, GL_COMPILE)
	if self.BALL_STICK:
	    glCallList(self.gl_ball_list, GL_COMPILE)
	    glCallList(self.gl_stick_list, GL_COMPILE)
	if self.WIRES:
	    glCallList(self.gl_wires_list, GL_COMPILE)
	    glCallList(self.gl_wired_stick_list, GL_COMPILE)
	if self.LINES:
	    glCallList(self.gl_lines_list, GL_COMPILE)
	if self.VDW:
	    glCallList(self.gl_vdw_list, GL_COMPILE)
	if self.PRETTY_VDW:
	    glCallList(self.gl_ball_list, GL_COMPILE)
	    glCallList(self.gl_stick_list, GL_COMPILE)
	    glCallList(self.gl_pretty_vdw_list, GL_COMPILE)
	if self.RIBBON:
	    glCallList(self.gl_ribbon_list, GL_COMPILE)
	if self.SPHERES:
	    glCallList(self.gl_sphere_list, GL_COMPILE)
    
    def draw_to_pick(self):
	""" Drawing method only to select atoms.
	"""
	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
	glClearColor(self.gl_backgrd[0],self.gl_backgrd[1],self.gl_backgrd[2],self.gl_backgrd[3])
	if self.DOTS_SURFACE:
	    glCallList(self.gl_points_list, GL_COMPILE)
	if self.DOTS:
	    glCallList(self.gl_point_list, GL_COMPILE)
	if self.BALL_STICK:
	    glCallList(self.gl_ball_list, GL_COMPILE)
	    glCallList(self.gl_stick_list, GL_COMPILE)
	if self.WIRES:
	    glCallList(self.gl_wires_list, GL_COMPILE)
	    glCallList(self.gl_wired_stick_list, GL_COMPILE)
	if self.LINES:
	    glCallList(self.gl_lines_list, GL_COMPILE)
	if self.VDW:
	    glCallList(self.gl_vdw_list, GL_COMPILE)
	if self.PRETTY_VDW:
	    glCallList(self.gl_ball_list, GL_COMPILE)
	    glCallList(self.gl_stick_list, GL_COMPILE)
	    glCallList(self.gl_pretty_vdw_list, GL_COMPILE)
	if self.RIBBON:
	    glCallList(self.gl_ribbon_list, GL_COMPILE)
	if self.SPHERES:
	    glCallList(self.gl_sphere_list, GL_COMPILE)
    
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
	    dist_z = op.get_euclidean(cam_pos, zrp)
	    vec_dir = op.unit_vector([atom_pos[0]-zrp[0], atom_pos[1]-zrp[1], atom_pos[2]-zrp[2]])
	    add_z = (self.z_far - self.z_near)/2
	    dist_z = op.get_euclidean(cam_pos, zrp)
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
		gl_context, gl_drawable = self.open_gl_ctx()
		x, y, width, height = self.get_allocation()
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(self.fovy, float(width)/float(height), self.z_near, self.z_far)
		glFogf(GL_FOG_START, self.fog_start)
		glFogf(GL_FOG_END, self.fog_end)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		gluLookAt(cam_pos[0], cam_pos[1], cam_pos[2],
			  pto[0], pto[1], pto[2],
			  up[0], up[1], up[2])
		self.window.invalidate_rect(self.allocation, False)
		self.window.process_updates(False)
		self.close_gl_ctx(gl_context, gl_drawable)
	    if dist%0.1 > 0:
		gl_context, gl_drawable = self.open_gl_ctx()
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
		self.close_gl_ctx(gl_context, gl_drawable)
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
	self.MODIFIED = True
	for i in range(len(self.data)):
	    self.frame_i = i
	    self.load_mol()
	    self.update_draw_view()
	    self.window.invalidate_rect(self.allocation, False)
	    self.window.process_updates(False)
    
    def pressed_1(self):
	""" Move to frame 1.
	"""
	self.MODIFIED = True
	self.frame_i = 1
	self.load_mol()
	self.update_draw_view()
    
    def pressed_2(self):
	""" Move to frame 2.
	"""
	self.MODIFIED = True
	self.frame_i = 2
	self.load_mol()
	self.update_draw_view()
    
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
	""" Change the representation to Ball-Stick.
	"""
	print 'Ball-Stick Representation'
	if self.gl_ball_list == None or self.MODIFIED:
	    self.gl_ball_list = glGenLists(1)
	    glNewList(self.gl_ball_list, GL_COMPILE)
	    for atom in self.ball_list:
		rep.draw_ball(atom)
	    glEndList()
	# Makes the bonds representations in sticks format
	if self.gl_stick_list == None or self.MODIFIED:
	    self.gl_stick_list = glGenLists(1)
	    glNewList(self.gl_stick_list, GL_COMPILE)
	    for bond in self.data[self.frame_i].bonds:
		rep.draw_bond_stick(bond[0], bond[1], bond[2], bond[3])
	    glEndList()
	self.queue_draw()
	return True
    
    def draw_dots(self):
	""" Change the representation to Dots.
	"""
	print 'Dots Representation'
	# Center dots representations of the atoms
	if self.gl_point_list == None or self.MODIFIED:
	    self.gl_point_list = glGenLists(1)
	    glNewList(self.gl_point_list, GL_COMPILE)
	    for atom in self.dot_list:
		rep.draw_point(atom)
	    glEndList()
	self.queue_draw()
	return True
    
    def draw_pretty_vdw(self):
	""" Change the representation to Pretty VDW.
	"""
	print 'Pretty Van-Der-Waals Representation'
	# Ball representation.
	if self.gl_ball_list == None or self.MODIFIED:
	    self.gl_ball_list = glGenLists(1)
	    glNewList(self.gl_ball_list, GL_COMPILE)
	    for atom in self.ball_list:
		rep.draw_ball(atom)
	    glEndList()
	# Makes the bonds representations in sticks format
	if self.gl_stick_list == None or self.MODIFIED:
	    self.gl_stick_list = glGenLists(1)
	    glNewList(self.gl_stick_list, GL_COMPILE)
	    for bond in self.data[self.frame_i].bonds:
		rep.draw_bond_stick(bond[0], bond[1], bond[2], bond[3])
	    glEndList()
	# Makes the pretty van-der-walls representation of the atoms. The
	# difference between vdw is that this representation is transparent.
	if self.gl_pretty_vdw_list == None or self.MODIFIED:
	    self.gl_pretty_vdw_list = glGenLists(1)
	    glNewList(self.gl_pretty_vdw_list, GL_COMPILE)
	    for atom in self.pretty_vdw_list:
		rep.draw_pretty_vdw(atom)
	    glEndList()
	self.queue_draw()
	return True
    
    def draw_ribbon(self):
	""" Change the representation to Ribbon.
	"""
	print 'Ribbon Representation'
	# Makes the ribbon representations
	if self.gl_ribbon_list == None or self.MODIFIED:
	    self.gl_ribbon_list = glGenLists(1)
	    glNewList(self.gl_ribbon_list, GL_COMPILE)
	    for ribbon in self.data[self.frame_i].ribbons:
		rep.draw_ribbon(ribbon[0], ribbon[1], ribbon[2], ribbon[3])
	    glEndList()
	self.queue_draw()
	return True
    
    def draw_spheres(self):
	""" Change the representation to Spheres.
	"""
	print 'Spheres Representation'
	# Sphere representation of the atoms, the difference between the ball
	# representation is that sphere uses the covalent radius and ball the
	# atomic radius.
	if self.gl_sphere_list == None:
	    self.gl_sphere_list = glGenLists(1)
	    glNewList(self.gl_sphere_list, GL_COMPILE)
	    for atom in self.sphere_list:
		rep.draw_sphere(atom)
	    glEndList()
	self.queue_draw()
	return True
    
    def draw_vdw(self):
	""" Change the representation to Van-Der-Waals.
	"""
	print 'Van-Der-Waals Representation'
	# Makes the van-der-walls representation of the atoms.
	if self.gl_vdw_list == None:
	    self.gl_vdw_list = glGenLists(1)
	    glNewList(self.gl_vdw_list, GL_COMPILE)
	    for atom in self.vdw_list:
		rep.draw_vdw(atom)
	    glEndList()
	self.queue_draw()
	return True
    
    def draw_wires(self):
	""" Change the representation to Wires.
	"""
	print 'Wired Representation'
	# Wires representation.
	if self.gl_wires_list == None:
	    self.gl_wires_list = glGenLists(1)
	    glNewList(self.gl_wires_list, GL_COMPILE)
	    for atom in self.wires_list:
		rep.draw_wire_sphere(atom)
	    glEndList()
	# Makes the bonds representations in wired sticks format
	if self.gl_wired_stick_list == None:
	    self.gl_wired_stick_list = glGenLists(1)
	    glNewList(self.gl_wired_stick_list, GL_COMPILE)
	    for bond in self.data[self.frame_i].bonds:
		rep.draw_bond_wired_stick(bond[0], bond[1], bond[2], bond[3])
	    glEndList()
	self.queue_draw()
	return True
    
    def update_draw_view(self):
	""" Redraws the representations with new data.
	"""
	reps = ['dots_surf', 'dots', 'vdw', 'pretty_vdw', 'ribbon', 'spheres', 'wires', 'ball_stick']
	for rep in reps:
	    func = getattr(self, 'draw_' + rep, None)
	    if func:
		func()
	#func = getattr(self, 'draw_ball_stick', None)
	#if func():
	    #func()
    
    def turn_off_reps(self):
	""" Hyde Everything
	"""
	self.DOTS_SURFACE = self.DOTS = self.LINES = self.VDW = self.PRETTY_VDW = self.RIBBON = self.SPHERES = self.WIRES = self.BALL_STICK = False
    
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
	    if self.pos_mouse[0] == x and self.pos_mouse[1] == y:
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
	    for chain in self.data[self.frame_i].chains.values():
		for residue in chain.residues.values():
		    for atom in residue.atoms.values():
			if atom.index == nearest[0]:
			    picked = atom
			    break
	return picked
    
    def get_cam_pos(self):
	""" Returns the position of the camera in XYZ coordinates
	    The type of data returned is 'numpy.ndarray'.
	"""
	modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
	crd_xyz = -1 * np.mat(modelview[:3,:3]) * np.mat(modelview[3,:3]).T
	return crd_xyz.A1
    

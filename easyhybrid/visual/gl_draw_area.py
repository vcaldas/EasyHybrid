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
from time import sleep
import math

from atom_types import get_color
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
    zero = None
    mouse_x = mouse_y = 0
    dist_cam_zpr = 0
    scroll = 1
    gl_sph_list = gl_bonds_list = gl_vdw_list = sph_list = vdw_list = bonds_list = None
    zpr_reference_point = target_point = np.array([0, 0, 0])
    mouse_rotate = mouse_pan = mouse_zoom = dragging = False
    gl_settings = {'sphere_scale':0.35, 'sphere_res':25}
    
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
	self.connect_after('realize', self._init)
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
	#self.realize()
    
    def _init(self, widget):
	""" Load the molecule if is any data and initialize the widget.
	"""
	assert(widget == self)
	self.load_mol()
        self.initialize()
	return True
	
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
    
    def initialize(self):
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
	self.sph_list = []
	self.vdw_list = []
	if data is None and self.data is None:
	    print 'No data to load'
	else:
	    if data is not None:
		pass
		for chain in data.chains.values():
		    for residue in chain.residues.values():
			for atom in residue.atoms.values():
			    if atom.sphere:
				self.sph_list.append(atom)
	    else:
		pass
		for chain in self.data.chains.values():
		    for residue in chain.residues.values():
			for atom in residue.atoms.values():
			    if atom.sphere:
				self.sph_list.append(atom)
			    if atom.vdw:
				self.vdw_list.append(atom)
	    
	    # Make calculations for the bonds, this part of the code must be more efficient
	    self.bonds_list = []
	    arr1 = np.array([0, 0, 1])
	    for i in range(len(self.sph_list)-1):
		for j in range(i+1, len(self.sph_list)):
		    if self.get_euclidean(self.sph_list[i].pos, self.sph_list[j].pos) <= (self.sph_list[i].cov_rad + self.sph_list[j].cov_rad):
			arr2 = self.unit_vector(self.sph_list[j].pos - self.sph_list[i].pos)
			angle = self.get_angle(arr1, arr2)
			vec_o = np.cross(arr1, arr2)
			length = self.get_euclidean(self.sph_list[i].pos, self.sph_list[j].pos)
			temp = (self.sph_list[i], length, angle, vec_o)
			#temp = (self.sph_list[i], self.sph_list[j])
			self.bonds_list.append(temp)
	    
	    # Surface dots representation of the atoms
	    for atom in self.sph_list:
		atom.dots_surf = op.get_surf_dots(atom)
	    self.gl_points_list = glGenLists(1)
	    glNewList(self.gl_points_list, GL_COMPILE)
	    for atom in self.sph_list:
		for point in atom.dots_surf:
		    rep.draw_dot(atom, point)
	    glEndList()
	    # Center dots representations of the atoms
	    self.gl_point_list = glGenLists(1)
	    glNewList(self.gl_point_list, GL_COMPILE)
	    for atom in self.sph_list:
		rep.draw_point(atom)
	    glEndList()
	    # Ball or sphere representation of the atoms, the difference between them
	    # is that ball are for ball-stick representation and sphere uses the
	    # atomic radius.
	    self.gl_sph_list = glGenLists(1)
	    glNewList(self.gl_sph_list, GL_COMPILE)
	    for atom in self.sph_list:
		rep.draw_sp(atom)
		#rep.draw_ball(atom)
	    glEndList()
	    # Makes the van-der-walls representation of the atoms or the pretty vdw,
	    # that is the vdw volume just transparent
	    self.gl_vdw_list = glGenLists(1)
	    glNewList(self.gl_vdw_list, GL_COMPILE)
	    for atom in self.vdw_list:
		rep.draw_pretty_vdw(atom)
		#rep.draw_vdw(atom)
	    glEndList()
	    # Makes the bonds representations, can be sticks or lines
	    self.gl_bonds_list = glGenLists(1)
	    glNewList(self.gl_bonds_list, GL_COMPILE)
	    for bond in self.bonds_list:
		rep.draw_bond_stick(bond[0], bond[1], bond[2], bond[3])
		#rep.draw_bond_line(bond[0], bond[1])
	    glEndList()
    
    def draw(self):
	""" Defines wich type of representations will be displayed
	"""
	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
	glClearColor(0.0, 0.0, 0.0, 0.0)
	#glCallList(self.gl_points_list, GL_COMPILE)
	#glCallList(self.gl_point_list, GL_COMPILE)
	glCallList(self.gl_sph_list, GL_COMPILE)
	glCallList(self.gl_bonds_list, GL_COMPILE)
	#glCallList(self.gl_vdw_list, GL_COMPILE)
    
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
	""" Test function for the A key.
	"""
	print 'Quitting'
	quit()
    
    def pressed_d(self):
	""" Test function for the A key.
	"""
	print 'd button pressed'
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glMatrixMode(GL_MODELVIEW)
	glRotate(5, 0, 1, 0)
	self.queue_draw()
	return True
    
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
        self.mouse_zoom = right and not (middle or left)
        self.mouse_pan = middle and not (right or left)
        x = self.mouse_x = event.x
        y = self.mouse_y = event.y
        self.drag_pos_x, self.drag_pos_y, self.drag_pos_z = self.pos(x, y)
        if event.button == 1 and event.type == gtk.gdk._2BUTTON_PRESS:
            nearest, hits = self._pick(x, self.get_allocation().height-1-y, 3, 3, event)
            self.pick(event, nearest, hits)
        if event.button == 2 and event.type == gtk.gdk.BUTTON_PRESS:
	    self.dist_cam_zpr = self.get_euclidean(self.zpr_reference_point, self.get_cam_pos())
    
    def mouse_released(self, widget, event):
	""" The mouse_released function serves, as the names states, to catch
	    mouse buttons events when released.
	"""
	self.mouse_rotate = self.mouse_pan = self.mouse_zoom = False
	if event.button == 2 and event.type == gtk.gdk.BUTTON_RELEASE:
	    if self.dragging:
		glMatrixMode(GL_MODELVIEW)
		modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
		dir_vec = modelview[:3, 2]
		cam_pos = self.get_cam_pos()
		dir_vec *= -self.dist_cam_zpr
		new_zpr = cam_pos + dir_vec
		self.dragging = False
	    else:
		pass
		#nearest, hits = self._pick(x, self.get_allocation().height-1-y, 3, 3, event)
		#self.pick(event, nearest, hits)
    
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
	gl_context, gl_drawable = self.open_gl_ctx()
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
	    x = self.zpr_reference_point[0]
	    y = self.zpr_reference_point[1]
	    z = self.zpr_reference_point[2]
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
        glTranslatef(*self.zpr_reference_point)
        func(*args)
        glTranslatef(*map(lambda x:-x, self.zpr_reference_point))
    
    def _pick(self, x, y, dx, dy, event):
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
        self.draw()
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
    
    def pick(self, event, nearest, hits):
	"""
	"""
        if event.button == 1 or event.button == 2:
	    if nearest != []:
		x = self.zero[nearest[0]][0]
		y = self.zero[nearest[0]][1]
		z = self.zero[nearest[0]][2]
		atom_pos = [x, y, z]
                self.zpr_reference_point = [x, y, z]
		self.target_point = atom_pos
        if event.button == 3 and nearest != []:
            px = self.zero[nearest[0]][0]
            py = self.zero[nearest[0]][1]
            pz = self.zero[nearest[0]][2]
            atom_position = [px, py, pz]
    
    def get_euclidean(self, pa, pb):
	""" Returns the distance between two points in R3
	"""
	if len(pa) == 1:
	    pa = [pa[0], 0, 0]
	if len(pa) == 2:
	    pa = [pa[0], pa[1], 0]
	if len(pb) == 1:
	    pb = [pb[0], 0, 0]
	if len(pb) == 2:
	    pb = [pb[0], pb[1], 0]
	return math.sqrt((pb[0]-pa[0])**2 +
			 (pb[1]-pa[1])**2 +
			 (pb[2]-pa[2])**2)
    
    def get_cam_pos(self):
	""" Returns the position of the camera in XYZ coordinates
	    The type of data returned is 'numpy.ndarray'.
	"""
	buffer = glGetDoublev(GL_MODELVIEW_MATRIX)
	crd_xyz = -1 * np.mat(buffer[:3,:3]) * np.mat(buffer[3,:3]).T
	return crd_xyz.A1
    
    def unit_vector(self, vector):
	""" Returns the unit vector of the vector.
	"""
	return vector / np.linalg.norm(vector)
    
    def get_angle(self, vecA, vecB):
	""" Return the angle in degrees of two vectors.
	"""
	vecA_u = self.unit_vector(vecA)
	vecB_u = self.unit_vector(vecB)
	return np.degrees(np.arccos(np.clip(np.dot(vecA_u, vecB_u), -1.0, 1.0)))
    

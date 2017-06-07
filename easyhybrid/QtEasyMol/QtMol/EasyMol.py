#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  EasyMol.py
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

import numpy as np
import operations as op
import representations as rep
import math
import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLE import *
from OpenGL.GLUT import *
from PySide import QtCore, QtGui, QtOpenGL

class DrawArea(QtOpenGL.QGLWidget):
    
    def __init__(self, parent=None):
        QtOpenGL.QGLWidget.__init__(self, parent)
        self.data   = None
        self.fovy   = 30.0
        self.aspect = 0.0
        self.z_near = 1.0
        self.z_far  = 10.0
        self.fog_start = self.z_far - 1.5
        self.fog_end = self.z_far
        self.width  = 640
        self.height = 420
        self.top    = 1.0
        self.bottom = -1.0
        self.left   = -10.0
        self.right  = 10
        self.selected_atoms = [None]*4
        self.mouse_x = mouse_y = 0
        self.dist_cam_zpr = frame_i = 0
        self.scroll = 1.0
        self.pick_radius = [10, 10]
        self.pos_mouse = [None, None]
        self.gl_backgrd = [0.0, 0.0, 0.0, 0.0]
        self.zrp = self.target_point = np.array([0, 0, 0])
        self.mouse_rotate = mouse_pan = mouse_zoom = dragging = False
        self.drag_pos_x = self.drag_pos_y = self.drag_pos_z = 0.0
        self.frame_i = 0
        self.LINES = self.DOTS = self.BALL_STICK = self.VDW = self.PRETTY_VDW = self.RIBBON = self.SPHERES = self.WIRES = self.SELECTION = self.MODIFIED = False
        self.gl_ball_stick_list = self.gl_point_list = self.gl_lines_list = self.gl_pretty_vdw_list = self.gl_ribbon_list =  self.gl_sphere_list = self.gl_vdw_list = self.gl_wires_list = None
        self.gl_crt_li = None
        self.CARTOON = False
    
    def initializeGL(self):
        """ Inside the realize function, you should put all you OpenGL
        	initialization code, e.g. set the projection matrix,
        	the modelview matrix, position of the camera.
        """
        glutInit()
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
        glFogf(GL_FOG_START, self.fog_start)
        glFogf(GL_FOG_END, self.fog_end)
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
        gluPerspective(self.fovy, float(self.width)/float(self.height), self.z_near, self.z_far)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0, 0, 10, 0, 0, 0, 0, 1, 0)
    
    def resizeGL(self, width, height):
        """
        Avoids error when resizing the window.
        """
        glViewport(0, 0, width, height)
        self.left = -float(width)/float(height)
        self.right = -self.left
        self.width = width
        self.height = height
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.fovy, float(width)/float(height), self.z_near, self.z_far)
        glMatrixMode(GL_MODELVIEW)
    
    def paintGL(self):
        """
        
        """
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glClearColor(self.gl_backgrd[0],self.gl_backgrd[1],self.gl_backgrd[2],self.gl_backgrd[3])
        
        #if self.DOTS:
            #glCallList(self.gl_point_list[self.frame_i])
        #if self.BALL_STICK:
            #glCallList(self.gl_ball_stick_list[self.frame_i])
        #if self.WIRES:
            #glCallList(self.gl_wires_list[self.frame_i])
        #if self.LINES:
            #glCallList(self.gl_lines_list[self.frame_i])
        #if self.VDW:
            #glCallList(self.gl_vdw_list[self.frame_i])
        #if self.PRETTY_VDW:
            #glCallList(self.gl_pretty_vdw_list[self.frame_i])
        if self.RIBBON:
            glCallList(self.gl_ribbon_list[self.frame_i])
        if self.SPHERES:
            glCallList(self.gl_sphere_list[self.frame_i])
        #rep.draw_helix(90, [0,1,0], 12.35)
        if self.CARTOON:
            glCallList(self.gl_crt_li)
    
    def minimumSizeHint(self):
        return QtCore.QSize(400, 400)
    
    def sizeHint(self):
        return QtCore.QSize(400, 400)
    
    def mousePressEvent(self, event):
        """
           
        """
        self.mouse_x = event.x()
        self.mouse_y = event.y()
        if (event.button() == QtCore.Qt.LeftButton):
            #print("Left click")
            self.mouse_rotate = True
            self.pos_mouse[0] = float(event.x())
            self.pos_mouse[1] = float(event.y())
        if (event.button() == QtCore.Qt.RightButton):
            #print("Right click")
            self.mouse_zoom = True
        if (event.button() == QtCore.Qt.MidButton):
            #print("Mid click")
            self.dist_cam_zpr = op.get_euclidean(self.zrp, self.get_cam_pos())
            self.drag_pos_x, self.drag_pos_y, self.drag_pos_z = self.pos(event.x(), event.y())
            self.mouse_pan = True
    
    def mouseDoubleClickEvent(self, event):
        """
           
        """
        if (event.button() == QtCore.Qt.LeftButton):
            nearest, hits = self.pick(event.x(), self.height-1-event.y(), self.pick_radius[0], self.pick_radius[1])
            selected = self.select(nearest, hits)
            if selected is not None:
                self.center_on_atom(selected.pos)
                self.zrp = selected.pos
                self.target_point = selected.pos
    
    def mouseReleaseEvent(self, event):
        """
           
        """
        self.mouse_rotate = False
        self.mouse_zoom = False
        self.mouse_pan = False
    
    def mouseMoveEvent(self, event):
        """
           
        """
        dx = float(event.x()) - self.mouse_x
        dy = float(event.y()) - self.mouse_y
        if ((dx == 0) and (dy == 0)):
            return
        self.mouse_x = float(event.x())
        self.mouse_y = float(event.y())
        changed = False
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        if (self.mouse_rotate):
            ax, ay, az = dy, dx, 0.0
            viewport = glGetIntegerv(GL_VIEWPORT)
            angle = math.sqrt(ax**2+ay**2+az**2)/float(viewport[2]+1)*180.0
            inv = np.matrix(glGetDoublev(GL_MODELVIEW_MATRIX)).I
            bx = (inv[0,0]*ax + inv[1,0]*ay)
            by = (inv[0,1]*ax + inv[1,1]*ay)
            bz = (inv[0,2]*ax + inv[1,2]*ay)
            glTranslate(self.zrp[0],self.zrp[1],self.zrp[2])
            glRotatef(angle,bx,by,bz)
            glTranslate(-self.zrp[0],-self.zrp[1],-self.zrp[2])
            changed = True
        elif (self.mouse_zoom):
            glMatrixMode(GL_MODELVIEW)
            modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
            # Delta is a modifier for the zoom effect, otherwise the zoom movement
            # would be too abrupt.
            delta = ((self.z_far-self.z_near)/2.0 + self.z_near)/200.0
            glLoadIdentity()
            # We only need to move along the Z axis, that is why only use the
            # glTranslatef function with a bz value
            bz = dy*delta
            glTranslatef(-self.zrp[0], -self.zrp[1], -self.zrp[2])
            glTranslatef(0, 0, bz)
            glTranslatef(self.zrp[0], self.zrp[1], self.zrp[2])
            glMultMatrixd(modelview)
            self.dist_cam_zpr += bz
            # Now we make the new projection view
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            self.z_near -= bz
            self.z_far -= bz
            self.fog_start -= bz
            self.fog_end -= bz
            # Depending how near we are from the z_near clipping plane, we need
            # to put some boundaries to avoid unexpected behaviors. Same with
            # the z_far clipping plane
            if (self.z_near > 0.1):
                gluPerspective(self.fovy, float(self.width)/float(self.height), self.z_near, self.z_far)
            elif (self.z_far <= 0.15):
                gluPerspective(self.fovy, float(self.width)/float(self.height), 0.1, 0.15)
            else:
                gluPerspective(self.fovy, float(self.width)/float(self.height), 0.1, self.z_far)
            glFogf(GL_FOG_START, self.fog_start)
            glFogf(GL_FOG_END, self.fog_end)
            glMatrixMode(GL_MODELVIEW)
            changed = True
        elif (self.mouse_pan):
            # The mouse pan function needs to be corrected to have
            # better behavior when the screen is far and near
            glMatrixMode(GL_MODELVIEW)
            px, py, pz = self.pos(event.x(), event.y())
            modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
            glLoadIdentity()
            glTranslatef((px-self.drag_pos_x)*(self.z_far)/10, 
                         (py-self.drag_pos_y)*(self.z_far)/10, 
                         #(pz-self.drag_pos_z)*(self.z_far)/10)
                          modelview[2,3])
            glMultMatrixd(modelview)
            self.drag_pos_x = px
            self.drag_pos_y = py
            self.drag_pos_z = pz
            changed = True
        if (changed):
            self.updateGL()
    
    def wheelEvent(self, event):
        """
           
        """
        if (event.delta() < 0):
            self.z_near += self.scroll
            self.z_far -= self.scroll
        if (event.delta() > 0):
            self.z_near -= self.scroll
            self.z_far += self.scroll
        if (self.z_near < 0.1):
            self.z_near = 0.1
        if (self.z_near >= self.z_far):
            self.z_near -= self.scroll
            self.z_far += self.scroll
        dist = float(self.z_far - self.z_near)
        self.fog_start = self.z_near + .85*dist
        self.fog_end = self.z_far;
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.fovy, float(self.width)/float(self.height), self.z_near, self.z_far)
        glFogf(GL_FOG_START, self.fog_start)
        glFogf(GL_FOG_END, self.fog_end)
        glMatrixMode(GL_MODELVIEW)
        self.updateGL()
    
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
            zrp = self.zrp
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
                #x, y, width, height = self.get_allocation()
                glMatrixMode(GL_PROJECTION)
                glLoadIdentity()
                gluPerspective(self.fovy, float(self.width)/float(self.height), self.z_near, self.z_far)
                glFogf(GL_FOG_START, self.fog_start)
                glFogf(GL_FOG_END, self.fog_end)
                glMatrixMode(GL_MODELVIEW)
                glLoadIdentity()
                gluLookAt(cam_pos[0], cam_pos[1], cam_pos[2],
                      pto[0], pto[1], pto[2],
                      up[0], up[1], up[2])
                self.updateGL()
            if dist%0.1 > 0:
                dist_z = op.get_euclidean(cam_pos, atom_pos)
                self.z_far = dist_z + add_z
                self.z_near = dist_z - add_z
                self.fog_start = self.z_far - 1.5
                self.fog_end = self.z_far
                #x, y, width, height = self.get_allocation()
                glMatrixMode(GL_PROJECTION)
                glLoadIdentity()
                gluPerspective(self.fovy, float(self.width)/float(self.height), self.z_near, self.z_far)
                glFogf(GL_FOG_START, self.fog_start)
                glFogf(GL_FOG_END, self.fog_end)
                glMatrixMode(GL_MODELVIEW)
                glLoadIdentity()
                gluLookAt(cam_pos[0], cam_pos[1], cam_pos[2], atom_pos[0], atom_pos[1], atom_pos[2], up[0], up[1], up[2])
            self.updateGL()
    
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
    
    def pick(self, x, y, dx, dy):
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
        self.paintGL()
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
    
    def select(self, nearest, hits):
        """
        """
        picked = None
        if nearest != []:
            for chain in list(self.data[self.frame_i].chains.values()):
                for residue in list(chain.residues.values()):
                    for atom in list(residue.atoms.values()):
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
        if data is None and self.data is None:
            print('No data to load')
        else:
            if data is not None:
                for chain in list(data[self.frame_i].chains.values()):
                    for residue in list(chain.residues.values()):
                        for atom in list(residue.atoms.values()):
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
            else:
                for chain in list(self.data[self.frame_i].chains.values()):
                    for residue in list(chain.residues.values()):
                        for atom in list(residue.atoms.values()):
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
            #self.LINES = self.draw_lines()
    
    def keyPressEvent(self, event):
        """ The mouse_button function serves, as the names states, to catch
            events in the keyboard, e.g. letter 'l' pressed, 'backslash'
            pressed. Note that there is a difference between 'A' and 'a'.
            Here I use a specific handler for each key pressed after
            discarding the CONTROL, ALT and SHIFT keys pressed (usefull
            for customized actions) and maintained, i.e. it's the same as
            using Ctrl+Z to undo an action.
        """
        if (event.key() == QtCore.Qt.Key_Escape):
            self.close()
        if (event.key() == QtCore.Qt.Key_B):
            self.pressed_b()
        if (event.key() == QtCore.Qt.Key_S):
            self.pressed_s()
        if (event.key() == QtCore.Qt.Key_R):
            self.pressed_r()
        if (event.key() == QtCore.Qt.Key_C):
            self.pressed_c()
    
    def pressed_Key_Escape(self):
        """ Turn on/off Ball-Stick representation.
        """
        self.close()
    
    def pressed_b(self):
        """ Turn on/off Ball-Stick representation.
        """
        self.BALL_STICK = not self.BALL_STICK
        self.draw_ball_stick()
        self.updateGL()
        return True
    
    def pressed_D(self):
        """ Turn on/off Dots representation.
        """
        self.DOTS = not self.DOTS
        self.draw_dots()
        self.updateGL()
        return True
    
    def pressed_l(self):
        """ Turn on/off Lines representation.
        """
        self.LINES = not self.LINES
        self.draw_lines()
        self.updateGL()
        return True
    
    def pressed_p(self):
        """ Turn on/off the Pretty VDW representation.
        """
        self.PRETTY_VDW = not self.PRETTY_VDW
        self.draw_pretty_vdw()
        self.updateGL()
        return True
    
    def pressed_r(self):
        """ Turn on/off the Ribbon representation.
        """
        self.RIBBON = not self.RIBBON
        self.draw_ribbon()
        self.updateGL()
        return True
    
    def pressed_s(self):
        """ Turn on/off the Sphere representation.
        """
        self.SPHERES = not self.SPHERES
        self.draw_spheres()
        self.updateGL()
        return True
    
    def pressed_v(self):
        """ Turn on/off the Van-Der-Waals representation.
        """
        self.VDW = not self.VDW
        self.draw_vdw()
        self.updateGL()
        return True
    
    def pressed_w(self):
        """ Turn on/off the Wires representation.
        """
        self.WIRES = not self.WIRES
        self.draw_wires()
        self.updateGL()
        return True
    
    def pressed_c(self, pdb_resids=20):
        """ Test Cartoon
        """
        import numpy as np, operations as op
        cart = [(1,'N'), (2,'H'), (3,'H'), (4,'H'), (5,'H'),
                (6,'H'), (7,'H'), (8,'H'), (9,'N'), (10,'N'),
                (11,'N'), (12,'N'), (13,'N'), (14,'N'), (15,'N'),
                (16,'N'), (17,'N'), (18,'N'), (19,'N'), (20,'N')]
        frame = self.data[0]
        i = 0
        cartoons = []
        while i < len(frame.ribbons):
            if cart[i][1] == 'N':
                temp = (0, frame.ribbons[i])
                cartoons.append(temp)
                i += 1
            elif cart[i][1] == 'H':
                atom1 = frame.ribbons[i][0]
                while cart[i][1] == 'H':
                    i += 1
                atom2 = frame.ribbons[i][0]
                arr1 = np.array([0, 0, 1])
                arr2 = op.unit_vector(atom2.pos - atom1.pos)
                angle = op.get_angle(arr1, arr2)
                vec_o = np.cross(arr1, arr2)
                length = op.get_euclidean(atom1.pos, atom2.pos)
                temp = (1,(atom1, length, angle, vec_o))
                cartoons.append(temp)
        self.gl_crt_li = glGenLists(1)
        glNewList(self.gl_crt_li, GL_COMPILE)
        for car in cartoons:
            if car[0] == 0:
                rep.draw_ribbon(car[1][0], car[1][1], car[1][2], car[1][3])
            elif car[0] == 1:
                rep.draw_helix(car[1][2], car[1][3], car[1][1], car[1][0])
        glEndList()
        self.CARTOON = True
        return True
    
    def draw_ball_stick(self):
        """ Draws all the elements for Ball-Stick representation.
        """
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
    
    def draw_dots(self):
        """ Change the representation to Dots.
        """
        # Center dots representations of the atoms
        if self.gl_point_list == None or self.MODIFIED:
            self.gl_point_list = []
            for i in range(len(self.data)):
                self.frame_i = i
                self.load_mol()
                gl_pt_li = glGenLists(1)
                glNewList(gl_pt_li, GL_COMPILE)
                for atom in self.dot_list:
                    rep.draw_point(atom)
                glEndList()
                self.gl_point_list.append(gl_pt_li)
        return True
    
    def draw_lines(self):
        """ Change the representation to lines.
            It is the default representation.
        """
        if self.gl_lines_list == None or self.MODIFIED:
            self.gl_lines_list = []
            for frame in self.data:
                gl_ln_li = glGenLists(1)
                glNewList(gl_ln_li, GL_COMPILE)
                for bond in frame.bonds:
                    rep.draw_bond_line(bond[0], bond[4])
                glEndList()
                self.gl_lines_list.append(gl_ln_li)
        return True
    
    def draw_pretty_vdw(self):
        """ Change the representation to Pretty VDW.
        """
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
    
    def draw_ribbon(self):
        """ Change the representation to Ribbon.
        """
        # Makes the ribbon representations
        if self.gl_ribbon_list == None or self.MODIFIED:
            self.gl_ribbon_list = []
            for frame in self.data:
                gl_rb_li = glGenLists(1)
                glNewList(gl_rb_li, GL_COMPILE)
                for ribbon in frame.ribbons:
                    rep.draw_ribbon(ribbon[0], ribbon[1], ribbon[2], ribbon[3])
                glEndList()
                self.gl_ribbon_list.append(gl_rb_li)
        return True
    
    def draw_spheres(self):
        """ Change the representation to Spheres.
        """
        #print('Spheres Representation')
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
    

if __name__ == '__main__':
    import vis_parser as vp
    app = QtGui.QApplication(sys.argv)
    window = DrawArea()
    pdb_data = vp.parse_pdb("pdbs/1l2y.pdb")
    window.data = pdb_data
    window.show()
    sys.exit(app.exec_())

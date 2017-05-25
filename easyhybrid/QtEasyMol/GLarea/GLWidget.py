#!/usr/bin/env python


import sys
import math
from PySide import QtCore, QtGui, QtOpenGL
import numpy as np

try:
    from OpenGL import GL
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL",
                            "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)

import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import GLarea.operations as op
import GLarea.representations as rep
from GLarea.vector_math import Vector


class GLWidget(QtOpenGL.QGLWidget):
    
    def __init__(self, parent=None, glmenu = None):
        QtOpenGL.QGLWidget.__init__(self, parent)
        
        self.glmenu          = glmenu
        self.trolltechGreen  = QtGui.QColor.fromCmykF(0.40, 0.0, 1.0, 0.0)
        self.trolltechPurple = QtGui.QColor.fromCmykF(0.39, 0.39, 0.0, 0.0)


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
        
        self.mouse_x = 0
        self.mouse_y = 0
        self.x_press = None
        self.y_press = None

        self.dist_cam_zpr = frame_i = 0
        self.scroll = 0.5
        self.pick_radius = [10, 10]
        self.pos_mouse = [None, None]
        self.gl_backgrd = [0.0, 0.0, 0.0, 0.0]
        
        #self.zrp          = np.array([0, 0, 0])
        self.target_point = np.array([0, 0, 0])
        
        self.mouse_rotate = False
        self.mouse_pan    = False
        self.mouse_zoom   = False
        self.dragging     = False

        self.zero_reference_point = np.array([0, 0, 0])

        
        
        self.drag_pos_x = 0.0
        self.drag_pos_y = 0.0
        self.drag_pos_z = 0.0
        self.frame = 0
        self.LINES = self.DOTS = self.BALL_STICK = self.VDW = self.PRETTY_VDW = self.RIBBON = self.SPHERES = self.WIRES = self.SELECTION = self.MODIFIED = False
        self.gl_ball_stick_list = self.gl_point_list = self.gl_lines_list = self.gl_pretty_vdw_list = self.gl_ribbon_list =  self.gl_sphere_list = self.gl_vdw_list = self.gl_wires_list = None  
        
        self.EMSession = None
    
    
    def initializeGL(self):
        #self.qglClearColor(self.trolltechPurple.darker())
        #GL.glShadeModel(GL.GL_FLAT)
        #GL.glEnable(GL.GL_DEPTH_TEST)
        #GL.glEnable(GL.GL_CULL_FACE)
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
        #self.object = self.makeObject()

    
        #glutInit()
        self.create_gl_lists()
        #self.load_mol()
        self.gl_initialize()
        return True

    
    def gl_initialize(self):
        """ Initializes all the parameters for the OpenGL context. Is in 
            another module to keep OpenGL commands separated from the gtk
            commands.
        """
        rep.init_gl(self.fog_start, self.fog_end, self.fovy, self.width, self.height, self.z_near, self.z_far)
        return True

    def create_gl_lists(self):
        """
        """
        #self.gl_ball_stick_list = self.gl_point_list = self.gl_lines_list = self.gl_pretty_vdw_list = self.gl_ribbon_list =  self.gl_sphere_list = self.gl_vdw_list = self.gl_wires_list = None
        




    def paintGL(self):
        #GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        
        ##GL.glLoadIdentity()
        ##GL.glTranslated(0.0, 0.0, -10 )
        ##GL.glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        ##GL.glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        ##GL.glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
        #GL.glCallList(self.object)
        self.draw()


    def draw(self, frame = -1):
        """ Defines wich type of representations will be displayed
        """
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glClearColor(self.gl_backgrd[0],self.gl_backgrd[1],self.gl_backgrd[2],self.gl_backgrd[3])
        frame = self.frame
        
        for Vobject in self.EMSession.Vobjects:    
            if Vobject.actived:   
                #-------------------------------------------------------
                # Necessary, once trajectories have different sizes
                #-------------------------------------------------------
                input_frame = frame

                if input_frame >= (len(Vobject.frames)-1):
                    input_frame = len(Vobject.frames) -1



                glDisable(GL_LIGHT0)
                glDisable(GL_LIGHTING)
                glDisable(GL_COLOR_MATERIAL)
                glEnable (GL_DEPTH_TEST)
                                
                if Vobject.show_dots    :
                    glCallList(Vobject.list_dots[input_frame], GL_COMPILE)

                if Vobject.show_lines   :
                    glCallList(Vobject.list_lines[input_frame], GL_COMPILE)

                if Vobject.show_ribbons :
                    glCallList(Vobject.list_ribbons[input_frame], GL_COMPILE)

                
                
                glEnable(GL_LIGHT0)
                glEnable(GL_LIGHTING)
                glEnable(GL_COLOR_MATERIAL)
                glEnable(GL_DEPTH_TEST)
                
                if Vobject.show_sticks  :
                    glCallList(Vobject.list_sticks        [input_frame], GL_COMPILE)

                if Vobject.show_ball_and_stick :
                    glCallList(Vobject.list_ball_and_stick[input_frame], GL_COMPILE)
                
                if Vobject.show_spheres :
                    glCallList(Vobject.list_spheres[input_frame], GL_COMPILE)

                if Vobject.show_surface :
                    glCallList(Vobject.list_surface[input_frame], GL_COMPILE)

        for i,atom in enumerate(self.selected_atoms):
            if atom is not None:
                glPushMatrix()
                glDisable(GL_DEPTH_TEST)
                glEnable(GL_LINE_SMOOTH)
                glColor3f(1, 0, 0)
                glLineWidth(2)
                glTranslate(float(atom.pos[0]), float( atom.pos[1]), float( atom.pos[2]))
                glRotate(0, 0, 1, 0)
                glScalef(0.006, 0.006, 0.006)
                glutStrokeCharacter(GLUT_STROKE_MONO_ROMAN, ord(str(i+1)))
                glPopMatrix()













    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        self.left = -float(width)/float(height)
        self.right = -self.left
        self.width = width
        self.height = height
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.fovy, float(width)/float(height), self.z_near, self.z_far)
        glMatrixMode(GL_MODELVIEW)

    def mousePressEvent(self, event):
        self.x_press = event.x()
        self.y_press = event.y()
        
        self.mouse_x = event.x()
        self.mouse_y = event.y()
        if (event.button() == QtCore.Qt.LeftButton):
            #print("Left click")
            self.mouse_rotate = True
            self.pos_mouse[0] = float(event.x())
            self.pos_mouse[1] = float(event.y())
            
            '''
            nearest, hits = self.pick( x, self.get_allocation().height-1-y, self.pick_radius[0], self.pick_radius[1], event)
            selected = self.select(event, nearest, hits)
            if selected is not None:
                self.center_on_atom(selected.pos)
                self.zero_reference_point = selected.pos
                self.target_point = selected.pos
            '''
            
        if (event.button() == QtCore.Qt.RightButton):
            #print("Right click")
            self.mouse_zoom = True
        if (event.button() == QtCore.Qt.MidButton):
            #print("Mid click")
            self.dist_cam_zpr = op.get_euclidean(self.zero_reference_point, self.get_cam_pos())
            self.drag_pos_x, self.drag_pos_y, self.drag_pos_z = self.pos(event.x(), event.y())
            self.mouse_pan = True

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
            self.apply_trans(glRotatef, angle, bx, by, bz)
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
            glTranslatef(-self.zero_reference_point[0], -self.zero_reference_point[1], -self.zero_reference_point[2])
            glTranslatef(0, 0, bz)
            glTranslatef(self.zero_reference_point[0], self.zero_reference_point[1], self.zero_reference_point[2])
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
            
            '''
            #x, y, width, height = self.get_allocation()
            #ax, ay, az = 0, 0, dy
            #modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
            ##self.line_width_refresh()
            #delta = ((self.z_far-self.z_near)/2)+ self.z_near
            #delta = delta/200
            #glLoadIdentity()
            
            #inv = np.matrix(glGetDoublev(GL_MODELVIEW_MATRIX)).I
            #bx = (inv[0,0]*ax + inv[1,0]*ay + inv[2,0]*az)/(1/(delta))
            #by = (inv[0,1]*ax + inv[1,1]*ay + inv[2,1]*az)/(1/(delta))
            #bz = (inv[0,2]*ax + inv[1,2]*ay + inv[2,2]*az)/(1/(delta))
            #self.apply_trans(glTranslatef, bx, by, bz)
            #glMultMatrixd(modelview)
            
            
            glMatrixMode(GL_MODELVIEW)
            modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
            # Delta is a modifier for the zoom effect, otherwise the zoom movement
            # would be too abrupt.
            delta = ((self.z_far-self.z_near)/2.0 + self.z_near)/200.0
            glLoadIdentity()
            
            # We only need to move along the Z axis, that is why only use the
            # glTranslatef function with a bz value
            bz = dy*delta
            glTranslatef(-self.zero_reference_point[0], -self.zero_reference_point[1], -self.zero_reference_point[2])
            glTranslatef(0, 0, bz)
            glTranslatef(self.zero_reference_point[0], self.zero_reference_point[1], self.zero_reference_point[2])
            glMultMatrixd(modelview)
            self.dist_cam_zpr += bz
            
            
            
            
            
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
            '''

        elif (self.mouse_pan):
            # The mouse pan function needs to be corrected to have
            # better behavior when the screen is far and near
            glMatrixMode(GL_MODELVIEW)
            px, py, pz = self.pos(event.x(), event.y())
            
            modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
            
            glLoadIdentity()
            '''
            glTranslatef((px-self.drag_pos_x)*(self.z_far)/10, 
                         (py-self.drag_pos_y)*(self.z_far)/10, 
                         #(pz-self.drag_pos_z)*(self.z_far)/10)
                          modelview[2,3])
            '''              
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
        
        if (changed):
            self.updateGL()

    def mouseReleaseEvent(self, event):
        
        """
           
        """
        self.mouse_rotate = False
        self.mouse_zoom = False
        self.mouse_pan = False
        
        
        self.lastPos = QtCore.QPoint(event.pos())
        
        dx = event.x() - self.x_press
        dy = event.y() - self.y_press
        
        if dx == 0 and dy == 0:
            button = event.button()
            if button == QtCore.Qt.MouseButton.RightButton:
                print('RightButton')
                menu = QtGui.QMenu(self)
                
                for item in self.glmenu:                
                    menu.addAction(item)
                menu.exec_(event.globalPos())
            
            if button == QtCore.Qt.MouseButton.LeftButton:
                print('LeftButton')
                
            else:
                print (button)
    
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
        """ 
            
            
            !!!  This fuction is called only to test new GL features  !!!  
            
            Loads the data (if is any) or replace it if new data is given.
            This is the core of the representations, and need to be more
            efficient.
        """
        
        glDisable(GL_LIGHT0)
        glDisable(GL_LIGHT1)
        glDisable(GL_LIGHT2)
        glDisable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_DEPTH_TEST)

        n = 1
        for Vobject in self.EMSession.Vobjects:
            #print Vobject.label
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

    
    
    
    def apply_trans(self, func, *args):
        """
        """
        glTranslatef(*self.zero_reference_point)
        func(*args)
        glTranslatef(*map(lambda x:-x, self.zero_reference_point))

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
    
    def draw_lines(self, Vobject = None , selection = None):
        """ Change the representation to lines.
            It is the default representation.
        """
        glDisable(GL_LIGHT0)
        glDisable(GL_LIGHT1)
        glDisable(GL_LIGHT2)
        glDisable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_DEPTH_TEST)
        n = 1
        for frame in Vobject.frames:
            gl_ln_li = glGenLists(n)
            
            glNewList(gl_ln_li, GL_COMPILE)
            glLineWidth(3)

            for bond in Vobject.index_bonds:
                
                atom1    = Vobject.atoms[bond[0]]
                atom2    = Vobject.atoms[bond[1]]
                coord1   = frame[bond[0]]
                coord2   = frame[bond[1]]

                midcoord = [
                        (coord1[0] + coord2[0])/2,	   
                        (coord1[1] + coord2[1])/2,
                        (coord1[2] + coord2[2])/2,
                        ]
                
                glPushMatrix()		
                glPushName(atom1.atom_id) 
                glColor3f(atom1.color[0], 
                          atom1.color[1], 
                      atom1.color[2])

                
                glBegin(GL_LINES)
                glVertex3f(coord1[0],coord1[1],coord1[2])
                glVertex3f(midcoord[0],midcoord[1],midcoord[2])
                glEnd()
                glPopName()
                glPopMatrix()
                
                
                glPushMatrix()		
                glPushName(atom2.atom_id) 
                glColor3f (atom2.color[0], 
                           atom2.color[1], 
                       atom2.color[2])

                glBegin(GL_LINES)
                glVertex3f(midcoord[0],midcoord[1],midcoord[2])
                glVertex3f(coord2[0],coord2[1],coord2[2])

                glEnd()
                glPopName()
                glPopMatrix()

            '''
            for bond in Vobject.bonds:
            
            glDisable(GL_LIGHT0)
            glDisable(GL_LIGHT1)
            glDisable(GL_LIGHT2)
            glDisable(GL_LIGHTING)
            glEnable(GL_COLOR_MATERIAL)
            glEnable(GL_DEPTH_TEST)
            glPushMatrix()
            glPushName(bond[0].atom_id) # old glPushName(bond[0].index)
            glColor3f(bond[0].color[0], bond[0].color[1], bond[0].color[2])
            glLineWidth(3)
            glBegin(GL_LINES)
            glVertex3f(bond[0].pos[0], bond[0].pos[1], bond[0].pos[2])
            glVertex3f(bond[4][0], bond[4][1], bond[4][2])
            glEnd()
            glPopName()
            glPopMatrix()
            '''
            glEndList()
            Vobject.list_lines.append(gl_ln_li)
            
        n += 1
        return True
        
        '''
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
        '''
    
    def draw_ribbon(self, Vobject = None , selection = None):
        """ Change the representation to Ribbon.
        """
	
        for frame in Vobject.frames:
            glEnable(GL_COLOR_MATERIAL)
            glEnable(GL_DEPTH_TEST)
            
            gl_rb_li = glGenLists(1)
            glNewList(gl_rb_li, GL_COMPILE)
            #print 'aqui'
            glLineWidth(7)

            #'''
            if Vobject.actived:
                for chain in  Vobject.chains:
                    for i in range(0, len(Vobject.chains[chain].backbone) -1):
                        ATOM1  = Vobject.chains[chain].backbone[i]
                        ATOM2  = Vobject.chains[chain].backbone[i+1]
                        #if (ATOM1.resi - ATOM2.resi) == 1:	    
                        coord1 = frame[ATOM1.index -1]
                        coord2 = frame[ATOM2.index -1]
                        #print coord1, coord2
                        glPushMatrix()
                        glColor3f(ATOM1.color[0],ATOM1.color[1], ATOM1.color[1])
                        glBegin(GL_LINES)
                        
                        glVertex3f(coord1[0],coord1[1],coord1[2])
                        glVertex3f(coord2[0],coord2[1],coord2[2])
                        
                        glEnd()
                        glPopName()
                        glPopMatrix()

            glEndList()
            #'''
            Vobject.list_ribbons.append(gl_rb_li)

    
    
    def draw_spheres(self):
        """ Change the representation to Spheres.
        """
        #print('Spheres Representation')
        # Sphere representation of the atoms, the difference between the ball
        # representation is that sphere uses the covalent radius and ball the
        # atomic radius.
        for frame in Vobject.frames:
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
    
    def draw_ball_and_stick (self, Vobject = None , selection = None):
        """ Draws all the elements for Ball-Stick representation.
        """

        for frame in Vobject.frames:
            glEnable(GL_LIGHT0)
            glEnable(GL_LIGHTING)
            glEnable(GL_COLOR_MATERIAL)
            glEnable(GL_DEPTH_TEST)
           
            gl_bs_li = glGenLists(2)
            glNewList(gl_bs_li, GL_COMPILE)
            
            for bond in Vobject.index_bonds:
                
                atom1    = Vobject.atoms[bond[0]]
                atom2    = Vobject.atoms[bond[1]]

                coord1   = frame[bond[0]]
                coord2   = frame[bond[1]]

                midcoord = [
                           (coord1[0] + coord2[0])/2,	   
                           (coord1[1] + coord2[1])/2,
                           (coord1[2] + coord2[2])/2,
                           ]



                #self.PointSize =20
                #-------------------------------------------------------
                #                        B A L L 
                #-------------------------------------------------------
                glPushMatrix()                
                glPushName(atom1.index)
                glTranslate(atom1.pos[0],   atom1.pos[1],   atom1.pos[2])
                glColor3f(atom1.color[0], atom1.color[1], atom1.color[2])
                glutSolidSphere(atom1.radius, 15, 15)
                glPopMatrix()
                glPopName()

                glPushMatrix()                
                glPushName(atom2.index)
                glTranslate(atom2.pos[0],   atom2.pos  [1],   atom2.pos  [2])
                glColor3f  (atom2.color[0], atom2.color[1],   atom2.color[2])
                glutSolidSphere(atom2.radius, 15, 15)                           
                glPopName()
                glPopMatrix()
                #-------------------------------------------------------


                #-------------------------------------------------------
                #                        S T I C K S
                #-------------------------------------------------------
                #rep.draw_stick_bond(atom1 = atom1, atom2 = atom2, radius = 2)
                
                v = Vector()
                #base of cylinder is at the origin, the top is in the positive z axis
                radius = 0.05
                a = coord1
                b = coord2
                
                axis_start = [0, 0, .1]
                axis_end = v.subtract(a, b)

                #find angle between the starting and ending axis
                angle = v.angle(axis_start, axis_end)
                
                # determina the axis of rotation of the angle
                axis_rotation = v.crossproduct (axis_start, axis_end)

                #calculate the distance from a to b
                length = v.mag(axis_end)
                glColor3f(0.9, 0.9, 0.9)

                # set the bottom  and the top radius to be the same thing
                radius_bottom = radius
                radius_top    = radius

                # draw the bond ( use glTranslate beofre using glRotate)
                cyl = gluNewQuadric()
                glPushMatrix()
                glTranslate(b[0], b[1], b[2])
                glRotate(angle, axis_rotation[0], axis_rotation[1], axis_rotation[2])
                gluCylinder(cyl, radius_bottom, radius_top, length, 15, 15)
                glPopMatrix()
                #-------------------------------------------------------





            
            glEndList()
            Vobject.list_ball_and_stick.append(gl_bs_li)  
            return True


    def change_background(self, color):
        """ Changes the color of the background.
            The color variable is an array of four elements 
            corresponding to Red, Green, Blue and Alpha values
            in the 0.0-1.0 range.
        """
        self.gl_backgrd = color
        glFogfv(GL_FOG_COLOR, color[:3])
        self.draw()
        self.updateGL()





















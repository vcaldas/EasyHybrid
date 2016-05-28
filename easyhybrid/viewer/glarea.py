#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  GLarea.py
#  
#  Copyright 2016 Fernando Bachega <fernando@Fenrir>
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


#------------------------------------------------------------------------------
import pygtk; pygtk.require('2.0')
import gtk, gtk.gdk as gdk, gtk.gtkgl as gtkgl, gtk.gdkgl as gdkgl
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import numpy
from numpy import matrix
import sys
import time
#------------------------------------------------------------------------------



class GLCanvas(gtkgl.DrawingArea):
    def __init__(self,session = None ,w=640,h=480):
        try:
            glconfig = gdkgl.Config(mode = (gdkgl.MODE_RGB|gdkgl.MODE_DOUBLE|gdkgl.MODE_DEPTH))
        except gtk.gdkgl.NoMatches:
            glconfig = gdkgl.Config(mode = (gdkgl.MODE_RGB|gdkgl.MODE_DEPTH))
        gtkgl.DrawingArea.__init__(self,glconfig)
        
        self.h = h
        self.w = w
        self.set_size_request(w,h)
        self.connect_after("realize"       ,self._init)
        self.connect("configure_event"     ,self._reshape)
        self.connect("expose_event"        ,self._draw)
        self.connect("button_press_event"  ,self._mouseButton)
        self.connect("button_release_event",self._mouseButton)
        self.connect("motion_notify_event" ,self._mouseMotion)
        self.connect("scroll_event"        ,self._mouseScroll)
        self.connect("key_press_event"     ,self._keyPress    )

        self.set_events(self.get_events()|
            gdk.BUTTON_PRESS_MASK|gdk.BUTTON_RELEASE_MASK|
            gdk.POINTER_MOTION_MASK|gdk.POINTER_MOTION_HINT_MASK|
            gdk.KEY_PRESS_MASK)
        
        #------------ isso que faltava para o keypress ----------#
        self.set_flags(gtk.HAS_FOCUS|gtk.CAN_FOCUS)              #
        self.grab_focus()                                        #
        #--------------------------------------------------------#


        #--------------------------------------------------------------#
        # glFrustum
        self.left    = 0.0
        self.right   = 0.0
        self.bottom  = 0.0
        self.top     = 0.0
        self.nearVal = 0.0
        self.farVal  = 0.0 
        #--------------------------------------------------------------#

        #--------------------------------------------------------------#
        # glLookAt                                                     # 
        self.eyeX    = 0.0                                             #
        self.eyeY    = 0.0                                             #
        self.eyeZ    = 0.0                                             #
        self.centerX = 0.0                                             #
        self.centerY = 0.0                                             #
        self.centerZ = -1.0                                            #
        self.upX     = 0.0                                             #
        self.upY     = 1.0                                             #
        self.upZ     = 0.0                                             #
        #--------------------------------------------------------------#
        
        #--------------------------------------------------------------#
        # glOrtho                                                      #
        self._left   = 10                                              #
        self._right  = 10                                              #
        self._bottom = 10                                              #
        self._top    = 10                                              #
        self._zNear, self._zFar = -3.0, 3.0                            #
        #--------------------------------------------------------------#

        #--------------------------------------------------------------#
        # gluPerspective
        self.fovy   = 30.0
        self.aspect = 0.0
        self.zNear  = 0.1
        self.zFar   = 10.0
        #--------------------------------------------------------------#


        #--------------------------------------------------------------#
        self.fog_start = 7
        self.fog_end   = 11
        #--------------------------------------------------------------#
        
        
        #---------------------------------------------------------------
        self.zero = None
        self.x_total = 0
        self.y_total = 0
        self.z_total = 0
        #---------------------------------------------------------------
        
        #--------------------------------------------------------------#
        self._zprReferencePoint = [0.,0.,0.,0.]
        #self.MassReferencePoint = [self.x_total,self.y_total,self.z_total,0.]
        self.MassReferencePoint = [self.x_total,self.y_total,self.z_total,0.]
        self._mouseX      = self._mouseY    = 0                        #
        self._dragPosX    = self._dragPosY  = self._dragPosZ = 0.      #
        self._dragPosX_P  = self._dragPosY_P = 0
        self._dragPosX_R  = self._dragPosY_R = 0
        self._mouseRotate = self._mouseZoom = self._mousePan = False   #
        self._dragging = False
	self._target_point = self._zprReferencePoint[:3]
	#--------------------------------------------------------------#
        
        self.line_width = 3
        
   
    class _Context:
        def __init__(self,widget):
            self._widget = widget
            self._count = 0
            self._modelview = self._projection = None
            self._persist = False
        
        def __enter__(self):
            assert(self._count == 0)
            self.ctx = gtkgl.widget_get_gl_context(self._widget)
            self.surface = gtkgl.widget_get_gl_drawable(self._widget)
            self._begin = self.surface.gl_begin(self.ctx)
            if self._begin:
                self._count += 1
                
                if self._projection is not None:
                    glMatrixMode(GL_PROJECTION)
                    glLoadMatrixd(self._projection)
                if self._modelview is not None:
                    glMatrixMode(GL_MODELVIEW)
                    glLoadMatrixd(self._modelview)
                return self
            return
        
        def __exit__(self,exc_type,exc_value,exc_traceback):
            if self._begin:
                self._count -= 1
                if self._persist and (exc_type is None):
                    self._modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
                    self._projection = glGetDoublev(GL_PROJECTION_MATRIX)
                self.surface.gl_end()
            del self.ctx
            del self.surface
            self._persist = False
            if exc_type is not None:
                import traceback
                traceback.print_exception(exc_type,exc_value,exc_traceback)
            return True # suppress
    
    def open_context(self,persist_matrix_changes = False):
        if not hasattr(self,"_context"):
            self._context = self._Context(self)
        assert(self._context._count == 0)
        self._context._persist = persist_matrix_changes
        return self._context

    def get_open_context(self):
        if hasattr(self,"_context") and (self._context._count > 0):
            return self._context
        
    def _init(self,widget):
        assert(widget == self)
        self.init() ### optionally overriden by subclasses
        return True
        
    def reset(self):
        with self.open_context(True):
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
         
    def init(self):
        pass
        #glLightfv(GL_LIGHT0,GL_AMBIENT, (0.,0.,0.,1.))
        #glLightfv(GL_LIGHT0,GL_DIFFUSE, (1.,1.,1.,1.))
        #glLightfv(GL_LIGHT0,GL_SPECULAR,(1.,1.,1.,1.))
        #glLightfv(GL_LIGHT0,GL_POSITION,(1.,1.,1.,0.))
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
        glFogf(GL_FOG_START ,  self.fog_start)
        glFogf(GL_FOG_END   ,  self.fog_end)
        glFogfv(GL_FOG_COLOR, [0,0,0])
        glFogfv(GL_FOG_DENSITY, 1)
        glEnable(GL_POINT_SMOOTH)
        
        # light
        light_0_position = [ 1.0,  1.0, 1.0, 0.0]
        light_1_position = [ 1.0, -1.0, 1.0, 0.0]
        light_2_position = [-1.0, -1.0, 1.0, 0.0]
        
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glShadeModel(GL_SMOOTH)
        
        glLightfv(GL_LIGHT0,   GL_POSITION, light_0_position)
        glLightfv(GL_LIGHT1,   GL_POSITION, light_1_position)
        glLightfv(GL_LIGHT2,   GL_POSITION, light_2_position)
        
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHT1)
        glEnable(GL_LIGHT2)
        glEnable(GL_LIGHTING)
        glEnable(GL_DEPTH_TEST)
        
        #  Antialiased lines
        glEnable (GL_LINE_SMOOTH)
        glEnable (GL_BLEND)
        glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glHint (GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
        
        #---------------------------------------------------------------
        self.line_width_refresh()
        #---------------------------------------------------------------
	with self.open_context(True):
	    gluLookAt(self.eyeX, self.eyeY, self.eyeZ, 
		      self.centerX, self.centerY, self.centerZ,
		      self.upX, self.upY, self.upZ)
	    self.queue_draw()
	
        #glLineWidth (2.5)
        #self._apply(glTranslatef,  0, 0,  5)

    def _reshape(self,widget,event):
        assert(self == widget) 
        with self.open_context(True):
            x, y, width, height = self.get_allocation()
            glViewport(0,0,width,height);
            self._top    =  1.0
            self._bottom = -1.0
            self._left   = -float(width)/float(height)
            self._right  = -self._left
            
            
            '''
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            

            glOrtho(self._left,
                    self._right,
                    self._bottom,
                    self._top,
                    self._zNear,
                    self._zFar)
            '''
            
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            gluPerspective(self.fovy, float(width)/float(height), self.zNear,self.zFar)

        if hasattr(self,"reshape"):
            self.reshape(event,x,y,width,height) ### optionally implemented by subclasses
        return True
        
    def _mouseMotion(self,widget,event):
        assert(widget==self)
        if event.is_hint:
            x, y, state = event.window.get_pointer()
        else:
            x = event.x
            y = event.y
            state = event.state
        dx = x - self._mouseX
        dy = y - self._mouseY

        if (dx==0 and dy==0): return
        
        self._mouseX, self._mouseY = x, y
        
        with self.open_context(True):
            changed = False
            if self._mouseZoom:
                '''
                # atingo, quando usava o Ortho
                xi, yi, width, height = self.get_allocation()
                s = math.exp(float(dy)*0.01)
                self._apply(glScalef,s,s,s)
                #self.zNear     += +s/10
                #self.zFar      += +s/10
                #self.fog_start += +s/10
                #self.fog_end   += +s/10
                #gluPerspective(self.fovy, float(width)/float(height), self.zNear, self.zFar)
                #glFogf(GL_FOG_START ,  self.fog_start)
                #glFogf(GL_FOG_END   ,  self.fog_end  )
                #'''
                
                
                #'''
                x, y, width, height = self.get_allocation()
                ax, ay, az = 0, 0, dy
                
                modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
                self.line_width_refresh()
                
                delta = ((self.zFar - self.zNear)/2)+ self.zNear
                #delta = math.exp(delta)*0.01
                delta = delta/200
                #print scale
                glLoadIdentity()
                inv   = matrix(glGetDoublev(GL_MODELVIEW_MATRIX)).I
                bx = (inv[0,0]*ax + inv[1,0]*ay + inv[2,0]*az)/(1/(delta))
                by = (inv[0,1]*ax + inv[1,1]*ay + inv[2,1]*az)/(1/(delta))
                bz = (inv[0,2]*ax + inv[1,2]*ay + inv[2,2]*az)/(1/(delta))
                
                self._apply(glTranslatef,bx,by,bz)
                glMultMatrixd(modelview)

                glMatrixMode(GL_PROJECTION)
                glLoadIdentity()
                self.zNear     += -bz
                self.zFar      += -bz
                self.fog_start += -bz
                self.fog_end   += -bz
                self.PrintCameraStatus()
                
                
                ##------------------------------#
                ##        gluPerspective        #
                ##------------------------------#
                if self.zNear >= 0.1:
                    gluPerspective(self.fovy, float(width)/float(height), self.zNear, self.zFar)
                else: 
                    gluPerspective(self.fovy, float(width)/float(height), 0.1, self.zFar)
                glFogf(GL_FOG_START ,  self.fog_start)
                glFogf(GL_FOG_END   ,  self.fog_end  )
                #'''

                '''
                #------------------------------#
                #            glOrtho           #
                #------------------------------#
                x, y, width, height = self.get_allocation()
                glMatrixMode(GL_PROJECTION)
                glLoadIdentity()
                glOrtho(self._left, 
                        self._right,
                        self._bottom, 
                        self._top, 
                        self.zNear, 
                        self.zFar)
                #'''
                changed = True



            elif self._mouseRotate:
                ax, ay, az = dy, dx, 0.
                
                viewport = glGetIntegerv(GL_VIEWPORT)
                #print viewport
                
                angle = math.sqrt(ax**2+ay**2+az**2)/float(viewport[2]+1)*180.0
                inv = matrix(glGetDoublev(GL_MODELVIEW_MATRIX)).I

                #print inv
                bx = (inv[0,0]*ax + inv[1,0]*ay + inv[2,0]*az)#*1000
                by = (inv[0,1]*ax + inv[1,1]*ay + inv[2,1]*az)#*1000
                bz = (inv[0,2]*ax + inv[1,2]*ay + inv[2,2]*az)#*1000
               
                #glRotatef(angle,bx,by,bz)  # poderia ser apenas este aqui
                 
                self._apply(glRotatef,angle,bx,by,bz)
                changed = True
                

            elif self._mousePan:
                px, py, pz = self._pos(x,y);
                modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
                #scale = (modelview[3][2]*-1)
                #px  = px*(self.zFar/10)
                #py  = py*(self.zFar/10)
                px  = px 
                py  = py 
                
                glLoadIdentity()
                glTranslatef((px-self._dragPosX)*(self.zFar)/10, 
                             (py-self._dragPosY)*(self.zFar)/10, 
                             (pz-self._dragPosZ)*(self.zFar)/10)
                glMultMatrixd(modelview)
		
                x = self._zprReferencePoint[0]
                y = self._zprReferencePoint[1]
                z = self._zprReferencePoint[2]
                
                self._dragPosX = px
                self._dragPosY = py
                self._dragPosZ = pz
                changed = True
            
            if changed:
                self.queue_draw()
	if state & gtk.gdk.BUTTON2_MASK:
	    self._dragging = True
    
    def _mouseScroll(self,widget,event):
        assert(self == widget)       
        '''
        if event.direction == gdk.SCROLL_UP:
            self._zNear -= 0.05
            self._zFar  += 0.05
            #self._right += 1.05
        if event.direction == gdk.SCROLL_DOWN:
            self._zNear += 0.05
            self._zFar  -= 0.05
            #self._right -= 1.05
        '''
        
        if event.direction == gdk.SCROLL_UP:
            
            
            #if self.zNear >= 0.1:
            self.zNear     -= 0.2
            self.zFar      += 0.2
            self.fog_start += 0.2
            self.fog_end   += 0.2
            
            
        if event.direction == gdk.SCROLL_DOWN:
            
        
            
            if self.zNear >= self.zFar:
                pass
                #self.zNear = 0.2
                #self.zFar  = 0.4
            #self.zNear     += 0.2
            else:
                self.zNear     += 0.2
                self.zFar      -= 0.2
                self.fog_start -= 0.2
                self.fog_end   -= 0.2

            #self._right -= 1.05
        
        self.PrintCameraStatus()
        #print "self.zNear", self.zNear, "self.zFar ", self.zFar, 'fog_start', self.fog_start
        
        with self.open_context(True):
            #'''
            #------------------------------#
            #        gluPerspective        #
            #------------------------------#
            x, y, width, height = self.get_allocation()
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            if self.zNear >= 0.1:
                gluPerspective(self.fovy, float(width)/float(height), self.zNear, self.zFar)
            else: 
                gluPerspective(self.fovy, float(width)/float(height), 0.1, self.zFar)
            
            #gluPerspective(self.fovy, float(width)/float(height), self.zNear,self.zFar)
            glFogf(GL_FOG_START ,  self.fog_start)
            glFogf(GL_FOG_END   ,  self.fog_end)
            #'''
            
            '''
            #------------------------------#
            #            glOrtho           #
            #------------------------------#
            x, y, width, height = self.get_allocation()
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            glOrtho(self._left, 
                    self._right,
                    self._bottom, 
                    self._top, 
                    self.zNear, 
                    self.zFar)
            glFogf(GL_FOG_START ,  self.fog_start)
            glFogf(GL_FOG_END   ,  self.fog_end)
            #'''
            #glFogf(GL_FOG_START,self._zNear)
            #glFogf(GL_FOG_END,  self._zFar)
            #gluLookAt(0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 1.0, 0.0)
            
            self.queue_draw()
    
    def _apply(self,func,*args):
        glTranslatef(*self._zprReferencePoint[0:3])
        func(*args)
        glTranslatef(*map(lambda x:-x,self._zprReferencePoint[0:3]))

    

        
    @classmethod
    def event_masked(cls,event,mask):
        return (event.state & mask) == mask
    
    @classmethod
    def _button_check(cls,event,button,mask):
        # this shouldn't be so crazy complicated
        if event.button == button:
            return (event.type == gdk.BUTTON_PRESS)                    
        return cls.event_masked(event,mask) 
        
    @classmethod
    def get_left_button_down(cls,event):
        return cls._button_check(event,1,gdk.BUTTON1_MASK)
             
    @classmethod
    def get_middle_button_down(cls,event):
        return cls._button_check(event,2,gdk.BUTTON2_MASK)

    @classmethod
    def get_right_button_down(cls,event):
        return cls._button_check(event,3,gdk.BUTTON3_MASK)

    def _mouseButton(self,widget,event):
        left   = self.get_left_button_down(event)
        middle = self.get_middle_button_down(event)
        right  = self.get_right_button_down(event)
        
        #print event
        
        self._mouseRotate = left   and not (middle or right)

        self._mouseZoom   = right  and not (middle or left) #middle or (left and right)
        
        self._mousePan    = middle and not (right or left) #right and self.event_masked(event,gdk.SHIFT_MASK) #right and self.event_masked(event,gdk.CONTROL_MASK)
        
        #self._mousePan2   = left   and self.event_masked(event,gdk.CONTROL_MASK)

        #test              = middle and self.event_masked(event,gdk.SHIFT_MASK)
        

        
        x = self._mouseX = event.x
        y = self._mouseY = event.y
        self._dragPosX, self._dragPosY, self._dragPosZ = self._pos(x,y)                          

        #------------------------------------------------------------------------------#
        if event.button == 1 and event.type == gtk.gdk._2BUTTON_PRESS:                 #
            nearest, hits =	self._pick(x,self.get_allocation().height-1-y,3,3,event)   #      # Double Click left button             
            self.pick(event,nearest,hits) # None if nothing hit                        #    
        #------------------------------------------------------------------------------#
                           
                
        ##-----------------------------------------------------------------------------------------#                                                                                          
        #if self._mousePan2:                                                                       #   modificado por mim 
        #    with self.open_context():                                                             #
        #        nearest, hits =	self._pick(x,self.get_allocation().height-1-y,3,3,event)          #
        #        self.pick(event,nearest,hits) # None if nothing hit                               #
        ##-----------------------------------------------------------------------------------------#	                                                                                      
        #self.queue_draw()
       
        #------------------------------------------------------------------------------#
        
        if event.button == 2 and event.type == gtk.gdk.BUTTON_PRESS:
	    self._dist_cam_zpr = self.get_euclidean(self._zprReferencePoint[:3],
						    self.get_cam_pos())
        #------------------------------------------------------------------------------#
	if event.button == 2 and event.type == gtk.gdk.BUTTON_RELEASE:
	    if self._dragging:
		glMatrixMode(GL_MODELVIEW)
		modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
		dir_vec = modelview[:3, 2]
		cam_pos = self.get_cam_pos()
		dir_vec *= -self._dist_cam_zpr
		new_zpr = cam_pos + dir_vec
		self.MassReferencePoint = [new_zpr[0], new_zpr[1], new_zpr[2], 0.0]
		self._zprReferencePoint = self.MassReferencePoint
		self._dragging = False
	    else:
		nearest, hits = self._pick(x,self.get_allocation().height-1-y,3,3,event)
		self.pick(event,nearest,hits) # None if nothing hit
	
	if event.button == 3 and event.type == gtk.gdk._2BUTTON_PRESS:
	    self.print_camera_pos()
	    cam_pos = self.get_cam_pos()
	    zpr = self._zprReferencePoint[:3]
	    print zpr, '<-- zpr point'
	    vecZ = glGetDoublev(GL_PROJECTION_MATRIX)
	    vecZ = vecZ[:3, 2]
	    zpr_cam = self.unit_vector([zpr[0]-cam_pos[0], zpr[1]-cam_pos[1], zpr[2]-cam_pos[2]])
	    print zpr_cam, '<-- vector zpr-cam'
	    print vecZ, '<-- vectorZ'
            
    
    def _keyPress    (self,widget,event):
        with self.open_context(True):
	    pass
	    #print event

    def pick(self,event,nearest,hits):
        if event.button == 1 or event.button == 2:
	    if nearest != []:
		x = self.zero[nearest[0]][0]
		y = self.zero[nearest[0]][1]
		z = self.zero[nearest[0]][2]
		atom_pos = [x, y, z]
		self.MassReferencePoint = [x, y, z, 0.0]
		#self._center_on_atom(atom_pos)
		self._center_on_atom_anim(atom_pos)
                self._zprReferencePoint = self.MassReferencePoint
		self._target_point = atom_pos
        if event.button == 3 and nearest != []:
	    #print 'event==3?'
            px = self.zero[nearest[0]][0]
            py = self.zero[nearest[0]][1]
            pz = self.zero[nearest[0]][2]
            #print px,py,pz
            atom_position = [px, py, pz]
            #px = 10.0 #self.MassReferencePoint[0]
            #py = 10.0 #self.MassReferencePoint[1]
            #pz = 10.0 #self.MassReferencePoint[2] + 10
	

            
            
            with self.open_context(True):
                #------------------------------#
                #        gluPerspective        #
                #------------------------------#
                x, y, width, height = self.get_allocation()
                #self._center_on_atom(atom_position)
            
    def _pos(self,x,y):
        """
        Use the ortho projection and viewport information
        to map from mouse co-ordinates back into world
        co-ordinates
        """  
        viewport = glGetIntegerv(GL_VIEWPORT)
        px = float(x-viewport[0])/float(viewport[2])
        py = float(y-viewport[1])/float(viewport[3])       
        px = self._left + px*(self._right-self._left)
        py = self._top  + py*(self._bottom-self._top)
        pz = self._zNear
        return (px,py,pz)
        
    def _pick(self,x,y,dx,dy,event):
        buf = glSelectBuffer(256)
        glRenderMode(GL_SELECT)
        glInitNames()
        glMatrixMode(GL_PROJECTION)
        glPushMatrix() # remember projection matrix
        viewport = glGetIntegerv(GL_VIEWPORT)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        glLoadIdentity()
        gluPickMatrix(x,y,dx,dy,viewport)
        glMultMatrixd(projection)        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        self.draw(event)
        glPopMatrix()
        hits = glRenderMode(GL_RENDER)
        nearest = []
        minZ = None
        for hit in hits:
            if (len(hit.names) > 0) and \
            ((minZ is None) or (hit.near < minZ)):
                minZ = hit.near
                nearest = hit.names
        glMatrixMode(GL_PROJECTION)
        glPopMatrix() # restore projection matrix 
        glMatrixMode(GL_MODELVIEW)
        return (nearest, hits)

    def _draw(self,widget,event):
        assert(self == widget)   
        with self.open_context() as ctx:
            glMatrixMode(GL_MODELVIEW)
            self.draw(event) ### implemented by subclasses
            if ctx.surface.is_double_buffered():
                ctx.surface.swap_buffers()
            else:
                glFlush()
        return True
    
    def print_camera_pos(self):
	""" Useless function.
	"""
	camMat = glGetDoublev(GL_MODELVIEW_MATRIX)
	crd_xyz = self.get_cam_pos()
	print camMat, '<-- matriz cam'
	print crd_xyz[0], crd_xyz[1], crd_xyz[2], '<-- pos camara en XYZ'
	#print self.zNear, self.zFar, '<-- zNear y zFar respect'
    
    def get_cam_pos(self):
	""" Returns the position of the camera in XYZ coordinates
	    The type of data returned is 'numpy.ndarray'.
	"""
	buffer = glGetDoublev(GL_MODELVIEW_MATRIX)
	crd_xyz = -1 * numpy.mat(buffer[:3,:3]) * numpy.mat(buffer[3,:3]).T
	return crd_xyz.A1
    
    def get_euclidean(self, pA, pB):
	if len(pA) == 1:
	    pA = [pA[0], 0, 0]
	if len(pA) == 2:
	    pA = [pA[0], pA[1], 0]
	if len(pB) == 1:
	    pB = [pB[0], 0, 0]
	if len(pB) == 2:
	    pB = [pB[0], pB[1], 0]
	return math.sqrt( (pB[0]-pA[0])**2 +
			  (pB[1]-pA[1])**2 +
			  (pB[2]-pA[2])**2
			)
    
    def unit_vector(self, vector):
	""" Returns the unit vector of the vector.
	"""
	return vector / numpy.linalg.norm(vector)
    
    def get_angle(self, vecA, vecB):
	""" Docs
	"""
	vecA_u = self.unit_vector(vecA)
	vecB_u = self.unit_vector(vecB)
	return numpy.degrees(numpy.arccos(numpy.clip(numpy.dot(vecA_u, vecB_u), -1.0, 1.0)))
    
    def get_angle_np(self, vA, vB):
	return math.acos((vA[0]*vB[0] + vA[1]*vB[1] + vA[2]*vB[2])/
			 (vA[0]**2 + vA[1]**2 + vA[2]**2)**0.5/
			 (vB[0]**2 + vB[1]**2 + vB[2]**2)**0.5)
    
    def get_projec_angle(self, vA, vB):
	""" Returns the angles between 2 vectors projected in the 3 planes
	    of the XYZ coordinates system, in the order [XY, XZ, YZ].
	    The angles returned are in degrees.
	    
	    vA and vB are vectors of R3.
	"""
	vA_xy = [vA[0], vA[1]]
	vA_xz = [vA[0], vA[2]]
	vA_yz = [vA[1], vA[2]]
	vB_xy = [vB[0], vB[1]]
	vB_xz = [vB[0], vB[2]]
	vB_yz = [vB[1], vB[2]]
	ang_vA_VB_xy = 180 - self.get_angle(vA_xy, vB_xy)
	ang_vA_VB_xz = 180 - self.get_angle(vA_xz, vB_xz)
	ang_vA_VB_yz = 180 - self.get_angle(vA_yz, vB_yz)
	return [ang_vA_VB_xy, ang_vA_VB_xz, ang_vA_VB_yz]
    
    def _center_on_atom(self, atom_pos):
        """ Only change the center of viewpoint of the camera.
	    It does not change (yet) the position of the camera.
	    
	    atom_pos is a vector containing the XYZ coordinates
	    of the selected atom.
	"""
	cam_pos = self.get_cam_pos()
	if self.get_euclidean(self._target_point, atom_pos) != 0:
	    with self.open_context(True):
		glMatrixMode(GL_MODELVIEW)
		modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
		up = modelview[:3, 1]
		glLoadIdentity()
		gluLookAt(cam_pos[0], cam_pos[1], cam_pos[2],
			  atom_pos[0], atom_pos[1], atom_pos[2],
			  up[0], up[1], up[2])
		self.queue_draw()

    def _center_on_atom_anim(self, atom_pos):
        """ Only change the center of viewpoint of the camera.
	    It does not change (yet) the position of the camera.
	    
	    atom_pos is a vector containing the XYZ coordinates
	    of the selected atom.
	"""
	if self.get_euclidean(self._target_point, atom_pos) != 0:
	    cam_pos = self.get_cam_pos()
	    glMatrixMode(GL_MODELVIEW)
	    modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
	    up = modelview[:3, 1]
	    zpr = self._zprReferencePoint[:3]
	    dist = self.get_euclidean(zpr, atom_pos)
	    dist_z = self.get_euclidean(cam_pos, zpr)
	    vec_dir = self.unit_vector([atom_pos[0]-zpr[0], atom_pos[1]-zpr[1], atom_pos[2]-zpr[2]])
	    add_z = (self.zFar - self.zNear)/2
	    cycles = int(1/.06)
	    to_add = float(dist/cycles)
	    for i in range(1, cycles):
		aum = i*to_add
		pto = [zpr[0]+vec_dir[0]*aum, zpr[1]+vec_dir[1]*aum, zpr[2]+vec_dir[2]*aum]
		self.zFar = dist_z + add_z
		self.zNear = dist_z - add_z
		self.fog_start = self.zFar - 3
		self.fog_end = self.zFar + 1
		dist_z = self.get_euclidean(cam_pos, pto)
		with self.open_context(True):
		    x, y, width, height = self.get_allocation()
		    glMatrixMode(GL_PROJECTION)
		    glLoadIdentity()
		    gluPerspective(self.fovy, float(width)/float(height), self.zNear, self.zFar)
		    glFogf(GL_FOG_START, self.fog_start)
		    glFogf(GL_FOG_END, self.fog_end)
		    glMatrixMode(GL_MODELVIEW)
		    glLoadIdentity()
		    gluLookAt(cam_pos[0], cam_pos[1], cam_pos[2],
			      pto[0], pto[1], pto[2],
			      up[0], up[1], up[2])
		self.window.invalidate_rect(self.allocation, False)
		self.window.process_updates(False)
	    if dist%0.1 > 0:
		with self.open_context(True):
		    dist_z = self.get_euclidean(cam_pos, atom_pos)
		    self.zFar = dist_z + add_z
		    self.zNear = dist_z - add_z
		    self.fog_start = self.zFar - 3
		    self.fog_end = self.zFar + 1
		    x, y, width, height = self.get_allocation()
		    glMatrixMode(GL_PROJECTION)
		    glLoadIdentity()
		    gluPerspective(self.fovy, float(width)/float(height), self.zNear, self.zFar)
		    glFogf(GL_FOG_START, self.fog_start)
		    glFogf(GL_FOG_END, self.fog_end)
		    glMatrixMode(GL_MODELVIEW)
		    glLoadIdentity()
		    gluLookAt(cam_pos[0], cam_pos[1], cam_pos[2], atom_pos[0], atom_pos[1], atom_pos[2], up[0], up[1], up[2])
	    self.queue_draw()

    def PrintCameraStatus (self, log = True):
        """ Function doc """
        if log:
	    pass
            #print 'zNear = ', self.zNear, 'zFar = ',   self.zFar, 'deltaZ = ', self.zNear - self.zFar, 'fog_start = ', self.fog_start, 'fog_end = ', self.fog_end, 'self.fog_end, deltaFog = ', self.fog_start - self.fog_end 
        else:
            pass 

    def line_width_refresh(self):
        """ Function doc """
        deltaZ =  self.zFar - self.zNear
        centro =  0 + (self.zNear+(deltaZ/2))  #mass_center[2] - centro
        line_width = (self.line_width)/(centro/10)
        glLineWidth(line_width)

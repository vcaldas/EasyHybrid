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
        self.eyeZ    = 20.0                                            #
        self.CenterX = 5.0                                             #
        self.CenterY = 5.0                                             #
        self.CenterZ = 5.0                                             #
        self.upX     = 0.0                                             #
        self.upY     = 0.0                                             #
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
        self.fog_start = 5
        self.fog_end   = 10
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
        self._mouseRotate = self._mouseZoom = self._mousePan = False   #
        #--------------------------------------------------------------#


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
        #glLineWidth (10.5)


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
                '''
                x, y, width, height = self.get_allocation()
                ax, ay, az = 0, 0, dy
                
                
                modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
                #scale      = (modelview[3][2]*-1)
                line_width = 100/self.zFar
                #print scale
                glLoadIdentity()
                inv   = matrix(glGetDoublev(GL_MODELVIEW_MATRIX)).I
                bx = (inv[0,0]*ax + inv[1,0]*ay + inv[2,0]*az)/10#(scale)
                by = (inv[0,1]*ax + inv[1,1]*ay + inv[2,1]*az)/10#(scale)
                bz = (inv[0,2]*ax + inv[1,2]*ay + inv[2,2]*az)/10#(scale)
                
                self._apply(glTranslatef,bx,by,bz)
                glMultMatrixd(modelview)


                glMatrixMode(GL_PROJECTION)
                glLoadIdentity()
                self.zNear     += -bz
                self.zFar      += -bz
                self.fog_start += -bz
                self.fog_end   += -bz
                
                self.PrintCameraStatus()
                
                gluPerspective(self.fovy, float(width)/float(height), self.zNear, self.zFar)
                glFogf(GL_FOG_START ,  self.fog_start)
                glFogf(GL_FOG_END   ,  self.fog_end  )
                
                glLineWidth(line_width)
                #x = self._zprReferencePoint[0]
                #y = self._zprReferencePoint[1]
                #z = self._zprReferencePoint[2]
                changed = True
                #print self._zprReferencePoint
                #self._zprReferencePoint = [x , y , z + bz, 0.]
                #print self._zprReferencePoint                
                
                
                ##-------------------------------------------------------------------------------
                #self.zNear     -= bz
                #self.zFar      -= bz
                #self.fog_start -= bz
                #self.fog_end   -= bz
                ##------------------------------#
                ##        gluPerspective        #
                ##------------------------------#
                #x, y, width, height = self.get_allocation()
                #glMatrixMode(GL_PROJECTION)
                #glLoadIdentity()
                #gluPerspective(self.fovy, float(width)/float(height), self.zNear,self.zFar)
                #glFogf(GL_FOG_START ,  self.fog_start)
                #glFogf(GL_FOG_END   ,  self.fog_end)
                #
                #'''
                ##------------------------------#
                ##            glOrtho           #
                ##------------------------------#
                #x, y, width, height = self.get_allocation()
                #glMatrixMode(GL_PROJECTION)
                #glLoadIdentity()
                #glOrtho(self._left, 
                #        self._right,
                #        self._bottom, 
                #        self._top, 
                #        self._zNear, 
                #        self._zFar)
                #'''
                ##glFogf(GL_FOG_START,self._zNear)
                ##glFogf(GL_FOG_END,  self._zFar)
                ##gluLookAt (0.0, 0.0, 50.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
                #
                #self.queue_draw()
                ##-------------------------------------------------------------------------------


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
                scale = (modelview[3][2]*-1)
                #px  = px*(self.zFar/10)
                #py  = py*(self.zFar/10)
                px  = px*scale/10
                py  = py*scale/10
                glLoadIdentity()
                glTranslatef(px-self._dragPosX, py-self._dragPosY, pz-self._dragPosZ)
                glMultMatrixd(modelview)

                '''
                x = self._zprReferencePoint[0]
                y = self._zprReferencePoint[1]
                z = self._zprReferencePoint[2]
                
                print self._zprReferencePoint
                self._zprReferencePoint = [x - (px-self._dragPosX),  
                                           y - (py-self._dragPosY), 
                                           z - (pz-self._dragPosZ), 0.]
                print self._zprReferencePoint
                '''
                self._dragPosX = px
                self._dragPosY = py
                self._dragPosZ = pz
                changed = True
            
            if changed:
                self.queue_draw()
    
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
            #------------------------------#
            #        gluPerspective        #
            #------------------------------#
            x, y, width, height = self.get_allocation()
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            gluPerspective(self.fovy, float(width)/float(height), self.zNear,self.zFar)
            glFogf(GL_FOG_START ,  self.fog_start)
            glFogf(GL_FOG_END   ,  self.fog_end)
            
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
                    self._zNear, 
                    self._zFar)
            '''
            #glFogf(GL_FOG_START,self._zNear)
            #glFogf(GL_FOG_END,  self._zFar)
            #gluLookAt (0.0, 0.0, 50.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
            
            self.queue_draw()
    
    def _apply(self,func,*args):
        glTranslatef(*self._zprReferencePoint[0:3])
        func(*args)
        glTranslatef(*map(lambda x:-x,self._zprReferencePoint[0:3]))

    
    def _orient (self, mass_center):
        """ Function doc  - nao funciona"""
        #px, py, pz = self._pos(x,y);
        px = mass_center[0]
        py = mass_center[1]
        pz = mass_center[2] + 10

        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        print modelview
        #glLoadIdentity()
        
        #self._apply(glTranslatef,  px-self._dragPosX, py-self._dragPosY,  pz-self._dragPosZ)
        glTranslatef(px-self._dragPosX, 
                     py-self._dragPosY, 
                     pz-self._dragPosZ)
        print glGetDoublev(GL_MODELVIEW_MATRIX)
        
        self._apply(glTranslatef,  px-self._dragPosX, py-self._dragPosY,  pz-self._dragPosZ)
        print glGetDoublev(GL_MODELVIEW_MATRIX)
        self.queue_draw()
        #modelview2 = glGetDoublev(GL_MODELVIEW_MATRIX)
        #print modelview2
        #glMultMatrixd(modelview)
        #
        #self._dragPosX = px
        #self._dragPosY = py
        #self._dragPosZ = pz
        ##changed = True
        #self.queue_draw()
        
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
        
        self._mouseRotate = left  and not (middle or right)

        self._mouseZoom   = right and not (middle or left) #middle or (left and right)
        
        self._mousePan    = middle and not (right or left) #right and self.event_masked(event,gdk.SHIFT_MASK) #right and self.event_masked(event,gdk.CONTROL_MASK)
        
        self._mousePan2   = left and self.event_masked(event,gdk.CONTROL_MASK)

        test              = middle and self.event_masked(event,gdk.SHIFT_MASK)
        

        
        x = self._mouseX = event.x
        y = self._mouseY = event.y
        self._dragPosX, self._dragPosY, self._dragPosZ = self._pos(x,y)                          

        #------------------------------------------------------------------------------#
        if event.button == 1 and event.type == gtk.gdk._2BUTTON_PRESS:                 #
            nearest, hits =	self._pick(x,self.get_allocation().height-1-y,3,3,event)   #      # Double Click left button 
            self.pick(event,nearest,hits) # None if nothing hit                        #                                                                 
        #------------------------------------------------------------------------------#
        if test:
            with self.open_context():                                                            
                nearest, hits =	self._pick(x,self.get_allocation().height-1-y,3,3,event)         
                self.pick(event,nearest,hits) # None if nothing hit                              
                
        #-----------------------------------------------------------------------------------------#                                                                                          
        if self._mousePan2:                                                                       #   modificado por mim 
            with self.open_context():                                                             #
                nearest, hits =	self._pick(x,self.get_allocation().height-1-y,3,3,event)          #
                self.pick(event,nearest,hits) # None if nothing hit                               #
        #-----------------------------------------------------------------------------------------#	                                                                                      
        self.queue_draw()
       
        #------------------------------------------------------------------------------#
        if event.button == 3 and event.type == gtk.gdk._2BUTTON_PRESS:                 #
            #print event.button
            nearest, hits =	self._pick(x,self.get_allocation().height-1-y,3,3,event)   #      # Double Click left button 
            self.pick(event,nearest,hits) # None if nothing hit                        #                                                                 
        #------------------------------------------------------------------------------#
       
       
    
    def _keyPress    (self,widget,event):
        print event

    def pick(self,event,nearest,hits):
        
        for hit in hits:
            print hit.near, hit.far, hit.names

        if event.button == 1:
            if nearest != []:
                x = self.zero[nearest[0]][0]
                y = self.zero[nearest[0]][1]
                z = self.zero[nearest[0]][2]
                print x,y,z
                self._zprReferencePoint = [x,  y, z, 0.]
            else:
                print self.x_total, self.y_total, self.z_total, self.MassReferencePoint
                self.MassReferencePoint[0] = self.x_total
                self.MassReferencePoint[1] = self.y_total
                self.MassReferencePoint[2] = self.z_total
                self._zprReferencePoint = self.MassReferencePoint
        
        if event.button == 3 and nearest != []:
            px = self.zero[nearest[0]][0]
            py = self.zero[nearest[0]][1]
            pz = self.zero[nearest[0]][2]
            print px,py,pz
            px = 10.0 #self.MassReferencePoint[0]
            py = 10.0 #self.MassReferencePoint[1]
            pz = 10.0 #self.MassReferencePoint[2] + 10

            modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
            print modelview
            glLoadIdentity()
            glTranslatef(px-self._dragPosX, 
                         py-self._dragPosY, 
                         pz-self._dragPosZ)
            
            #print glGetDoublev(GL_MODELVIEW_MATRIX)
            #self._apply(glTranslatef,  px-self._dragPosX, py-self._dragPosY,  pz-self._dragPosZ)
            #print glGetDoublev(GL_MODELVIEW_MATRIX)
            self.queue_draw()
            
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
    
    def PrintCameraStatus (self, log = True):
        """ Function doc """
        if log:
            print 'zNear = ', self.zNear, 'zFar = ',   self.zFar, 'deltaZ = ', self.zNear - self.zFar, 'fog_start = ', self.fog_start, 'fog_end = ', self.fog_end, 'self.fog_end, deltaFog = ', self.fog_start - self.fog_end 
        else:
            pass 

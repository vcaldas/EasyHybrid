/*
 * MyDrawArea.cxx
 * 
 * Copyright 2017 Carlos Eduardo Sequeiros Borja <casebor@gmail.com>
 * 
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 * MA 02110-1301, USA.
 * 
 * 
 */

#include <gtk/gtk.h>
#include <gtk/gtkgl.h>

#include <GL/gl.h>
#include <GL/glu.h>
#include <GL/glut.h>

#include <iostream>
#include "MyDrawArea.h"


// Light parameters
GLfloat MyDrawArea::self_light_amb[] = {0.7,0.7,0.7,1.0};
GLfloat MyDrawArea::self_light_dif[] = {0.8,0.8,0.8,1.0};
GLfloat MyDrawArea::self_light_spe[] = {1.0,1.0,1.0,1.0};
GLfloat MyDrawArea::self_light_shi = 100.0;
// Fog parameters
GLfloat MyDrawArea::self_fog_start = 8.5;
GLfloat MyDrawArea::self_fog_end = 10.0;
GLfloat MyDrawArea::self_fog_color[] = {0,0,0};
GLfloat MyDrawArea::self_fog_density = 1.0;
// Lights positions
GLfloat MyDrawArea::self_light_0_position[] = { 1.0,  1.0, 1.0, 0.0};
GLfloat MyDrawArea::self_light_1_position[] = { 1.0, -1.0, 1.0, 0.0};
GLfloat MyDrawArea::self_light_2_position[] = {-1.0, -1.0, 1.0, 0.0};
// Background color
GLfloat MyDrawArea::self_bckgrnd_color[] = {0.0, 0.0, 0.0, 0.0};
//Camera settings
GLdouble MyDrawArea::self_fovy = 30.0;
GLdouble MyDrawArea::self_z_near = 1.0;
GLdouble MyDrawArea::self_z_far = 10.0;


MyDrawArea::MyDrawArea(){
    
    // Creates the class atributes for OpenGL
    self_drawing_area = gtk_drawing_area_new ();
    self_glconfig = gdk_gl_config_new_by_mode (static_cast<GdkGLConfigMode>(GDK_GL_MODE_RGB | GDK_GL_MODE_DEPTH | GDK_GL_MODE_DOUBLE));
    
    // Add OpenGL capability to the drawing area
    gtk_widget_set_gl_capability (self_drawing_area, self_glconfig, NULL, TRUE, GDK_GL_RGBA_TYPE);
    
    // Add the signals that will allow the draw area configure itself, 
    // catch events and so on
    g_signal_connect_after(G_OBJECT(self_drawing_area), "realize", G_CALLBACK(this->realize), NULL);
    g_signal_connect(G_OBJECT(self_drawing_area), "configure_event", G_CALLBACK(this->reshape_wind), NULL);
    g_signal_connect(G_OBJECT(self_drawing_area), "expose_event", G_CALLBACK(this->my_draw), NULL);
    
}

void MyDrawArea::realize(GtkWidget *widget, gpointer data){
    /*
     * Inside the realize function, you should put all you OpenGL
     * initialization code, e.g. set the projection matrix,
     * the modelview matrix, position of the camera.
     */
    GdkGLContext *gl_context = gtk_widget_get_gl_context (widget);
    GdkGLDrawable *gl_drawable = gtk_widget_get_gl_drawable (widget);
    
    // All OpenGL initialization code goes here
    glMaterialfv(GL_FRONT,GL_AMBIENT, self_light_amb);
    glMaterialfv(GL_FRONT,GL_DIFFUSE, self_light_dif);
    glMaterialfv(GL_FRONT,GL_SPECULAR, self_light_spe);
    glMaterialf(GL_FRONT,GL_SHININESS, self_light_shi);
    glDepthFunc(GL_LESS);
    glEnable(GL_NORMALIZE);
    glEnable(GL_COLOR_MATERIAL);
    // FOG
    glEnable(GL_FOG);
    glFogi(GL_FOG_MODE, GL_LINEAR);
    glFogf(GL_FOG_START, self_fog_start);
    glFogf(GL_FOG_END, self_fog_end);
    glFogfv(GL_FOG_COLOR, self_fog_color);
    glFogf(GL_FOG_DENSITY, self_fog_density);
    glEnable(GL_POINT_SMOOTH);
    glClearColor(self_bckgrnd_color[0], self_bckgrnd_color[1], self_bckgrnd_color[2], self_bckgrnd_color[3]);
    glClearColor(0,0,0,0);
    glShadeModel(GL_SMOOTH);
    glLightfv(GL_LIGHT0, GL_POSITION, self_light_0_position);
    glLightfv(GL_LIGHT1, GL_POSITION, self_light_1_position);
    glLightfv(GL_LIGHT2, GL_POSITION, self_light_2_position);
    glEnable(GL_LIGHT0);
    glEnable(GL_LIGHT1);
    glEnable(GL_LIGHT2);
    glEnable(GL_LIGHTING);
    glEnable(GL_DEPTH_TEST);
    // Antialiased lines
    glEnable(GL_LINE_SMOOTH);
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE);
    // Initialize view
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(self_fovy, 640.0/420.0, self_z_near, self_z_far);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    gluLookAt(0, 0, 10, 0, 0, 0, 0, 1, 0);
    
    gdk_gl_drawable_gl_end (gl_drawable);
}


gboolean MyDrawArea::reshape_wind(GtkWidget *widget, GdkEventConfigure *event, gpointer data){
    /*
     * All modifications to the ratio of visualization have to be done in this
     * function. 
     */
    GdkGLContext *gl_context = gtk_widget_get_gl_context (widget);
    GdkGLDrawable *gl_drawable = gtk_widget_get_gl_drawable (widget);
    
    if (!gdk_gl_drawable_gl_begin (gl_drawable, gl_context))
	return false;
    glViewport (0, 0, widget->allocation.width, widget->allocation.height);
    
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(self_fovy, widget->allocation.width/widget->allocation.height, self_z_near, self_z_far);
    glMatrixMode(GL_MODELVIEW);
    
    gdk_gl_drawable_gl_end (gl_drawable);
    return true;
}

gboolean MyDrawArea::my_draw(GtkWidget *widget, GdkEventExpose *event, gpointer data){
    /*
     * Function Description
     */
    GdkGLContext *gl_context = gtk_widget_get_gl_context (widget);
    GdkGLDrawable *gl_drawable = gtk_widget_get_gl_drawable (widget);
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glClearColor(0,0,0,0);
    glMatrixMode(GL_MODELVIEW);
    
    draw(widget);
    
    if (!gdk_gl_drawable_gl_begin(gl_drawable, gl_context))
	return false;
    
    if (gdk_gl_drawable_is_double_buffered (gl_drawable))
	gdk_gl_drawable_swap_buffers(gl_drawable);
    else
	glFlush ();
    
    gdk_gl_drawable_gl_end (gl_drawable);
    return true;
}

void MyDrawArea::draw(GtkWidget *widget){
    /*
     * The actual drawing goes here.
     */
    glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    
    float cube0[] = { 1, 0, 1};
    float cube1[] = {-1, 0, 1};
    float cube2[] = {-1, 1, 1};
    float cube3[] = { 1, 1, 1};
    glBegin(GL_LINE_STRIP);
    glColor3f(0.0, 1.0, 1.0); glVertex3f(cube0[0], cube0[1], cube0[2]);
    glColor3f(0.0, 1.0, 1.0); glVertex3f(cube1[0], cube1[1], cube1[2]);
    glColor3f(0.0, 1.0, 1.0); glVertex3f(cube2[0], cube2[1], cube2[2]);
    glColor3f(0.0, 1.0, 1.0); glVertex3f(cube3[0], cube3[1], cube3[2]);
    glColor3f(0.0, 1.0, 1.0); glVertex3f(cube0[0], cube0[1], cube0[2]);
    glEnd();
}



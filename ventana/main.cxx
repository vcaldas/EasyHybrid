/*
 * main.cxx
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

int main(int argc, char *argv[]){
    
    // Initialize the gtk, glut and gtkglext libraries.
    // IS VERY IMPORTANT THAT THIS LINES BE AT THE TOP OF MAIN FUNCTION!!!
    gtk_init(&argc, &argv);
    gtk_gl_init(&argc, &argv);
    gdk_gl_init_check(&argc, &argv);
    glutInit(&argc, argv);
    
    // Creating the window widget to add the drawing area
    GtkWidget *window;
    MyDrawArea prueba;
    
    window = gtk_window_new (GTK_WINDOW_TOPLEVEL);
    
    gtk_widget_set_size_request (prueba.self_drawing_area, 200, 200);
    
    gtk_container_add (GTK_CONTAINER (window), prueba.self_drawing_area);
    
    gtk_widget_show (prueba.self_drawing_area);
    gtk_widget_show (window);
    
    gtk_main ();
    
    return 0;
}

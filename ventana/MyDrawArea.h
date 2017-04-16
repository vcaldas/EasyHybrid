/*
 * MyDrawArea.h
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


#ifndef MY_DRAW_AREA_H
#define MY_DRAW_AREA_H

class MyDrawArea{
    public:
	
	MyDrawArea();
	
	GtkWidget *self_drawing_area;
	GdkGLConfig *self_glconfig;
	
	// Light parameters
	static GLfloat self_light_amb[];
	static GLfloat self_light_dif[];
	static GLfloat self_light_spe[];
	static GLfloat self_light_shi;
	// Fog parameters
	static GLfloat self_fog_start;
	static GLfloat self_fog_end;
	static GLfloat self_fog_color[];
	static GLfloat self_fog_density;
	// Lights positions
	static GLfloat self_light_0_position[];
	static GLfloat self_light_1_position[];
	static GLfloat self_light_2_position[];
	// Background color
	static GLfloat self_bckgrnd_color[];
	//Camera settings
	static GLdouble self_fovy;
	static GLdouble self_z_near;
	static GLdouble self_z_far;
	
	static void realize(GtkWidget *widget, gpointer data);
	static gboolean reshape_wind(GtkWidget *widget, GdkEventConfigure *event, gpointer data);
	static gboolean my_draw(GtkWidget *widget, GdkEventExpose *event, gpointer data);
	static void draw(GtkWidget *widget);

};

#endif

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  __main__.py
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

import sys
import pygtk
pygtk.require('2.0')
import gtk
import gl_draw_area as gda
import vis_parser

def main():
    frames = vis_parser.parse_pdb(sys.argv[1])
    wind = gtk.Window(type=gtk.WINDOW_TOPLEVEL)
    # Add title
    wind.set_title("Ventana gtk de prueba")
    # Create a GTK area with OpenGL functions
    glarea = gda.GLCanvas(data=frames[0])
    # Put the area object into the gtk window
    wind.add(glarea)
    wind.show_all()
    gtk.main()
    return 0

if __name__ == '__main__':
    main()


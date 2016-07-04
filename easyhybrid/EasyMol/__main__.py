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
from visual import gl_draw_area as gda, vis_parser

def main():
    frames = vis_parser.parse_pdb(sys.argv[1])
    glarea = gda.GLCanvas(frames)
    builder = gtk.Builder()
    builder.add_from_file('EasyMol/visual_gui/main_window.glade')
    boton = builder.get_object('btn_ball_stick')
    window = builder.get_object('main_window')
    window.set_size_request(800,600)
    window.connect('key_press_event', glarea.key_press)
    vbox = builder.get_object('vbox_main')
    vbox.pack_end(glarea, True, True)
    window.show_all()
    gtk.main()
    return 0

if __name__ == '__main__':
    main()


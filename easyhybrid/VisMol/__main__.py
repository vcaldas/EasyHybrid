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

import gi, sys
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from visual import vismol, vis_parser, vismol_shaders as vm_sh

def main():
    
    frames = vis_parser.parse_pdb(sys.argv[1])
    
    #vism = vismol.MyGLProgram(frames, vm_sh.vertex_shader_point_light, vm_sh.fragment_shader_point_light)
    vism = vismol.MyGLProgram(frames, vm_sh.vertex_shader4, vm_sh.fragment_shader4)
    wind = Gtk.Window()
    wind.add(vism)
    
    wind.connect("delete-event", Gtk.main_quit)
    wind.connect("key-press-event", vism.key_press)
    
    wind.show_all()
    Gtk.main()
    
    return 0

if __name__ == '__main__':
    main()


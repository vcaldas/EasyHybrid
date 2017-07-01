#!/usr/bin/env python3
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

#from visual import vismol
#from visual import vis_parser
#from visual import vismol_shaders as vm_sh

from VISMOL  import vismol_core
from GTKGUI  import gtkgui
#from easymol import * 
#from EasyMol import vis_parser

def main():
    
    #frames = vis_parser.parse_pdb(sys.argv[1])
    
    vismolSession  =  vismol_core.VisMolSession(glwidget = True, backend = 'gtk3')

    #vism = vismol.MyGLProgram(frames, vm_sh.vertex_shader_point_light, vm_sh.fragment_shader_point_light)
    #vism  = vismol.MyGLProgram(frames)
    #vism =  None
    gui   = gtkgui.GTKGUI(vismolSession)
    return 0

if __name__ == '__main__':
    main()


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

#import sys
#import pygtk
#pygtk.require('2.0')
#import gtk
#from visual import gl_draw_area as gda, vis_parser
##from visual_gui import FileChooserWindow
#from visual.vis_parser import parse_pdb

from visual.gtkgui import GTKGUI
from visual.easyMolObj import EasyMolSession





def main():
    
    EasyMol = EasyMolSession()
    gtkgui  = GTKGUI(EasyMol)


if __name__ == '__main__':
    main()


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
import molecular_model as mm
import pygtk
pygtk.require('2.0')
import gtk
import gl_draw_area as gda
from OpenGL.GLUT import glutInit
import representations as rep
import numpy as np

def main():
    with open(sys.argv[1], 'r') as pdb_file:
	pdb = list(pdb_file)
    chains_m = {}
    frames = mm.Frame()
    for lin in pdb:
	if lin[:4] == 'ATOM' or lin[:6] == 'HETATM':
	    at_name = lin[12:16].strip()
	    at_index = int(lin[6:11])
	    at_pos = np.array([float(lin[30:38]), float(lin[38:46]), float(lin[46:54])])
	    at_res_i = int(lin[22:26])
	    at_res_n = lin[17:20].strip()
	    at_ch = lin[22]
	    atm = mm.Atom(name=at_name, index=at_index, pos=at_pos, residue=at_res_i)
	    atm.sphere = True
	    atm.vdw = True
	    if at_ch == ' ':
		at_ch = 'A'
	    if chains_m.has_key(at_ch):
		ch = chains_m[at_ch]
	    else:
		ch = mm.Chain(name=at_ch, frame=frames)
		chains_m[at_ch] = ch
	    if ch.residues.has_key(at_res_i):
		res = ch.residues[at_res_i]
	    else:
		res = mm.Residue(name=at_res_n, index=at_res_i, chain=at_ch)
		ch.residues[at_res_i] = res
	    if not res.atoms.has_key(at_index):
		res.atoms[at_index] = atm
    frames.chains = chains_m
    #for rs in frames.chains['A'].residues.values():
	#for at in rs.atoms.values():
	#    print at.index, '<-- atom index ', at.name, '<-- atom name'
	#print '<------------------------------------------------------>'
    #
    # Create a new window
    wind = gtk.Window(type=gtk.WINDOW_TOPLEVEL)
    # Add title
    wind.set_title("Ventana gtk de prueba")
    # Create a GTK area with OpenGL functions
    glutInit(sys.argv)
    #wind.connect("destroy",lambda event: gtk.main_quit())
    glarea = gda.GLCanvas(data=frames)
    #glarea
    # Put the area object into the gtk window
    wind.add(glarea)
    # Draw the molecule
    #glarea._init(glarea)
    #glarea.realize()
    # Show all the elements
    #glarea.draw = rep.draw_mol
    glarea.load_mol()
    glarea.draw()
    wind.show_all()
    #glarea.draw_mol()
    gtk.main()
    return 0

if __name__ == '__main__':
    main()


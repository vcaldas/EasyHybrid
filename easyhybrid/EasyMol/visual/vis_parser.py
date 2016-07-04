#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  vis_parser.py
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

import molecular_model as mm
import numpy as np

def parse_pdb(infile):
    """
    """
    frames = []
    with open(infile, 'r') as pdb_file:
	frame = mm.Frame()
	chains_m = {}
	frame.chains = chains_m
	atoms = []
	for line in pdb_file:
	    if line[:4] == 'ATOM' or line[:6] == 'HETATM':
		at_name = line[12:16].strip()
		at_index = int(line[6:11])
		at_pos = np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])])
		at_res_i = int(line[22:26])
		at_res_n = line[17:20].strip()
		at_ch = line[22]
		atm = mm.Atom(name=at_name, index=at_index, pos=at_pos, residue=at_res_i)
		atm.sphere     = True
		atm.ball       = True
		atm.vdw        = True
		atm.pretty_vdw = True
		atm.dot        = True
		atm.wires      = True
		if at_ch == ' ':
		    at_ch = 'A'
		if chains_m.has_key(at_ch):
		    ch = chains_m[at_ch]
		else:
		    ch = mm.Chain(name=at_ch, frame=frame)
		    chains_m[at_ch] = ch
		if ch.residues.has_key(at_res_i):
		    res = ch.residues[at_res_i]
		else:
		    res = mm.Residue(name=at_res_n, index=at_res_i, chain=at_ch)
		    ch.residues[at_res_i] = res
		if atm.name == 'CA':
		    ch.backbone.append(atm)
		if not res.atoms.has_key(at_index):
		    res.atoms[at_index] = atm
		atoms.append(atm)
	    elif line[:6] == 'ENDMDL':
		frame.chains = chains_m
		frame.atoms = atoms
		frame.load_bonds()
		frame.load_ribbons()
		frames.append(frame)
		frame = mm.Frame()
		chains_m = {}
		atoms = []
	#if len(frame.chains.values()) > 0:
	    #frame.atoms = atoms
	    #frame.load_bonds()
	    #frame.load_ribbons()
	    #frames.append(frame)
    return frames

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

import GLarea.molecular_model as mm
import os
import numpy as np
#import atom_types as atypes
from pprint import pprint
import random

def parse_xyz(infile = None, counter = 0, atom_dic_id = None, Vobject_id = None ):
    """ Function doc """
    #frames = []
    
    with open(infile, 'r') as xyz_file:        
        label = os.path.basename(infile)

        xyz_lines = xyz_file.readlines()
        total_size      = len(xyz_lines)    
        xyz_model_size  = int(xyz_lines[0])
        model_size      = xyz_model_size+2   # include first and secound lines in a xyzfile
        
        models     = []
        for i in range(0, int(total_size/model_size)): 
            #print (i*model_size) , (i+1)*model_size
            model = xyz_lines[(i*model_size) : (i+1)*model_size]
            models.append(model)

        pprint (models[-1][2:])
        
        Vobject  = mm.Vobject()
        Vobject.label  = label.split('.')
        Vobject.label  = Vobject.label[0]
        chains_m = {}
        residues = {}
        atoms    = []
        
        index = 1
        sum_x = 0
        sum_y = 0
        sum_z = 0  
        
        
        frame = []
        for line in models[0][2:]:
            line2 = line.split()
            #print line2, [float(line[1]), float(line[2]), float(line[3])]
            at_name  = line2[0].strip()
            at_pos   = np.array([float(line2[1]), float(line2[2]), float(line2[3])])
            at_res_i = 1
            at_res_n = 'UNK'
            at_ch    = 'A'
            
            #print at_name, '<--------'
            atm = mm.Atom(name       =  at_name, 
                          index      =  index, 
                          pos        =  at_pos, 
                          resi       =  at_res_i, 
                          resn       =  at_res_n, 
                          chain      =  at_ch, 
                          atom_id    =  counter, 
                          Vobject_id =  Vobject_id,
                          Vobject_name =  Vobject.label)


            if atom_dic_id is not None:
                atom_dic_id[counter] = atm
            
            counter += 1
            index   += 1
        
            coords = []
            
            if at_ch in chains_m.keys():
                ch = chains_m[at_ch]
            else:
                ch = mm.Chain(name=at_ch, label = 'UNK')
                chains_m[at_ch] = ch

            if at_res_i in ch.residues.keys():
                res = ch.residues[at_res_i]
                ch.residues[at_res_i].atoms.append(atm)
                Vobject.atoms.append(atm)
                frame.append([atm.pos[0],atm.pos[1],atm.pos[2]])

            else:
                res = mm.Residue(name=at_res_n, index=at_res_i, chain=at_ch)
                ch.residues[at_res_i] = res
                ch.residues[at_res_i].atoms.append(atm)
                Vobject.atoms.append(atm)
                frame.append([atm.pos[0],atm.pos[1],atm.pos[2]])

            sum_x += atm.pos[0]
            sum_y += atm.pos[1]
            sum_z += atm.pos[2]
        
        # add a new frame to frames list
        Vobject.frames.append(frame)
        Vobject.chains = chains_m
        total = len(Vobject.atoms)
        
        Vobject.list_atom_lines          = [True] *total
        Vobject.list_atom_ribbons        = [False]*total
        Vobject.list_atom_dots           = [False]*total
        Vobject.list_atom_sticks         = [False]*total
        Vobject.list_atom_spheres        = [False]*total
        Vobject.list_atom_surface        = [False]*total
        Vobject.list_atom_ball_and_stick = [False]*total
        
        
        Vobject.mass_center[0] = sum_x / total
        Vobject.mass_center[1] = sum_y / total
        Vobject.mass_center[2] = sum_z / total
        
        n = 1
        for model_i  in models[1:]:
            frame = []
            for line in model_i[2:]:
                line2 = line.split()
                #print line2, [float(line[1]), float(line[2]), float(line[3])]
                #at_name  = line2[0].strip()
                #at_pos   = np.array([float(line2[1]), float(line2[2]), float(line2[3])])
                frame.append([float(line2[1]), float(line2[2]), float(line2[3])])
            
            #pprint (n) 
            #pprint (frame)
            Vobject.frames.append(frame)
            n += 1
        #print atom_dic_id
        return Vobject, atom_dic_id


def parse_pdb(infile = None, counter = 0, atom_dic_id = None, Vobject_id = None ):
    """ Function doc """
    #frames = []
    with open(infile, 'r') as pdb_file:
        label = os.path.basename(infile)

        
        Vobject = mm.Vobject()
        
        Vobject.label  = label.split('.')
        Vobject.label  = Vobject.label[0]
                
        chains_m = {}
        residues = {}
        atoms    = []
        
        index = 1
        
        sum_x = 0
        sum_y = 0
        sum_z = 0
        frame = []
        for line in pdb_file:
            if line[:4] == 'ATOM' or line[:6] == 'HETATM':
                at_name = line[12:16].strip()
                #at_index = int(line[6:11])
                at_pos = np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])])
                at_res_i = int(line[22:26])
                at_res_n = line[17:20].strip()
                at_ch = line[21]
                
                atm = mm.Atom(name         =  at_name, 
                              index        =  index, 
                              pos          =  at_pos, 
                              resi         =  at_res_i, 
                              resn         =  at_res_n, 
                              chain        =  at_ch, 
                              atom_id      =  counter, 
                              Vobject_id   =  Vobject_id,
                              Vobject_name =  Vobject.label )
                
                if atom_dic_id is not None:
                    atom_dic_id[counter] = atm
                
                counter += 1
                index += 1
                
                if at_ch in chains_m.keys():
                    ch = chains_m[at_ch]
                    #print 'existe'
                else:
                    ch = mm.Chain(name=at_ch, label = 'UNK')
                    chains_m[at_ch] = ch
                    #print 'n existe'

                if at_res_i in ch.residues.keys():
                    res = ch.residues[at_res_i]
                    #print 'existe'
                    ch.residues[at_res_i].atoms.append(atm)
                    Vobject.atoms.append(atm)
                    frame.append([atm.pos[0],atm.pos[1],atm.pos[2]])


                else:
                    #print at_res_n, at_res_i, at_ch
                    res = mm.Residue(name=at_res_n, index=at_res_i, chain=at_ch)
                    ch.residues[at_res_i] = res
                    ch.residues[at_res_i].atoms.append(atm)
                    Vobject.atoms.append(atm)
                    frame.append([atm.pos[0],atm.pos[1],atm.pos[2]])

                
                if atm.name == 'CA':
                    ch.backbone.append(atm)
                    #ch.backbone.append(atm.pos[0])
                    #ch.backbone.append(atm.pos[1])
                    #ch.backbone.append(atm.pos[2])
                
                sum_x += atm.pos[0]
                sum_y += atm.pos[1]
                sum_z += atm.pos[2]
                    
                    
                #res.atoms[at_index] = atm
                
                #if not res.atoms.has_key(at_index):
                #    res.atoms[at_index] = atm
                #    atoms.append(atm)
                
                #elif line[:6] == 'ENDMDL':
                #
                #    Vobject.chains = chains_m
                #    #frame.atoms = atoms
                #    #frame.load_bonds()
                #    #frame.load_ribbons()
                #    #frames.append(frame)
                #    #frame = mm.Frame()
                #    #chains_m = {}
                #    #atoms = []
                ##print atoms
        
        # add a new frame to frames list
        Vobject.frames.append(frame)
        Vobject.chains = chains_m
        
        total = len(Vobject.atoms)
        Vobject.list_atom_lines          = [True] *total
        Vobject.list_atom_ribbons        = [False]*total
        Vobject.list_atom_dots           = [False]*total
        Vobject.list_atom_sticks         = [False]*total
        Vobject.list_atom_spheres        = [False]*total
        Vobject.list_atom_surface        = [False]*total
        Vobject.list_atom_ball_and_stick = [False]*total

        
        Vobject.mass_center[0] = sum_x / total
        Vobject.mass_center[1] = sum_y / total
        Vobject.mass_center[2] = sum_z / total
        #print Vobject.mass_center
        return Vobject, atom_dic_id


def parse_pdb2(infile = None, counter = 0, atom_dic_id = None, Vobject_id = None ):
    """ Function doc """
    import time
    
    print (infile)
    initial = time.time()
    with open(infile, 'r') as pdb_file:
        label = os.path.basename(infile)
        pdb_file = pdb_file.readlines()
        print (len(pdb_file))
        
        new_lines = []
        coords     = []
        
        for line in pdb_file:
            if line[:4] == 'ATOM' or line[:6] == 'HETATM':
                at_name = line[12:16].strip()
                #at_index = int(line[6:11])
                
                coords.append(float(line[30:38]))
                coords.append(float(line[38:46])) 
                coords.append(float(line[46:54]))
                
                #at_pos = np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])])
                at_res_i = int(line[22:26])
                at_res_n = line[17:20].strip()
                at_ch    = line[21]
                
                
                new_lines.append([at_name,at_res_i,at_res_n, at_ch])
       
        #print  round(min(coords[::3]) ), round(max(coords[::3]) ) , round(max(coords[::3]) )- round(min(coords[::3]) ),  (round(max(coords[::3]) )- round(min(coords[::3]) ))/10
        #print  round(min(coords[1::3])), round(max(coords[1::3])) , round(max(coords[1::3]))- round(min(coords[1::3])),  (round(max(coords[1::3]))- round(min(coords[1::3])))/10
        #print  round(min(coords[2::3])), round(max(coords[2::3])) , round(max(coords[2::3]))- round(min(coords[2::3])),  (round(max(coords[2::3]))- round(min(coords[2::3])))/10
        
        x_coords = coords[ ::3]
        y_coords = coords[1::3]
        z_coords = coords[2::3]
        
        x_max  =  round(max(x_coords)) 
        y_max  =  round(max(y_coords)) 
        z_max  =  round(max(z_coords)) 
        
        x_min  =  round(min(x_coords)) 
        y_min  =  round(min(y_coords)) 
        z_min  =  round(min(z_coords)) 
    
        sector_size = 10

        x_sector = []
        y_sector = []
        z_sector = []

        for x in  x_coords:
            x_sector.append(int(round(x/sector_size)))
        
        for y in  y_coords:
            y_sector.append(int(round(y/sector_size)))
        
        for z in  z_coords:
            z_sector.append(int(round(z/sector_size)))
        
        x_sector_min = min(x_sector)
        y_sector_min = min(y_sector)
        z_sector_min = min(z_sector)
        
        #if x_sector_min < 0:
        #    map(lambda(n): n + x_sector_min, x_sector)
        #
        #if y_sector_min < 0:
        #    map(lambda(n): n + y_sector_min, y_sector)
        #
        #if z_sector_min < 0:
        #    map(lambda(n): n + z_sector_min, z_sector)
                          
        print (min(x_sector), max(x_sector))
        print (min(y_sector), max(y_sector))
        print (min(z_sector), max(z_sector))
        
      

    print (time.time() - initial)


def soma_int (x):
    
    """ Function doc """
    


#parse_xyz(infile = '/home/fernando/programs/EasyHybrid/pdbs/1gab.xyz')


#sys = parse_pdb2('/home/fernando/Desktop/step5_assembly.pdb')
#
#sys = parse_pdb('/home/fernando/programs/EasyHybrid/pdbs/1bx4.pdb')

'''

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
		at_ch = line[21]
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
	if len(frame.chains.values())>0 and len(frames)==0:
	    frame.atoms = atoms
	    frame.load_bonds()
	    frame.load_ribbons()
	    frames.append(frame)
    return frames
'''

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  molecular_model.py
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
from visual import gl_draw_area as gda, vis_parser
from visual.vis_parser import parse_pdb





class EasyMolSession:
    """ Class doc """

    def load (self, infile):
        """ Function doc """
        
        Vobject, self.atom_dic_id = parse_pdb(infile     = infile,  
                                             counter     = self.atom_id_counter,  
                                             atom_dic_id = self.atom_dic_id
                                             )
        
        Vobject.generate_bonds()
        self.atom_id_counter += len(Vobject.atoms)
        self.Vobjects.append(Vobject)
        #print self.atom_dic_id
        #print self.atom_id_counter
    
    def delete(self, obj = None):
        """ Function doc """
    
    def select (self, obj =  None):
        """ Function doc """

    def orient (self, obj =  None):
        """ Function doc """  

    def center (self, obj =  None):
        """ Function doc """  
    
    def hide (self, _type = 'lines', obj =  None):
        """ Function doc """    
    
    def show (self, _type = 'lines', obj =  None):
        """ Function doc """
    
    def disable (self, index):
        """ Function doc """
        #print type(index)
        self.Vobjects[index].actived = False
        self.glarea.draw()
        
    def enable (self, index):
        """ Function doc """
        self.Vobjects[index].actived = True
        self.glarea.draw()
        
    def __init__ (self):
        """ Class initialiser """
        #frames = vis_parser.parse_pdb(sys.argv[1])
        self.Vobjects         = []
        
        self.atom_id_counter  = 0
        self.atom_dic_id      = {
                                # atom_id : obj_atom 
                                 }
        
        self.glarea            = gda.GLCanvas(self) # a gl area recebe 
        
        
        self.glarea_parameters = {
                                 'line_width'   : 1      ,
                                 'sphere_scale' : 1      ,
                                 'antialias'    : False  ,
                                 'bg_color'     : 'black',
                                 }

        
        
        
        #self.builder = self.init_gtk(self.glarea)
        #self.builder.connect_signals(self)                                                #

       

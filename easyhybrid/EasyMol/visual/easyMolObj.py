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
from visual.vis_parser import parse_pdb, parse_xyz





class EasyMolSession:
    """ Class doc """

    def load (self, infile):
        """ Function doc """
        Vobject_id = len(self.Vobjects)
        
	
	if infile[-3:] == 'pdb':
	    Vobject, self.atom_dic_id = parse_pdb(infile     = infile,  
						 counter     = self.atom_id_counter,  
						 atom_dic_id = self.atom_dic_id,
						 Vobject_id  = Vobject_id
						 )
        
	if infile[-3:] == 'xyz':

	    Vobject, self.atom_dic_id = parse_xyz(infile     = infile,  
						 counter     = self.atom_id_counter,  
						 atom_dic_id = self.atom_dic_id,
						 Vobject_id  = Vobject_id
						 )
	
	print 'number of frames: ',len(Vobject.frames) , '<---------------'
	for frame in Vobject.frames:
	    print 'framesize:', len(frame)
	
        Vobject.generate_bonds()
        self.atom_id_counter += len(Vobject.atoms)
        self.Vobjects.append(Vobject)
        
	#print self.atom_dic_id
        #print self.atom_id_counter
    
    def _hide_ribbons (self, Vobject_index ):
        """ Function doc """
        self.Vobjects[Vobject_index].show_ribbons = False
        self.glarea.draw_ribbon(self.Vobjects[Vobject_index])
        self.glarea.draw()
    
    def _show_ribbons (self, Vobject_index ):
        """ Function doc """
        self.Vobjects[Vobject_index].show_ribbons = True
        self.glarea.draw_ribbon(self.Vobjects[Vobject_index])
        self.glarea.draw()
        
    def _hide_lines (self, Vobject_index ):
        """ Function doc """
        self.Vobjects[Vobject_index].show_lines = False
        self.glarea.draw_lines(self.Vobjects[Vobject_index])
        self.glarea.draw()
	#print 'aqui'

    def _show_lines (self, Vobject_index ):
        """ Function doc """
        self.Vobjects[Vobject_index].show_lines = True
        self.glarea.draw_lines(self.Vobjects[Vobject_index])
        self.glarea.draw()
	#print 'aqui'
    
    def hide (self, _type = 'lines', Vobject_index =  None):
        """ Function doc """    
        if _type == 'lines':
            self._hide_lines (Vobject_index )
	    #print 'aqui'

        if _type == 'ribbons':
            self._hide_ribbons (Vobject_index )
        
    def show (self, _type = 'lines', Vobject_index =  None):
        """ Function doc """
        if _type == 'lines':
            self._show_lines (Vobject_index )
	    #print 'aqui'
        if _type == 'ribbons':
            self._show_ribbons (Vobject_index )
        

    def delete(self, obj = None):
        """ Function doc """
    
    def select (self, obj =  None):
        """ Function doc """

    def orient (self, obj =  None):
        """ Function doc """  

    def center (self, Vobject_index =  None):
        """ Function doc """  
	mass_center = self.Vobjects[Vobject_index].mass_center
	self.glarea.center_on_atom(mass_center)
        
        
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
        self.Vobjects_dic     = {}        

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



       

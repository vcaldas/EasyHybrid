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
#from visual import gl_draw_area as gda, vis_parser
from GLarea.vis_parser import parse_pdb, parse_xyz
from pprint import pprint




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
        
        print ('number of frames: ',len(Vobject.frames) , '<---------------')
        
        for frame in Vobject.frames:
            print ('framesize:', len(frame))
	
        Vobject.generate_bonds()
        
        self.atom_id_counter += len(Vobject.atoms)
        self.Vobjects.append(Vobject)
        
        pprint(self.Vobjects)
        self.glwidget.draw_lines(self.Vobjects[-1])
        
        return True
        
    
    def _hide_ribbons (self, Vobject_index ):
        """ Function doc """
        self.Vobjects[Vobject_index].show_ribbons = False
        self.glwidget.draw_ribbon(self.Vobjects[Vobject_index])
        self.glwidget.draw()
    
    def _show_ribbons (self, Vobject_index ):
        """ Function doc """
        self.Vobjects[Vobject_index].show_ribbons = True
        self.glwidget.draw_ribbon(self.Vobjects[Vobject_index])
        self.glwidget.draw()
        
    def _hide_lines (self, Vobject_index ):
        """ Function doc """
        self.Vobjects[Vobject_index].show_lines = False
        self.glwidget.draw_lines(self.Vobjects[Vobject_index])

    def _show_lines (self, Vobject_index ):
        """ Function doc """
        self.Vobjects[Vobject_index].show_lines = True
        self.glwidget.draw_lines(self.Vobjects[Vobject_index])
    
    def hide (self, _type = 'lines', Vobject_index =  None):
        """ Function doc """    
        if _type == 'lines':
            self._hide_lines (Vobject_index )
	    #print 'aqui'

        if _type == 'ribbons':
            self._hide_ribbons (Vobject_index )
        self.glwidget.queue_draw()

    def show (self, _type = 'lines', Vobject_index =  None):
        """ Function doc """
        if _type == 'lines':
            self._show_lines (Vobject_index )
	    #print 'aqui'
        if _type == 'ribbons':
            self._show_ribbons (Vobject_index )
        self.glwidget.queue_draw()

    def delete(self, obj = None):
        """ Function doc """
    
    def select (self, obj =  None):
        """ Function doc """

    def orient (self, obj =  None):
        """ Function doc """  

    def center (self, Vobject_index =  None):
        """ Function doc """  
        mass_center = self.Vobjects[Vobject_index].mass_center
        self.glwidget.center_on_atom(mass_center)
        
    def disable (self, index):
        """ Function doc """
        #print type(index)
        self.Vobjects[index].actived = False
        self.glwidget.draw()
        
    def enable (self, index):
        """ Function doc """
        self.Vobjects[index].actived = True
        self.glwidget.draw()
        
    def set_frame (self, frame = 0):
        """ Function doc """
        self.glwidget.frame = frame
        self.glwidget.queue_draw()
    
    def get_frame (self):
        """ Function doc """
        """ Function doc """
        frame = self.glwidget.frame
        return frame
        
    def get_vobject_list (self):
        """ Function doc """
        Vobjects_dic = {}
	
        for Vobject in self.Vobjects:
            index = self.Vobjects.index(Vobject)
            label = Vobject.label
            Vobjects_dic[index] = label
	
        return Vobjects_dic
	
    def __init__ (self, glwidget):
        """ Class initialiser """
        self.Vobjects         = []
        self.Vobjects_dic     = {}        
        self.atom_id_counter  = 0
        self.atom_dic_id      = {
                                # atom_id : obj_atom 
                                 }
        


        self.glwidget            = glwidget # a gl area recebe 
        
        self.glwidget.EMSession = self
        
        self.glwidget_parameters = {
                                 'line_width'   : 1      ,
                                 'sphere_scale' : 1      ,
                                 'antialias'    : False  ,
                                 'bg_color'     : 'black',
                                 }



       

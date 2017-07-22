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

#from   GLarea.vis_parser import load_pdb_files, parse_xyz
#import GLarea.molecular_model as mm

#from vis_parser import load_pdb_files

#from pprint import pprint
#from GLarea.GLWidget   import GLWidget
from VISMOL.vModel import VismolObject
from VISMOL.vBabel import PDBFiles
from VISMOL.vCore.VismolSelections  import VisMolPickingSelection as vPick
from VISMOL.vCore.VismolSelections  import VisMolViewingSelection as vSele

import VISMOL.glCore.shapes as shapes



import os

class ShowHideVisMol:
    """ Class doc """
    
    def __init__ (self):
        """ Class initialiser """
        pass
    
    def _hide_dots (self, Vobjects ):
        for Vobject in Vobjects:
            Vobject.flat_sphere_representation.actived = False
            #self.flat_sphere_representation.update()

    def _show_dots (self, Vobjects = []):
        """ Function doc """
        for Vobject in Vobjects:
            Vobject.flat_sphere_representation.actived = True
            Vobject.flat_sphere_representation.update()
            
            #self.glwidget.draw_dots(Vobject)

    #def _hide_flat_spheres (self, Vobjects ):
    #    for Vobject in Vobjects:
    #        Vobject.show_dots = False
    #
    #def _show_flat_spheres (self, Vobjects = []):
    #    """ Function doc """
    #    for Vobject in Vobjects:
    #        Vobject.show_dots = True
    #        #self.glwidget.draw_dots(Vobject)

    def _hide_ribbons (self, Vobjects ):
        """ Function doc """
        for Vobject in Vobjects:
            pass
            #self.flat_sphere_representation.actived = False
            #self.flat_sphere_representation.update()
    
    def _show_ribbons (self, Vobjects ):
        """ Function doc """
        for Vobject in Vobjects:
            Vobject.show_ribbons = True
            #self.glwidget.draw_ribbon(Vobject)
        
    def _hide_lines (self, Vobjects ):
        """ Function doc """
        for Vobject in Vobjects:
            #Vobject.show_lines = False
            Vobject.line_representation.actived = False

    def _show_lines (self, Vobjects ):
        """ Function doc """
        for Vobject in Vobjects:
            #Vobject.show_lines = True
            Vobject.line_representation.actived = True
            Vobject.line_representation.update()

    def _hide_ball_and_stick (self, Vobjects ):
        """ Function doc """
        for Vobject in Vobjects:
            Vobject.show_ball_and_stick = False
        
    def _show_ball_and_stick(self, Vobjects):
        """ Function doc """
        for Vobject in Vobjects:
            Vobject.show_ball_and_stick = True
            #self.glwidget.draw_ball_and_stick(Vobject)
    
    def _hide_spheres (self, Vobjects ):
        """ Function doc """
        for Vobject in Vobjects:
            Vobject.show_spheres = False
        
    def _show_spheres (self, Vobjects):
        """ Function doc """
        for Vobject in Vobjects:
            Vobject.show_spheres = True
            #self.glwidget.draw_spheres(Vobject)
    
    def hide (self, _type = 'lines', Vobjects =  []):
        """ Function doc """    
        if _type == 'dots':
            self._hide_dots (Vobjects )

        if _type == 'lines':
            self._hide_lines (Vobjects )

        if _type == 'ribbons':
            self._hide_ribbons (Vobjects )
        
        if _type == 'ball_and_stick':
            self._hide_ball_and_stick(Vobjects )
        
        if _type == 'spheres':
            self._hide_spheres (Vobjects )            
        
        self.glwidget.updateGL()

    def show (self, _type = 'lines', Vobjects =  []):
        """ Function doc """
        if _type == 'dots':
            self._show_dots (Vobjects )

        if _type == 'lines':
            self._show_lines (Vobjects )

        if _type == 'ribbons':
            self._show_ribbons (Vobjects )
        
        if _type == 'ball_and_stick':
            self._show_ball_and_stick(Vobjects)
        
        if _type == 'spheres':
            self._show_spheres(Vobjects ) 
    
        self.glwidget.updateGL()



class VisMolSession (ShowHideVisMol):
    """ Class doc """

    def __init__ (self, glwidget = False, backend = 'gtk3'):
        """ Class initialiser """
        #self.vismol_objects         = [] # self.vismol_objects
        #self.vismol_objects_dic     = {} # self.vismol_objects_dic   
        
        self.vismol_objects     = [] # old Vobjects
        self.vismol_objects_dic = {}
        
        self.atom_id_counter  = 0  # 
        self.atom_dic_id      = {
                                # atom_id : obj_atom 
                                 }
        

        #---------------------------------------------------------------------------
        # gl stuffs
        #---------------------------------------------------------------------------
        self.gl_parameters      =     {
                                      
                                      'dot_size'                   : 5      ,
                                      'line_width'                 : 3      ,
                                      'sphere_scale'               : 0.85    ,
                                      'stick_scale'                : 1.5    ,
                                      'ball_and_sick_sphere_scale' : 1      ,
                                      'antialias'                  : False  ,
                                      'bg_color'                   : [0,0,0,1],
                                      }
        
        

        if glwidget:
            if backend == 'gtk3':
                from VISMOL.glWidget import gtk3 as VisMolGLWidget
                self.glwidget   = VisMolGLWidget.GtkGLWidget (self)
            
            if backend == 'qt4':
                self.glwidget   = VisMolGLWidget.QtGLWidget (self)
        else:
            self.glwidget = None
        #---------------------------------------------------------------------------
        
        
        
        
        
        self._picking_selection_mode = False # True/False  - interchange between viewing  and picking mode
        #---------------------------------------------------------------
        #  VIEWING SELECTIONS
        #---------------------------------------------------------------
        selection = vSele()
        self.selections = {
                          'sel01' : selection
                          }
        self.current_selection = 'sel01'
        
        #---------------------------------------------------------------
        #  PICKING SELECTIONS
        #---------------------------------------------------------------
        self.picking_selections =  vPick()
        


    def load (self, infile):
        """ Function doc """
        #Vobject_id = len(self.vismol_objects)

        
        if infile[-3:] == 'pdb':
            self._load_pdb_file(infile = infile)
            
        #if infile[-3:] == 'xyz':
        #
        #    Vobject, self.atom_dic_id = parse_xyz(infile     = infile,  
        #                     counter     = self.atom_id_counter,  
        #                     atom_dic_id = self.atom_dic_id,
        #                     Vobject_id  = Vobject_id
        #                     )
        
        #self.atom_id_counter += len(Vobject.atoms)
        
        
        #if self.glwidget:
        #    print ('starting _make_gl_lines') 
        #    shapes._make_gl_lines(self.glwidget.lines_program, vismol_object = self.vismol_objects[-1])
        #    print ('_make_gl_lines finished') 
        #    self.glwidget.make_lines(vismol_object = self.vismol_objects[-1])
        self.vismol_objects[-1].actived = True
        self.glwidget.queue_draw()
        #self.center_by_index (index =  -1)
        return True
        
    def _load_pdb_file (self, infile):
        """ Function doc """
        print(infile)
        atoms, frames  = PDBFiles.load_pdb_files (infile = infile)
        name = os.path.basename(infile)
        vismol_object  = VismolObject.VismolObject(name        = name, 
                                                   atoms       = atoms, 
                                                   EMSession   = self, 
                                                   trajectory  = frames)
			      
        self.vismol_objects.append(vismol_object)
        
    def delete_by_index(self, index = None):
        """ Function doc """
        self.viewing_selections = []
        self.picking_selections = [None]*4        
        self.vismol_objects.pop(index)
        #self.glwidget.updateGL()
        
    def select (self, obj =  None):
        """ Function doc """

    def orient (self, obj =  None):
        """ Function doc """  

    def center_by_index(self, Vobject =  None, index = None):
        """ Function doc """  
        mass_center = self.vismol_objects[index].mass_center
        #self.glwidget.center_on_atom(mass_center)

    def disable_by_index (self, index = 0):
        self.vismol_objects[index].actived = False
        #self.glwidget.draw()
        self.glwidget.queue_draw()
            
    def enable_by_index (self, index = 0):
        """ Function doc """
        self.vismol_objects[index].actived = True
        #self.glwidget.draw()
        self.glwidget.queue_draw()
        
    def set_frame (self, frame = 0):
        """ Function doc """
        self.glwidget.frame = frame
        self.glwidget.queue_draw()

        #self.glwidget.updateGL()
    
    def get_frame (self):
        """ Function doc """
        #""" Function doc """
        frame = self.glwidget.frame
        return frame
        
    def get_vobject_list (self):
        """ Function doc """
        Vobjects_dic = {}
	
        for Vobject in self.vismol_objects:
            #print ('----------------------- > get_vobject_list ', Vobject.label)
            index = self.vismol_objects.index(Vobject)
            name = Vobject.label
            #print( '\n label get_vobject_list:', name, index, len(Vobject.atoms) )
            Vobjects_dic[index] = name
	
        return Vobjects_dic

    def selection_mode(self, selmode = 'atom'):
        """ Function doc """        
        self.selections[self.current_selection]._selection_mode = selmode
    
    def selection_function (self, pickedID):
        """ Function doc """
        if pickedID is None:
            selected = None
        else:
            selected = self.atom_dic_id[pickedID]
        
        #"""     P I C K I N G     S E L E C T I O N S     """
        if self._picking_selection_mode:
            self.picking_selections.selection_function_picking(selected)
        
        else:
            self.selections[self.current_selection].selection_function_viewing(selected)

       

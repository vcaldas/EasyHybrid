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
from GLarea.GLWidget   import GLWidget




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
        #self.glwidget.draw_dots(self.Vobjects[-1])
        #Vobject.show_dots = False
        self.center (Vobject_index =  -1)
        for atom in self.Vobjects[-1].atoms:
            print (atom.index-1, atom.name, atom.connected)
        
        return True
        

    def _hide_dots (self, Vobject_index ):
        """ Function doc """
        self.Vobjects[Vobject_index].show_dots = False
        #self.glwidget.draw_dots(self.Vobjects[Vobject_index])

    def _show_dots (self, Vobject_index = None, selection = False ):
        """ Function doc """
        
        self.Vobjects[Vobject_index].show_dots = True
        self.glwidget.draw_dots(Vobject = self.Vobjects[Vobject_index], selection = True)

    def _hide_ribbons (self, Vobject_index ):
        """ Function doc """
        self.Vobjects[Vobject_index].show_ribbons = False
        #self.glwidget.draw_ribbon(self.Vobjects[Vobject_index])
        #self.glwidget.draw()
    
    def _show_ribbons (self, Vobject_index ):
        """ Function doc """
        self.Vobjects[Vobject_index].show_ribbons = True
        self.glwidget.draw_ribbon(self.Vobjects[Vobject_index])
        self.glwidget.draw()
        
    def _hide_lines (self, Vobject_index ):
        """ Function doc """
        self.Vobjects[Vobject_index].show_lines = False
        #self.glwidget.draw_lines(self.Vobjects[Vobject_index])

    def _show_lines (self, Vobject_index ):
        """ Function doc """
        self.Vobjects[Vobject_index].show_lines = True
        self.glwidget.draw_lines(self.Vobjects[Vobject_index])
    
    
    def _hide_ball_and_stick (self, Vobject_index ):
        """ Function doc """
        #print ('here  _hide_ball_and_stick')
        self.Vobjects[Vobject_index].show_ball_and_stick = False
        #self.glwidget.draw_ball_and_stick(self.Vobjects[Vobject_index])
        
    def _show_ball_and_stick(self, Vobject_index):
        """ Function doc """
        self.Vobjects[Vobject_index].show_ball_and_stick = True
        self.glwidget.draw_ball_and_stick(self.Vobjects[Vobject_index])
    
    
    
    def _hide_spheres (self, Vobject_index ):
        """ Function doc """
        #print ('here  _hide_ball_and_stick')
        self.Vobjects[Vobject_index].show_spheres = False
        #self.glwidget.draw_spheres(self.Vobjects[Vobject_index])
        
    def _show_spheres (self, Vobject_index):
        """ Function doc """
        self.Vobjects[Vobject_index].show_spheres = True
        self.glwidget.draw_spheres(self.Vobjects[Vobject_index])
    

    def hide (self, _type = 'lines', Vobject_index =  None):
        """ Function doc """    
        if _type == 'dots':
            self._hide_dots (Vobject_index )

        if _type == 'lines':
            self._hide_lines (Vobject_index )

        if _type == 'ribbons':
            self._hide_ribbons (Vobject_index )
        
        if _type == 'ball_and_stick':
            self._hide_ball_and_stick(Vobject_index )
        
        if _type == 'spheres':
            self._hide_spheres(Vobject_index )            
        
        self.glwidget.updateGL()

    def show (self, _type = 'lines', Vobject_index =  None):
        """ Function doc """
        if _type == 'dots':
            self._show_dots (Vobject_index )

        if _type == 'lines':
            self._show_lines (Vobject_index )

        if _type == 'ribbons':
            self._show_ribbons (Vobject_index )
        
        if _type == 'ball_and_stick':
            self._show_ball_and_stick(Vobject_index)
        
        if _type == 'spheres':
            self._show_spheres(Vobject_index ) 
    
        self.glwidget.updateGL()

    
    def delete(self, Vobject_index = None):
        """ Function doc """
        self.Vobjects.pop(Vobject_index)
        self.glwidget.updateGL()
    
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
        self.glwidget.updateGL()
        
    def enable (self, index):
        """ Function doc """
        self.Vobjects[index].actived = True
        self.glwidget.draw()
        self.glwidget.updateGL()
        
    def set_frame (self, frame = 0):
        """ Function doc """
        self.glwidget.frame = frame
        self.glwidget.updateGL()
    
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
	
    def selection_mode(self, selmode = 'atom'):
        """ Function doc """
        self._selection_mode = selmode
        #print(self._selection_mode)
        #self.glwidget.selection_mode(mode = 'resid')
        if self._selection_mode == 'atom':
            self.glwidget.selection_mode(mode = 'atom')
        
        if self._selection_mode == 'residue':
            self.glwidget.selection_mode(mode = 'resid')
        
        if self._selection_mode == 'chain':
            self.glwidget.selection_mode(mode = 'chain')
        
        if self._selection_mode == 'molecule':
            self.glwidget.selection_mode(mode = 'molecule')
        
    def selection_change_presentation_mode (self, _type = 'lines', show =  True):
        """ Function doc """
        modified_objects = [False] * len(self.Vobjects)
        
        for atom in self.viewing_selections:
            index      = atom.index-1
            vobj_index = atom.Vobject_id
            
            modified_objects[vobj_index] = True
            
            if _type == 'lines':
                if show:
                    atom.lines = True
                else:
                    atom.lines = False
                self.Vobjects[vobj_index].modified_lines    = True
            
            if _type == 'dots':
                if show:
                    atom.dots = True
                else:
                    atom.dots = False
                self.Vobjects[vobj_index].modified_dots     = True
            
            if _type == 'ribbons':
                if show:
                    atom.ribbons = True
                else:
                    atom.ribbons = False
                self.Vobjects[vobj_index].modified_ribbons  = True
            
            if _type == 'spheres':
                if show:
                    atom.spheres = True
                else:
                    atom.spheres = False
                self.Vobjects[vobj_index].modified_spheres  = True
            
            if _type == 'ball_and_stick':
                if show:
                    atom.ball_and_stick = True
                else:
                    atom.ball_and_stick = False
                self.Vobjects[vobj_index].modified_ball_and_stick = True
            
            if _type == 'surface':
                if show:
                    atom.surface = True
                else:
                    atom.surface = False
                self.Vobjects[vobj_index].modified_surface  = True
        
        #self.modified_sticks   = False

        '''
        if selection:
            _vobjects = [[]]* len(self.EMSession.Vobjects)
            
            print ('len(self.EMSession.Vobjects)',_vobjects )
            print ('len(self.EMSession.viewing_selections)',len(self.EMSession.viewing_selections) )
            
            for atom in self.EMSession.viewing_selections:
                _vobjects[atom.Vobject_id].append(atom)
            
            for _vobject in _vobjects:
                if _vobject == []:
                    pass
                
                else:
                    vobj_index = _vobjects.index(_vobject)
                                        
                    gl_dt_li = glGenLists(self.gl_lists_counter)
                    glNewList(gl_dt_li, GL_COMPILE)
                    
                    for frame in self.EMSession.Vobjects[vobj_index].frames:
                        for atom in _vobject:
                            #-------------------------------------------------------
                            #                        D O T S
                            #-------------------------------------------------------
                            glPushMatrix()
                            glPushName(atom.atom_id)
                            glColor3f(atom.color[0], atom.color[1], atom.color[2])
                            glPointSize(self.EMSession.GL_parameters['dot_size']*atom.vdw_rad)# *self.scale_zoom
                            glBegin(GL_POINTS)
                            coord1   = frame[atom.index-1]
                            glVertex3f(float(coord1[0]),float( coord1[1]),float( coord1[2]))
                            glEnd()
                            glPopName()
                            glPopMatrix()
        
                    glEndList()            
                    self.EMSession.Vobjects[vobj_index].GL_list_dots.append(gl_dt_li) 
        '''
    
    def selection_function (self, selected):
        """ Function doc """

        #"""     P I C K I N G     S E L E C T I O N S     """
        if self._picking_selection_mode:
            if selected is None:
                self.picking_selections = [None]*len(self.picking_selections)
                #self.selected_residues = []
            else:
                if selected not in self.picking_selections:
                    for i in range(len(self.picking_selections)):
                        if self.picking_selections[i] == None:
                            self.picking_selections[i] = selected
                            selected = None
                            break
                    if selected is not None:
                        self.picking_selections[len(self.picking_selections)-1] = selected
                else:
                    for i in range(len(self.picking_selections)):
                        if self.picking_selections[i] == selected:
                            self.picking_selections[i] = None

        #"""     V I E W I N G     S E L E C T I O N S     """
        else:
            if selected is None:
                self.viewing_selections = []
                self.selected_residues  = []
            else:
                if self._selection_mode == 'atom':
                    if selected not in self.viewing_selections:
                        self.viewing_selections.append(selected)
                        
                    else:
                        index = self.viewing_selections.index(selected)
                        self.viewing_selections.pop(index)
                
                elif self._selection_mode == 'residue':
                    # if the selected atoms is not on the selected list
                    if selected not in self.viewing_selections:
                        print ('residue',selected.Vobject_id, selected.resi)
                        print (self.Vobjects[selected.Vobject_id].chains[selected.chain].residues[selected.resi])
                        # So, add all atoms  - selected residue <- selected.resi
                        for atom in self.Vobjects[selected.Vobject_id].chains[selected.chain].residues[selected.resi].atoms:
                            
                            # the atom is not on the list -  add atom by atom
                            if atom not in self.viewing_selections:
                                self.viewing_selections.append(atom)
                            
                            # the atom IS on the list - do nothing 
                            else:
                                pass
                
                    # if the selected atoms IS on the selected list
                    else:
                        # So, add all atoms  - selected residue <- selected.resi
                        for atom in self.Vobjects[selected.Vobject_id].chains[selected.chain].residues[selected.resi].atoms:
                            
                            # the atom is not on the list -  add atom by atom
                            if atom in self.viewing_selections:
                                index = self.viewing_selections.index(atom)
                                self.viewing_selections.pop(index)                            
                            # the atom IS on the list - do nothing 
                            else:
                                pass                    
                    
                    
                elif self._selection_mode == 'chain':
                    # if the selected atoms is not on the selected list
                    if selected not in self.viewing_selections:
                        # So, add all atoms  - selected residue <- selected.resi
                        for residue in self.Vobjects[selected.Vobject_id].chains[selected.chain].residues:
                            for atom in residue.atoms:
                                # the atom is not on the list -  add atom by atom
                                if atom not in self.viewing_selections:
                                    self.viewing_selections.append(atom)
                                
                                # the atom IS on the list - do nothing 
                                else:
                                    pass
                
                    # if the selected atoms IS on the selected list
                    else:
                        for residue in self.Vobjects[selected.Vobject_id].chains[selected.chain].residues:
                            #for residue in chain.residues:
                            for atom in residue.atoms:
                                # the atom is not on the list -  add atom by atom
                                if atom in self.viewing_selections:
                                    index = self.viewing_selections.index(atom)
                                    self.viewing_selections.pop(index)                            
                                # the atom IS on the list - do nothing 
                                else:
                                    pass          
                
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    print ('selected atoms: ',len(self.viewing_selections))
                    
                    #for atom in self.EMSession.Vobjects[selected.Vobject_id].chains[selected.chain].residues[selected.resi]

    
    
    def __init__ (self, parent = None, glwidget = None):
        """ Class initialiser """
        self.Vobjects         = []
        self.Vobjects_dic     = {}        
        self.atom_id_counter  = 0
        self.atom_dic_id      = {
                                # atom_id : obj_atom 
                                 }
        

        #---------------------------------------------------------------
        # gl stuffs
        #---------------------------------------------------------------
        self.glwidget = GLWidget (parent   , EMSession = self)
        #self.glwidget           = glwidget # a gl area recebe 
        #self.glwidget.EMSession = self
        #self.glwidget.generate_gL_actions()
        self.gl_parameters      =     {
                                      
                                      'dot_size'      : 3      ,
                                      'line_width'    : 2      ,
                                      'sphere_scale'  : 0.7    ,
                                      'stick_scale'   : 1      ,
                                
                                      'antialias'     : False  ,
                                      'bg_color'      : 'black',
                                      }
        
        
        #---------------------------------------------------------------
        #                S E L E C T I O N S
        #---------------------------------------------------------------

        self._picking_selection_mode = False # True/False  - interchange between viewing  and picking mode
        self._selection_mode    = 'residue'
        self.viewing_selections = []
        self.picking_selections = [None]*4
        self.selected_residues  = []

       

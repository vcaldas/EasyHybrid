#!/usr/bin/env python


import sys
import math
from PySide import QtCore, QtGui, QtOpenGL
import numpy as np

try:
    from OpenGL import GL
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL",
                            "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)

import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import GLarea.operations as op
import GLarea.representations as rep
from GLarea.vector_math import Vector


class glMenu:
    """ Class doc """
    def __init__ (self):
        """ Class initialiser """
        self.glwidget  = glwidget
        self.EMSession = EMSession
        


    def change_show_hide_ (self, selection_type = 'atom', _type = 'lines', show = True):
        """ Function doc """
        selection_list = []
        sel = self.selected_atom_on_click
        
        if selection_type == 'atom':
            #chain = self.selected_atom_on_click.chain
            #name  = self.selected_atom_on_click.name
            #index = self.selected_atom_on_click.index
            #label = selected.Vobject_name+' / '+selected.chain+' / '+str(selected.resn)+ ' ' +str(selected.resi)+' / '+str(selected.name)+' ' +str(selected.index)                    
            atom   = sel
            selection_list = [atom]
            sel.dots = True
            print('atom: ',atom.chain, atom.resi, atom.resn, atom.index, atom.name)    
            if show:
                if _type == 'dots':
                    atom.dots = True
                if _type == 'lines':
                    atom.lines = True
                if _type == 'ribbons':
                    atom.ribbons = True
                if _type == 'ball_and_stick':
                    atom.ball_and_stick = True                        
                if _type == 'spheres':
                    atom.spheres = True
                if _type == 'surface':
                    atom.surface = True
            else:
                if _type == 'dots':
                    atom.dots = False
                if _type == 'lines':
                    atom.lines = False
                if _type == 'ribbons':
                    atom.ribbons = False
                if _type == 'ball_and_stick':
                    atom.ball_and_stick = False                        
                if _type == 'spheres':
                    atom.spheres = False
                if _type == 'surface':
                    atom.surface = False
        
        if selection_type == 'residue':
            sel = self.selected_atom_on_click
           
            for atom in self.EMSession.Vobjects[sel.Vobject_id].chains[sel.chain].residues[sel.resi].atoms:
                selection_list.append(atom)
                atom.dots = True
                
                if show:
                    if _type == 'dots':
                        atom.dots = True
                    if _type == 'lines':
                        atom.lines = True
                    if _type == 'ribbons':
                        atom.ribbons = True
                    if _type == 'ball_and_stick':
                        atom.ball_and_stick = True                        
                    if _type == 'spheres':
                        atom.spheres = True
                    if _type == 'surface':
                        atom.surface = True
                else:
                    if _type == 'dots':
                        atom.dots = False
                    if _type == 'lines':
                        atom.lines = False
                    if _type == 'ribbons':
                        atom.ribbons = False
                    if _type == 'ball_and_stick':
                        atom.ball_and_stick = False                        
                    if _type == 'spheres':
                        atom.spheres = False
                    if _type == 'surface':
                        atom.surface = False
                print('atom: ',atom.chain, atom.resi, atom.resn, atom.index, atom.name)    

        if selection_type == 'chain':
            for residue in self.EMSession.Vobjects[sel.Vobject_id].chains[sel.chain].residues:
                for atom in self.EMSession.Vobjects[sel.Vobject_id].chains[sel.chain].residues[residue].atoms:            
                    selection_list.append(atom)
                    print('atom: ',atom.chain, atom.resi, atom.resn, atom.index, atom.name)    
                    if show:
                        if _type == 'dots':
                            atom.dots = True
                        if _type == 'lines':
                            atom.lines = True
                        if _type == 'ribbons':
                            atom.ribbons = True
                        if _type == 'ball_and_stick':
                            atom.ball_and_stick = True                        
                        if _type == 'spheres':
                            atom.spheres = True
                        if _type == 'surface':
                            atom.surface = True
                    else:
                        if _type == 'dots':
                            atom.dots = False
                        if _type == 'lines':
                            atom.lines = False
                        if _type == 'ribbons':
                            atom.ribbons = False
                        if _type == 'ball_and_stick':
                            atom.ball_and_stick = False                        
                        if _type == 'spheres':
                            atom.spheres = False
                        if _type == 'surface':
                            atom.surface = False
        self.EMSession.show (_type = _type , Vobject_indexes = [sel.Vobject_id])


    def _show_atom_dots    (self):
        self.change_show_hide_ (selection_type = 'atom', _type = 'dots', show = True)
    
    def _show_residue_dots (self):
        self.change_show_hide_ (selection_type = 'residue', _type = 'dots', show = True)

    def _show_chain_dots   (self):
        self.change_show_hide_ (selection_type = 'chain', _type = 'dots', show = True)
   
    def _hide_atom_dots    (self):
        self.change_show_hide_ (selection_type = 'atom', _type = 'dots', show = False)

    def _hide_residue_dots (self):
        self.change_show_hide_ (selection_type = 'residue', _type = 'dots', show = False)
    
    def _hide_chain_dots   (self):
        self.change_show_hide_ (selection_type = 'chain', _type = 'dots', show = False)

    '''  LINES '''
    def _show_atom_lines    (self):
        self.change_show_hide_ (selection_type = 'atom', _type = 'lines', show = True)
    
    def _show_residue_lines (self):
        self.change_show_hide_ (selection_type = 'residue', _type = 'lines', show = True)

    def _show_chain_lines   (self):
        self.change_show_hide_ (selection_type = 'chain', _type = 'lines', show = True)
   
    def _hide_atom_lines    (self):
        self.change_show_hide_ (selection_type = 'atom', _type = 'lines', show = False)

    def _hide_residue_lines (self):
        self.change_show_hide_ (selection_type = 'residue', _type = 'lines', show = False)
    
    def _hide_chain_lines   (self):
        self.change_show_hide_ (selection_type = 'chain', _type = 'lines', show = False)




    '''  RIBBONS '''
    def _show_atom_ribbons    (self):
        self.change_show_hide_ (selection_type = 'atom', _type = 'ribbons', show = True)
    
    def _show_residue_ribbons (self):
        self.change_show_hide_ (selection_type = 'residue', _type = 'ribbons', show = True)

    def _show_chain_ribbons   (self):
        self.change_show_hide_ (selection_type = 'chain', _type = 'ribbons', show = True)
   
    def _hide_atom_ribbons    (self):
        self.change_show_hide_ (selection_type = 'atom', _type = 'ribbons', show = False)

    def _hide_residue_ribbons (self):
        self.change_show_hide_ (selection_type = 'residue', _type = 'ribbons', show = False)
    
    def _hide_chain_ribbons   (self):
        self.change_show_hide_ (selection_type = 'chain', _type = 'ribbons', show = False)



    '''  ball_and_stick '''
    def _show_atom_ball_and_stick    (self):
        self.change_show_hide_ (selection_type = 'atom', _type = 'ball_and_stick', show = True)
    
    def _show_residue_ball_and_stick (self):
        self.change_show_hide_ (selection_type = 'residue', _type = 'ball_and_stick', show = True)

    def _show_chain_ball_and_stick   (self):
        self.change_show_hide_ (selection_type = 'chain', _type = 'ball_and_stick', show = True)
   
    def _hide_atom_ball_and_stick    (self):
        self.change_show_hide_ (selection_type = 'atom', _type = 'ball_and_stick', show = False)

    def _hide_residue_ball_and_stick (self):
        self.change_show_hide_ (selection_type = 'residue', _type = 'ball_and_stick', show = False)
    
    def _hide_chain_ball_and_stick   (self):
        self.change_show_hide_ (selection_type = 'chain', _type = 'ball_and_stick', show = False)

    
    '''  spheres '''
    def _show_atom_spheres    (self):
        self.change_show_hide_ (selection_type = 'atom', _type = 'spheres', show = True)
    
    def _show_residue_spheres (self):
        self.change_show_hide_ (selection_type = 'residue', _type = 'spheres', show = True)

    def _show_chain_spheres   (self):
        self.change_show_hide_ (selection_type = 'chain', _type = 'spheres', show = True)
   
    def _hide_atom_spheres    (self):
        self.change_show_hide_ (selection_type = 'atom', _type = 'spheres', show = False)

    def _hide_residue_spheres (self):
        self.change_show_hide_ (selection_type = 'residue', _type = 'spheres', show = False)
    
    def _hide_chain_spheres   (self):
        self.change_show_hide_ (selection_type = 'chain', _type = 'spheres', show = False)


    '''  surface '''
    def _show_atom_surface    (self):
        self.change_show_hide_ (selection_type = 'atom', _type = 'surface', show = True)
    
    def _show_residue_surface (self):
        self.change_show_hide_ (selection_type = 'residue', _type = 'surface', show = True)

    def _show_chain_surface   (self):
        self.change_show_hide_ (selection_type = 'chain', _type = 'surface', show = True)
   
    def _hide_atom_surface    (self):
        self.change_show_hide_ (selection_type = 'atom', _type = 'surface', show = False)

    def _hide_residue_surface (self):
        self.change_show_hide_ (selection_type = 'residue', _type = 'surface', show = False)
    
    def _hide_chain_surface   (self):
        self.change_show_hide_ (selection_type = 'chain', _type = 'surface', show = False)






    def _selection_show_dots (self):
        """ Function doc """
    
    def _selection_hide_dots (self):
        """ Function doc """
        
        


    def  generate_gL_actions(self):       
        
        
        
        """     Clicked On Atom    """
        
        '''    Center    '''
        self.Action_center = QtGui.QAction('Center', self)
        
        '''    Delete    '''
        self.Action_delete = QtGui.QAction('Delete', self)

        self.Action_show_atom_dots    = QtGui.QAction('dots', self)
        self.Action_show_residue_dots = QtGui.QAction('dots', self)
        self.Action_show_chain_dots   = QtGui.QAction('dots', self)
        self.Action_hide_atom_dots    = QtGui.QAction('dots', self)
        self.Action_hide_residue_dots = QtGui.QAction('dots', self)
        self.Action_hide_chain_dots   = QtGui.QAction('dots', self)
        
        self.Action_show_atom_dots   .triggered.connect(self._show_atom_dots)
        self.Action_show_residue_dots.triggered.connect(self._show_residue_dots)
        self.Action_show_chain_dots  .triggered.connect(self._show_chain_dots)
        self.Action_hide_atom_dots   .triggered.connect(self._hide_atom_dots)
        self.Action_hide_residue_dots.triggered.connect(self._hide_residue_dots)
        self.Action_hide_chain_dots  .triggered.connect(self._hide_chain_dots)
        
        
        self.Action_show_atom_lines    = QtGui.QAction('lines', self)
        self.Action_show_residue_lines = QtGui.QAction('lines', self)
        self.Action_show_chain_lines   = QtGui.QAction('lines', self)
        self.Action_hide_atom_lines    = QtGui.QAction('lines', self)
        self.Action_hide_residue_lines = QtGui.QAction('lines', self)
        self.Action_hide_chain_lines   = QtGui.QAction('lines', self)
        
        self.Action_show_atom_lines   .triggered.connect(self._show_atom_lines)
        self.Action_show_residue_lines.triggered.connect(self._show_residue_lines)
        self.Action_show_chain_lines  .triggered.connect(self._show_chain_lines)
        self.Action_hide_atom_lines   .triggered.connect(self._hide_atom_lines)
        self.Action_hide_residue_lines.triggered.connect(self._hide_residue_lines)
        self.Action_hide_chain_lines  .triggered.connect(self._hide_chain_lines)
        


        self.Action_show_atom_spheres    = QtGui.QAction('spheres', self)
        self.Action_show_residue_spheres = QtGui.QAction('spheres', self)
        self.Action_show_chain_spheres   = QtGui.QAction('spheres', self)
        self.Action_hide_atom_spheres    = QtGui.QAction('spheres', self)
        self.Action_hide_residue_spheres = QtGui.QAction('spheres', self)
        self.Action_hide_chain_spheres   = QtGui.QAction('spheres', self)
        
        self.Action_show_atom_spheres   .triggered.connect(self._show_atom_spheres)
        self.Action_show_residue_spheres.triggered.connect(self._show_residue_spheres)
        self.Action_show_chain_spheres  .triggered.connect(self._show_chain_spheres)
        self.Action_hide_atom_spheres   .triggered.connect(self._hide_atom_spheres)
        self.Action_hide_residue_spheres.triggered.connect(self._hide_residue_spheres)
        self.Action_hide_chain_spheres  .triggered.connect(self._hide_chain_spheres)

        self.Action_show_atom_ball_and_stick    = QtGui.QAction('ball_and_stick', self)
        self.Action_show_residue_ball_and_stick = QtGui.QAction('ball_and_stick', self)
        self.Action_show_chain_ball_and_stick   = QtGui.QAction('ball_and_stick', self)
        self.Action_hide_atom_ball_and_stick    = QtGui.QAction('ball_and_stick', self)
        self.Action_hide_residue_ball_and_stick = QtGui.QAction('ball_and_stick', self)
        self.Action_hide_chain_ball_and_stick   = QtGui.QAction('ball_and_stick', self)
        
        self.Action_show_atom_ball_and_stick   .triggered.connect(self._show_atom_ball_and_stick)
        self.Action_show_residue_ball_and_stick.triggered.connect(self._show_residue_ball_and_stick)
        self.Action_show_chain_ball_and_stick  .triggered.connect(self._show_chain_ball_and_stick)
        self.Action_hide_atom_ball_and_stick   .triggered.connect(self._hide_atom_ball_and_stick)
        self.Action_hide_residue_ball_and_stick.triggered.connect(self._hide_residue_ball_and_stick)
        self.Action_hide_chain_ball_and_stick  .triggered.connect(self._hide_chain_ball_and_stick)

        self.Action_show_atom_ribbons    = QtGui.QAction('ribbons', self)
        self.Action_show_residue_ribbons = QtGui.QAction('ribbons', self)
        self.Action_show_chain_ribbons   = QtGui.QAction('ribbons', self)
        self.Action_hide_atom_ribbons    = QtGui.QAction('ribbons', self)
        self.Action_hide_residue_ribbons = QtGui.QAction('ribbons', self)
        self.Action_hide_chain_ribbons   = QtGui.QAction('ribbons', self)
        
        self.Action_show_atom_ribbons   .triggered.connect(self._show_atom_ribbons)
        self.Action_show_residue_ribbons.triggered.connect(self._show_residue_ribbons)
        self.Action_show_chain_ribbons  .triggered.connect(self._show_chain_ribbons)
        self.Action_hide_atom_ribbons   .triggered.connect(self._hide_atom_ribbons)
        self.Action_hide_residue_ribbons.triggered.connect(self._hide_residue_ribbons)
        self.Action_hide_chain_ribbons  .triggered.connect(self._hide_chain_ribbons)

        self.Action_show_atom_surface    = QtGui.QAction('surface', self)
        self.Action_show_residue_surface = QtGui.QAction('surface', self)
        self.Action_show_chain_surface   = QtGui.QAction('surface', self)
        self.Action_hide_atom_surface    = QtGui.QAction('surface', self)
        self.Action_hide_residue_surface = QtGui.QAction('surface', self)
        self.Action_hide_chain_surface   = QtGui.QAction('surface', self)
        
        self.Action_show_atom_surface   .triggered.connect(self._show_atom_surface)
        self.Action_show_residue_surface.triggered.connect(self._show_residue_surface)
        self.Action_show_chain_surface  .triggered.connect(self._show_chain_surface)
        self.Action_hide_atom_surface   .triggered.connect(self._hide_atom_surface)
        self.Action_hide_residue_surface.triggered.connect(self._hide_residue_surface)
        self.Action_hide_chain_surface  .triggered.connect(self._hide_chain_surface)




        """     Clicked On Selection    """
        self.Action_show_dots = QtGui.QAction('dots', self)
        self.Action_hide_dots = QtGui.QAction('dots', self)
        self.Action_show_dots.triggered.connect(self._selection_show_dots)
        self.Action_hide_dots.triggered.connect(self._selection_hide_dots)

        '''    Lines    '''
        # show
        self.Action_show_lines = QtGui.QAction('Lines', self)
        self.Action_show_lines.setStatusTip('Show lines')
        #self.Action_show_lines.triggered.connect(self.show_lines)
        # hide
        self.Action_hide_lines = QtGui.QAction('Lines', self)
        self.Action_hide_lines.setStatusTip('Show lines')
        #self.Action_hide_lines.triggered.connect(self.hide_lines)

        '''   Ribbons   '''
        # show
        self.Action_show_ribbons = QtGui.QAction('Ribbons', self)
        self.Action_show_ribbons.setStatusTip('Show Ribbons')
        #self.Action_show_ribbons.triggered.connect(self.show_ribbons)
        # hide
        self.Action_hide_ribbons = QtGui.QAction('Ribbons', self)
        self.Action_hide_ribbons.setStatusTip('Hide Ribbons')
        #self.Action_hide_ribbons.triggered.connect(self.hide_ribbons)
        
        '''   Ball and Stick   '''
        # show
        self.Action_show_ball_and_stick = QtGui.QAction('Ball and Stick', self)
        self.Action_show_ball_and_stick.setStatusTip('Show Ball and Stick')
        #self.Action_show_ball_and_stick.triggered.connect(self.show_ball_and_stick)
        # hide
        self.Action_hide_ball_and_stick = QtGui.QAction('Ball and Stick', self)
        self.Action_hide_ball_and_stick.setStatusTip('Hide Ball and Stick')
        #self.Action_hide_ball_and_stick.triggered.connect(self.hide_ball_and_stick2)
        
        '''   Spheres   '''
        # show
        self.Action_show_spheres = QtGui.QAction('Spheres', self)
        self.Action_show_spheres.setStatusTip('Show Spheres')
        #self.Action_show_spheres.triggered.connect(self.show_spheres)
        # hide          
        self.Action_hide_spheres = QtGui.QAction('Spheres', self)
        self.Action_hide_spheres.setStatusTip('Hide Spheres')
        #self.Action_hide_spheres.triggered.connect(self.hide_spheres2)



    def open_gl_menu (self, _type = 'on_bg', selected = None, event = None):
        """ Function doc """
        menu = QtGui.QMenu()
        if _type == 'on_bg':
            for item in self.glmenu['on_bg']:
                menu.addAction(item)
        else:
            if _type == 'on_atom':
                if selected not in self.EMSession.viewing_selections:
                    #               obj             /      chain      /       residue                  resi           /         atom                  index
                    label = selected.Vobject_name+' / '+selected.chain+' / '+str(selected.resn)+ ' ' +str(selected.resi)+' / '+str(selected.name)+' ' +str(selected.index)                    
                    #str(selected.index) + ' ' + str(selected.name) + ' ' + str(selected.resi)+ ' ' + str(selected.resn)
                    Action_label = QtGui.QAction(label, self)
                    #Action_delete.triggered.connect(self.delete_obj)                    
                    menu.addAction(Action_label)
                    menu.addSeparator()            
                
                    menu.addAction(self.Action_center)
                    menu_atom = menu.addMenu("&Atom")

                    ''' S H O W    A T O M S '''
                    menu_atom_show = menu_atom.addMenu("&Show")
                    menu_atom_show.addAction(self.Action_show_atom_dots)
                    menu_atom_show.addAction(self.Action_show_atom_lines)
                    menu_atom_show.addAction(self.Action_show_atom_ribbons)
                    menu_atom_show.addAction(self.Action_show_atom_ball_and_stick)
                    menu_atom_show.addAction(self.Action_show_atom_spheres)
                    menu_atom_show.addAction(self.Action_show_atom_surface)

                    
                    ''' H I D E    A T O M S '''
                    menu_atom_hide = menu_atom.addMenu("&Hide")
                    menu_atom_hide.addAction(self.Action_hide_atom_dots)
                    menu_atom_hide.addAction(self.Action_hide_atom_lines)
                    menu_atom_hide.addAction(self.Action_hide_atom_ribbons)
                    menu_atom_hide.addAction(self.Action_hide_atom_ball_and_stick)
                    menu_atom_hide.addAction(self.Action_hide_atom_spheres)
                    menu_atom_hide.addAction(self.Action_hide_atom_surface)

                    
                    ''' S H O W     R E S I D U E '''
                    menu_residue = menu.addMenu("&Residue")
                    menu_residue_show = menu_residue.addMenu("&Show")
                    menu_residue_show.addAction(self.Action_show_residue_dots)
                    menu_residue_show.addAction(self.Action_show_residue_lines)
                    menu_residue_show.addAction(self.Action_show_residue_ribbons)
                    menu_residue_show.addAction(self.Action_show_residue_ball_and_stick)
                    menu_residue_show.addAction(self.Action_show_residue_spheres)
                    menu_residue_show.addAction(self.Action_show_residue_surface)
                    
                    
                    ''' H I D E      R E S I D U E '''
                    menu_residue_hide = menu_residue.addMenu("&Hide")
                    menu_residue_hide.addAction(self.Action_hide_residue_dots)
                    menu_residue_hide.addAction(self.Action_hide_residue_lines)
                    menu_residue_hide.addAction(self.Action_hide_residue_ribbons)
                    menu_residue_hide.addAction(self.Action_hide_residue_ball_and_stick)
                    menu_residue_hide.addAction(self.Action_hide_residue_spheres)
                    menu_residue_hide.addAction(self.Action_hide_residue_surface)
                    
                    ''' S H O W     C H A I N '''
                    menu_chain = menu.addMenu("&Chain")
                    menu_chain_show = menu_chain.addMenu("&Show")
                    menu_chain_show.addAction(self.Action_show_chain_dots)
                    menu_chain_show.addAction(self.Action_show_chain_lines)
                    menu_chain_show.addAction(self.Action_show_chain_ribbons)
                    menu_chain_show.addAction(self.Action_show_chain_ball_and_stick)
                    menu_chain_show.addAction(self.Action_show_chain_spheres)
                    menu_chain_show.addAction(self.Action_show_chain_surface)
                    
                    ''' H I D E     C H A I N '''
                    menu_chain_hide = menu_chain.addMenu("&Hide")
                    menu_chain_hide.addAction(self.Action_hide_chain_dots)
                    menu_chain_hide.addAction(self.Action_hide_chain_lines)
                    menu_chain_hide.addAction(self.Action_hide_chain_ribbons)
                    menu_chain_hide.addAction(self.Action_hide_chain_ball_and_stick)
                    menu_chain_hide.addAction(self.Action_hide_chain_spheres)
                    menu_chain_hide.addAction(self.Action_hide_chain_surface)

                    menu.addSeparator()
                    menu.addAction(self.Action_delete)
            
            if _type == 'on_selection':
                label ='Selection'
                Action_label = QtGui.QAction(label, self)
                #Action_delete.triggered.connect(self.delete_obj)                    
                menu.addAction(Action_label)
                menu.addSeparator()
                menu.addAction(self.Action_center)

                menu_show = menu.addMenu("&Show")
                #menu_show.addAction(self.Action_show_dots)
                #menu_show.addAction(self.Action_show_lines)
                #menu_show.addAction(self.Action_show_ribbons)
                #menu_show.addAction(self.Action_show_ball_and_stick)
                #menu_show.addAction(self.Action_show_spheres)

                menu_hide = menu.addMenu("&Hide")
                #menu_hide.addAction(self.Action_hide_dots)
                #menu_hide.addAction(self.Action_hide_lines)
                #menu_hide.addAction(self.Action_hide_ribbons)
                #menu_hide.addAction(self.Action_hide_ball_and_stick)
                #menu_hide.addAction(self.Action_hide_spheres)

                menu.addSeparator()
                menu.addAction(self.Action_delete)

        menu.exec_(event.globalPos())













class GLWidget(QtOpenGL.QGLWidget, glMenu):
    
    def __init__(self, parent=None, EMSession = None):
        """ GLWidget is a QtWidget with OpenGL capabilities.
            Attributes:
            
            + self.fovy --> Specifies the field of view angle, in degrees, in the y direction.
            + self.aspect --> Specifies the aspect ratio that determines the field of view in the x direction. The aspect ratio is the ratio of x (width) to y (height).
            + self.z_near --> Specifies the distance from the viewer to the near clipping plane (always positive).
            + self.z_far --> Specifies the distance from the viewer to the far clipping plane (always positive).
            + self.fog_start --> Specifies the start for the near distance used in the linear fog equation. The initial near distance is 0.
            + self.fog_end --> Specifies the end for the near distance used in the linear fog equation. The initial near distance is 1.
            + self.width --> Specifies the width of the window, only the drawing area, not the interface.
            + self.height --> Specifies the height of the window, only the drawing area, not the interface.
            + self.top --> Specifies the top value for the viewport. A positive value used to map the mouse coordinates into 3D world coordinates.
            + self.bottom --> Specifies the bottom value for the viewport. A negative value used to map the mouse coordinates into 3D world coordinates.
            + self.left --> Specifies the ratio between width and height. A negative value used to map the mouse coordinates into 3D world coordinates.
            + self.right --> Specifies the ratio between width and height. A positive value used to map the mouse coordinates into 3D world coordinates.
            + self.selected_atoms --> An array containing Atom types. The array contains the atoms selected with the mouse.
            + self.mouse_x --> Specifies the X position of the mouse in the window. It's used for the rotation function of the mouse.
            + self.mouse_y --> Specifies the Y position of the mouse in the window. It's used for the rotation function of the mouse.
            + self.dist_cam_zrp --> Specifies the distance from the camera (eye) to the zero reference point (zrp) of the 3D world. Used in zoom and pan functions.
            + self.scroll --> Specifies the amount of distance that the mouse wheel moves the clipping planes.
            + self.pick_radius --> An array containing the X and Y radius for selection. Specifies how much far the object to the mouse can be to be selected when clicked.
            + self.gl_backgrd --> An array containing a RGBA color in 0.0 to 1.0 scale. Specifies the color for the background.
            + self.zrp --> An array containing X, Y and Z coordinates in 3D world. Specifies the Zero Reference Point of the 3D world. This parameter determines the center of rotation.
            + self.mouse_rotate --> Flag for the rotation function. Specifies if the mouse is in rotation mode or not.
            + self.mouse_pan --> Flag for the pan function. Specifies if the mouse is in pan mode or not.
            + self.mouse_zoom --> Flag for the zoom function. Specifies if the mouse is in zoom mode or not.
            + self.dragging --> Flag for dragging the mouse. Specifies if the mouse is being dragged or not. Used to diferentiate between selection or movement.
            + self.drag_pos_x --> Specifies the X coordinate the mouse is being dragged.
            + self.drag_pos_y --> Specifies the Y coordinate the mouse is being dragged.
            + self.drag_pos_z --> Specifies the Z coordinate the mouse is being dragged.
            + self.frame --> Specifies the frame in the trajectory file.
            
        """
        QtOpenGL.QGLWidget.__init__(self, parent)
        
        #self.glmenu          = glmenu
        self.trolltechGreen  = QtGui.QColor.fromCmykF(0.40, 0.0, 1.0, 0.0)
        self.trolltechPurple = QtGui.QColor.fromCmykF(0.39, 0.39, 0.0, 0.0)
        
        #self.data   = None
        self.fovy   = 30.0
        self.aspect = 0.0
        self.z_near = 1.0
        self.z_far  = 10.0
        
        self.fog_start  = self.z_far - 4.5
        self.fog_end    = self.z_far
        self.scale_zoom = self.fog_start # increse /decrese the dot size and line width
        
        self.width  = 640
        self.height = 420
        self.top    = 1.0
        self.bottom = -1.0
        self.left   = -10.0
        self.right  = 10
        
        self.mouse_x = 0
        self.mouse_y = 0
        
        self.dist_cam_zrp = frame_i = 0
        self.scroll = 0.5
        self.pick_radius = [10, 10]
        #self.pos_mouse = [None, None]
        self.gl_backgrd = [0.0, 0.0, 0.0, 0.0]
        
        self.zrp          = np.array([0, 0, 0])
        
        self.mouse_rotate = False
        self.mouse_pan    = False
        self.mouse_zoom   = False
        self.dragging     = False
        
        self.drag_pos_x = 0.0
        self.drag_pos_y = 0.0
        self.drag_pos_z = 0.0
        self.frame = 0
        self.LINES = self.DOTS = self.BALL_STICK = self.VDW = self.PRETTY_VDW = self.RIBBON = self.SPHERES = self.WIRES = self.SELECTION = self.MODIFIED = False
        self.gl_ball_stick_list = self.gl_point_list = self.gl_lines_list = self.gl_pretty_vdw_list = self.gl_ribbon_list =  self.gl_sphere_list = self.gl_vdw_list = self.gl_wires_list = None  
        
        #self.sel_atom = True
        #self.sel_resid = self.sel_chain = self.sel_mol = False
        
        self.gl_lists_counter = 1
        self.EMSession = EMSession
        self.generate_gL_actions()

        #self.gl_menu   = glMenu(glwidget = self, EMSession = EMSession)
        self.selected_atom_on_click = None
    
        
    def initializeGL(self):
        """ Inside the realize function, you should put all you OpenGL
            initialization code, e.g. set the projection matrix,
            the modelview matrix, position of the camera.
        """
        glutInit()
        rep.init_gl(self.fog_start, self.fog_end, self.fovy, self.width, self.height, self.z_near, self.z_far, self.gl_backgrd)
        return True
    
    def resizeGL(self, width, height):
        """ 
        """
        glViewport(0, 0, width, height)
        self.left = -float(width)/float(height)
        self.right = -self.left
        self.width = width
        self.height = height
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.fovy, float(width)/float(height), self.z_near, self.z_far)
        glMatrixMode(GL_MODELVIEW)
    
    def paintGL(self):
        """ 
        """
        self.draw()
    
    def draw(self, frame = -1):
        """ Defines wich type of representations will be displayed
        """
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glClearColor(self.gl_backgrd[0],self.gl_backgrd[1],self.gl_backgrd[2],self.gl_backgrd[3])
        frame = self.frame
        #glPointSize(self.scale_zoom)# *self.scale_zoom

        for Vobject in self.EMSession.Vobjects:    
            if Vobject.actived:   
                #-------------------------------------------------------
                # Necessary, once trajectories have different sizes
                #-------------------------------------------------------
                input_frame = frame

                if input_frame >= (len(Vobject.frames)-1):
                    input_frame = len(Vobject.frames) -1
                
                glDisable(GL_LIGHT0)
                glDisable(GL_LIGHTING)
                glDisable(GL_COLOR_MATERIAL)
                glEnable (GL_DEPTH_TEST)
                
                if Vobject.show_dots    :
                    glCallList(Vobject.GL_list_dots[input_frame], GL_COMPILE)
                
                if Vobject.show_lines   :
                    glCallList(Vobject.list_lines[input_frame], GL_COMPILE)
                
                if Vobject.show_ribbons :
                    glCallList(Vobject.list_ribbons[input_frame], GL_COMPILE)
                
                glEnable(GL_LIGHT0)
                glEnable(GL_LIGHTING)
                glEnable(GL_COLOR_MATERIAL)
                glEnable(GL_DEPTH_TEST)
                
                if Vobject.show_sticks  :
                    glCallList(Vobject.list_sticks        [input_frame], GL_COMPILE)
                
                if Vobject.show_ball_and_stick :
                    glCallList(Vobject.list_ball_and_stick[input_frame], GL_COMPILE)
                
                if Vobject.show_spheres :
                    glCallList(Vobject.list_spheres[input_frame], GL_COMPILE)
                
                if Vobject.show_surface :
                    glCallList(Vobject.list_surface[input_frame], GL_COMPILE)
                
        glDisable(GL_LIGHT0)
        glDisable(GL_LIGHTING)
        glDisable(GL_COLOR_MATERIAL)
        glDisable(GL_DEPTH_TEST)
        
        # S E L E C T E D    A T O M S     P I C K I N G    
        if self.EMSession._picking_selection_mode:
            for i,atom in enumerate(self.EMSession.picking_selections):
                if atom is not None:
                    #print (atom, atom.index, frame, atom.Vobject_id, self.EMSession.Vobjects[atom.Vobject_id].frames, self.EMSession.Vobjects[atom.Vobject_id].coords  )
                    #rep.draw_picked(atom)
                    coord = self.EMSession.Vobjects[atom.Vobject_id].frames[frame][atom.index-1]
                    #glVertex3f(coord1[0], coord1[1], coord1[2])
                    rep.draw_selected(atom, coord)
                    rep.draw_numbers(atom, i+1, coord)

        
        # S E L E C T E D    A T O M S     V I E W I N G
        else:
            for i,atom in enumerate(self.EMSession.viewing_selections):
                #print (atom, atom.index, frame, atom.Vobject_id, self.EMSession.Vobjects[atom.Vobject_id].frames, self.EMSession.Vobjects[atom.Vobject_id].coords  )
                #rep.draw_picked(atom)
                coord = self.EMSession.Vobjects[atom.Vobject_id].frames[frame][atom.index-1]
                #glVertex3f(coord1[0], coord1[1], coord1[2])
                rep.draw_selected(atom, coord)

    def draw_to_pick(self, frame = -1):
        """ Defines wich type of representations will be displayed for the pick
            function to work. The only difference with the draw method should be
            that in this function there is no drawing for the selected items.
        """
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glClearColor(self.gl_backgrd[0],self.gl_backgrd[1],self.gl_backgrd[2],self.gl_backgrd[3])
        frame = self.frame
        for Vobject in self.EMSession.Vobjects:    
            if Vobject.actived:   
                #-------------------------------------------------------
                # Necessary, once trajectories have different sizes
                #-------------------------------------------------------
                input_frame = frame
                if input_frame >= (len(Vobject.frames)-1):
                    input_frame = len(Vobject.frames) -1
                glDisable(GL_LIGHT0)
                glDisable(GL_LIGHTING)
                glDisable(GL_COLOR_MATERIAL)
                glEnable (GL_DEPTH_TEST)
                if Vobject.show_dots    :
                    glCallList(Vobject.GL_list_dots[input_frame], GL_COMPILE)
                if Vobject.show_lines   :
                    glCallList(Vobject.list_lines[input_frame], GL_COMPILE)
                if Vobject.show_ribbons :
                    glCallList(Vobject.list_ribbons[input_frame], GL_COMPILE)
                glEnable(GL_LIGHT0)
                glEnable(GL_LIGHTING)
                glEnable(GL_COLOR_MATERIAL)
                glEnable(GL_DEPTH_TEST)
                if Vobject.show_sticks  :
                    glCallList(Vobject.list_sticks        [input_frame], GL_COMPILE)
                if Vobject.show_ball_and_stick :
                    glCallList(Vobject.list_ball_and_stick[input_frame], GL_COMPILE)
                if Vobject.show_spheres :
                    glCallList(Vobject.list_spheres[input_frame], GL_COMPILE)
                if Vobject.show_surface :
                    glCallList(Vobject.list_surface[input_frame], GL_COMPILE)
    
    def mousePressEvent(self, event):
        """ 
        """
        self.mouse_x = event.x()
        self.mouse_y = event.y()
        if (event.button() == QtCore.Qt.LeftButton):
            self.mouse_rotate = True
            #self.pos_mouse[0] = float(event.x())
            #self.pos_mouse[1] = float(event.y())
        if (event.button() == QtCore.Qt.RightButton):
            self.mouse_zoom = True
        if (event.button() == QtCore.Qt.MidButton):
            self.dist_cam_zrp = op.get_euclidean(self.zrp, self.get_cam_pos())
            self.drag_pos_x, self.drag_pos_y, self.drag_pos_z = self.pos(event.x(), event.y())
            self.mouse_pan = True
    
    def mouseDoubleClickEvent(self, event):
        """ 
        """
        if (event.button() == QtCore.Qt.LeftButton):
            nearest, hits = self.pick(event.x(), self.height-1-event.y(), self.pick_radius[0], self.pick_radius[1])
            selected = self.select(nearest, hits)
            if selected is not None:
                self.center_on_atom(selected.pos)
    
    def mouseMoveEvent(self, event):
        """ 
        """
        dx = float(event.x()) - self.mouse_x
        dy = float(event.y()) - self.mouse_y
        if ((dx == 0) and (dy == 0)):
            return
        self.mouse_x = float(event.x())
        self.mouse_y = float(event.y())
        changed = False
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.dragging = True
        
        if (self.mouse_rotate):
            ax, ay = dy, dx
            viewport = glGetIntegerv(GL_VIEWPORT)
            angle = math.sqrt(ax**2+ay**2)/float(viewport[2]+1)*180.0
            inv = np.matrix(glGetDoublev(GL_MODELVIEW_MATRIX)).I
            bx = (inv[0,0]*ax + inv[1,0]*ay)
            by = (inv[0,1]*ax + inv[1,1]*ay)
            bz = (inv[0,2]*ax + inv[1,2]*ay)
            glTranslate(self.zrp[0], self.zrp[1], self.zrp[2])
            glRotatef(angle, bx, by, bz)
            glTranslate(-self.zrp[0], -self.zrp[1], -self.zrp[2])
            changed = True
            
        elif (self.mouse_zoom):

            glMatrixMode(GL_MODELVIEW)
            modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
            # Delta is a modifier for the zoom effect, otherwise the zoom movement
            # would be too abrupt.
            delta = ((self.z_far-self.z_near)/2.0 + self.z_near)/200.0
            glLoadIdentity()
            # We only need to move along the Z axis, that is why only use the
            # glTranslatef function with a bz value
            bz = dy*delta
            glTranslatef(-self.zrp[0], -self.zrp[1], -self.zrp[2])
            glTranslatef(0, 0, bz)
            glTranslatef(self.zrp[0], self.zrp[1], self.zrp[2])
            glMultMatrixd(modelview)
            self.dist_cam_zrp += bz
            # Now we make the new projection view
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            self.z_near -= bz
            self.z_far -= bz
            self.fog_start -= bz
            self.fog_end -= bz
            self.scale_zoom -= bz
            # Depending how near we are from the z_near clipping plane, we need
            # to put some boundaries to avoid unexpected behaviors. Same with
            # the z_far clipping plane
            if (self.z_near > 0.1):
                gluPerspective(self.fovy, float(self.width)/float(self.height), self.z_near, self.z_far)
            elif (self.z_far <= 0.15):
                gluPerspective(self.fovy, float(self.width)/float(self.height), 0.1, 0.15)
            else:
                gluPerspective(self.fovy, float(self.width)/float(self.height), 0.1, self.z_far)
            glFogf(GL_FOG_START, self.fog_start)
            glFogf(GL_FOG_END, self.fog_end)
            glMatrixMode(GL_MODELVIEW)
            changed = True
            #print (self.z_near, self.z_far, self.fovy, self.fog_start, self.fog_end, self.scale_zoom)
            #glPointSize(self.scale_zoom)
        elif (self.mouse_pan):
            # The mouse pan function needs to be corrected to have
            # better behavior when the screen is far and near
            glMatrixMode(GL_MODELVIEW)
            px, py, pz = self.pos(event.x(), event.y())
            modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
            glLoadIdentity()
            glTranslatef((px-self.drag_pos_x)*(self.z_far)/10, 
                         (py-self.drag_pos_y)*(self.z_far)/10, 
                          modelview[2,3])
            '''
            # Here in the Z axis you don't need to calculate anything, since 
            # the movement is on the X and Y axis
            glTranslatef((px-self.drag_pos_x)*(self.z_far)/10, 
                         (py-self.drag_pos_y)*(self.z_far)/10, 
                         (pz-self.drag_pos_z)*(self.z_far)/10)
            '''
            glMultMatrixd(modelview)
            self.drag_pos_x = px
            self.drag_pos_y = py
            self.drag_pos_z = pz
            changed = True
        
        if (changed):
            self.updateGL()

    def mouseReleaseEvent(self, event):
        """ 
        """
        self.mouse_rotate = False
        self.mouse_zoom = False
        self.mouse_pan = False
        self.lastPos = QtCore.QPoint(event.pos())
        dx = event.x() - self.mouse_x
        dy = event.y() - self.mouse_y
        
        if dx == 0 and dy == 0:
            button = event.button()
            if button == QtCore.Qt.MouseButton.RightButton and not self.dragging:

                nearest, hits = self.pick(event.x(), self.height-1-event.y(), self.pick_radius[0], self.pick_radius[1])
                selected = self.select(nearest, hits)                    
                #menu = QtGui.QMenu(self)
                self.selected_atom_on_click = selected
                if selected is None:
                    self.open_gl_menu (_type = 'on_bg', selected = selected, event = event)
                    #for item in self.glmenu['background']:
                    #    menu.addAction(item)

                else:
                    if self.EMSession._picking_selection_mode:
                        pass
                    
                    else:
                        if selected not in self.EMSession.viewing_selections:
                            self.open_gl_menu (_type = 'on_atom', selected = selected, event = event)
                            ##               obj             /      chain      /       residue                  resi           /         atom                  index
                            #label = selected.Vobject_name+' / '+selected.chain+' / '+str(selected.resn)+ ' ' +str(selected.resi)+' / '+str(selected.name)+' ' +str(selected.index)                    
                            ##str(selected.index) + ' ' + str(selected.name) + ' ' + str(selected.resi)+ ' ' + str(selected.resn)
                            #Action_label = QtGui.QAction(label, self)
                            ##Action_delete.triggered.connect(self.delete_obj)                    
                            #menu.addAction(Action_label)
                            #menu.addSeparator()
                        else:
                            self.open_gl_menu (_type = 'on_selection', selected = selected, event = event)

                            #label = 'Selection'
                            #Action_label = QtGui.QAction(label, self)
                            ##Action_delete.triggered.connect(self.delete_obj)                    
                            #menu.addAction(Action_label)
                            #menu.addSeparator()
                
                #menu.exec_(event.globalPos())
            
            if button == QtCore.Qt.MouseButton.LeftButton and not self.dragging:
                #print('LeftButton')
                if dx <= self.pick_radius[0] and dy <= self.pick_radius[1]:
                    nearest, hits = self.pick(event.x(), self.height-1-event.y(), self.pick_radius[0], self.pick_radius[1])
                    selected = self.select(nearest, hits)                    
                    self.EMSession.selection_function(selected)
                    self.updateGL()

            
            if button == QtCore.Qt.MouseButton.MidButton:
                if self.dragging:
                    glMatrixMode(GL_MODELVIEW)
                    modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
                    dir_vec = modelview[:3, 2]
                    cam_pos = self.get_cam_pos()
                    dir_vec *= -self.dist_cam_zrp
                    new_zrp = cam_pos + dir_vec
                    self.zrp = np.array([new_zrp[0], new_zrp[1], new_zrp[2]])
                else:
                    nearest, hits = self.pick(event.x(), self.height-1-event.y(), self.pick_radius[0], self.pick_radius[1])
                    selected = self.select(nearest, hits)
                    if selected is not None:
                        self.center_on_atom(selected.pos)
        self.dragging = False
    
    def wheelEvent(self, event):
        """ 
        """
        if (event.delta() < 0):
            self.z_near += self.scroll
            self.z_far -= self.scroll
        if (event.delta() > 0):
            self.z_near -= self.scroll
            self.z_far += self.scroll
        if (self.z_near < 0.1):
            self.z_near = 0.1
        if (self.z_near >= self.z_far):
            self.z_near -= self.scroll
            self.z_far += self.scroll
        
        dist = float(self.z_far - self.z_near)
        self.fog_start = self.z_near + .85*dist
        self.fog_end = self.z_far;
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.fovy, float(self.width)/float(self.height), self.z_near, self.z_far)
        glFogf(GL_FOG_START, self.fog_start)
        glFogf(GL_FOG_END, self.fog_end)
        glMatrixMode(GL_MODELVIEW)
        self.updateGL()
    
    def center_on_atom(self, atom_pos):
        """ Only change the center of viewpoint of the camera.
            It does not change (yet) the position of the camera.
            atom_pos is a vector containing the XYZ coordinates
            of the selected atom.
        """
        if op.get_euclidean(self.zrp, atom_pos) != 0:
            cam_pos = self.get_cam_pos()
            glMatrixMode(GL_MODELVIEW)
            modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
            up = modelview[:3, 1]
            zrp = self.zrp
            dist = op.get_euclidean(zrp, atom_pos)
            vec_dir = op.unit_vector([atom_pos[0]-zrp[0], atom_pos[1]-zrp[1], atom_pos[2]-zrp[2]])
            add_z = (self.z_far - self.z_near)/2
            dist_z = op.get_euclidean(cam_pos, zrp)
            if dist_z < add_z:
                add_z = dist_z - 0.1
            cycles = 15
            to_add = float(dist/cycles)
            for i in range(1, cycles):
                aum = i*to_add
                pto = [zrp[0]+vec_dir[0]*aum, zrp[1]+vec_dir[1]*aum, zrp[2]+vec_dir[2]*aum]
                self.z_far = dist_z + add_z
                self.z_near = dist_z - add_z
                self.fog_start = self.z_far - 1.5
                self.fog_end = self.z_far
                dist_z = op.get_euclidean(cam_pos, pto)
                glMatrixMode(GL_PROJECTION)
                glLoadIdentity()
                gluPerspective(self.fovy, float(self.width)/float(self.height), self.z_near, self.z_far)
                glFogf(GL_FOG_START, self.fog_start)
                glFogf(GL_FOG_END, self.fog_end)
                glMatrixMode(GL_MODELVIEW)
                glLoadIdentity()
                gluLookAt(cam_pos[0], cam_pos[1], cam_pos[2],
                      pto[0], pto[1], pto[2],
                      up[0], up[1], up[2])
                self.updateGL()
            if dist%0.1 > 0:
                dist_z = op.get_euclidean(cam_pos, atom_pos)
                self.z_far = dist_z + add_z
                self.z_near = dist_z - add_z
                self.fog_start = self.z_far - 1.5
                self.fog_end = self.z_far
                glMatrixMode(GL_PROJECTION)
                glLoadIdentity()
                gluPerspective(self.fovy, float(self.width)/float(self.height), self.z_near, self.z_far)
                glFogf(GL_FOG_START, self.fog_start)
                glFogf(GL_FOG_END, self.fog_end)
                glMatrixMode(GL_MODELVIEW)
                glLoadIdentity()
                gluLookAt(cam_pos[0], cam_pos[1], cam_pos[2], atom_pos[0], atom_pos[1], atom_pos[2], up[0], up[1], up[2])
            self.zrp = atom_pos
            self.updateGL()
    
    def pos(self, x, y):
        """ Use the ortho projection and viewport information
            to map from mouse co-ordinates back into world
            co-ordinates
        """  
        viewport = glGetIntegerv(GL_VIEWPORT)
        px = float(x-viewport[0])/float(viewport[2])
        py = float(y-viewport[1])/float(viewport[3])
        px = self.left + px*(self.right-self.left)
        py = self.top + py*(self.bottom-self.top)
        pz = self.z_near
        return px, py, pz
    
    def pick(self, x, y, dx, dy):
        """ 
        """
        buf = glSelectBuffer(256)
        glRenderMode(GL_SELECT)
        glInitNames()
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        viewport = glGetIntegerv(GL_VIEWPORT)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        glLoadIdentity()
        gluPickMatrix(x, y, dx, dy, viewport)
        glMultMatrixd(projection)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        self.draw_to_pick()
        glPopMatrix()
        hits = glRenderMode(GL_RENDER)
        nearest = []
        min_z = None
        for hit in hits:
            if (len(hit.names) > 0) and ((min_z is None) or (hit.near < min_z)):
                min_z = hit.near
                nearest = hit.names
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        return nearest, hits
    
    def select(self, nearest, hits):
        """ 
        """
        picked = None
        if nearest != []:
            picked = self.EMSession.atom_dic_id[nearest[0]]
        return picked
    
    def get_cam_pos(self):
        """ Returns the position of the camera in XYZ coordinates
            The type of data returned is 'numpy.ndarray'.
        """
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        crd_xyz = -1 * np.mat(modelview[:3,:3]) * np.mat(modelview[3,:3]).T
        return crd_xyz.A1

    def load_mol(self, data=None):
        """
            !!!  This fuction is called only to test new GL features  !!!  
            
            Loads the data (if is any) or replace it if new data is given.
            This is the core of the representations, and need to be more
            efficient.
        """
        
        glDisable(GL_LIGHT0)
        glDisable(GL_LIGHT1)
        glDisable(GL_LIGHT2)
        glDisable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_DEPTH_TEST)

        n = 1
        for Vobject in self.EMSession.Vobjects:
            #print Vobject.label
            if Vobject.actived:
                
                for chain in  Vobject.chains:
                    
                    for res in Vobject.chains[chain].residues:
                        for atom in Vobject.chains[chain].residues[res].atoms:
                            glPushMatrix()
                            
                            glPushName(atom.index)
                            
                            glColor3f(atom.color[0], atom.color[1], atom.color[2])
                            glPointSize(self.PointSize*atom.vdw_rad)
                            glBegin(GL_POINTS)
                            glVertex3f(float(atom.pos[0]),float( atom.pos[1]),float( atom.pos[2]))
                            glEnd()
                            glPopName()
                            glPopMatrix()
                            #print atom.name, atom.pos
                    #'''
                    
                   
                    color = 1.0/n
                    
                    #'''
                    for i in range(0, len(Vobject.chains[chain].backbone) -1):
                        
                        ATOM1 = Vobject.chains[chain].backbone[i]
                        ATOM2 = Vobject.chains[chain].backbone[i+1]
                        
                        glEnable(GL_COLOR_MATERIAL)
                        glEnable(GL_DEPTH_TEST)
                        glPushMatrix()
                        
                        
                        glColor3f(1,  color, 2*color)
                        
                        glLineWidth(self.LineWidth*3)
                        #print Vobject.bonds[i],Vobject.bonds[i+1],Vobject.bonds[i+2], Vobject.bonds[i+3],Vobject.bonds[i+4],Vobject.bonds[i+5]
                        glBegin(GL_LINES)
                        
                        glVertex3f(ATOM1.pos[0],ATOM1.pos[1],ATOM1.pos[2])
                        glVertex3f(ATOM2.pos[0],ATOM2.pos[1],ATOM2.pos[2])
                        
                        glEnd()
                        glPopName()
                        glPopMatrix()
                        
                        #color += 0.001
                    #'''
            
                
                #initial = time.time()
                for bond in Vobject.bonds:
                    #glPushMatrix()
                    #glDisable(GL_LIGHT0)
                    #glDisable(GL_LIGHT1)
                    #glDisable(GL_LIGHT2)
                    #glDisable(GL_LIGHTING)
                    glEnable(GL_COLOR_MATERIAL)
                    glEnable(GL_DEPTH_TEST)
                    glPushMatrix()
                    #glPushName(bond[0])
                    
                    #glColor3f(0, 1, 1)
                    
                    glColor3f(Vobject.atoms[bond[0]].color[0], 
                              Vobject.atoms[bond[0]].color[1], 
                              Vobject.atoms[bond[0]].color[2])
                    
                    glLineWidth(self.LineWidth)
                    
                    #glBegin(GL_LINES)
                    glBegin(GL_LINE_STRIP)
                    glVertex3f(Vobject.atoms[bond[0]].pos[0], 
                               Vobject.atoms[bond[0]].pos[1], 
                               Vobject.atoms[bond[0]].pos[2])
                    
                    
                    glVertex3f((Vobject.atoms[bond[0]].pos[0] + Vobject.atoms[bond[1]].pos[0])/2, 
                               (Vobject.atoms[bond[0]].pos[1] + Vobject.atoms[bond[1]].pos[1])/2, 
                               (Vobject.atoms[bond[0]].pos[2] + Vobject.atoms[bond[1]].pos[2])/2)                    

                    
                    glColor3f(Vobject.atoms[bond[1]].color[0], 
                              Vobject.atoms[bond[1]].color[1], 
                              Vobject.atoms[bond[1]].color[2])
                    
                    glVertex3f((Vobject.atoms[bond[0]].pos[0] + Vobject.atoms[bond[1]].pos[0])/2, 
                               (Vobject.atoms[bond[0]].pos[1] + Vobject.atoms[bond[1]].pos[1])/2, 
                               (Vobject.atoms[bond[0]].pos[2] + Vobject.atoms[bond[1]].pos[2])/2) 

                    glVertex3f(Vobject.atoms[bond[1]].pos[0], 
                               Vobject.atoms[bond[1]].pos[1], 
                               Vobject.atoms[bond[1]].pos[2])                    
                    
                    glEnd()
                    glPopName()
                    glPopMatrix()
                #final = time.time() 
                #print final - initial

            else:
                pass
            n += 1
    
    def draw_dots(self, Vobject = None, selection = True):
        """ Change the representation to Dots.
        """
        Vobject.GL_list_dots =[]
        for frame in Vobject.frames:
            gl_dt_li = glGenLists(self.gl_lists_counter)
            glNewList(gl_dt_li, GL_COMPILE)
            for chain in  Vobject.chains:
                for res in Vobject.chains[chain].residues:
                    for atom in Vobject.chains[chain].residues[res].atoms:
                        # checking if the selection is actived
                        if atom.dots:
                            #-------------------------------------------------------
                            #                        D O T S
                            #-------------------------------------------------------
                            glPushMatrix()
                            glPushName(atom.atom_id)
                            glColor3f(atom.color[0], atom.color[1], atom.color[2])
                            glPointSize(self.EMSession.gl_parameters['dot_size']*atom.vdw_rad)# *self.scale_zoom
                            glBegin(GL_POINTS)
                            coord1   = frame[atom.index-1]
                            glVertex3f(float(coord1[0]),float( coord1[1]),float( coord1[2]))
                            glEnd()
                            glPopName()
                            glPopMatrix()
                        else:
                            pass
                            
            glEndList()
            Vobject.GL_list_dots.append(gl_dt_li) 
            self.gl_lists_counter += 1
        return True
        
    def draw_lines(self, Vobject = None , selection = None):
        """ Change the representation to lines.
            It is the default representation.
        """
        glDisable(GL_LIGHT0)
        glDisable(GL_LIGHT1)
        glDisable(GL_LIGHT2)
        glDisable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_DEPTH_TEST)
        Vobject.list_lines =[]
        for frame in Vobject.frames:
            gl_ln_li = glGenLists(self.gl_lists_counter)
            
            glNewList(gl_ln_li,GL_COMPILE) #GL_COMPILE_AND_EXECUTE) #GL_COMPILE)
            glLineWidth(self.EMSession.gl_parameters['line_width'])

            for bond in Vobject.index_bonds:

                atom1    = Vobject.atoms[bond[0]]
                atom2    = Vobject.atoms[bond[1]]
                # checking if the selection is actived
                if  atom1.lines and atom2.lines:
                
                    coord1   = frame[bond[0]]
                    coord2   = frame[bond[1]]

                    midcoord = [
                            (coord1[0] + coord2[0])/2,	   
                            (coord1[1] + coord2[1])/2,
                            (coord1[2] + coord2[2])/2,
                            ]
                    
                    glPushMatrix()		
                    glPushName(atom1.atom_id) 
                    glColor3f(atom1.color[0], 
                              atom1.color[1], 
                          atom1.color[2])

                    
                    glBegin(GL_LINES)
                    glVertex3f(coord1[0],coord1[1],coord1[2])
                    glVertex3f(midcoord[0],midcoord[1],midcoord[2])
                    glEnd()
                    glPopName()
                    glPopMatrix()
                    
                    
                    glPushMatrix()		
                    glPushName(atom2.atom_id) 
                    glColor3f (atom2.color[0], 
                               atom2.color[1], 
                           atom2.color[2])

                    glBegin(GL_LINES)
                    glVertex3f(midcoord[0],midcoord[1],midcoord[2])
                    glVertex3f(coord2[0],coord2[1],coord2[2])

                    glEnd()
                    glPopName()
                    glPopMatrix()
            glEndList()
            Vobject.list_lines.append(gl_ln_li)
            
            self.gl_lists_counter += 1
        return True

    def draw_ribbon(self, Vobject = None , selection = None):
        """ Change the representation to Ribbon.
        """
        Vobject.list_ribbons =[]

        for frame in Vobject.frames:
            glEnable(GL_COLOR_MATERIAL)
            glEnable(GL_DEPTH_TEST)
            
            gl_rb_li = glGenLists(self.gl_lists_counter)
            glNewList(gl_rb_li, GL_COMPILE)
            #print 'aqui'
            glLineWidth(7)

            #'''
            if Vobject.actived:
                for chain in  Vobject.chains:
                    for i in range(0, len(Vobject.chains[chain].backbone) -1):
                        ATOM1  = Vobject.chains[chain].backbone[i]
                        ATOM2  = Vobject.chains[chain].backbone[i+1]
                        if  ATOM1.ribbons and   ATOM2.ribbons:
                            #if (ATOM1.resi - ATOM2.resi) == 1:	    
                            coord1 = frame[ATOM1.index -1]
                            coord2 = frame[ATOM2.index -1]
                            #print coord1, coord2
                            glPushMatrix()
                            glColor3f(ATOM1.color[0],ATOM1.color[1], ATOM1.color[1])
                            glBegin(GL_LINES)
                            glVertex3f(coord1[0],coord1[1],coord1[2])
                            glVertex3f(coord2[0],coord2[1],coord2[2])
                            glEnd()
                            glPopMatrix()

            glEndList()
            #'''
            Vobject.list_ribbons.append(gl_rb_li)
            self.gl_lists_counter += 1
    
    '''
    def draw_spheres(self):
        """ Change the representation to Spheres.
        """
        #print('Spheres Representation')
        # Sphere representation of the atoms, the difference between the ball
        # representation is that sphere uses the covalent radius and ball the
        # atomic radius.
        for frame in Vobject.frames:
            if self.gl_sphere_list == None or self.MODIFIED:
                self.gl_sphere_list = []
                for i in range(len(self.data)):
                    self.frame_i = i
                    self.load_mol()
                    gl_sp_li = glGenLists(1)
                    glNewList(gl_sp_li, GL_COMPILE)
                    for atom in self.sphere_list:
                        rep.draw_sphere(atom)
                    glEndList()
                    self.gl_sphere_list.append(gl_sp_li)
            return True    
    #'''
    def draw_ball_and_stick (self, Vobject = None , selection = None):
        """ Draws all the elements for Ball-Stick representation.
        """
        Vobject.list_ball_and_stick =[]
        sphere_quality = 15
        for frame in Vobject.frames:
            glEnable(GL_LIGHT0)
            glEnable(GL_LIGHTING)
            glEnable(GL_COLOR_MATERIAL)
            glEnable(GL_DEPTH_TEST)
           
            gl_bs_li = glGenLists(self.gl_lists_counter)
            glNewList(gl_bs_li, GL_COMPILE)
            
            for bond in Vobject.index_bonds:
                
                atom1    = Vobject.atoms[bond[0]]
                atom2    = Vobject.atoms[bond[1]]

                if atom1.ball_and_stick  and atom2.ball_and_stick:
                    coord1   = frame[bond[0]]
                    coord2   = frame[bond[1]]

                    midcoord = [
                               (coord1[0] + coord2[0])/2,	   
                               (coord1[1] + coord2[1])/2,
                               (coord1[2] + coord2[2])/2,
                               ]



                    #self.PointSize =20
                    #-------------------------------------------------------
                    #                        B A L L 
                    #-------------------------------------------------------
                    glPushMatrix()                
                    glPushName(atom1.atom_id)
                    
                    coord1   = frame[atom1.index-1]
                    glTranslate(coord1[0],   coord1[1],   coord1[2])
                    glColor3f(atom1.color[0], atom1.color[1], atom1.color[2])
                    glutSolidSphere(atom1.radius *self.EMSession.gl_parameters['sphere_scale'], sphere_quality, sphere_quality)
                    glPopMatrix()
                    glPopName()

                    glPushMatrix()                
                    glPushName(atom2.atom_id)
                    coord2   = frame[atom2.index-1]
                    glTranslate(coord2[0]     ,   coord2[1]   ,   coord2[2])
                    glColor3f  (atom2.color[0], atom2.color[1],   atom2.color[2])
                    glutSolidSphere(atom2.radius *self.EMSession.gl_parameters['sphere_scale'] , sphere_quality, sphere_quality)                           
                    glPopName()
                    glPopMatrix()
                    #-------------------------------------------------------


                    #-------------------------------------------------------
                    #                        S T I C K S
                    #-------------------------------------------------------
                    #rep.draw_stick_bond(atom1 = atom1, atom2 = atom2, radius = 2)
                    
                    v = Vector()
                    #base of cylinder is at the origin, the top is in the positive z axis
                    radius = 0.07
                    a = coord1
                    b = coord2
                    
                    axis_start = [0, 0, .1]
                    axis_end = v.subtract(a, b)

                    #find angle between the starting and ending axis
                    angle = v.angle(axis_start, axis_end)
                    
                    # determina the axis of rotation of the angle
                    axis_rotation = v.crossproduct (axis_start, axis_end)

                    #calculate the distance from a to b
                    length = v.mag(axis_end)
                    glColor3f(0.9, 0.9, 0.9)

                    # set the bottom  and the top radius to be the same thing
                    radius_bottom = radius
                    radius_top    = radius

                    # draw the bond ( use glTranslate beofre using glRotate)
                    cyl = gluNewQuadric()
                    glPushMatrix()
                    glTranslate(b[0], b[1], b[2])
                    glRotate(angle, axis_rotation[0], axis_rotation[1], axis_rotation[2])
                    
                    gluCylinder(cyl, radius_bottom *self.EMSession.gl_parameters['stick_scale'], 
                                     radius_top*self.EMSession.gl_parameters['stick_scale'], 
                                     length, 15, 15)
                    glPopMatrix()
                    #-------------------------------------------------------

            glEndList()
            Vobject.list_ball_and_stick.append(gl_bs_li)
            self.gl_lists_counter += 1 
        return True

    #'''
    def draw_spheres (self, Vobject = None , selection = None):
        """ Draws all the elements for Ball-Stick representation.
        """
        Vobject.list_spheres = []
        sphere_quality = 15
        for frame in Vobject.frames:
            glEnable(GL_LIGHT0)
            glEnable(GL_LIGHTING)
            glEnable(GL_COLOR_MATERIAL)
            glEnable(GL_DEPTH_TEST)
           
            gl_bs_li = glGenLists(self.gl_lists_counter)
            glNewList(gl_bs_li, GL_COMPILE)
            
            for atom in Vobject.atoms:
                #-------------------------------------------------------
                #                        S P H E R E S
                #-------------------------------------------------------
                if atom.spheres:
                    glPushMatrix()                
                    glPushName(atom.atom_id)
                    coord1 = frame[atom.index-1]
                    glTranslate(float(coord1[0]),float( coord1[1]),float( coord1[2]))
                    glColor3f(atom.color[0],   atom.color[1], atom.color[2])
                    glutSolidSphere(atom.vdw_rad, sphere_quality, sphere_quality)
                    glPopMatrix()
                    glPopName()
            
            #for chain in  Vobject.chains:
            #    for res in Vobject.chains[chain].residues:
            #        for atom in Vobject.chains[chain].residues[res].atoms:
            #            #-------------------------------------------------------
            #            #                        S P H E R E S
            #            #-------------------------------------------------------
            #            glPushMatrix()                
            #            glPushName(atom.atom_id)
            #            coord1 = frame[atom.index-1]
            #            glTranslate(float(coord1[0]),float( coord1[1]),float( coord1[2]))
            #            glColor3f(atom.color[0],   atom.color[1], atom.color[2])
            #            glutSolidSphere(atom.vdw_rad, sphere_quality, sphere_quality)
            #            glPopMatrix()
            #            glPopName()
            #
           
            glEndList()
            Vobject.list_spheres.append(gl_bs_li)
            self.gl_lists_counter += 1  
        return True

    #'''

    def change_background(self, color):
        """ Changes the color of the background.
            The color variable is an array of four elements 
            corresponding to Red, Green, Blue and Alpha values
            in the 0.0-1.0 range.
        """
        self.gl_backgrd = color
        glFogfv(GL_FOG_COLOR, color[:3])
        self.draw()
        self.updateGL()
    
    def selection_mode(self, mode):
        """ Defines the selection mode used. This modifies the behavior of the
            draw method for selected objects.
        """
        if mode == "atom":
            self.sel_atom  = True
            self.sel_resid = False
            self.sel_chain = False
            self.sel_mol   = False
        
        elif mode == "resid":
            self.sel_resid = True
            self.sel_atom  = False
            self.sel_chain = False
            self.sel_mol   = False
        
        elif mode == "chain":
            self.sel_chain = True
            self.sel_atom  = False
            self.sel_resid = False
            self.sel_mol   = False
        
        elif mode == "mol":
            self.sel_mol   = True
            self.sel_atom  = False
            self.sel_resid = False
            self.sel_chain = False
        
        else:
            self.sel_atom = self.sel_resid = self.sel_chain = self.sel_mol = False
        return True
    
    def keyPressEvent(self, event):
        """ The keyPressEvent function serves, as the names states, to catch
            events in the keyboard.
        """
        if (event.key() == QtCore.Qt.Key_Escape):
            self.close()
        if (event.key() == QtCore.Qt.Key_R):
            self.selection_mode("resid")
        if (event.key() == QtCore.Qt.Key_A):
            self.selection_mode("atom")



















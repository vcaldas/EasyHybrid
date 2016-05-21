#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Main3.py
#  
#  Copyright 2014 fernando <fernando@Fenrir>
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
#  ####


#------------------------------------------------------------------------------
import pygtk; pygtk.require('2.0')
try:
        import gtk, gtk.gdk as gdk, gtk.gtkgl as gtkgl, gtk.gdkgl as gdkgl
except:
        print "try: sudo apt-get install  python-gtkglext1"
        
try:        
        from OpenGL.GL import *
        from OpenGL.GLU import *
        from OpenGL.GLUT import *
except:
        print "try: sudo apt-get install  pyOpenGL - mudar essa msg"
#------------------------------------------------------------------------------


'''
#-----------------------------------------------------------------------------
for name in (GL_VENDOR,GL_RENDERER,GL_SHADING_LANGUAGE_VERSION,GL_EXTENSIONS):
    print name,glGetString(name)
print glGetString(GL_VERSION)
print glGetString(GL_RENDERER)
print glGetString(GL_VENDOR)
print "\n\n"
#-----------------------------------------------------------------------------
'''


import os
#PYOPENMOL = os.environ.get('PYOPENMOL_ROOT')
#print PYOPENMOL


#pdynamo
#from pBabel           import *
#from pCore            import * 
#from pMolecule        import * 
#from pMoleculeScripts import * 

#------------------------------------------------------------------------------
from easyhybrid.viewer.glarea import GLCanvas
#------------------------------------------------------------------------------
from easyhybrid.viewer.atom_types import ATOMTYPES
#------------------------------------------------------------------------------
from pprint import pprint 
#------------------------------------------------------------------------------
from easyhybrid.gui.file_chooser_dialog import FileChooser
#------------------------------------------------------------------------------
from easyhybrid.pdynamo.main import pDynamoSession
#------------------------------------------------------------------------------
import sys
#------------------------------------------------------------------------------




#-----------------------------------------gui---------------------------------------------------#
from easyhybrid.gui.new_project                         import *                     #



class GLAreaDraw:
    """ Class doc """
    def __init__ (self):
        """ Class initialiser """
        self.data        = None
        self.bonds       = None
        self.lista       = 0
        self.lista_bonds = 0
        #self.qc_table = []
        
        self.settings = {
                        'sphere_scale' : 0.5,
                         
                        }
        
        pass

    def change_light_propreties (gl_AMBIENT = None, 
                                 gl_DIFFUSE = None, 
                                gl_SPECULAR = None, 
                                gl_POSITION = None):
        """ Function doc """
        
        if gl_AMBIENT  == None:
            GL_AMBIENT  = [0.,0.,0.,1.]
        if GL_DIFFUSE  == None:
            GL_DIFFUSE  = [1.,1.,1.,1.]
        if GL_SPECULAR == None:
            GL_SPECULAR = [1.,1.,1.,1.]
        if GL_POSITION == None:
            GL_POSITION = [1.,1.,1.,0.]
        
        
        #glMaterialfv(GL_FRONT,GL_AMBIENT, (.7,.7,.7,1.))
        #glMaterialfv(GL_FRONT,GL_DIFFUSE, (.8,.8,.8,1.))
        #glMaterialfv(GL_FRONT,GL_SPECULAR,(1.,1.,1.,1.))

        
        glLightfv(GL_LIGHT0,GL_AMBIENT, (gl_AMBIENT[0],
                                         gl_AMBIENT[1],
                                         gl_AMBIENT[2],
                                         gl_AMBIENT[4]))
        
        glLightfv(GL_LIGHT0,GL_DIFFUSE, (gl_DIFFUSE[0],
                                         gl_DIFFUSE[1],
                                         gl_DIFFUSE[2],
                                         gl_DIFFUSE[3]))
        
        glLightfv(GL_LIGHT0,GL_SPECULAR,(gl_SPECULAR[0],
                                         gl_SPECULAR[1],
                                         gl_SPECULAR[2],
                                         gl_SPECULAR[3]))
        
       
        glLightfv(GL_LIGHT0,GL_POSITION,(gl_POSITION[0],
                                         gl_POSITION[1],
                                         gl_POSITION[2],
                                         gl_POSITION[3]))
                                         
                                         
        glMaterialfv(GL_FRONT,GL_AMBIENT, (.7,.7,.7,1.))
        glMaterialfv(GL_FRONT,GL_DIFFUSE, (.8,.8,.8,1.))
        glMaterialfv(GL_FRONT,GL_SPECULAR,(1.,1.,1.,1.))
        glMaterialfv(GL_FRONT,GL_SHININESS,100.0)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_FOG)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_NORMALIZE)
        glEnable(GL_COLOR_MATERIAL)

    def DrawBondLines (self, bond = None):
        glDisable(GL_LIGHT0)
        glDisable(GL_LIGHT1)
        glDisable(GL_LIGHT2)
        glDisable(GL_LIGHTING)
        #glDisable(GL_DEPTH_TEST)
        #print self.data
        a = self.data.pos[0][bond[0]]
        b = self.data.pos[0][bond[1]]
       
        #glLineWidth(1.5)
        glPushMatrix()

        ''' calculating the middle point between the two bonds'''
        ix,iy,iz = a[0], a[1], a[2]
        jx,jy,jz = b[0], b[1], b[2]                

        mx = 0.5 * ( ix + jx )
        my = 0.5 * ( iy + jy )                
        mz = 0.5 * ( iz + jz )                

        ''' Atom 1 (a) - importing colors'''
        glPushName(bond[0])         # nome da esfera = int ex. 1,2,4,5
        glColor3f(self.data.a_color[bond][0][0],
                  self.data.a_color[bond][0][1],
                  self.data.a_color[bond][0][2])

        glBegin( GL_LINES )                
        glVertex3f ( ix, iy, iz )                
        glVertex3f ( mx, my, mz )                
                                    # importante para o vetor nao estourar
        glEnd( )                
        glPopName() 
        
        ''' Atom 2 (b) - importing colors'''
        glPushName(bond[1]) 
        glColor3f(self.data.a_color[bond][1][0],
                  self.data.a_color[bond][1][1],
                  self.data.a_color[bond][1][2])
        glBegin( GL_LINES )
        glVertex3f ( mx, my, mz )                
        glVertex3f ( jx, jy, jz )                

        glEnd( )
        glPopName()                
        glPopMatrix()

    def DrawCaRibbon (self, a, b, radius):
        v = Vector()
        #base of cylinder is at the origin, the top is in the positive z axis
        axis_start = [0, 0, .1]
        #
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
        radius_top =  radius
        # draw the bond ( use glTranslate beofre using glRotate)
        cyl = gluNewQuadric()
        glPushMatrix()
        #glLoadIdentity()
        #glTranslate(0,0,-10)
        #glRotate(self.auto_rotation_angle, 1, 1, 1)
        glTranslate(b[0], b[1], b[2])
        glRotate(angle, axis_rotation[0], axis_rotation[1], axis_rotation[2])
        gluCylinder(cyl, radius_bottom, radius_top, length, 5, 5)
        glPopMatrix()

    def DrawSpheres (self, index = None):
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHT1)
        glEnable(GL_LIGHT2)
        glEnable(GL_LIGHTING)
        glEnable(GL_DEPTH_TEST)
        """ Function doc """
        atom      = self.data.pos[0][index]
        atom_size = self.data.a_size[index] * self.settings['sphere_scale']
        glPushMatrix()
        glTranslate(atom[0], atom[1], atom[2])
        glPushName(index+1)                           # nome da esfera = int ex. 1,2,4,5
        glColor3f(self.data.a_color[index][0],self.data.a_color[index][1],self.data.a_color[index][2])
        glutSolidSphere(atom_size, 15, 15)
        #glCallList(self.lista)
        glPopName()                               # importante para o vetor nao estourar
        glPopMatrix()                     
        glFlush()
        #-------------------------------------------------------------------
    def _demo_draw(self, event):
        
        if self.data == None:
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            #glClearColor(0.7, 0.7, 0.7, 1.0)     # -  CLARO
            glClearColor(0.0, 0.0, 0.0, 1.0)     # -  CLARO

        else:
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            #glClearColor(0.7, 0.7, 0.7, 1.0)     # -  CLARO
            glClearColor(0.0, 0.0, 0.0, 1.0)     # -  CLARO

            glCallList(self.lista,GL_COMPILE)
            glCallList(self.lista_bonds,GL_COMPILE)
            







class TreeviewHistory(object):
    """ Class doc """

    def __init__ (self):
        """ Class initialiser """
        pass

    def on_treeview2_show_logFile (self, item):
        """ Function doc """
        filein = self.project.settings['job_history'][self.selectedID]['log']
        editor = TextEditor.EasyHybridTextEditor(filein)
        
    def on_menuitem_PlotLogFile_activate(self, item):
        """ Function doc """
        filein = self.project.settings['job_history'][self.selectedID]['log']
        #print    self.project.settings['job_history'][self.selectedID]['log']
        parameters = ParseProcessLogFile(filein)

        #xlabel = 'Frames'
        #ylabel = 'Energy (KJ)'
        #title  = os.path.split(filein)[-1]
        #print  X, Y
        #
        #parameters = {
        #             'title' : title ,
        #             'X'     : X     ,
        #             'Y'     : Y     ,
        #             'xlabel': xlabel,
        #             'ylabel': ylabel,
        #             }

        PlotGTKWindow(parameters)

    def on_show_items_activate (self, item, event):
        """ Function doc """
        PyMOL_Obj = self.selectedObj

        if item == self.builder.get_object('menuitem_show_lines'):
            cmd.show ('lines', PyMOL_Obj)

        if item == self.builder.get_object('menuitem_show_sticks'):
            cmd.show ('sticks', PyMOL_Obj)

        if item == self.builder.get_object('menuitem_show_ribbon'):
            cmd.show ('ribbon', PyMOL_Obj)

        if item == self.builder.get_object('menuitem_show_cartoon'):
            cmd.show ('cartoon', PyMOL_Obj)

        if item == self.builder.get_object('menuitem_show_mesh'):
            cmd.show ('mesh', PyMOL_Obj)

        if item == self.builder.get_object('menuitem_show_surface'):
            cmd.show ('surface', PyMOL_Obj)

        if item == self.builder.get_object('menuitem_center'):
            cmd.center(PyMOL_Obj)

    def on_menuitem_set_as_active_activate (self, item):#, event):
        """ Function doc """
        #label     = self.builder.get_object('TreeViewObjLabel').get_text()
        actualObj = self.project.settings['PyMOL_Obj']
        label     = 'test'
        PyMOL_Obj = self.selectedObj
        data_path = self.project.settings['data_path']
        file_out  = 'exportXYZ.xyz'
        state     = -1

        '''
                                                  d i a l o g
                                         #  -  I M P O R T A N T  -  #
                            #---------------------------------------------------------#
                            #                                                         #
                            #        Message Dialog  -  when 2 buttons will be showed #
                            #  1 -create the warning message                          #
                            #  2 -hide the actual dialog - optional                   #
                            #  3 -show the message dialog                             #
                            #  4 -hide the message dialog                             #
                            #  5 -check the returned valor by the message dialog      #
                            #  6 -do something                                        #
                            #  7 -restore the actual dialog - optional                #
                            #---------------------------------------------------------#
        '''

        self.builder.get_object('MessageDialogQuestion').format_secondary_text("Set object: " +PyMOL_Obj +" as active?")
        dialog = self.builder.get_object('MessageDialogQuestion')

        a = dialog.run()  # possible "a" valors
        # 4 step          # -8  -  yes
        dialog.hide()     # -9  -  no
                          # -4  -  close
                          # -5  -  OK
                          # -6  -  Cancel

        # 5 step
        if a == -8:
            # 6 step
            filename = PyMOL_export_XYZ_to_file(PyMOL_Obj, label, data_path, file_out, state)
            self.project.load_coordinate_file_to_system(filename)
            self.project.settings['PyMOL_Obj'] = PyMOL_Obj
            self.project.SystemCheck(status = True, PyMOL = True, _color = False, _cell = True, treeview_selections = True)

            #liststore = self.builder.get_object('liststore2')
            #self.window_control.TREEVIEW_ADD_DATA2(liststore, self.project.settings['job_history'] , PyMOL_Obj)
            #print filename
        else:
            return 0

    def on_hide_items_activate (self, item, event):
        """ Function doc """
        PyMOL_Obj = self.selectedObj

        if item == self.builder.get_object('menuitem_hide_everything'):
            cmd.hide ('everything', PyMOL_Obj)

        if item == self.builder.get_object('menuitem_hide_lines'):
            cmd.hide ('lines', PyMOL_Obj)

        if item == self.builder.get_object('menuitem_hide_sticks'):
            cmd.hide ('sticks', PyMOL_Obj)

        if item == self.builder.get_object('menuitem_hide_ribbon'):
            cmd.hide ('ribbon', PyMOL_Obj)

        if item == self.builder.get_object('menuitem_hide_cartoon'):
            cmd.hide ('cartoon', PyMOL_Obj)

        if item == self.builder.get_object('menuitem_hide_mesh'):
            cmd.hide ('mesh', PyMOL_Obj)

        if item == self.builder.get_object('menuitem_hide_surface'):
            cmd.hide ('surface', PyMOL_Obj)

    def on_color_items_activate (self, item, event):
        """ Function doc """
        #print 'view log'
        #pprint(self.project.settings['job_history'][self.selectedID])

        PyMOL_Obj = self.selectedObj

        if item == self.builder.get_object('menuitem_black'):
            cmd.color('grey10',PyMOL_Obj)
            cmd.util.cnc(PyMOL_Obj)

        if item == self.builder.get_object('menuitem_green'):
            cmd.util.cbag(PyMOL_Obj)

        if item == self.builder.get_object('menuitem_cyan'):
            cmd.util.cbac(PyMOL_Obj)

        if item == self.builder.get_object('menuitem_magenta'):
            cmd.util.cbam(PyMOL_Obj)

        if item == self.builder.get_object('menuitem_yellow'):
            cmd.util.cbay(PyMOL_Obj)

        if item == self.builder.get_object('menuitem_salmon'):
            cmd.util.cbas(PyMOL_Obj)

        if item == self.builder.get_object('menuitem_white'):
            cmd.util.cbaw(PyMOL_Obj)

        if item == self.builder.get_object('menuitem_slate'):
            cmd.util.cbab(PyMOL_Obj)

        if item == self.builder.get_object('menuitem_orange'):
            cmd.util.cbao(PyMOL_Obj)

        if item == self.builder.get_object('menuitem_purple'):
            cmd.util.cbap(PyMOL_Obj)

        if item == self.builder.get_object('menuitem_pink'):
            cmd.util.cbak(PyMOL_Obj)

        if self.project.settings['fix_table'] != []:
            #PymolPutTable(self.project.settings['fix_table'], "FIX_atoms")
            cmd.color(self.EasyHybridConfig['fixed'],'FIX_atoms')

    def on_treeview_PyMOL_Objects_button_release_event(self, tree, event):
        if event.button == 3:
            #print "Mostrar menu de contexto botao3"
            selection     = tree.get_selection()
            model         = tree.get_model()
            (model, iter) = selection.get_selected()
            if iter != None:
                self.selectedID  = str(model.get_value(iter, 1))  # @+
                self.selectedObj = str(model.get_value(iter, 2))
                self.builder.get_object('TreeViewObjLabel').set_label('- ' +self.selectedObj+' -' )

                widget = self.builder.get_object('treeview_menu')
                widget.popup(None, None, None, event.button, event.time)


		if event.button == 2:
			selection     = tree.get_selection()
			model         = tree.get_model()
			(model, iter) = selection.get_selected()
			pymol_object = model.get_value(iter, 0)

			string2 = 'select sele, '+ pymol_object
			cmd.do(string2)
			cmd.center('sele')


        if event.button == 1:
            #print "Mostrar menu de contexto botao1"
            selection     = tree.get_selection()
            model         = tree.get_model()
            (model, iter) = selection.get_selected()

            if iter != None:
                #print model, iter
                pymol_object  = model.get_value(iter, 2)  # @+
                true_or_false = model.get_value(iter, 0)
                #print pymol_object
                if true_or_false == False:
                    cmd.enable(pymol_object)
                    true_or_false = True
                    model.set(iter, 0, true_or_false)
                    # print true_or_false

                else:
                    cmd.disable(pymol_object)
                    true_or_false = False
                    model.set(iter, 0, true_or_false)




class MainMenu(object):
    """ Class doc """
    
    def __init__ (self):
        """ Class initialiser """
        pass
    
    def on_imagemenuitem_new_project_activate (self, wigdet):
        print wigdet
        self.open_New_Project_dialog()

    def on_imagemenuitem_open_activate (self, wigdet):
        print wigdet
        self.open_file()
        
    def on_imagemenuitem_save_activate (self, wigdet):
        print wigdet
        self.orient_molecule()
        
    def on_imagemenuitem_Save_as_activate (self, wigdet):
        print wigdet

    def on_menuitem_about_activate (self, wigdet):  
        print wigdet

    def on_menuitem_mopac_activate (self, wigdet):  
        print wigdet

    def on_menuitem_wham_equation_solver_activate (self, wigdet):  
        print wigdet

    def on_menuitem_plot_log_graphs_activate (self, wigdet):  
        print wigdet

    def on_menuitem_neb_activate (self, wigdet):  
        print wigdet

    def on_menuitem_saw_activate (self, wigdet):  
        print wigdet

    def on_menuitem_umbrella_sampling_activate (self, wigdet):  
        print wigdet

    def on_menuitem_scan_2d_activate (self, wigdet):  
        print wigdet

    def on_menuitem_scan_activate (self, wigdet):  
        print wigdet

    def on_menuitem_energy_refinement_activate (self, wigdet):  
        print wigdet

    def on_menuitem_surfaces_activate (self, wigdet):  
        print wigdet

    def on_menuitem_normal_modes_activate (self, wigdet):  
        print wigdet

    def on_menuitem_molecular_dynamics_activate (self, wigdet):  
        print wigdet

    def on_menuitem_geometry_optimization_activate (self, wigdet):  
        print wigdet

    def on_menuitem_compute_energy_activate (self, wigdet):  
        print wigdet

    def on_menuitem_selection_tool_activate (self, wigdet):  
        print wigdet

    def on_menuitem_compute_charges_activate (self, wigdet):  
        print wigdet

    def on_menuitem_prune_to_selection_activate (self, wigdet):  
        print wigdet

    def on_menuitem_set_as_fixed_atoms_activate (self, wigdet):  
        print wigdet

    def on_menuitem_set_as_qc_atoms_activate (self, wigdet):  
        print wigdet

    def on_menuitem_terminal_activate (self, wigdet):  
        print wigdet

    def on_menuitem_sequences_activate (self, wigdet):  
        print wigdet

    def on_menuitem_cell_toggled (self, wigdet):  
        print wigdet

    def on_menuitem_show_valences_activate (self, wigdet):  
        print wigdet

    def on_menuitem_preferences_activate (self, wigdet):  
        print wigdet

    def on_menuitem_nb_model_activate (self, wigdet):  
        print wigdet

    def on_menuitem_rescale_activate (self, wigdet):  
        print wigdet

    def on_menuitem_correction_activate (self, wigdet):  
        print wigdet

    def on_menuitem_clear_fixed_atoms_activate (self, wigdet):  
        print wigdet

    def on_menuitem_clear_qc_atoms_activate (self, wigdet):  
        print wigdet

    def on_menuitem_quit_activate (self, wigdet):  
        print wigdet

    def on_menuitem_export_image_activate (self, wigdet):  
        print wigdet

    def on_menuitem_export_selection_activate (self, wigdet):  
        print wigdet

    def on_menuitem_export_coordinates_activate (self, wigdet):  
        print wigdet

    def on_menuitem_selection_activate (self, wigdet):  
        print wigdet

    def on_menuitem_trajectory_activate (self, wigdet):  
        print wigdet

    def on_menuitem_coordinates_activate (self, wigdet):  
        print wigdet

    def on_menuitem_amber12_to_amber11_topologies_activate (self, wigdet):  
        print wigdet
        
class MainToolBar(object):
    """ Class doc """
    
    def __init__ (self):
        """ Class initialiser """
        pass
    
    def on_combobox_selection_mode_changed(self, wigdet): 
        print wigdet
    
    def on_togglebutton_selection_mode_toggled(self, wigdet): 
        print wigdet
    
    def on_toolbutton_molecular_dynamics_clicked(self, wigdet): 
        print wigdet
    
    def on_toolbutton_geometry_optimization_clicked(self, wigdet): 
        print wigdet
    
    def on_toolbutton_single_point_clicked(self, wigdet): 
        print wigdet
    
    def on_toolbutton_check_system_clicked(self, wigdet): 
        print wigdet
    
    def on_toolbutton_quantum_chemistry_clicked(self, wigdet): 
        print wigdet
    
    def on_toolbutton_measures_clicked(self, wigdet): 
        print wigdet
    
    def on_toolbutton_sequence_toggled(self, wigdet): 
        print wigdet
    
    def on_toolbutton_clear_system_clicked(self, wigdet): 
        print wigdet
    
    def on_toolbutton_save_as_clicked(self, wigdet): 
        print wigdet
    
    def on_toolbutton_save_clicked(self, wigdet): 
        print wigdet
    
    def on_toolbutton_open_project_clicked(self, wigdet): 
        #print wigdet
        self.open_file()
    def on_toolbutton_new_project_clicked(self, wigdet): 
        print wigdet
        self.open_New_Project_dialog()



class EasyMolActions:
    """ Class doc """
    
    def __init__ (self):
        """ Class initialiser """
        pass
    
    def orient_molecule (self):
        """ Function doc """
        mass_center = self.pDynamoSession.easymol_objects[0].mass_center
        print mass_center
        #print mass_center
        self.zpr._center_on_atom_anim(mass_center)

    
class EasyHybridConfig(object):
    """ Class doc """
    def __init__ (self):
        """ Class initialiser """
        pass

class EasyHybridMain(EasyHybridConfig, EasyMolActions, MainMenu, MainToolBar):
    

    def open_New_Project_dialog (self):
        """ Function doc """
        self._NewProjectDialog.dialog.run()
        self._NewProjectDialog.dialog.hide()    
        
    def open_file (self):
        """ Function doc """
        _file          = FileChooser  (path        = None, 
                                       main_window = self.window)
        self.import_file_to_system(_file)

        
    def import_file_to_system (self, _file):
        """ Function doc """
        self.pDynamoSession.load_new_system(filename = _file)
        self.show_EasyMol_objects()
        self.orient_molecule()
        
    def show_EasyMol_objects(self):
        """ Function doc """
        #print "aqui1!"
        for easymol_object in self.pDynamoSession.easymol_objects:
            if easymol_object.activate:
                
                
                data  = easymol_object
                bonds = easymol_object.bonds
                
                self.zpr.zero = easymol_object.pos[0]
                #---------------------------------------------------------------
                #                           A T O M S
                #---------------------------------------------------------------
                self.gl_area_draw.data  = data
                
                self.gl_area_draw.lista = glGenLists(1)
                glNewList(self.gl_area_draw.lista,GL_COMPILE)

                #-----------------------------------#
                #               Spheres             #
                #-----------------------------------#
                for atom_index in range(len(easymol_object.pos[0])):
                    #print "drawing spheres"
                    if easymol_object.sphere[atom_index]:
                        self.gl_area_draw.DrawSpheres(index = atom_index)
                    atom_index +=1  
                glEndList()
                #---------------------------------------------------------------

            
                
                #---------------------------------------------------------------
                #                         B O N D S
                #---------------------------------------------------------------
                self.gl_area_draw.lista_bonds = glGenLists(1)
                glNewList(self.gl_area_draw.lista_bonds,GL_COMPILE)
                print "drawing self.bonds done"
                #-----------------------------------#
                #          Sticks   Lines           #
                #-----------------------------------#
                if bonds:
                    print "drawing self.bonds"
                    for bond in bonds:
                        if easymol_object.lines[bond][0] and easymol_object.lines[bond][1]:
                            self.gl_area_draw.DrawBondLines (bond)
                       
                        #if easymol_object.stick[bond][0] and easymol_object.stick[bond][1]:
                        #    pass
                else:
                    print 'self.gl_area_draw.self.bonds = ', None
                glEndList()
                #---------------------------------------------------------------

    def __init__(self):
        print 'intializing EasyMol gui'
        glutInit(sys.argv)
        #---------------------------------------------------------------
        #                            G T K
        #---------------------------------------------------------------   
        self.builder = gtk.Builder()
        self.builder.add_from_file(os.path.join(
		"easyhybrid/gui/glade/MainWindow/MainWindow.glade"))
        self.window  = self.builder.get_object("window1")                            
        self.window.set_size_request(800,600)
        self.window.connect("destroy",lambda event: gtk.main_quit())
        #self.window.connect('key_press_event', self.key_cb)
        self.vbox    = self.builder.get_object("vbox2")                               
        
        self.builder.connect_signals(self) 
        self.builder.get_object('notebook1').hide()
        #---------------------------------------------------------------   


        ##------------------------------ EasyHybrid Config ------------------------------------#
        self.HOME = os.environ.get('HOME')                                                     #
        try:                                                                                   #
            self.ORCA           = os.environ.get('ORCA')                                       #
        except:                                                                                #
            self.ORCA           = ''                                                           #
            print 'ORCA path not found'                                                        #
            pass                                                                               #
        ##-------------------------------------------------------------------------------------#
        self.EasyHybridConfig = {                                                              #
                               'HideWorkSpaceDialog': False    ,                               #
                               'WorkSpace'          : self.HOME,                               #
                               'ORCAPATH'           : self.ORCA,                               #
                               'bg_color'           : 'black'  ,                               #
                               'fixed'              : 'grey80' ,                               #
                               'color'              : 'radon'  ,                               #
                                                                                               #
                               "FIX": {                                                        #
                                        "dots"   : False,                                      #
                                        "spheres": False,                                      #
                                        "lines"  : True,                                       #
                                        "sticks" : False                                       #
                                      },                                                       #
                                                                                               #
                               "QC": {                                                         #
                                        "dots"   : False,                                      #
                                        "spheres": True ,                                      #
                                        "lines"  : False,                                      #
                                        "sticks" : True                                        #
                                      },                                                       #
                               'History'            : {}       }                               #
        ##-------------------------------------------------------------------------------------#




        ##------------------------------ EasyHybrid Dialogs -------------------------------------#
        ##                                                                                       #
        #'''os dialogs precisam ser criados aqui para que nao percam as alteracoes               #
        ## que o usuario farah nas 'entries' '''                                                 #
                                                                                                 #
        self._NewProjectDialog            = NewProjectDialog(self)                               #
                                                                                                 #
        #self._02MinimizationWindow       = MinimizationWindow(self)                             #
        #                                                                                        #
        #self.MolecularDynamicsWindow     = MolecularDynamicsWindow(self)                        #
        #                                                                                        #
        #self._NewProjectDialog           = NewProjectDialog(self)                               #
        #                                                                                        #
        #self.QuantumChemistrySetupDialog = QuantumChemistrySetupDialog(self)                    #
        #                                                                                        #
        #self.NonBondDialog               = NonBondDialog(self)                                  #
        #                                                                                        #
        #self.ScanWindow                  = ScanWindow(self)                                     #
        #                                                                                        #
        #self.ScanWindow2D = ScanWindow2D(self)                                                  #
        #                                                                                        #
        #self.TrajectoryDialog = TrajectoryDialog(self)                                          #
        #                                                                                        #
        #self.WorkSpaceDialog = WorkSpaceDialog(self)                                            #
        #                                                                                        #
        #self.pDynamoSelectionWindow = pDynamoSelectionWindow(self)                              #
        #                                                                                        #
        #self.ChargeRescaleDialog = ChargeRescaleDialog(self)                                    #
        #                                                                                        #
        #self.DialogAmber12ToAmber11 = DialogAmber12ToAmber11(self)                              #
        #                                                                                        #
        #self.PreferencesDialog   = PreferencesDialog(self)                                      #
        #                                                                                        #
        #self.UmbrellaSamplingWindow = UmbrellaSamplingWindow(self)                              #
        #                                                                                        #
        #self.DialogImportCoordinates = ImportCoordinatesDialog(self)                            #
        #                                                                                        #
        #self.DialogExportCoordinates = ExportCoordinatesDialog(self)                            #
        #                                                                                        #
        #self.AboutDialog             = AboutDialog(self)                                        #
        #self.SAWDialog               = SAWDialog(self)                                          #
        #self.NEBDialog               = NEBDialog(self)                                          #
        #self.EnergyRefineDialog      = TrajectoryEnergyRefineDialog(self)                       #
        #                                                                                        #
        #self.WHAMEquationSolver      = WHAMEquationSolverDialog(self)                           #
        #self.DialogMOPACSEnergy      = MOPACSEnergyDialog(self)                                 #
        ##---------------------------------------------------------------------------------------#

        
        #---------------------------------------------------------------
        #                         G L A r e a
        #---------------------------------------------------------------        
        self.zpr = GLCanvas(session = self)
        self.gl_area_draw = GLAreaDraw()
        self.zpr.draw = self.gl_area_draw._demo_draw
        #self.vbox.pack_start(self.zpr,True,True)
        self.vbox.pack_end(self.zpr,True,True)
        #---------------------------------------------------------------

        #---------------------------------------------------------------
        #                        E A S Y M O L
        #---------------------------------------------------------------
        self.pDynamoSession = pDynamoSession(self)
        #---------------------------------------------------------------

        self.window.show_all()
        if len (sys.argv) > 1:
            self.import_file_to_system(sys.argv[1])
        gtk.main()                                                              
        
    def run(self):
        gtk.main()
                

if __name__ == '__main__':
    print "\n\nCreating object"
    PyOpenMol = EasyHybridMain()
    PyOpenMol.run() 




        
        
        
        



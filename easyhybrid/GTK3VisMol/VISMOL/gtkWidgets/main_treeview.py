#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  gtk3.py
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


#import VISMOL.glCore.shapes as shapes
#import VISMOL.glCore.glaxis as glaxis
#import VISMOL.glCore.glcamera as cam
#import VISMOL.glCore.operations as op
#import VISMOL.glCore.sphere_data as sph_d
#import VISMOL.glCore.vismol_shaders as vm_shader
#import VISMOL.glCore.matrix_operations as mop

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk



class FileChooser:
    """ Class doc """
    
    def __init__ (self, main_window = None):
        """ Class initialiser """
        self.main_window = main_window

    
    def open (self):

        """ Function doc """
        #main = gtkmain
        main = self.main_window
        filename = None
        
        chooser = Gtk.FileChooserDialog("Open File...", main,0,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OK, Gtk.ResponseType.OK))

        filter = Gtk.FileFilter()  
        filter.set_name("PDB files - *.pdb")
        #
        filter.add_mime_type("PDB files")
        filter.add_pattern("*.pdb")
        #
        chooser.add_filter(filter)
        filter = Gtk.FileFilter()
        filter.set_name("All files")
        filter.add_pattern("*")
        #
        chooser.add_filter(filter)  

        response = chooser.run()
        if response == Gtk.ResponseType.OK:
            filename = chooser.get_filename()
        chooser.destroy()
        return filename
        #print (filename)




class GtkMainTreeView():
    """ 
    """
    
    def __init__(self, vismolSession):
        """ 
        """
        self.builder = Gtk.Builder()
        self.builder.add_from_file('GTK3VisMol/VISMOL/gtkWidgets/main_treeview.glade')
        self.builder.connect_signals(self)
        self.vismolSession = vismolSession
        
    def refresh_gtk_main_treeview (self):
        """ Function doc """
        #print ('refresh_gtk_main_treeview',)
        #print (widget)
        liststore = self.builder.get_object('liststore1')
        model = liststore  
        model.clear()
        n = 0
        i = 1
        
        for vis_object in self.vismolSession.vismol_objects:
            print ('\n\n',vis_object.name,'\n\n')
            
            if vis_object.actived:
                actived = True
            else:
                actived = False
        
            data = [actived, str(i)        ,
                   vis_object.name      , 
                   str(len(vis_object.atoms)) , 
                   str(len(vis_object.frames)),
                   ]
            model.append(data)
            i +=1
            n = n + 1
        treeView = self.builder.get_object('treeview1')
        treeView.set_model(liststore)
        print ('load fuction finished')
        
    
    
    def on_treeview_Objects_button_release_event(self, tree, event):
        if event.button == 3:
            selection     = tree.get_selection()
            model         = tree.get_model()
            (model, iter) = selection.get_selected()
            if iter != None:
                self.selectedID  = str(model.get_value(iter, 1))  # @+
                self.selectedObj = str(model.get_value(iter, 2))
    
                self.builder.get_object('TreeViewObjLabel').set_label('- ' +self.selectedObj+' -' )

                widget = self.builder.get_object('treeview_menu')
                widget.popup(None, None, None, None, event.button, event.time)
                print ('button == 3')


        if event.button == 2:
            #selection     = tree.get_selection()
            #model         = tree.get_model()
            #(model, iter) = selection.get_selected()
            #pymol_object = model.get_value(iter, 0)
            self.refresh_gtk_main_treeview()
            print ('button == 2')
            
            #self.selectedID  = int(model.get_value(iter, 1))  # @+
            #self.vismolSession.center(Vobject_index = self.selectedID -1)

        if event.button == 1:
            selection     = tree.get_selection()
            model         = tree.get_model()
            (model, iter) = selection.get_selected()
            print ('button == 1')

            if iter != None:
                #print model, iter
                pymol_object  = model.get_value(iter, 2)  # @+
                true_or_false = model.get_value(iter, 0)
                obj_index     = model.get_value(iter, 1)
                #print pymol_object
                if true_or_false == False:
                    self.vismolSession.enable_by_index(int(obj_index)-1)
                    true_or_false = True
                    model.set(iter, 0, true_or_false)
                    # print true_or_false
                    self.vismolSession.glwidget.queue_draw()
                
                else:
                    self.vismolSession.disable_by_index(int(obj_index)-1)
                    true_or_false = False
                    model.set(iter, 0, true_or_false)
                    self.vismolSession.glwidget.queue_draw()
       
    def on_treemenu_item_selection (self, widget, event = None , data = None):
        """ Function doc """
        
        if widget == self.builder.get_object('menuitem5_rename'):
            tree = self.builder.get_object('treeview1')
            selection = tree.get_selection()
            model = tree.get_model()
            (model, iter) = selection.get_selected()
            obj_index = model.get_value(iter, 1)
            self.vismolSession.edit_by_index(int(obj_index)-1)
            self.vismolSession.glwidget.vm_widget.editing_mols = not self.vismolSession.glwidget.vm_widget.editing_mols
    


        tree = self.builder.get_object('treeview1')
        selection = tree.get_selection()
        model = tree.get_model()
        (model, iter) = selection.get_selected()
        obj_index = model.get_value(iter, 1)
        visObj = self.vismolSession.vismol_objects[(int(obj_index)-1)]

        
        if widget == self.builder.get_object('menuitem_center'):
            self.vismolSession.glwidget.vm_widget.center_on_coordinates(visObj, visObj.mass_center)

        
        if widget == self.builder.get_object('menu_show_lines'):
            self.vismolSession.vismol_objects[(int(obj_index)-1)].lines_actived     =  True
            #self.vismolSession._show_lines (visObj = visObj)


        if widget == self.builder.get_object('menu_show_sticks'):
            self.vismolSession.vismol_objects[(int(obj_index)-1)].cylinders_actived =  True

        if widget == self.builder.get_object('menu_show_spheres'):
            self.vismolSession.vismol_objects[(int(obj_index)-1)].spheres_actived   =  True

        if widget == self.builder.get_object('menu_show_ribbons'):
            self.vismolSession.vismol_objects[(int(obj_index)-1)].ribbons_actived   =  True

        if widget == self.builder.get_object('menu_show_dots'):
            self.vismolSession.vismol_objects[(int(obj_index)-1)].dots_actived      =  True


        
        
        if widget == self.builder.get_object('menu_hide_lines'):
            self.vismolSession.vismol_objects[(int(obj_index)-1)].lines_actived     = False
            #self.vismolSession._hide_lines (visObj = visObj)

        if widget == self.builder.get_object('menu_hide_sticks'):
            self.vismolSession.vismol_objects[(int(obj_index)-1)].cylinders_actived = False

        if widget == self.builder.get_object('menu_hide_spheres'):
            self.vismolSession.vismol_objects[(int(obj_index)-1)].spheres_actived   = False

        if widget == self.builder.get_object('menu_hide_ribbons'):
            self.vismolSession.vismol_objects[(int(obj_index)-1)].ribbons_actived   = False
            
        if widget == self.builder.get_object('menu_hide_dots'):
            self.vismolSession.vismol_objects[(int(obj_index)-1)].dots_actived      = False



import sys
import pygtk
pygtk.require('2.0')
import gtk
#from visual_gui import FileChooserWindow
from easyhybrid.EasyMol.visual.vis_parser import parse_pdb
from easyhybrid.EasyMol.visual_gui.AnimateTrajectory import TrajectoryTool

import gobject



class WindowControl():

    """ Class doc 
    Needed to fill the contents of combobox, 
    spin buttons and other widgets.

    - this object has been created for the 
    EasyHybrid_main class contains only those 
    methods associated with the events.

    """

    def __init__(self, builder):
        """ Class initialiser """
        self.builder = builder
        self.FileChooserWindow_TrueFalse = False
        self.window3                     = False  # not available yet
        self.ScanWindow                  = False
        self.Scan2DWindow                = False

    def SETUP_COMBOBOXES(self, combobox=None, combolist=[], active=0):
        """ Function doc """

        cbox = self.builder.get_object(combobox)  # ----> combobox_MM_model
        store = gtk.ListStore(gobject.TYPE_STRING)
        cbox.set_model(store)

        for i in combolist:
            cbox.append_text(i)

        cell = gtk.CellRendererText()
        cbox.pack_start(cell, True)
        cbox.add_attribute(cell, 'text', 0)
        cbox.set_active(active)
        #'01_main_window_combobox_MM_model'

    def TREEVIEW_ADD_DATA(self, liststore=None, pymol_objects=[], active=0):
        """ Function doc """
        model = liststore  # @+
        model.clear()
        n = 0
        for i in pymol_objects:
            data = [i]
            model.append(data)
            n = n + 1

    def TREEVIEW_ADD_DATA2(self, liststore=None, job_history={}, pymol_id=None):
        """ Function doc """

        model = liststore  
        model.clear()
        n = 0
                       
                       
                       
                         # this is necessary to sort the job_history #
        #-----------------------------------------------------------------------------#
        numbers  = list(job_history)                                                  #
        #print job_history                                                             #
        numbers2 = []                                                                 #
        #print numbers                                                                 #
                                                                                      #
        for i in numbers:                                                             #
            numbers2.append(int(i))                                                   #
        numbers2.sort()                                                               #
        #print numbers2                                                                #
        #-----------------------------------------------------------------------------#


        for i in numbers2:
            i = str(i)
            cell = self.builder.get_object('cellrenderertext2')
            cell.props.weight_set = True
            cell.props.weight = pango.WEIGHT_NORMAL
            data = [False, i                          ,
                           job_history[i]['object']   , #job_history[i][0],
                           job_history[i]['type']     , #job_history[i][1],
                           job_history[i]['potencial'],
                           ' '                       
                           ] #job_history[i][2]]

            
            if job_history[i]['object'] == pymol_id:
                
                #print '\n\n'
                #print job_history[i]['object']
                #print '\n\n'
                
                cell = self.builder.get_object('cellrenderertext2')
                #cell.props.weight_set = True
                cell.props.weight = pango.WEIGHT_BOLD
                
                data = [True, i                          ,
                              job_history[i]['object']   , 
                              job_history[i]['type']     ,
                              job_history[i]['potencial'],
                              ' A! '
                              ]

            model.append(data)
            n = n + 1
        

        '''
        for i in job_history:
            cell = self.builder.get_object('cellrenderertext2')
            cell.props.weight_set = True
            cell.props.weight = pango.WEIGHT_NORMAL
            data = [False, job_history[i]['object']   , #job_history[i][0],
                           job_history[i]['type']     , #job_history[i][1],
                           job_history[i]['potencial']] #job_history[i][2]]
            

            
            if job_history[i]['object'] == pymol_id:
               
                cell = self.builder.get_object('cellrenderertext2')
                #cell.props.weight_set = True
                cell.props.weight = pango.WEIGHT_BOLD
                
                data = [True, job_history[i]['object']   , 
                              job_history[i]['type']     ,
                              job_history[i]['potencial']]

            model.append(data)
            n = n + 1
        '''


    def STATUSBAR_SET_TEXT(self, text):
        """ Function doc """
        self.builder.get_object('statusbar1').push(0, text)

    def SETUP_SPINBUTTON (self, spinbutton, config):
        """ Function doc """
        adjustment  = gtk.Adjustment(config[0],config[1],config[2],config[3],config[4],config[5])
        SpinButton  = self.builder.get_object(spinbutton)
        SpinButton.set_adjustment(adjustment)	
        SpinButton.update()


    
class ToolBarMenu:
    """ Class doc """
    
    def __init__ (self):
        """ Class initialiser """
        pass
    
    def on_toolbarbuttons_click (self, button):
        """ Function doc """
        if button == self.builder.get_object('toolbutton_trajectory_tool'):
            
            if button.get_active() == True:
                self.TrajectoryTool.open_window()
                self.TrajectoryTool.actived =  True
            else:
                print ('desligado')
                self.TrajectoryTool.window.destroy()
                self.TrajectoryTool.actived =  False
                #cmd.set('valence', 0.0)
                #self.builder.get_object('handlebox1').hide()









class TreeviewHistory(object):
    """ Class doc """

    def __init__ (self):
        """ Class initialiser """
        pass
    
    '''
    def on_treeview2_show_logFile (self, item):
        """ Function doc """
        #pprint(self.project.settings['job_history'][self.selectedID]['log'])
        filein = self.project.settings['job_history'][self.selectedID]['log']
        #print   self.project.settings['job_history'][self.selectedID]['log']
        editor = TextEditor.EasyHybridTextEditor(filein)
        #editor.load_file(filein)
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

        self.PlotGTKWindow.plot(parameters)

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

        """
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
        """

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
            cmd.disable('all')
            liststore = self.builder.get_object('liststore2')
            self.window_control.TREEVIEW_ADD_DATA2(liststore, self.project.settings['job_history'], self.project.settings['PyMOL_Obj'] )
            self.project.SystemCheck(status = True, PyMOL = True, _color = False, _cell = True, treeview_selections = True)
            cmd.enable(self.project.settings['PyMOL_Obj'])
            #liststore = self.builder.get_object('liststore2')
            #self.window_control.TREEVIEW_ADD_DATA2(liststore, self.project.settings['job_history'] , PyMOL_Obj)
            #print filename
            
            #pprint (self.project.settings['job_history'][str(ID)])
            #self.project.settings['job_history'].pop(str(ID))
            #cmd.disable('all')
            #cmd.delete(PyMOL_Obj)
            #liststore = self.builder.get_object('liststore2')
            #self.window_control.TREEVIEW_ADD_DATA2(liststore, self.project.settings['job_history'], self.project.settings['PyMOL_Obj'] )
            #cmd.enable(self.project.settings['PyMOL_Obj'])
            #self.project.SystemCheck()
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
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

    def on_deleteItem_activate (self, item):
        """ Function doc """
        print item
        PyMOL_Obj = self.selectedObj
        ID        = self.selectedID
        
        if self.project.settings['PyMOL_Obj'] == PyMOL_Obj:
            message =  'Selected object is active - aborted deletion'
            print message
            self.builder.get_object('MessageDialogError').format_secondary_text(message)
            dialog = self.builder.get_object('MessageDialogError')
            a = dialog.run()  # possible "a" valors
            # 4 step          # -8  -  yes
            dialog.hide()     # -9  -  no
            pass
            
        else:
            #pprint (self.project.settings['job_history'][str(ID)])
            """
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
            """

            self.builder.get_object('MessageDialogQuestion').format_secondary_text("Delete object: " +PyMOL_Obj +"?")
            dialog = self.builder.get_object('MessageDialogQuestion')

            a = dialog.run()  # possible "a" valors
            # 4 step          # -8  -  yes
            dialog.hide()     # -9  -  no
                              # -4  -  close
                              # -5  -  OK
                              # -6  -  Cancel

            # 5 step
            if a == -8:
                self.project.settings['job_history'].pop(str(ID))
                cmd.disable('all')
                cmd.delete(PyMOL_Obj)
                liststore = self.builder.get_object('liststore2')
                self.window_control.TREEVIEW_ADD_DATA2(liststore, self.project.settings['job_history'], self.project.settings['PyMOL_Obj'] )
                cmd.enable(self.project.settings['PyMOL_Obj'])
                self.project.SystemCheck()
            
    def on_menuitem_center_activate (self, item, event):
        """ Function doc """
        
        #print 'on_menuitem_center_activate'
        tree          = self.builder.get_object('treeview2')
        selection     = tree.get_selection()
        model         = tree.get_model()
        (model, iter) = selection.get_selected()
        
        if iter != None:
            self.selectedID  = int(model.get_value(iter, 1))  # @+
            #print self.selectedID
            sys = self.EMSession.Vobjects[self.selectedID-1]
            self.EMSession.glarea.center_on_atom(sys.mass_center)
    
    def on_menuitem_show_dots_button_release_event (self, item, event):
        """ Function doc """
        print 'on_menuitem_show_dots_button_release_event'

    def on_menuitem_hide_dots_button_release_event (self, item, event):
        """ Function doc """
        print 'on_menuitem_hide_dots_button_release_event'
       
    def on_menuitem_show_ribbons_button_release_event (self, item, event):
        """ Function doc """
        #print 'on_menuitem_center_activate'
        tree          = self.builder.get_object('treeview2')
        selection     = tree.get_selection()
        model         = tree.get_model()
        (model, iter) = selection.get_selected()
        
        if iter != None:
            self.selectedID  = int(model.get_value(iter, 1))  # @+
            self.EMSession.show (_type = 'ribbons', Vobject_index = self.selectedID -1)


    def on_menuitem_hide_ribbons1_button_release_event (self, item, event):
        """ Function doc """
        #print 'on_menuitem_center_activate'
        tree          = self.builder.get_object('treeview2')
        selection     = tree.get_selection()
        model         = tree.get_model()
        (model, iter) = selection.get_selected()
        
        if iter != None:
            self.selectedID  = int(model.get_value(iter, 1))  # @+
            self.EMSession.hide (_type = 'ribbons', Vobject_index = self.selectedID -1)       
        
    '''
    
    def on_treeview_menuitem_button_release_event (self, item, event):
        """ Function doc """
        #print 'on_menuitem_center_activate'
        tree          = self.builder.get_object('treeview2')
        selection     = tree.get_selection()
        model         = tree.get_model()
        (model, iter) = selection.get_selected()

        #-------------------------------------#
        #             C E N T E R             #
        #-------------------------------------#
        if item == self.builder.get_object('menuitem_center'):
            #print 'aqui'
            if iter != None:
                self.selectedID  = int(model.get_value(iter, 1))  # @+
                self.EMSession.center(Vobject_index = self.selectedID -1)
                #self.EMSession.glarea.center_on_atom(sys.mass_center)

        #-------------------------------------#
        #               L I N E S             #
        #-------------------------------------#
        """ hide """
        if item == self.builder.get_object('menuitem_hide_lines'):
            if iter != None:
                self.selectedID  = int(model.get_value(iter, 1))  # @+
                self.EMSession.hide (_type = 'lines', Vobject_index = self.selectedID -1)  
        
        """ show """
        if item == self.builder.get_object('menuitem_show_lines'):
            if iter != None:
                self.selectedID  = int(model.get_value(iter, 1))  # @+
                self.EMSession.show (_type = 'lines', Vobject_index = self.selectedID -1)  
            
        
        #-------------------------------------#
        #            R I B B O N S            #
        #-------------------------------------#
        """ hide """
        if item == self.builder.get_object('menuitem_hide_ribbons'):
            if iter != None:
                self.selectedID  = int(model.get_value(iter, 1))  # @+
                self.EMSession.hide (_type = 'ribbons', Vobject_index = self.selectedID -1)  
        
        """ show """
        if item == self.builder.get_object('menuitem_show_ribbons'):
            if iter != None:
                self.selectedID  = int(model.get_value(iter, 1))  # @+
                self.EMSession.show (_type = 'ribbons', Vobject_index = self.selectedID -1)  
        
        
        
class GTKGUI (TreeviewHistory , WindowControl, ToolBarMenu):
    """ Class doc """
    
    def __init__ (self, EMSession):
        """ Class initialiser """
        #glarea = gda.GLCanvas()
        self.builder = gtk.Builder()
        self.builder.add_from_file('easyhybrid/EasyMol/visual_gui/main_window.glade')

        self.window = self.builder.get_object('main_window')
        self.boton =  self.builder.get_object('btn_ball_stick')
        self.builder.connect_signals(self)
        
        self.EMSession = EMSession
        
        self.EMSession.glarea.funcao_de_click = self.test_popup_menu
        #window.set_size_request(800,600)
        #self.handlers = {"on_btn_BallStick_clicked": self.glarea.switch_ball_stick,
        #                 "on_file_quit_activate":    gtk.main_quit}
        #self.builder.connect_signals(self.handlers)

        self.window.connect('key_press_event', self.EMSession.glarea.key_press)

        self.vbox = self.builder.get_object('vbox1')
        self.vbox.pack_start(self.EMSession.glarea, True, True)
        self.window.show_all()
        
        self.builder.get_object('toolbar_trajectory').hide()
        self.builder.get_object('notebook1').hide()
        
        
              #------------------------------------------------#
              #-                 WindowControl                 #
              #------------------------------------------------#
        #------------------------------------------------------------#
        self.window_control = WindowControl(self.builder)            #

        #------------------------------------------------------------#

        #--------------------- Setup ComboBoxes ---------------------#
        #                                                            #
        combobox = 'combobox1'                                       #
        combolist = ["Atom", "Residue", "Chain", "Molecule"]         #
        self.window_control.SETUP_COMBOBOXES(combobox, combolist, 1) #
        #------------------------------------------------------------#
        
        
        
        

        #------------------------------ EasyHybrid Dialogs -------------------------------------#
        #                                                                                       #
        self.TrajectoryTool = TrajectoryTool(self) 
        
        

        gtk.main()


    def test_popup_menu (self, event = None):
        """ Function doc """
        print 'aquioh'
        widget = self.builder.get_object('menu4')
        widget.popup(None, None, None, event.button, event.time)


    def on_treeview_PyMOL_Objects_button_release_event(self, tree, event):
        if event.button == 3:
            selection     = tree.get_selection()
            model         = tree.get_model()
            (model, iter) = selection.get_selected()
            if iter != None:
                self.selectedID  = str(model.get_value(iter, 1))  # @+
                self.selectedObj = str(model.get_value(iter, 2))
    
                self.builder.get_object('TreeViewObjLabel').set_label('- ' +self.selectedObj+' -' )

                widget = self.builder.get_object('treeview_menu')
                widget.popup(None, None, None, event.button, event.time)
                print 'button == 3'


        if event.button == 2:
            selection     = tree.get_selection()
            model         = tree.get_model()
            (model, iter) = selection.get_selected()
            pymol_object = model.get_value(iter, 0)
            print 'button == 2'
            
            self.selectedID  = int(model.get_value(iter, 1))  # @+
            self.EMSession.center(Vobject_index = self.selectedID -1)

        if event.button == 1:
            selection     = tree.get_selection()
            model         = tree.get_model()
            (model, iter) = selection.get_selected()
            print 'button == 1'

            if iter != None:
                #print model, iter
                pymol_object  = model.get_value(iter, 2)  # @+
                true_or_false = model.get_value(iter, 0)
                obj_index     = model.get_value(iter, 1)
                #print pymol_object
                if true_or_false == False:
                    self.EMSession.enable(int(obj_index)-1)
                    true_or_false = True
                    model.set(iter, 0, true_or_false)
                    # print true_or_false
                    self.EMSession.glarea.queue_draw()
                
                else:
                    self.EMSession.disable(int(obj_index)-1)
                    true_or_false = False
                    model.set(iter, 0, true_or_false)
                    self.EMSession.glarea.queue_draw()


    def on_menuitem1_activate(self, menuitem, click=None):
        print 'openfile'
        gtk.main_quit()
    
    
    def on_file_open_activate (self, widget, click=None):

        """ Function doc """

        main = self.builder.get_object("main_window")
        filename = None
        chooser = gtk.FileChooserDialog("Open File...", main,
                                        gtk.FILE_CHOOSER_ACTION_OPEN,
                                        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                         gtk.STOCK_OPEN, gtk.RESPONSE_OK))

        filter = gtk.FileFilter()  
        filter.set_name("PDB files - *.pdb")
        #
        filter.add_mime_type("PDB files")
        filter.add_pattern("*.pdb")
        #
        chooser.add_filter(filter)
        filter = gtk.FileFilter()
        filter.set_name("All files")
        filter.add_pattern("*")
        #
        chooser.add_filter(filter)  

        response = chooser.run()
        if response == gtk.RESPONSE_OK:
            filename = chooser.get_filename()
        chooser.destroy()
        
        self.EMSession.load(filename)

        liststore = self.builder.get_object('liststore2')
        model = liststore  
        model.clear()
        n = 0
        i = 1
        actived = False

        for Vobject in self.EMSession.Vobjects:
            
            if Vobject.actived:
                actived = True
            else:
                actived = False

            data = [actived, i        ,
                   Vobject.label      , 
                   str(len(Vobject.atoms)) , 
                   str(len(Vobject.frames)),
                   ' '                       
                   ]
            model.append(data)
            i +=1
            n = n + 1

        self.EMSession.glarea.draw_lines(self.EMSession.Vobjects[-1])


    def on_Quit_activate (self, menuitem):
            """ Function doc """
            print '''\n\nThanks for using EasyHybrid \n\n'''
            gtk.main_quit()
            #cmd.quit()
            sys.exit()


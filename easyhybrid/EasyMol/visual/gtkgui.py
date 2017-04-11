import sys
import pygtk
pygtk.require('2.0')
import gtk
#from visual_gui import FileChooserWindow
from visual.vis_parser import parse_pdb

    

class TreeviewHistory(object):
    """ Class doc """

    def __init__ (self):
        """ Class initialiser """
        pass

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
            
    def on_menuitem_center_activate (self, item):
        """ Function doc """
        
class GTKGUI:
    """ Class doc """
    
    def __init__ (self, EMSession):
        """ Class initialiser """
        #glarea = gda.GLCanvas()
        self.builder = gtk.Builder()
        self.builder.add_from_file('EasyMol/visual_gui/main_window.glade')

        self.window = self.builder.get_object('main_window')
        self.boton =  self.builder.get_object('btn_ball_stick')
        self.builder.connect_signals(self)
        
        self.EMSession = EMSession
        
        
        #window.set_size_request(800,600)
        #self.handlers = {"on_btn_BallStick_clicked": self.glarea.switch_ball_stick,
        #                 "on_file_quit_activate":    gtk.main_quit}
        #self.builder.connect_signals(self.handlers)

        self.window.connect('key_press_event', self.EMSession.glarea.key_press)

        self.vbox = self.builder.get_object('vbox1')
        self.vbox.pack_start(self.EMSession.glarea, True, True)
        self.window.show_all()
        
        self.builder.get_object('toolbar_trajectory').hide()
        gtk.main()

    '''
    def  on_treeview_history_select_cursor_parent(self, tree, path, column):
        """ Function doc """
        print 'aaaa'
        model = tree.get_model()  # @+
        iter = model.get_iter(path)  # @+
        pymol_object = model.get_value(iter, 2)  # @+
        true_or_false = model.get_value(iter, 0)


        if true_or_false == False:
            cmd.enable(pymol_object)
            true_or_false = True
            model.set(iter, 0, true_or_false)

        else:
            cmd.disable(pymol_object)
            true_or_false = False
            model.set(iter, 0, true_or_false)
    '''
    '''
    def row_activated(self, tree, path, column):

        model = tree.get_model()
        iter = model.get_iter(path)
        pymol_object = model.get_value(iter, 0)

        string2 = 'select sele, '+ pymol_object
        cmd.do(string2)
        cmd.enable('sele')
        print 'row_activated'
    '''
    
    '''
    def row_activated2(self, tree, path, column):
        #model = tree.get_model()  # @+
        #iter = model.get_iter(path)  # @+
        #ID = model.get_value(iter, 1)  # @+
        print 'row_activated2'
        
        
        model = tree.get_model()  # @+
        iter = model.get_iter(path)  # @+
        pymol_object = model.get_value(iter, 2)  # @+
        true_or_false = model.get_value(iter, 0)


        if true_or_false == False:
            #cmd.enable(pymol_object)
            true_or_false = True
            model.set(iter, 0, true_or_false)

        else:
            #cmd.disable(pymol_object)
            true_or_false = False
            model.set(iter, 0, true_or_false)
    '''
    
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
                print 'button == 3'


        if event.button == 2:
            selection     = tree.get_selection()
            model         = tree.get_model()
            (model, iter) = selection.get_selected()
            pymol_object = model.get_value(iter, 0)
            print 'button == 2'
            #string2 = 'select sele, '+ pymol_object
            #cmd.do(string2)
            #cmd.center('sele')


        if event.button == 1:
            #print "Mostrar menu de contexto botao1"
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

        #return filename
        
        print filename
        
        sys = parse_pdb(filename)
        #
        ##print sys.atoms[0].name
        ##sys.atoms[0].name = 'ATOM _ new name'
        #
        #for chain in  sys.chains:
        #    for res in sys.chains[chain].residues:
        #        for atom in sys.chains[chain].residues[res].atoms:
        #            
        #            print atom.name, atom.pos
        #
        #print sys.coords
        ##print sys.coords[0]
        #sys.coords[0] = .0
        ##print sys.coords[0]
        #print sys.coords
        #
        #
        #for chain in  sys.chains:
        #    for res in sys.chains[chain].residues:
        #        for atom in sys.chains[chain].residues[res].atoms:
        #            print atom.name, atom.pos
        
        
        
        
        sys.generate_bonds()
        
        self.EMSession.Vobjects.append(sys)


        liststore = self.builder.get_object('liststore2')
        model = liststore  
        model.clear()
        n = 0
        
        i = 1
        actived = False
        for Vobject in self.EMSession.Vobjects:
            
            if Vobject.actived:
                actived = True
                #cell = self.builder.get_object('cellrenderertext2')
                #cell.props.weight_set = True
                #cell.props.weight = pango.WEIGHT_NORMAL
            else:
                actived = False

            data = [actived, i        ,
                   Vobject.label   , 
                   Vobject.Type    , 
                   'None',
                   ' '                       
                   ]
            model.append(data)
            i +=1
            n = n + 1
        
        
        self.EMSession.glarea.load_mol()
        self.EMSession.glarea.center_on_atom(sys.mass_center)
        
        
        '''
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
        '''
    

    
    
    

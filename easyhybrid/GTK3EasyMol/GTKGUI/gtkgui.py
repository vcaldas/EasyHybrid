import gi, sys
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


class GTKGUI ():
    """ Class doc """
    
    def test_gl (self, widget):
        """ Function doc """
        self.vismolSession.glwidget.test_gl()
        
    def on_file_open_activate (self, widget, click=None):

        """ Function doc """

        main = self.builder.get_object("window1")
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
        
        print (filename)
        
        self.vismolSession.load(filename)
        
        #
        liststore = self.builder.get_object('liststore1')
        model = liststore  
        model.clear()
        n = 0
        i = 1
    
        
        
        for vis_object in self.vismolSession.vismol_objects:
            print (vis_object.name)
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
        print ('load fuction finished')
        #self.EMSession.glarea.draw_lines(self.EMSession.Vobjects[-1])
    
    
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
                widget.popup(None, None, None, event.button, event.time)
                print ('button == 3')


        if event.button == 2:
            selection     = tree.get_selection()
            model         = tree.get_model()
            (model, iter) = selection.get_selected()
            pymol_object = model.get_value(iter, 0)
            print ('button == 2', pymol_object)
            
            self.selectedID  = int(model.get_value(iter, 1))  # @+
            self.vismolSession.center(Vobject_index = self.selectedID -1)

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
    
    
    
    def __init__ (self, vismolSession = None):
        """ Class initialiser """
        #glarea = gda.GLCanvas()

        #self.glarea  = glarea
        self.builder = Gtk.Builder()
        self.builder.add_from_file('GTK3EasyMol/GTKGUI/MainWindow.glade')
        self.builder.connect_signals(self)
        
        self.window    = self.builder.get_object('window1')
        
        self.vismolSession = vismolSession
        if self.vismolSession is not None:
            self.container = self.builder.get_object('paned1')
            self.container.add(self.vismolSession.glwidget)
            self.window.connect("key-press-event", self.vismolSession.glwidget.key_pressed)
            self.window.connect("key-release-event", self.vismolSession.glwidget.key_released)

        self.window.connect("delete-event",    Gtk.main_quit)
        self.window.show_all()
        Gtk.main()
        
        
        
        
        #window.set_size_request(800,600)
        #self.handlers = {"on_btn_BallStick_clicked": self.glarea.switch_ball_stick,
        #                 "on_file_quit_activate":    gtk.main_quit}
        #self.builder.connect_signals(self.handlers)

        #self.window.connect('key_press_event', self.EMSession.glarea.key_press)

        #self.vbox = self.builder.get_object('vbox1')
        #self.vbox.pack_start(self.EMSession.glarea, True, True)
        #self.window.show_all()
        
        #self.builder.get_object('toolbar_trajectory').hide()
        #self.builder.get_object('notebook1').hide()
        
        
              #------------------------------------------------#
              #-                 WindowControl                 #
              #------------------------------------------------#
        ##------------------------------------------------------------#
        #self.window_control = WindowControl(self.builder)            #
        #
        ##------------------------------------------------------------#
        #
        ##--------------------- Setup ComboBoxes ---------------------#
        ##                                                            #
        #combobox = 'combobox1'                                       #
        #combolist = ["Atom", "Residue", "Chain", "Molecule"]         #
        #self.window_control.SETUP_COMBOBOXES(combobox, combolist, 1) #
        ##------------------------------------------------------------#

import gi, sys
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


class AnimatedWindow:
    """ Class doc """
    
    def __init__ (self, main_window):
        """ Class initialiser """
        self.actived =  False
        self.main_window = main_window
        #self.EMSession =  GTKSession.EMSession
    
    def open_window (self, text = None):
        """ Function doc """
        if self.actived  ==  False:
            self.builder = Gtk.Builder()
            self.builder.add_from_file('GTK3EasyMol/GTKGUI/AnimateTrajectory.glade')
            
            self.window = self.builder.get_object('animate_window')
            self.builder.connect_signals(self)
            
            self.window.show_all()
            self.window.set_keep_above (self.window)

            scale = self.builder.get_object("scale1")  
            scale.set_range(1, 1000)                               
            scale.set_increments(1, 10)                           
            actual_frame = int(self.main_window.vismolSession.get_frame())
            scale.set_digits(1)

            scale.set_digits(actual_frame)                        
            #gtk.main()

    def on_TrajectoryTool_HSCALE_update (self, MIN = 1, MAX = 100):
        """ Function doc """
        #MAX  = int(self.builder.get_object('trajectory_max_entrey').get_text())
        #MIN  = int(self.builder.get_object('trajectory_min_entrey').get_text())

        scale = self.builder.get_object("scale1")
        scale.set_range(MIN, MAX)
        scale.set_increments(1, 10)
        scale.set_digits(1)
    
    def on_TrajectoryTool_BarSetFrame(self, hscale, text= None,  data=None):            # SETUP  trajectory window
        valor = hscale.get_value()
	
        if self.main_window.vismolSession != None:
            self.main_window.vismolSession.set_frame(int(valor-1))
            #self.main_window.vismolSession.glwidget.queue_draw()
        else:
            print (valor)

    def on_animate_trajectory_window_destroy(self, widget):
        """ Function doc """
        self.actived  =  False
        self.main_window.builder.get_object('toolbutton_trajectory_tool').set_active(False)










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
    
    
    def on_main_toolbar_open_animate_trajectory (self, widget):
        """ Function doc """
        #animated_window = AnimatedWindow(self)
        if widget == self.builder.get_object('toolbutton_trajectory_tool'):
            if widget.get_active() == True:
                self.TrajectoryTool.open_window()
                self.TrajectoryTool.actived =  True
            else:
                print ('desligado')
                self.TrajectoryTool.window.destroy()
                self.TrajectoryTool.actived =  False
                #cmd.set('valence', 0.0)
                #self.builder.get_object('handlebox1').hide()
    
    def on_treemenu_item_selection (self, widget):
        """ Function doc """
        #print ( widget)
        if widget == self.builder.get_object('menuitem6_center'):
            print(widget)
        if widget == self.builder.get_object('menuitem5_rename'):
            tree      = self.builder.get_object('treeview1')
            selection = tree.get_selection()
            model = tree.get_model()
            (model, iter) = selection.get_selected()
            obj_index = model.get_value(iter, 1)
            #self.vismolSession.glwidget.edit_molecule()
            print(widget,"<=es el widget",obj_index,model  )
            #coord = np.array(coord, dtype=np.float32) 
            #self.vismolSession.glwidget.center_on_atom(coord)
        
    def on_resize (self, widget):
        """ Function doc """
        print(widget)
        print(self.window.get_size ())
    
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
            #self.container = self.builder.get_object('box4')

            self.container.add(self.vismolSession.glwidget)
            self.window.connect("key-press-event", self.vismolSession.glwidget.key_pressed)
            self.window.connect("key-release-event", self.vismolSession.glwidget.key_released)

        self.window.connect("delete-event",    Gtk.main_quit)
        self.window.show_all()
        
        #animated_window = AnimatedWindow(self)
        self.TrajectoryTool = AnimatedWindow(self)
        #self.window.set_keep_above (self.window)
        #self.builder.get_object('notebook2').hide()
        #self.builder.get_object('notebook1').hide()
        #self.builder.get_object('statusbar1').hide()
        
        #print (a ,b, " <----------aqui oh")
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

import gi, sys
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


class GTKGUI ():
    """ Class doc """


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
        
        #self.EMSession.glarea.draw_lines(self.EMSession.Vobjects[-1])
    
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
            self.window.connect("key-press-event", self.vismolSession.glwidget.key_press)

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

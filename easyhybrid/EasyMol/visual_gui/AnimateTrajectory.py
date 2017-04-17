import gtk

class GTKGUI :
    """ Class doc """
    
    def __init__ (self, EMSession):
        """ Class initialiser """
        #glarea = gda.GLCanvas()
        self.builder = gtk.Builder()
        self.builder.add_from_file('AnimateTrajectory.glade')

        self.window = self.builder.get_object('window1')
        #self.boton =  self.builder.get_object('btn_ball_stick')
        #self.builder.connect_signals(self)
        #
        #self.EMSession = EMSession
        #
        #self.EMSession.glarea.funcao_de_click = self.test_popup_menu
        ##window.set_size_request(800,600)
        ##self.handlers = {"on_btn_BallStick_clicked": self.glarea.switch_ball_stick,
        ##                 "on_file_quit_activate":    gtk.main_quit}
        ##self.builder.connect_signals(self.handlers)
        #
        #self.window.connect('key_press_event', self.EMSession.glarea.key_press)
        #
        #self.vbox = self.builder.get_object('vbox1')
        #self.vbox.pack_start(self.EMSession.glarea, True, True)
        self.window.show_all()
        #
        #self.builder.get_object('toolbar_trajectory').hide()
        #self.builder.get_object('notebook1').hide()
        
        

        gtk.main()


def main():
    
    #EasyMol = EasyMolSession()
    gtkgui  = GTKGUI(None)


if __name__ == '__main__':
    main()

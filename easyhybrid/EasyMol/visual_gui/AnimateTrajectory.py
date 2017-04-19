import gtk

class TrajectoryTool :
    """ Class doc """
    
    def __init__ (self, GTKSession):
        """ Class initialiser """
        
	self.actived =  False
	self.GTKSession = GTKSession
	#self.EMSession =  GTKSession.EMSession

    def open_window (self, text = None):
        """ Function doc """
        if self.actived  ==  False:
            self.builder = gtk.Builder()
            self.builder.add_from_file('EasyMol/visual_gui/AnimateTrajectory.glade')
            
	    self.window = self.builder.get_object('window1')
	    self.builder.connect_signals(self)
	    self.window.show_all()
	    
	    scale = self.builder.get_object("trajectory_hscale")  
	    scale.set_range(1, 100)                               
	    scale.set_increments(1, 10)                           
	    actual_frame = int(self.GTKSession.EMSession.get_frame())
	    scale.set_digits(actual_frame)                        
	    gtk.main()

    def on_TrajectoryTool_HSCALE_update (self, MIN = 1, MAX = 100):
        """ Function doc """
        #MAX  = int(self.builder.get_object('trajectory_max_entrey').get_text())
        #MIN  = int(self.builder.get_object('trajectory_min_entrey').get_text())

        scale = self.builder.get_object("trajectory_hscale")
        scale.set_range(MIN, MAX)
        scale.set_increments(1, 10)
        scale.set_digits(0)
    
    def on_TrajectoryTool_BarSetFrame(self, hscale, text= None,  data=None):            # SETUP  trajectory window
        valor = hscale.get_value()
	
	if self.GTKSession.EMSession != None:
	    self.GTKSession.EMSession.set_frame(int(valor-1))
	else:
	    print valor

    def on_animate_trajectory_window_destroy(self, widget):
        """ Function doc """
        self.actived  =  False
	self.GTKSession.builder.get_object('toolbutton_trajectory_tool').set_active(False)

def main():
    #EasyMol = EasyMolSession()
    trajectoryTool  = TrajectoryTool(None)


if __name__ == '__main__':
    main()

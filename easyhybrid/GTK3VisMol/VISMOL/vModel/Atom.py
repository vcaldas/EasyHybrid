import VISMOL.vModel.atom_types as at 

#GTK3EasyMol/VISMOL/Model/atom_types.py
class Atom:
    """ Class doc """
    
    def __init__ (self, name         ='Xx',
                        index        =None, 
                        symbol       ='X', 
                        pos          = None, 
                        resi         = None, 
                        resn         = None, 
                        chain        = '', 
                        atom_id      = 0, 
                        residue      = None,
                        #Vobject_id   = None, 
                        #Vobject_name = '', 
                        Vobject      = None):
        """ Class initialiser """
        
        if pos is None:
            pos = np.array([0.0, 0.0, 0.0])
        
        self.pos          = pos                   # - coordinates of the first frame
        self.index        = index                 # 
        self.name         = name                  #
        self.symbol       = symbol                #
        self.resi         = resi                  #
        self.resn         = resn                  #
        self.chain        = chain                 #
        #self.Vobject_id   = Vobject_id            #
        #self.Vobject_name = Vobject_name          #
        self.Vobject      = Vobject
        self.residue      = residue                                
        
        self.atom_id      = atom_id               # An unique number

        self.color        = at.get_color    (name)
        #self.color.append(0.0)  
            
        self.col_rgb      = at.get_color_rgb(name)
        self.radius       = at.get_radius   (name)
        self.vdw_rad      = at.get_vdw_rad  (name)
        self.cov_rad      = at.get_cov_rad  (name)
        self.ball_radius  = at.get_ball_rad (name)

        self.lines          = True
        self.dots           = False
        self.ribbons        = False
        self.ball_and_stick = False
        self.sticks         = False
        self.spheres        = False
        self.surface        = False
        self.connected      = []
    
    def coords (self):
        """ Function doc """
        frame  = self.Vobject.vismol_session.glwidget.vm_widget.frame
        
        coords = [self.Vobject.frames[frame][(self.index-1)*3  ],
                  self.Vobject.frames[frame][(self.index-1)*3+1],
                  self.Vobject.frames[frame][(self.index-1)*3+2],]
        
        return coords

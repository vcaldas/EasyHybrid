
class Model:
    """ Class doc """
    
    def __init__ (self):
        """ Class initialiser """
        self.chains = []
        self.bonds  = []
        self.frame  = 0
        self.mass_center = [0,0,0]

class Chain:
    """ Class doc """
    
    def __init__ (self):
        """ Class initialiser """
        
        self.residues   = []
        self.chain_name = ''  # one letter code -> like chain "A" or "X"
        
class Residue:
    """ Class doc """
    
    def __init__ (self):
        """ Class initialiser """
        
        self.atoms = []
        self.resn  = 'UNK'
        self.resi  = None
        self.chain = None

class Atom:
    """ Class doc """
    
    def __init__ (self):
        """ Class initialiser """
        #---------------------------------------------------------------
        #                        property
        #---------------------------------------------------------------
        self.pos     = [0,0,0]      # position x,y,z
        self.index   = None         # atom index 
        self.name    = 'UNK'        # atom name ->   like "CA" carbom
        self.symbol  = None         # atom symbol -> like "C"  carbom
        self.charge  = None         # partial charge  
        self.resn    = None         # residue name
        self.resi    = None         # residue index
        self.chain   = None         # chain ID
        #---------------------------------------------------------------

        
        #---------------------------------------------------------------
        #                    representation
        # 
        #---------------------------------------------------------------
        self.sphere   = False      #
        self.stick    = False      #
        self.vdw      = False      #
        self.lines    = False      #
        self.surface  = False      #
        self.dots     = False      #
        #---------------------------------------------------------------


class EasyMolObject2:
    """ Class doc """
    
    def __init__ (self):
        """ Class initialiser """
        
        
        
        
        


class EasyMolObject():
    """ Class doc """
    
    def __init__ (self, label = 'NewObject'):
        """ Class initialiser """
        self.activate    = True
        self.label       = label
                         
        #self.data       = None
        self.pos         = []
        self.a_color     = None
        self.a_name      = None
        self.a_symbol    = None
        self.a_number    = None
        self.a_charge    = None
        self.mass_center = [0,0,0]
        
        self.sphere   = None
        self.stick    = None
        self.vdw      = None
        self.lines    = None
        self.a_size   = None
        self.bonds    = None
        
        #--------------------------- NEW ------------------------------#
        self.models   = []
        self.a_size   = None
        #--------------------------------------------------------------#



'''
@<TRIPOS>MOLECULE
*****
 8 7 0 0 0
SMALL
GASTEIGER

@<TRIPOS>ATOM
      1 C          -0.4467    0.9180   -0.0478 C.3     1  LIG1        0.0331
      2 C           0.7345   -0.0217    0.0770 C.2     1  LIG1        0.3016
      3 O           1.8603    0.4381   -0.0254 O.2     1  LIG1       -0.2513
      4 O           0.5903   -1.3496    0.2982 O.3     1  LIG1       -0.4808
      5 H          -0.2672   -1.7832    0.3906 H       1  LIG1        0.2950
      6 H          -0.0940    1.9134   -0.2197 H       1  LIG1        0.0342
      7 H          -1.0191    0.8934    0.8559 H       1  LIG1        0.0342
      8 H          -1.0616    0.6109   -0.8679 H       1  LIG1        0.0342
@<TRIPOS>BOND
     1     2     1    1
     2     2     3    2
     3     2     4    1
     4     4     5    1
     5     1     6    1
     6     1     7    1
     7     1     8    1

'''
           #0   1        2          3          4      5    6     7        8 
molecule =[[1, 'C',  -0.4467,    0.9180,   -0.0478, 'C.3', 1, 'LIG1',  0.0331],
           [2, 'C',   0.7345,   -0.0217,    0.0770, 'C.2', 1, 'LIG1',  0.3016],
           [3, 'O',   1.8603,    0.4381,   -0.0254, 'O.2', 1, 'LIG1', -0.2513],
           [4, 'O',   0.5903,   -1.3496,    0.2982, 'O.3', 1, 'LIG1', -0.4808],
           [5, 'H',  -0.2672,   -1.7832,    0.3906, 'H  ', 1, 'LIG1',  0.2950],
           [6, 'H',  -0.0940,    1.9134,   -0.2197, 'H  ', 1, 'LIG1',  0.0342],
           [7, 'H',  -1.0191,    0.8934,    0.8559, 'H  ', 1, 'LIG1',  0.0342],
           [8, 'H',  -1.0616,    0.6109,   -0.8679, 'H  ', 1, 'LIG1',  0.0342]]





def __main__ ():
    """ Function doc """
    obj = EasyMolObject()
  
    
if __main__:
    __main__()
    
    


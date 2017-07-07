import numpy as np
import time
import os
import multiprocessing as mp

#import VISMOL.Model.cfunctions as cfunctions
#import VISMOL.Model.Chain as Chain
from VISMOL.vModel.Chain      import Chain
from VISMOL.vModel.Residue    import Residue
from VISMOL.vModel.cfunctions import C_generate_bonds
#import VISMOL.Model as model



class VismolObject:
    """ Class doc """
    
    def __init__ (self, 
                  name       = 'UNK', 
                  atoms      = [],
                  EMSession  = None, 
                  trajectory = None):
        
        """ Class initialiser """
        self.EMSession = EMSession
        self.actived            = False       
        self.Type               = 'molecule'
        self.name               = name#self._get_name(name)

        
        self.atoms              = atoms
        self.residues           = []
        self.chains             = {}
                                
        self.bonds              = []
        self.frames             = trajectory
        self.mass_center        = np.array([0.0, 0.0, 0.0])

        self.atom_unique_id_dic = {}
        self.index_bonds        = None
       
        self._generate_chain_structure()
        self._generate_atom_unique_color_id()
        self._generate_bonds()
        
        #self._generate_colors()
        
        """   L I N E S   """
        #self.line_representation = LineRepresentation(self)
        #self.line_representation.update()

        """   F L A T   S P H E R E   """
        #self.flat_sphere_representation = FlatSphereRepresentation(self)
        print ('frames:     ', len(self.frames))
        print ('frame size: ', len(self.frames[0]))
        
        # OpenGL attributes
        self.dots_vao = None
        self.lines_vao = None
        self.spheres_vao = None
        self.dot_buffers = None
        self.line_buffers = None
        self.sphere_buffers = None
        self.dot_indexes = None
        self.model_mat = np.identity(4, dtype=np.float32)
        self.normal_mat = np.identity(3, dtype=np.float32)
    
    def generate_dot_indexes(self):
        """ Function doc
        """
        self.dot_indexes = []
        for i in range(int(len(self.atoms))):
            self.dot_indexes.append(i)
        self.dot_indexes = np.array(self.dot_indexes, dtype=np.uint16)
    
    def _generate_chain_structure (self):
        """ Function doc """
        print ('\ngenerate_chain_structure starting')
        initial          = time.time()
        
        parser_resi  = None
        parser_resn  = None
        chains_m     = {}

        sum_x   = 0
        sum_y   = 0
        sum_z   = 0
        frame   = []
        
        index   = 1
        
        for atom in self.atoms:
        
            #self.atoms[self.atoms.index(atom)].index   = index
            #self.atoms[self.atoms.index(atom)].atom_id = counter
            #print  (self.atoms[self.atoms.index(atom)].atom_id)
            atom.index   = index
            atom.atom_id = self.EMSession.atom_id_counter
            atom.Vobject =  self
            if atom.chain in self.chains.keys():
                ch = self.chains[atom.chain]
                #print 'existe'
            
            else:
                ch = Chain(name = atom.chain, label = 'UNK')
                self.chains[atom.chain] = ch
                #print 'n existe'

            if atom.resi == parser_resi:# and at_res_n == parser_resn:
                atom.residue = ch.residues[-1]
                ch.residues[-1].atoms.append(atom)
                frame.append([atom.pos[0],atom.pos[1],atom.pos[2]])

            else:
                residue = Residue(name=atom.resn, index=atom.resi, chain=atom.chain)
                atom.residue     = residue
                residue.atoms.append(atom)
                
                ch.residues.append(residue)
                frame.append([atom.pos[0],atom.pos[1],atom.pos[2]])
                parser_resi  = atom.resi
                parser_resn  = atom.resn


            if atom.name == 'CA':
                ch.backbone.append(atom)

            self.EMSession.atom_dic_id[self.EMSession.atom_id_counter] = atom
            
            sum_x += atom.pos[0]
            sum_y += atom.pos[1]
            sum_z += atom.pos[2]
            index   +=1
            self.EMSession.atom_id_counter +=1
            
        #self.frames.append(frame)
        total = len(self.atoms)
        self.list_atom_lines          = [True ]*total
        self.list_atom_ribbons        = [False]*total
        self.list_atom_dots           = [False]*total
        self.list_atom_sticks         = [False]*total
        self.list_atom_spheres        = [False]*total
        self.list_atom_surface        = [False]*total
        self.list_atom_ball_and_stick = [False]*total
        self.mass_center[0] = sum_x / total
        self.mass_center[1] = sum_y / total
        self.mass_center[2] = sum_z / total
        final = time.time() 
        print ('generate_chain_structure end -  total time: ', final - initial, '\n')
        return True

    def _get_name (self, name):
        """ Function doc """
        self.name  = os.path.basename(name)
        #self.name  = name.split('.')
        #self.name  = self.name[0]
    
    def _generate_bonds (self):
        """ Function doc """
        print ('\ngenerate_bonds starting')
        initial          = time.time()
        self.index_bonds = C_generate_bonds(self.atoms)
        final = time.time() 
        print ('generate_bonds end -  total time: ', final - initial, '\n')

    def _generate_atom_unique_color_id (self):
        self.coordinates_color_ids  = []        
#        self.atom_unique_id_dic     = {}

        """ Function doc """
        for atom in self.atoms:
            i = atom.atom_id
            r = (i & 0x000000FF) >>  0
            g = (i & 0x0000FF00) >>  8
            b = (i & 0x00FF0000) >> 16
           
            self.coordinates_color_ids.append(r/255.0)
            self.coordinates_color_ids.append(g/255.0)
            self.coordinates_color_ids.append(b/255.0)
            
            pickedID = r + g * 256 + b * 256*256
            print (pickedID)
            self.EMSession.atom_dic_id[pickedID] = atom
            #self.atom_unique_id_dic[pickedID] = atom
        self.coordinates_color_ids = np.array(self.coordinates_color_ids, dtype=np.float32)
        
    def _generate_colors  (self):
        """ Function doc """
        #self.bond_colors           = []
        #for bond in self.index_bonds:
        #    atom1    = self.atoms[bond[0]]
        #    atom2    = self.atoms[bond[1]]
        #    # checking if the selection is actived
        #    if  atom1.lines and atom2.lines:
        #        ## colors
        #        self.bond_colors.append(atom1.color[0])        
        #        self.bond_colors.append(atom1.color[1])        
        #        self.bond_colors.append(atom1.color[2])  
        #        
        #        self.bond_colors.append(atom1.color[0])        
        #        self.bond_colors.append(atom1.color[1])        
        #        self.bond_colors.append(atom1.color[2])
        #        
        #        self.bond_colors.append(atom2.color[0])        
        #        self.bond_colors.append(atom2.color[1])        
        #        self.bond_colors.append(atom2.color[2])
        #        
        #        self.bond_colors.append(atom2.color[0])        
        #        self.bond_colors.append(atom2.color[1])        
        #        self.bond_colors.append(atom2.color[2])
        #
        #self.bond_colors  = np.array(self.bond_colors, dtype=np.float32)
    
        
        self.coordinates_colors = []        
        for atom in self.atoms:
            #if atom.dots:
            #-------------------------------------------------------
            #                        D O T S
            #-------------------------------------------------------
            self.coordinates_colors.append(atom.color[0])        
            self.coordinates_colors.append(atom.color[1])        
            self.coordinates_colors.append(atom.color[2])   
            #self.coordinates_colors.append(atom.color[3])   

        self.coordinates_colors  = np.array(self.coordinates_colors, dtype=np.float32)
    

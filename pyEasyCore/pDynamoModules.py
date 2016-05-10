# pDynamo
from pBabel           import *
from pCore            import *
from pMolecule        import *
from pMoleculeScripts import *
from EasyMol          import EasyMolObject


#------------------------------------------------------------------------------
from AtomTypes import ATOMTYPES
#------------------------------------------------------------------------------

def GetFileType(filename):
    file_type = filename.split('.')
    return file_type[-1]







        



class NewProject(object):
    """ Class doc """
    
    def __init__ (self):
        """ Class initialiser """
        pass
    
    def set_AMBER_MM(self, amber_params, amber_coords, dualLog=None):
        self.system = AmberTopologyFile_ToSystem(amber_params, dualLog)
        self.load_coordinate_file_to_system(amber_coords, dualLog=None)
        self.settings['force_field'] = "AMBER"
        self.settings['parameters']  = amber_params
        self.settings['coordinates'] = amber_coords
        self.settings['potencial']   = "MM"

    def set_CHARMM_MM(self, charmm_params, charmm_topologies, dualLog=None):
        #coords     =  '/home/fernando/programs/pDynamo-1.9.0/pBabel-1.9.0/data/charmm/ava.chm'

        #print charmm_params
        #print charmm_topologies
		
        parameters  = CHARMMParameterFiles_ToParameters([charmm_params])
        self.system = CHARMMPSFFile_ToSystem(charmm_topologies, isXPLOR=True, parameters=parameters)
        #self.system.coordinates3 = CHARMMCRDFile_ToCoordinates3 ( coords )

        #system.coordinates3 = CHARMMCRDFile_ToCoordinates3 ( coords )
        #coords     = '/home/fernando/programs/pDynamo-1.9.0/pBabel-1.9.0/data/charmm/ava.chm'

        #self.system.coordinates3 = CHARMMCRDFile_ToCoordinates3 ( coords )
        #Pickle('old.pkl', self.system)
        
        
        self.settings['force_field'] = "CHARMM"
        self.settings['parameters']  = charmm_params
        self.settings['topology']    = charmm_topologies
        self.settings['potencial']   = "MM"

    def set_GROMACS_MM(self, gromacs_params, gromacs_coords, dualLog=None):

        parameters = GromacsParameters_ToParameters(
            gromacs_params,  log=dualLog)
        self.system = GromacsDefinitions_ToSystem(
            gromacs_params,  log=dualLog, parameters=parameters)
        self.system.coordinates3 = GromacsCrdFile_Process(
            gromacs_coords,  system=self.system,  log=dualLog)

        self.settings['force_field'] = "GROMACS"
        self.settings['potencial']   = "MM"
        self.settings['parameters']  = gromacs_params
        self.settings['coordinates'] = gromacs_coords

    def set_OPLS_MM(self, opls_params, opls_coords,  dualLog=None):

        path_levels = opls_params.split("/")
        path = "/"

        for level in path_levels:
            # "if the parameters directory is included, does not consider"
            if level != path_levels[-1]:
                path = path + '/' + level

        print "Your path is ", path
        print "your parameters are: ", path_levels[-1]

        mmModel = MMModelOPLS(path_levels[-1], path=path)

        file_type = opls_coords.split(".")
        file_type = file_type[-1]

        if file_type == "mol":
            self.system = MOLFile_ToSystem(
                os.path.join(opls_coords), log=dualLog)

        elif file_type == "pdb":
            self.system = PDBFile_ToSystem(opls_coords, 
                                           log=dualLog, 
                                           #modelNumber=1, 
                                           useComponentLibrary=True)

        elif file_type == "mol2":
            self.system = MOL2File_ToSystem(
                os.path.join(opls_coords), log=dualLog)

        self.system.DefineMMModel(mmModel)
        self.settings['force_field'] = "OPLS"
        self.settings['potencial']   = "MM"
        self.settings['parameters']  = opls_params
        self.settings['coordinates'] = opls_coords

    def Create_New_Project(self, name = "UNK",  # str
                           data_path  = None,  # str
                           FileType   = None,  # str
                           filesin    = None,  # dictionary
                           BufferText = None):  # buffertext
        """ Function doc """

        self.name = name

        if data_path is not None:
            self.settings['data_path'] = data_path

        FileType = FileType
        filesin = filesin

        if FileType == "AMBER":
            amber_params = filesin['amber_params']
            amber_coords = filesin['amber_coords']
            self.set_AMBER_MM(amber_params, amber_coords, self.dualLog)
            self.set_nbModel_to_system()

        elif FileType == "CHARMM":
            charmm_params     = filesin['charmm_params']
            charmm_topologies = filesin['charmm_topologies']
            charmm_coords     = filesin['charmm_coords']
            
            self.set_CHARMM_MM(charmm_params, charmm_topologies, self.dualLog)
            filetype = self.load_coordinate_file_to_system(charmm_coords, self.dualLog)
            self.set_nbModel_to_system()

        elif FileType == "GROMACS":
            gromacs_params = filesin['gromacs_params']
            gromacs_coords = filesin['gromacs_coords']

            self.set_GROMACS_MM(gromacs_params, gromacs_coords, self.dualLog)
            self.set_nbModel_to_system()

        elif FileType == "OPLS":
            opls_params = filesin['opls_params']
            opls_coords = filesin['opls_coords']
            self.set_OPLS_MM(opls_params, opls_coords, self.dualLog)
            self.set_nbModel_to_system()

        elif FileType == "pDynamo files(*.pkl,*.yaml)":
            NewSystem = filesin["pDynamoFile"]					#
            self.load_new_system(NewSystem)

        elif FileType == "Other(*.pdb,*.xyz,*.mol2...)":
            NewSystem = filesin["coordinates"]					#
            self.load_new_system(NewSystem)

        #print BufferText
        self.system.label = name
        
        if self.EasyHybridMain:
            print 'EasyHybridMain'
            self.EasyHybridMain.show_EasyMol_objects()
        else:
            print 'EasyHybridMain = None'
        #self.From_PDYNAMO_to_EasyHybrid(type_='new')
    def DeleteActualProject (self):
        """ Function doc """
        pass
        '''
        self.settings = {
                       'add_info'     : None,
                       'force_field'  : None,
                       'parameters'   : None,
                       'topology'     : None,
                       'coordinates'  : None,
                       
                       'nbModel_type' : 'NBModelABFS',
                       #'nbModel'      : "NBModelABFS()",
                       'ABFS_options' : {"innerCutoff": 8.0, "outerCutoff": 12.0, "listCutoff": 13.5},
                       'types_allowed': {'pdb': True, 'xyz': False, 'mol2': False},
        
                       'prune_table'  : [],
                       'fix_table'    : [],
                       'qc_table'     : [],
                       
                       'QC'           : False,
                       'potencial'    : None,
                       'qc_method'    : None,
                       
                       'data_path'    : None,   # estah sendo usado 
                       'step'         : 0,
                       'last_step'    : None,
                      
                       
                       
                       'job_history'  :{
                                       # actual style
                                       #'1': ['Step_1', 'new', '"AMBER/AM1/ABFS"', '43', 'black']  
                                       
                                       # new propose
                                       #'1': {                                                      
                                       #      'object'    : 'Step1'           ,
                                       #      'type'      : 'new/min/dyn/prn' ,
                                       #      'parameters': parameters        ,       -  extracted from the log -  checksystem
                                       #      'potencial' : "AMBER/AM1/ABFS"  ,
                                       #      'CQatoms'   : '43'              ,
                                       #      'color'     : 'black'
                                       #     }
                                       },
                       
                       'PyMOL_Obj'     : None,
                       'filename'      : None,   # ex.  /home/fernando/pDynamoWorkSpace/Enolase_Dec_11_2014/projectBaseName
                       'pymol_session' : None,   #    - pdynamo pkl/yaml file
                       'pDynamo_system': None    #    - pymol pse file
                       } 
        self.nbModel         = 'NBModelABFS()'
        self.ABFS_options    = {"innerCutoff": 8.0, "outerCutoff": 12.0, "listCutoff": 13.5}
        self.parameters      = None
        self.system          = None          
        #self.PyMOL           = PyMOL         
        self.dualLog         = None          
        #self.builder         = builder       
        #self.window_control  = window_control
        #self.ActiveMode      = False 
        self.pdbInfo         = {}
        '''




class pDynamoSession(NewProject):
    """ Class doc """
    def __init__ (self, EasyHybridMain = None):
        
        self.EasyHybridMain = EasyHybridMain
        #print EasyHybridMain , 'aqui'
        #-----------------------------------------------
        self.system                 = None     # a pdynamo system itself
        self.settings               = {}
        self.settings['prune_table']= []
        self.settings['fix_table']  = []
        self.settings['qc_table']   = []
        self.settings['QC']         = False
        self.easymol_objects        = []       # objects that will be render (like pymol objects list)
        #-----------------------------------------------

        #-------------------------------------------
        # essas variaveis nao deveriam estar por aqui
        self.data        = None
        self.bonds       = None
        self.mass_center = [0,0,0]
        #-------------------------------------------
        self.dualLog  = None         
    
    def load_coordinate_file_as_new_system(self, filename, dualLog=None):
        #self.settings['prune_table']= []
        #self.settings['fix_table']  = []
        #self.settings['qc_table']   = []
        #self.settings['QC']         = False
        print filename
        type_ = GetFileType(filename)
        print type_

        if type_ == "xyz":
            self.system = XYZFile_ToSystem(filename,  dualLog)
        
        elif type_ == "pdb":
            self.system = PDBFile_ToSystem(filename,  log=dualLog)

        elif type_ == "cif":
            self.system = mmCIFFile_ToSystem(filename,  dualLog)

        elif type_ == "mop":
            self.system = MopacInputFile_ToSystem(filename,  dualLog)

        elif type_ == "mol":
            self.system = MOLFile_ToSystem(filename, log=dualLog)

        # --- pkl ---

        elif type_ == "pkl":
            self.system = Unpickle(filename)
            try:
                self.settings[
                    'fix_table'] = list(self.system.hardConstraints.fixedAtoms)
                # print 'fix_table = :',self.settings['fix_table']
            except:
                a = None

            try:
                qc_table = list(
                    self.system.energyModel.qcAtoms.QCAtomSelection())
                boundaryAtoms = list(
                    self.system.energyModel.qcAtoms.BoundaryAtomSelection())

                self.settings['boundaryAtoms'] = boundaryAtoms
                # print 'qc_table : '  , qc_table
                #print 'boundaryAtoms', (boundaryAtoms)

                qc = []
                for l in qc_table:
                    if l in boundaryAtoms:
                        pass
                        #print l
                    else:
                        qc.append(l)

                self.settings['qc_table'] = qc
                self.settings['QC']       = True
                #print 'qc_table : ', self.settings['qc_table']

            except:
                print "System has no QC atoms"
            
       
        # --- yaml ---

        elif type_ == "yaml":
            self.system = YAMLUnpickle(filename)

            try:
                self.settings['fix_table'] = list(
                    self.system.hardConstraints.fixedAtoms)
                #print 'fix_table = :', self.settings['fix_table']
            except:
                a = None

            try:
                qc_table = list(
                    self.system.energyModel.qcAtoms.QCAtomSelection())
                boundaryAtoms = list(
                    self.system.energyModel.qcAtoms.BoundaryAtomSelection())

                self.settings['boundaryAtoms'] = boundaryAtoms
                #print 'qc_table : '  , qc_table
                #print 'boundaryAtoms', (boundaryAtoms)

                qc = []
                for l in qc_table:
                    if l in boundaryAtoms:
                        pass
                        #print l
                    else:
                        qc.append(l)

                self.settings['qc_table'] = qc
                self.settings['QC']     = True
                #print 'qc_table : ', self.settings['qc_table']
            except:
                print "System has no QC atoms"

        else:
            return "ops!"
        try:
            self.system.Summary(dualLog)
        except:
            print "system empty"

        return type_
        
    def load_new_system (self, filename = None):
        """ Function doc """
        #---------------------------------------------------------------
        #                        P D Y N A M O
        #---------------------------------------------------------------
        self.load_coordinate_file_as_new_system(filename = filename, dualLog=None)
        self.system.Summary()
        
        easymol_object = EasyMolObject()
        self.building_atom_matrix(easymol_object = easymol_object)
        self.build_bonds         (easymol_object =easymol_object)
        easymol_object.activate =True
        self.easymol_objects.append(easymol_object)
        print len(self.easymol_objects)
                    
    def building_atom_matrix (self, easymol_object =  None):
        """ Function doc """
        import numpy as np
        xyz         = self.system.coordinates3
        m_size      = self.system.coordinates3.size/3
        
        
        self.data   = np.zeros(m_size, [('a_position', np.float32, 3),
                                        ('a_color'   , np.float32, 3),
                                        ('a_name'    , np.str,     1),
                                        ('a_symbol'  , np.str,     1),
                                        ('a_number'  , np.float32, 1),
                                        ('a_charge'  , np.float32, 1),
                                        ('sphere'    , np.bool,  True),
                                        ('stick'     , np.bool,  True),
                                        ('vdw'       , np.bool,  True),
                                        ('line'      , np.bool,  True),
                                        ('a_size'    , np.float32, 1)])
        
        for index in range(m_size):
            self.data['a_position'][index][0] = xyz[index][0]
            self.data['a_position'][index][1] = xyz[index][1]
            self.data['a_position'][index][2] = xyz[index][2]
            self.mass_center[0] += xyz[index][0]
            self.mass_center[1] += xyz[index][1]
            self.mass_center[2] += xyz[index][2]
          
            #-----    S P H E R E S    -----
            
            if index in self.settings['qc_table']:
                self.data['sphere'][index] = True
            
            #-----    L I N E S    -----
            self.data['line'][index] =  True
            
            atom = self.system.atoms[index]
            self.data['a_name'][index] = atom.label

            if self.data['a_name'] [index]== "H":
                self.data['a_size'][index] = 0.25
            else:
                self.data['a_size'][index] = 0.4
            try:
                self.data['a_color'][index] = ATOMTYPES[self.data['a_name'][index]][3]
            except:
                print self.data['a_name'], index
                self.data['a_color'][index] = [0,5,5] 
            
            
        self.mass_center[0] = self.mass_center[0]/m_size
        self.mass_center[1] = self.mass_center[1]/m_size
        self.mass_center[2] = self.mass_center[2]/m_size
        
        easymol_object.pos = []
        easymol_object.pos.append(self.data['a_position'])
        easymol_object.a_color     = self.data['a_color'   ]
        easymol_object.a_name      = self.data['a_name'    ]
        easymol_object.a_symbol    = self.data['a_symbol'  ]
        easymol_object.a_number    = self.data['a_number'  ]
        easymol_object.a_charge    = self.data['a_charge'  ]
        easymol_object.a_size      = self.data['a_size'  ]
        
        
        easymol_object.sphere      = self.data['sphere']
        easymol_object.lines       = self.data['line']

        easymol_object.mass_center = self.mass_center

    def build_bonds (self,  easymol_object = None):
        """ Function doc """


        #self.zpr.x_total = mass_center[0]
        #self.zpr.y_total = mass_center[1]
        #self.zpr.z_total = mass_center[2]
        #self.zpr.zero    = data['a_position']
        #self.zpr.MassReferencePoint[mass_center[0],
        #                            mass_center[1],
        #                            mass_center[2],0.]
        
        
        #---------------------------------------------------------------
        #                        GETING CONNECTIONS
        #---------------------------------------------------------------
        print "---------------------------------------------------------"
        print "GETING CONNECTIONS"
        #-----------------------------------------------------------------------
        print 'connectivity BondsFromCoordinates3'
        if  self.system.connectivity.bonds == None:
            self.system.BondsFromCoordinates3()
        print 'connectivity BondsFromCoordinates3 -done'

        selection = None
        # . Get the selection.
        if selection is None: towrite = range ( len ( self.system.atoms ) )
        else:                 towrite = selection
        #-----------------------------------------------------------------------
        
        cIndices  = {}
        _NCONECTS = 4
        ncon      = 0
        natm      = 0
        nter      = 0
        self.bonds = []
        
        for iatom in towrite:
            atom = self.system.atoms [iatom]
            cIndices[iatom] = ( natm + nter + 1 )
            natm += 1
        
        if (self.system.connectivity.bonds is not None ) and ( len (self.system.connectivity.bonds ) > 0 ):
            self.system.connectivity.bonds.MakeConnections ( )
            for iatom in towrite:
                # . Get the connections.
                iconnections = self.system.connectivity.bonds.GetConnectedAtoms ( iatom ) # . Normal indices.
                # . Transform to pdb indices.
                iindex   = cIndices[iatom]
                jindices = []
                for j in iconnections:
                    jindex = cIndices.get ( j, -1 )
                    if jindex > 0: jindices.append ( jindex )
                # . Output.
                nindices = len ( jindices )
                if nindices > 0:
                    for i in range ( 0, nindices, _NCONECTS ):
                        
                        #self.file.write ( _CONECTLINEFORMAT1.format ( "CONECT", iindex ) )
                        for j in range ( i, min ( i + _NCONECTS, nindices ) ): 
                            #self.file.write ( _CONECTLINEFORMAT2.format ( jindices[j] ) )
                            #print iindex, jindices[j]
                            
                            if [iindex, jindices[j]] in self.bonds or [jindices[j], iindex, ] in self.bonds:
                                #print iindex, jindices[j], 'ops!'
                                pass
                            
                            else:
                                self.bonds.append([iindex -1, jindices[j]-1])
                                #print iindex, jindices[j]
                        #self.file.write ( "\n" )
                        ncon += 1
        #---------------------------------------------------------------
        
        print "GETING CONNECTIONS done"
        print "---------------------------------------------------------"
        easymol_object.bonds = self.bonds
    
    def SystemCheck(self, status = True, #
                           PyMOL = True, # - refresh the QC region
                              QC = True, # - refresh the QC region
                             FIX = True, # - refresh the Fixed region
                         disable = True, # - disable selections in PyMOL
                          _color = True, #
                           _cell = True, #
             treeview_selections = True, #
                     ORCA_backup = True  #
                    ): 
        
        """ Function doc 
                          status = True, #
                           PyMOL = True, # - refresh the QC region
                              QC = True, # - refresh the QC region
                             FIX = True, # - refresh the Fixed region
                         disable = True, # - disable selections in PyMOL
                          _color = True, #
                           _cell = True, #
             treeview_selections = True, #
                     ORCA_backup = True  #

        """

        #print '----------------------antes-----------------------'
        #pprint (self.settings)
        
        if self.system == None:
            #print "System empty"
            StatusText =''
            self.window_control.STATUSBAR_SET_TEXT(StatusText)
            return 0
        
        if status == True:
            SummaryFile = self.GetStatusFromSystemSummary()
            SummaryFile = os.path.join(self.settings['data_path'], SummaryFile)

        if PyMOL == True:
            PyMOL_Obj      = self.settings['PyMOL_Obj'] # this is the PyMOL_Obj in memory
            if QC:
                # self.settings['QC'] indicates that a QC system exist 
                if self.settings['QC'] == True:
                    self.HideQCRegion(PyMOL_Obj)                
                    self.ShowQCRegion(PyMOL_Obj)
                #else:
                #    self.HideQCRegion(PyMOL_Obj)
            if FIX:
                self.ShowFIXRegion (PyMOL_Obj)
                    
            if disable: # disable selections
                self.DisableSelections()                       

            if _color:
                self.SetColors()

        if treeview_selections:
            pymol_objects2 = cmd.get_names('selections')
            liststore      = self.builder.get_object('liststore1')
            self.window_control.TREEVIEW_ADD_DATA (liststore, pymol_objects2)
        
        if self.ShowCell == True:
            cell = self.importCellParameters()
            DrawCell(cell)
            #print cell
            try:
                cmd.enable('box_1')
            except:
                pass
        else:
            try:
                cmd.disable('box_1')
            except:
                pass
        #-----------------------------------------------#

        if ORCA_backup == True:
            self.back_orca_output()

        if status == True:
            return SummaryFile
            # Only necessary to open the log file with TextEditor
        
        #print '----------------------depois-----------------------'
        #pprint (self.settings)

def __main__ ():
    """ Function doc """
    print 11
    session  = pDynamoSession()
    session.load_new_system (filename = '/home/fernando/programs/EasyHybrid/cyclohexane.pkl')
if __main__:
    __main__()

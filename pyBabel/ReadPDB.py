#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  pdb.py
#  
#  Copyright 2014 Fernando Bachega <fernando@bachega>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

from Molecule import *
from vector_math import*
from AtomTypes import *

class Pdb (object):
    """ Class to load all the molecules in a .pdb file """

    def __init__ (self, filename):
        """ Class initialiser """
        self.filename = filename
        self.molecules = [] # currently only one molecule
        self.readData()

    def PDBSummary (self):
        #m = self.molecules
        for m in self.molecules:
            print "molecule name is: %s" % m.name

            for key in m.atoms.keys():
                a = m.atoms[key]
                print (a.id, a.symbol, float(a.pos[0]),float( a.pos[1]), float(a.pos[2]))
            
            for bond in m.bonds:
                print bond.type ,bond.atom_id_1, bond.atom_id_2
            """ Function doc """

    def readData (self):
        """ Function doc """
        molecule = Molecule(name  =  self.filename)
        f =  open(self.filename, 'r')

        for line in f.readlines():
            if line[0:4] == 'ATOM' or line[0:6] == 'HETATOM':
                atom = self._readAtom(line)
                molecule.atoms[atom.id] = atom
            if line[0:6] == 'CONECT':
                #print line
                pass
                bonds_in_line =  self._readBonds(line)
                for bond in bonds_in_line:
                    molecule.bonds.append(bond)
        f.close()

        #if the pdb had no bond information we should calculate them    ##########################################
        if len (molecule.bonds) == 0:                                   #     esta funcao precisa ser otimizada  #
            #pass                                                       #     esta funcao precisa ser otimizada  #
            molecule.bonds = self._calcBonds(molecule.atoms)            #     esta funcao precisa ser otimizada  #
                                                                        ##########################################
        self.molecules.append(molecule)

    def _readAtom(self, line):
        """ Function doc 
        # variable where the PDB file will be rewritten	  
        #		
        #		self.symbol    = symbol
        #                  HETATM 1884  O   HOH A 372      21.952   9.654  -3.812  1.00 50.58           O		self.name      = name
        #	exemplo, line: ATOM  85830  CLA CLA I 154    -106.883-110.916-110.774  1.00  0.00      ION CL		self.charge    = charge
        #   	                             		'    '									'          line[76:78]		self.occupancy = occupancy
        #												  li[30:38]		self.bfactor   = bfactor
        #														  li[38:46]													
        #																  li[46:54]				
        #		index   = line[6:11]			#	indice
        # 	line1  is the variable that presents the string "ATOM  " or "HETATM"		A_name  = line[11:16]			#	atom name     ex" CA "
        
        index   = line[6:11]			#	indice
        A_name  = line[11:16]			#	atom name     ex" CA "		
        resn    = line[16:20] 			#	residue name   ex" LYS"
        chain   = line[20:22]			#   chain    ex " A"
        resi    = line[22:26]			#   residue number
        gap     = line[26:30]			#	gap between residue number and coordinates
        x       = line[30:38]			#	coordinate X
        y       = line[38:46]			#	coordinate Y
        z       = line[46:54]			#	coordinate Z
                                        #
        b       = line[54:60]			#	B-factor
        oc      = line[60:66]			#	Occupancy
        gap2    = line[66:76]			#	gap between Occupancy and atomic type'    '
        atom    = line[76:78] 			# 	atomic type		
        
        """
        newAtom           = Atom()
        newAtom.id        = int(line[7:11])
        newAtom.symbol    = line[76:78].strip()
        newAtom.name      = line[11:16].strip()        
        newAtom.resn      = line[16:20].strip()                      
        newAtom.resi      = line[22:26].strip()                       
        #newAtom.charge    = None                    
        try:
            newAtom.bfactor   = float(line[54:60].strip())
        except:
            pass
        try:
            newAtom.occupancy = float(line[60:66].strip())               
        except:
            pass
        #newAtom.wdw       = wdw
        
        #print newAtom.symbol
        
        if newAtom.symbol == '':
            newAtom.symbol = self._check_atom_type(newAtom.name)
        
        if newAtom.symbol == None:
            newAtom.symbol = newAtom.name[0]
        
        try:
            newAtom.a_number  = atypes[newAtom.symbol][0]
            newAtom.fname     = atypes[newAtom.symbol][1]
        except:
            pass
        
        print newAtom.symbol, newAtom.name
        
        newAtom.pos[0] = float(line[31:38]) # x
        newAtom.pos[1] = float(line[39:46]) # y
        newAtom.pos[2] = float(line[47:54]) # z
        
        return newAtom

    def _calcBonds(self, atoms):
        """ Calculate the bonds among atoms based on their distance"""
        v = Vector()
        bonds = []
        
        for id_1 in atoms.keys():
            for id_2 in atoms.keys():
                if id_1 != id_2:
                    atom1 = atoms[id_1]
                    atom2 = atoms[id_2]
                    distance = v.mag (v.subtract(atom1.pos, atom2.pos))
                    
                    #print "distance between "
                    if distance < 1.6:
                        duplicate = False
                        for bond in bonds:
                            if bond.atom_id_1 == id_2 and bond.atom_id_2 == id_1:
                                duplicate = True
                        
                        
                        if not duplicate:
                            bond= Bond()
                            bond.atom_id_1 = id_1
                            bond.atom_id_2 = id_2
                            bondtype = 'single'
                            bonds.append(bond)
        return bonds					
                    
    def _readBonds(self,line):
        """
            Extract the bonds in a CONECT line.
            Sample:
            CONECT    3    2    4    4    6       
            Means that atom #3 has:
            a single bond to atom #2
            a double bond to atom #4
            a single bond to atom #6

            A CONECT record will at least have two numbers.

            other:
            CONECT 6891 6581 6890                                                   1HIU8825
        """
        if len(line) > 60: line=line[0:60] # get rid of anything way to the right
        fields = line.split()

        bonds = []
        n = 2
        while n < len(fields):
            bond = Bond()

            bond.atom_id_1 = int(fields[1])
            bond.atom_id_2 = int(fields[n])

            number_of_bonds = fields.count(fields[n])

            if number_of_bonds == 1:
                bond.type = "single"
                n += 1
            elif number_of_bonds == 2:
                bond.type = "double"
                n += 2 # skip the next item in the fields list
            else:
                bond.type = "triple"
                n += 3 # skip the next two items in the fields list
            if bond.atom_id_2 != 0:  # i don't think atom id numbers are ever 0 
                if bond.atom_id_1 != bond.atom_id_2:  # they should be the same
                    bonds.append(bond)
        
        return bonds

    def _check_atom_type (self, atom):
        """ Function doc """
        for i in atypes:
            if atom in atypes[i][2]:
                    #print atom_types[i]
                    return i 



#	def _readBonds (self, line):
#        #"""
#        #    Extract the bonds in a CONECT line.
#        #    Sample:
#        #    CONECT    3    2    4    4    6       
#        #    Means that atom #3 has:
#        #    a single bond to atom #2
#        #    a double bond to atom #4
#        #    a single bond to atom #6
#        #
#        #    A CONECT record will at least have two numbers.
#        #
#        #    other:
#        #    CONECT 6891 6581 6890                                                   1HIU8825
#        #"""
#		if len(line) > 60: 
#			line=line[0:60] # get rid of anything way to the right
#		
#		fields = line.split()
#		bonds = []
#		n = 2
#		while n  < len(fields):
#			bond = Bond()
#			
#			bond.atom_id_1 = fields[1]
#			bond.atom_id_2 = fields[n]
#			
#			number_of_bonds = int(fields.count(fields[n]))
#			if number_of_bonds == 1:
#				bond.type = 'single'
#				n += 1
#			if number_of_bonds == 2:
#				bond.type = 'double'
#				n += 2
#			if number_of_bonds == 1:
#				bond.type = 'triple'
#				n += 3
#			bonds.append(bond)

			
if __name__ == '__main__':
	# code to test the pdb class
	# load the molecule data from the PDB file 
	
	molecules = Pdb("gly.pdb").molecules
	
	
	for m in molecules:
		print "molecule name is: %s" % m.name

		for key in m.atoms.keys():
			a = m.atoms[key]
			print (a.id, a.symbol, float(a.pos[0]),float( a.pos[1]), float(a.pos[2]))
		
		for bond in m.bonds:
			print bond.type ,bond.atom_id_1, bond.atom_id_2


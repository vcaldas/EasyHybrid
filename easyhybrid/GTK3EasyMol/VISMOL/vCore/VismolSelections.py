#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  molecular_model.py
#  
#  Copyright 2016 Carlos Eduardo Sequeiros Borja <casebor@gmail.com>
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



class VisMolPickingSelection:
    """ Class doc """
    
    def __init__ (self):
        """ Class initialiser """
        self.picking_selections = [None]*4
        #self.picking_selection_coordinates = []
    
    def _generate_picking_selection_coordinates (self):
        """ Function doc """
        pass
        #for i,atom in enumerate(self.picking_selections):
        #    if atom is not None:
        #        coord = [atom.Vobject.frames[frame][(atom.index-1)*3  ],
        #                 atom.Vobject.frames[frame][(atom.index-1)*3+1],
        #                 atom.Vobject.frames[frame][(atom.index-1)*3+2],]
        #                
        #        rep.draw_selected(atom, coord, [0.83, 0.48, 1])
        #        rep.draw_numbers(atom, i+1, coord)
    
    def selection_function_picking (self, selected):
        """ Function doc """
        if selected is None:
            self.picking_selections = [None]*len(self.picking_selections)
            #self.selected_residues = []
        else:
            if selected not in self.picking_selections:
                for i in range(len(self.picking_selections)):
                    if self.picking_selections[i] == None:
                        self.picking_selections[i] = selected
                        selected = None
                        break
                if selected is not None:
                    self.picking_selections[len(self.picking_selections)-1] = selected
            else:
                for i in range(len(self.picking_selections)):
                    if self.picking_selections[i] == selected:
                        self.picking_selections[i] = None
    

class VisMolViewingSelection:
    """ Class doc """
    
    def __init__ (self):
        #---------------------------------------------------------------
        #                S E L E C T I O N S
        #---------------------------------------------------------------
        self.actived = True
        
        self._selection_mode    = 'residue'
        
        self.viewing_selections = []
        
        self.selected_residues  = []
        
        """ Class initialiser """
        self.selected_atoms = []
        self.selected_frames= []
	
    def _generate_viewing_selection_coordinates (self):
        """ Function doc """
        pass
        
        #for i,atom in enumerate(self.EMSession.selections[self.EMSession.current_selection].viewing_selections):
        #    #print (atom, atom.index, frame, atom.Vobject_id, self.EMSession.Vobjects[atom.Vobject_id].frames, self.EMSession.Vobjects[atom.Vobject_id].coords  )
        #    #rep.draw_picked(atom)
        #    coord = atom.Vobject.frames[frame][atom.index-1]
        #    #glVertex3f(coord1[0], coord1[1], coord1[2])
        #    rep.draw_selected(atom, coord)
        ##'''
    
    def selecting_by_atom (self, selected):
        """ Function doc """
        if selected not in self.viewing_selections:
            self.viewing_selections.append(selected)
            
        else:
            index = self.viewing_selections.index(selected)
            self.viewing_selections.pop(index)
    
    def selecting_by_residue (self, selected):
        """ Function doc """
        # if the selected atoms is not on the selected list
        if selected not in self.viewing_selections:
            
            for atom in selected.residue.atoms:
                print (len(selected.residue.atoms), atom.name, atom.index)
                
        # the atom is not on the list -  add atom by atom
                if atom not in self.viewing_selections:
                    self.viewing_selections.append(atom)
                
                # the atom IS on the list - do nothing 
                else:
                    pass
    
        # else: if the selected atoms IS on the selected list
        else:
            # So, add all atoms  - selected residue <- selected.resi
            for atom in selected.residue.atoms:
                
                # the atom is not on the list -  add atom by atom
                if atom in self.viewing_selections:
                    index = self.viewing_selections.index(atom)
                    self.viewing_selections.pop(index)                            
                # the atom IS on the list - do nothing 
                else:
                    pass   

    def selecting_by_chain (self, selected):
        
        # if the selected atoms is not on the selected list
        if selected not in self.viewing_selections:
            # So, add all atoms  - selected residue <- selected.resi
            for residue in selected.Vobject.chains[selected.chain].residues:
                for atom in residue.atoms:
                    # the atom is not on the list -  add atom by atom
                    if atom not in self.viewing_selections:
                        self.viewing_selections.append(atom)
                    
                    # the atom IS on the list - do nothing 
                    else:
                        pass

        # if the selected atoms IS on the selected list
        else:
            for residue in selected.Vobject.chains[selected.chain].residues:
                #for residue in chain.residues:
                for atom in residue.atoms:
                    # the atom is not on the list -  add atom by atom
                    if atom in self.viewing_selections:
                        index = self.viewing_selections.index(atom)
                        self.viewing_selections.pop(index)                            
                    # the atom IS on the list - do nothing 
                    else:
                        pass          

        print ('selected atoms: ',len(self.viewing_selections))

    def selection_function_viewing (self, selected):
        
        if selected is None:
            self.viewing_selections = []
            self.selected_residues  = []
        
        else:
            if self._selection_mode == 'atom':
                self.selecting_by_atom (selected)
                '''
                #if selected not in self.viewing_selections:
                #    self.viewing_selections.append(selected)
                #    
                #else:
                #    index = self.viewing_selections.index(selected)
                #    self.viewing_selections.pop(index)
                '''
            
            elif self._selection_mode == 'residue':
                self.selecting_by_residue (selected)
                '''
                #if selected not in self.viewing_selections:
                #    
                #    for atom in selected.residue.atoms:
                #        print (len(selected.residue.atoms), atom.name, atom.index)
                #        
                ## the atom is not on the list -  add atom by atom
                #        if atom not in self.viewing_selections:
                #            self.viewing_selections.append(atom)
                #        
                #        # the atom IS on the list - do nothing 
                #        else:
                #            pass
                #
                ## if the selected atoms IS on the selected list
                #else:
                #    # So, add all atoms  - selected residue <- selected.resi
                #    for atom in selected.residue.atoms:
                #        
                #        # the atom is not on the list -  add atom by atom
                #        if atom in self.viewing_selections:
                #            index = self.viewing_selections.index(atom)
                #            self.viewing_selections.pop(index)                            
                #        # the atom IS on the list - do nothing 
                #        else:
                #            pass                    
                '''
                
            elif self._selection_mode == 'chain':
                self.selecting_by_chain (selected)
                '''
                ## if the selected atoms is not on the selected list
                #if selected not in self.viewing_selections:
                #    # So, add all atoms  - selected residue <- selected.resi
                #    for residue in selected.Vobject.chains[selected.chain].residues:
                #        for atom in residue.atoms:
                #            # the atom is not on the list -  add atom by atom
                #            if atom not in self.viewing_selections:
                #                self.viewing_selections.append(atom)
                #            
                #            # the atom IS on the list - do nothing 
                #            else:
                #                pass
                #
                ## if the selected atoms IS on the selected list
                #else:
                #    for residue in selected.Vobject.chains[selected.chain].residues:
                #        #for residue in chain.residues:
                #        for atom in residue.atoms:
                #            # the atom is not on the list -  add atom by atom
                #            if atom in self.viewing_selections:
                #                index = self.viewing_selections.index(atom)
                #                self.viewing_selections.pop(index)                            
                #            # the atom IS on the list - do nothing 
                #            else:
                #                pass          
                #
                #print ('selected atoms: ',len(self.viewing_selections))
                '''
        

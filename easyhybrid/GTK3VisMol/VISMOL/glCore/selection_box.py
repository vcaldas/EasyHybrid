#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  selection_box.py
#  
#  Copyright 2017 Carlos Eduardo Sequeiros Borja <casebor@gmail.com>
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

import numpy as np

class SelectionBox:
    """ Class doc """
    
    def __init__ (self):
        """ Class initialiser """
        self.vao = None
        self.buffers = None
        self.start = None
        self.end = None
        self.points = None
        self.color = np.array([ 0.0, 0.5, 0.5, 0.0, 0.5, 0.5, 0.0, 0.5, 0.5,
                                0.0, 0.5, 0.5, 0.0, 0.5, 0.5],dtype=np.float32)
        self.indexes = np.array([ 0, 1, 2, 3, 4],dtype=np.uint32)
    
    def update_points(self):
        """ Function doc """
        assert(self.start is not None)
        assert(self.end is not None)
        self.points = np.array([self.start[0], self.start[1], self.start[0], self.end[1],
                                self.end[0], self.end[1], self.end[0], self.start[1],
                                self.start[0], self.start[1]], dtype=np.float32)
    

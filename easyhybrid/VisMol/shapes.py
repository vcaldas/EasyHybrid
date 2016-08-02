#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  shapes.py
#  
#  Copyright 2016 Carlos Eduardo Sequeiros Borja <casebor@gmail.com>
#  
#  This program is free software, you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY, without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program, if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import numpy as np
import math

def get_cube(center, r):
    """ Generates the vertex of a cube for using the 
        GL_TRIANGLES_STRIP option in opengl.
        
        Keyword arguments:
        center -- The center of the cube
        r -- Distance of the center to the walls
    """
    assert(len(center)==3)
    assert(r>0)
    vertices = []
    vertices += [center[0]-r, center[1]+r, center[2]+r]
    vertices += [center[0]-r, center[1]+r, center[2]-r]
    vertices += [center[0]+r, center[1]+r, center[2]-r]
    vertices += [center[0]-r, center[1]-r, center[2]-r]
    vertices += [center[0]+r, center[1]-r, center[2]-r]
    vertices += [center[0]+r, center[1]-r, center[2]+r]
    vertices += [center[0]+r, center[1]+r, center[2]-r]
    vertices += [center[0]+r, center[1]+r, center[2]+r]
    vertices += [center[0]-r, center[1]+r, center[2]+r]
    vertices += [center[0]+r, center[1]-r, center[2]+r]
    vertices += [center[0]-r, center[1]-r, center[2]+r]
    vertices += [center[0]-r, center[1]-r, center[2]-r]
    vertices += [center[0]-r, center[1]+r, center[2]+r]
    vertices += [center[0]-r, center[1]+r, center[2]-r]
    vertices = np.array(vertices,dtype=np.float32)
    return vertices

def get_icosahedron(radius):
    """ A radius circumscribed to it has the radius:
            rad = (edge/4)*sqrt(10+2*sqrt(5))
        Fixed value of sqrt(10+2*sqrt(5)) to 3.804226065180614
        Then one edge of the icosahedron is equal to '2b'
        and the distance of the center to one edge is 'a'.
        Now we can get all the vertices with the form:
            {[+-a,+-b,0.0],[0.0,+-a,+-b],[+-a,0.0,+-b]}
    """
    assert(radius>0.0)
    val = 3.804226065180614
    b = 2*radius/val
    a = math.sqrt(radius*radius-b*b)
    vertices = np.array([ 0,  a,  b,
                          0,  a, -b,
                          0, -a,  b,
                          0, -a, -b,
                         -b,  0,  a,
                          b,  0,  a,
                         -b,  0, -a,
                          b,  0, -a,
                         -a,  b,  0,
                         -a, -b,  0,
                          a,  b,  0,
                          a, -b,  0],dtype=np.float32)
    triangles = np.array([ 0, 4, 5, 0, 5,10, 0,10, 1, 0, 1, 8,
                           0, 8, 4, 3, 6, 7, 3, 6, 9, 3, 9, 2,
                           3, 2,11, 3,11, 7, 4, 2, 5, 5,11,10,
                           1,10, 7, 1, 6, 8, 8, 9, 4, 7, 6, 1,
                           6, 9, 8, 2, 4, 9, 2,11, 5,10,11, 7],dtype=np.uint32)
    return vertices, triangles

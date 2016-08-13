#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  cylinder_data.py
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

import numpy as np

cylinder_vertices = { 'level_0':np.array(
    [ 1.000000000000, 0.000000000000, 0.000000000000,
      0.500000000000, 0.000000000000, 0.866025403784,
     -0.500000000000, 0.000000000000, 0.866025403784],dtype=np.float32),
    'level_1':np.array(
    [ 1.000000000000, 0.000000000000, 0.000000000000,
      0.707106781187, 0.000000000000, 0.707106781187,
      0.000000000000, 0.000000000000, 1.000000000000,
     -0.707106781187, 0.000000000000, 0.707106781187],dtype=np.float32),
    'level_2':np.array(
    [ 1.000000000000, 0.000000000000, 0.000000000000,
      0.809016994375, 0.000000000000, 0.587785252292,
      0.309016994375, 0.000000000000, 0.951056516295,
     -0.309016994375, 0.000000000000, 0.951056516295,
     -0.809016994375, 0.000000000000, 0.587785252292],dtype=np.float32),
    'level_3':np.array(
    [ 1.000000000000, 0.000000000000, 0.000000000000,
      0.866025403784, 0.000000000000, 0.500000000000,
      0.500000000000, 0.000000000000, 0.866025403784,
      0.000000000000, 0.000000000000, 1.000000000000,
     -0.500000000000, 0.000000000000, 0.866025403784,
     -0.866025403784, 0.000000000000, 0.500000000000],dtype=np.float32),
    'level_4':np.array(
    [ 1.000000000000, 0.000000000000, 0.000000000000,
      0.900968867902, 0.000000000000, 0.433883739118,
      0.623489801859, 0.000000000000, 0.781831482468,
      0.222520933956, 0.000000000000, 0.974927912182,
     -0.222520933956, 0.000000000000, 0.974927912182,
     -0.623489801859, 0.000000000000, 0.781831482468,
     -0.900968867902, 0.000000000000, 0.433883739118],dtype=np.float32)
    'level_5':np.array(
    [ 1.000000000000, 0.000000000000, 0.000000000000,
      0.923879532511, 0.000000000000, 0.382683432365,
      0.707106781187, 0.000000000000, 0.707106781187,
      0.382683432365, 0.000000000000, 0.923879532511,
      0.000000000000, 0.000000000000, 1.000000000000,
     -0.382683432365, 0.000000000000, 0.923879532511,
     -0.707106781187, 0.000000000000, 0.707106781187,
     -0.923879532511, 0.000000000000, 0.382683432365],dtype=np.float32)
}

cylinder_triangles = { 'level_0':np.array(
    [ 0,   1,   3,   1,   2,   4,   2,   0,   3, 
      3,   4,   1,   4,   5,   2,   5,   3,   0],dtype=np.uint16),
    'level_1':np.array(
    [ 0,   1,   4,   1,   2,   5,   2,   3,   6,   3,   0,   4,
      4,   5,   1,   5,   6,   2,   6,   7,   3,   7,   4,   0],dtype=np.uint16),
    'level_2':np.array(
    [ 0,   1,   5,   1,   2,   6,   2,   3,   7,   3,   4,   8,   4,   0,   5,
      5,   6,   1,   6,   7,   2,   7,   8,   3,   8,   9,   4,   9,   5,   0],dtype=np.uint16),
    'level_3':np.array(
    [ 0,   1,   6,   1,   2,   7,   2,   3,   8,   3,   4,   9,   4,   5,  10,   5,   0,   6,
      6,   7,   1,   7,   8,   2,   8,   9,   3,   9,  10,   4,  10,  11,   5,  11,   6,   0],dtype=np.uint16),
    'level_4':np.array(
    [ 0,   1,   7,   1,   2,   8,   2,   3,   9,   3,   4,  10,   4,   5,  11,   5,   6,  12,   6,   0,   7,
      7,   8,   1,   8,   9,   2,   9,  10,   3,  10,  11,   4,  11,  12,   5,  12,  13,   6,  13,   7,   0],dtype=np.uint16),
    'level_5':np.array(
    [ 0,   1,   8,   1,   2,   9,   2,   3,  10,   3,   4,  11,   4,   5,  12,   5,   6,  13,   6,   7,  14,   7,   0,   8,
      8,   9,   1,   9,  10,   2,  10,  11,   3,  11,  12,   4,  12,  13,   5,  13,  14,   6,  14,  15,   7,  15,   8,   0],dtype=np.uint16)
}



























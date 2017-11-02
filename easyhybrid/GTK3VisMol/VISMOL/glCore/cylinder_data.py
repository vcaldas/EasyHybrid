#!/usr/bin/env python3
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
     -0.500000000000, 0.000000000000, 0.866025403784,
     -0.500000000000, 0.000000000000,-0.866025403784],dtype=np.float32),
    'level_1':np.array(
    [ 1.000000000000, 0.000000000000, 0.000000000000,
      0.000000000000, 0.000000000000, 1.000000000000,
     -1.000000000000, 0.000000000000, 0.000000000000,
     -0.000000000000, 0.000000000000,-1.000000000000],dtype=np.float32),
    'level_2':np.array(
    [ 1.000000000000, 0.000000000000, 0.000000000000,
      0.309016994375, 0.000000000000, 0.951056516295,
     -0.809016994375, 0.000000000000, 0.587785252292,
     -0.809016994375, 0.000000000000,-0.587785252292,
      0.309016994375, 0.000000000000,-0.951056516295],dtype=np.float32),
    'level_3':np.array(
    [ 1.000000000000, 0.000000000000, 0.000000000000,
      0.500000000000, 0.000000000000, 0.866025403784,
     -0.500000000000, 0.000000000000, 0.866025403784,
     -1.000000000000, 0.000000000000, 0.000000000000,
     -0.500000000000, 0.000000000000,-0.866025403784,
      0.500000000000, 0.000000000000,-0.866025403784],dtype=np.float32),
    'level_4':np.array(
    [ 1.000000000000, 0.000000000000, 0.000000000000,
      0.623489801859, 0.000000000000, 0.781831482468,
     -0.222520933956, 0.000000000000, 0.974927912182,
     -0.900968867902, 0.000000000000, 0.433883739118,
     -0.900968867902, 0.000000000000,-0.433883739118,
     -0.222520933956, 0.000000000000,-0.974927912182,
      0.623489801859, 0.000000000000,-0.781831482468],dtype=np.float32),
    'level_5':np.array(
    [ 1.000000000000, 0.000000000000, 0.000000000000,
      0.707106781187, 0.000000000000, 0.707106781187,
      0.000000000000, 0.000000000000, 1.000000000000,
     -0.707106781187, 0.000000000000, 0.707106781187,
     -1.000000000000, 0.000000000000, 0.000000000000,
     -0.707106781187, 0.000000000000,-0.707106781187,
     -0.000000000000, 0.000000000000,-1.000000000000,
      0.707106781187, 0.000000000000,-0.707106781187],dtype=np.float32),
    'level_6':np.array(
    [ 1.000000000000, 0.000000000000, 0.000000000000,
      0.766044443119, 0.000000000000, 0.642787609687,
      0.173648177667, 0.000000000000, 0.984807753012,
     -0.500000000000, 0.000000000000, 0.866025403784,
     -0.939692620786, 0.000000000000, 0.342020143326,
     -0.939692620786, 0.000000000000,-0.342020143326,
     -0.500000000000, 0.000000000000,-0.866025403784,
      0.173648177667, 0.000000000000,-0.984807753012,
      0.766044443119, 0.000000000000,-0.642787609687],dtype=np.float32),
    'level_7':np.array(
    [ 1.000000000000, 0.000000000000, 0.000000000000,
      0.809016994375, 0.000000000000, 0.587785252292,
      0.309016994375, 0.000000000000, 0.951056516295,
     -0.309016994375, 0.000000000000, 0.951056516295,
     -0.809016994375, 0.000000000000, 0.587785252292,
     -1.000000000000, 0.000000000000, 0.000000000000,
     -0.809016994375, 0.000000000000,-0.587785252292,
     -0.309016994375, 0.000000000000,-0.951056516295,
      0.309016994375, 0.000000000000,-0.951056516295,
      0.809016994375, 0.000000000000,-0.587785252292],dtype=np.float32),
    'level_8':np.array(
    [ 1.000000000000, 0.000000000000, 0.000000000000,
      0.841253532831, 0.000000000000, 0.540640817456,
      0.415415013002, 0.000000000000, 0.909631995355,
     -0.142314838273, 0.000000000000, 0.989821441881,
     -0.654860733945, 0.000000000000, 0.755749574354,
     -0.959492973614, 0.000000000000, 0.281732556841,
     -0.959492973614, 0.000000000000,-0.281732556841,
     -0.654860733945, 0.000000000000,-0.755749574354,
     -0.142314838273, 0.000000000000,-0.989821441881,
      0.415415013002, 0.000000000000,-0.909631995355,
      0.841253532831, 0.000000000000,-0.540640817456],dtype=np.float32),
    'level_9':np.array(
    [ 1.000000000000, 0.000000000000, 0.000000000000,
      0.866025403784, 0.000000000000, 0.500000000000,
      0.500000000000, 0.000000000000, 0.866025403784,
      0.000000000000, 0.000000000000, 1.000000000000,
     -0.500000000000, 0.000000000000, 0.866025403784,
     -0.866025403784, 0.000000000000, 0.500000000000,
     -1.000000000000, 0.000000000000, 0.000000000000,
     -0.866025403784, 0.000000000000,-0.500000000000,
     -0.500000000000, 0.000000000000,-0.866025403784,
     -0.000000000000, 0.000000000000,-1.000000000000,
      0.500000000000, 0.000000000000,-0.866025403784,
      0.866025403784, 0.000000000000,-0.500000000000],dtype=np.float32)
}

cylinder_vertices2 = { 'level_0':np.array(
    [ 0.500000000000, 0.000000000000, 0.866025403784,
     -1.000000000000, 0.000000000000, 0.000000000000,
      0.500000000000, 0.000000000000,-0.866025403784],dtype=np.float32),
    'level_1':np.array(
    [ 0.707106781187, 0.000000000000, 0.707106781187,
     -0.707106781187, 0.000000000000, 0.707106781187,
     -0.707106781187, 0.000000000000,-0.707106781187,
      0.707106781187, 0.000000000000,-0.707106781187],dtype=np.float32),
    'level_2':np.array(
    [ 0.809016994375, 0.000000000000, 0.587785252292,
     -0.309016994375, 0.000000000000, 0.951056516295,
     -1.000000000000, 0.000000000000, 0.000000000000,
     -0.309016994375, 0.000000000000,-0.951056516295,
      0.809016994375, 0.000000000000,-0.587785252292],dtype=np.float32),
    'level_3':np.array(
    [ 0.866025403784, 0.000000000000, 0.500000000000,
      0.000000000000, 0.000000000000, 1.000000000000,
     -0.866025403784, 0.000000000000, 0.500000000000,
     -0.866025403784, 0.000000000000,-0.500000000000,
     -0.000000000000, 0.000000000000,-1.000000000000,
      0.866025403784, 0.000000000000,-0.500000000000],dtype=np.float32),
    'level_4':np.array(
    [ 0.900968867902, 0.000000000000, 0.433883739118,
      0.222520933956, 0.000000000000, 0.974927912182,
     -0.623489801859, 0.000000000000, 0.781831482468,
     -1.000000000000, 0.000000000000, 0.000000000000,
     -0.623489801859, 0.000000000000,-0.781831482468,
      0.222520933956, 0.000000000000,-0.974927912182,
      0.900968867902, 0.000000000000,-0.433883739118],dtype=np.float32),
    'level_5':np.array(
    [ 0.923879532511, 0.000000000000, 0.382683432365,
      0.382683432365, 0.000000000000, 0.923879532511,
     -0.382683432365, 0.000000000000, 0.923879532511,
     -0.923879532511, 0.000000000000, 0.382683432365,
     -0.923879532511, 0.000000000000,-0.382683432365,
     -0.382683432365, 0.000000000000,-0.923879532511,
      0.382683432365, 0.000000000000,-0.923879532511,
      0.923879532511, 0.000000000000,-0.382683432365],dtype=np.float32),
    'level_6':np.array(
    [ 0.939692620786, 0.000000000000, 0.342020143326,
      0.500000000000, 0.000000000000, 0.866025403784,
     -0.173648177667, 0.000000000000, 0.984807753012,
     -0.766044443119, 0.000000000000, 0.642787609687,
     -1.000000000000, 0.000000000000, 0.000000000000,
     -0.766044443119, 0.000000000000,-0.642787609687,
     -0.173648177667, 0.000000000000,-0.984807753012,
      0.500000000000, 0.000000000000,-0.866025403784,
      0.939692620786, 0.000000000000,-0.342020143326],dtype=np.float32),
    'level_7':np.array(
    [ 0.951056516295, 0.000000000000, 0.309016994375,
      0.587785252292, 0.000000000000, 0.809016994375,
      0.000000000000, 0.000000000000, 1.000000000000,
     -0.587785252292, 0.000000000000, 0.809016994375,
     -0.951056516295, 0.000000000000, 0.309016994375,
     -0.951056516295, 0.000000000000,-0.309016994375,
     -0.587785252292, 0.000000000000,-0.809016994375,
     -0.000000000000, 0.000000000000,-1.000000000000,
      0.587785252292, 0.000000000000,-0.809016994375,
      0.951056516295, 0.000000000000,-0.309016994375],dtype=np.float32),
    'level_8':np.array(
    [ 0.959492973614, 0.000000000000, 0.281732556841,
      0.654860733945, 0.000000000000, 0.755749574354,
      0.142314838273, 0.000000000000, 0.989821441881,
     -0.415415013002, 0.000000000000, 0.909631995355,
     -0.841253532831, 0.000000000000, 0.540640817456,
     -1.000000000000, 0.000000000000, 0.000000000000,
     -0.841253532831, 0.000000000000,-0.540640817456,
     -0.415415013002, 0.000000000000,-0.909631995355,
      0.142314838273, 0.000000000000,-0.989821441881,
      0.654860733945, 0.000000000000,-0.755749574354,
      0.959492973614, 0.000000000000,-0.281732556841],dtype=np.float32),
    'level_9':np.array(
    [ 0.965925826289, 0.000000000000, 0.258819045103,
      0.707106781187, 0.000000000000, 0.707106781187,
      0.258819045103, 0.000000000000, 0.965925826289,
     -0.258819045103, 0.000000000000, 0.965925826289,
     -0.707106781187, 0.000000000000, 0.707106781187,
     -0.965925826289, 0.000000000000, 0.258819045103,
     -0.965925826289, 0.000000000000,-0.258819045103,
     -0.707106781187, 0.000000000000,-0.707106781187,
     -0.258819045103, 0.000000000000,-0.965925826289,
      0.258819045103, 0.000000000000,-0.965925826289,
      0.707106781187, 0.000000000000,-0.707106781187,
      0.965925826289, 0.000000000000,-0.258819045103],dtype=np.float32)
}

cylinder_triangles = { 'level_0':np.array(
    [ 1,   0,   3,   2,   1,   4,   0,   2,   5, 
      3,   4,   1,   4,   5,   2,   5,   3,   0],dtype=np.uint16),
    'level_1':np.array(
    [ 1,   0,   4,   2,   1,   5,   3,   2,   6,   0,   3,   7,
      4,   5,   1,   5,   6,   2,   6,   7,   3,   7,   4,   0],dtype=np.uint16),
    'level_2':np.array(
    [ 1,   0,   5,   2,   1,   6,   3,   2,   7,   4,   3,   8,   0,   4,   9,
      5,   6,   1,   6,   7,   2,   7,   8,   3,   8,   9,   4,   9,   5,   0],dtype=np.uint16),
    'level_3':np.array(
    [ 1,   0,   6,   2,   1,   7,   3,   2,   8,   4,   3,   9,   5,   4,  10,   0,   5,  11,
      6,   7,   1,   7,   8,   2,   8,   9,   3,   9,  10,   4,  10,  11,   5,  11,   6,   0],dtype=np.uint16),
    'level_4':np.array(
    [ 1,   0,   7,   2,   1,   8,   3,   2,   9,   4,   3,  10,   5,   4,  11,   6,   5,  12,   0,   6,  13,
      7,   8,   1,   8,   9,   2,   9,  10,   3,  10,  11,   4,  11,  12,   5,  12,  13,   6,  13,   7,   0],dtype=np.uint16),
    'level_5':np.array(
    [ 1,   0,   8,   2,   1,   9,   3,   2,  10,   4,   3,  11,   5,   4,  12,   6,   5,  13,   7,   6,  14,   0,   7,  15,
      8,   9,   1,   9,  10,   2,  10,  11,   3,  11,  12,   4,  12,  13,   5,  13,  14,   6,  14,  15,   7,  15,   8,   0],dtype=np.uint16),
    'level_6':np.array(
    [ 1,   0,   9,   2,   1,  10,   3,   2,  11,   4,   3,  12,   5,   4,  13,   6,   5,  14,   7,   6,  15,   8,   7,  16,   0,   8,  17,
      9,  10,   1,  10,  11,   2,  11,  12,   3,  12,  13,   4,  13,  14,   5,  14,  15,   6,  15,  16,   7,  16,  17,   8,  17,   9,   0],dtype=np.uint16),
    'level_7':np.array(
    [ 1,   0,  10,   2,   1,  11,   3,   2,  12,   4,   3,  13,   5,   4,  14,   6,   5,  15,   7,   6,  16,   8,   7,  17,   9,   8,  18,   0,   9,  19,
     10,  11,   1,  11,  12,   2,  12,  13,   3,  13,  14,   4,  14,  15,   5,  15,  16,   6,  16,  17,   7,  17,  18,   8,  18,  19,   9,  19,  10,   0],dtype=np.uint16),
    'level_8':np.array(
    [ 1,   0,  11,   2,   1,  12,   3,   2,  13,   4,   3,  14,   5,   4,  15,   6,   5,  16,   7,   6,  17,   8,   7,  18,   9,   8,  19,  10,   9,  20,   0,  10,  21,
     11,  12,   1,  12,  13,   2,  13,  14,   3,  14,  15,   4,  15,  16,   5,  16,  17,   6,  17,  18,   7,  18,  19,   8,  19,  20,   9,  20,  21,  10,  21,  11,   0],dtype=np.uint16),
    'level_9':np.array(
    [ 1,   0,  12,   2,   1,  13,   3,   2,  14,   4,   3,  15,   5,   4,  16,   6,   5,  17,   7,   6,  18,   8,   7,  19,   9,   8,  20,  10,   9,  21,  11,  10,  22,   0,  11,  23,
     12,  13,   1,  13,  14,   2,  14,  15,   3,  15,  16,   4,  16,  17,   5,  17,  18,   6,  18,  19,   7,  19,  20,   8,  20,  21,   9,  21,  22,  10,  22,  23,  11,  23,  12,   0],dtype=np.uint16)
}


























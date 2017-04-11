#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  atom_types.py
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

hydrogen = ['H','HA','HB','HD','HE','HH','HB2','HB3','HG','HD11','HD12','HD13','HD21','HD22','HD23','HNC','H14','H15','H16','H17','H18','H19','H20','H21','H22','H24','1HB','2HB','3HB','H1']
carbon   = ['CA','C','CB','CD','CE','CG','CD1','CD2','CE1','CE2','CZ']
oxygen   = ['O','OD1','OD2', 'OW', 'OH', 'OH2', 'OXT']

# name : [atomic number, [RGB colors in 0-1 scale], [another colors], [another], atomic radius, Van Der Walls radius, covalent radius]
ATOM_TYPES = {
            'H'  : [ 1,   [1.000000, 1.000000, 1.000000], [204, 204, 204], [250,  22, 145], 0.53, 1.20, 0.37 ],	
            'He' : [ 2,   [0.850000, 1.000000, 1.000000], [140, 140, 180], [255, 255, 255], 0.31, 1.40, 0.32 ],	
            'Li' : [ 3,   [0.800000, 0.500000, 1.000000], [180, 180, 180], [217, 255, 255], 1.67, 1.82, 1.34 ],	
            'Be' : [ 4,   [0.760000, 1.000000, 0.000000], [130,  90,  30], [204, 128, 255], 1.12, 0.30, 0.90 ],	
            'B'  : [ 5,   [1.000000, 0.710000, 0.710000], [ 90, 130,  30], [194, 255,   0], 0.87, 0.30, 0.82 ],	
            'C'  : [ 6,   [0.231372, 0.619607, 0.44705 ], [ 80, 180, 180], [255, 181, 181], 0.67, 1.70, 0.77 ],	
            #'C'  : [ 6,   [0.100000, 0.1000, 0.10000 ], [ 80, 180, 180], [255, 181, 181], 0.67, 1.70, 0.77 ],	
            'N'  : [ 7,   [0.050000, 0.050000, 1.000000], [  0, 160,   0], [144, 144, 144], 0.56, 1.55, 0.75 ],	
            'O'  : [ 8,   [1.000000, 0.050000, 0.050000], [ 60,  60, 150], [ 48,  80, 248], 0.48, 1.52, 0.73 ],	
            'F'  : [ 9,   [0.700000, 1.000000, 1.000000], [160,   0,   0], [255,  13,  13], 0.42, 1.47, 0.71 ],	
            'Ne' : [ 10,  [0.700000, 0.890000, 0.960000], [  0, 160, 160], [144, 224,  80], 0.38, 1.54, 0.69 ],	
            'Na' : [ 11,  [0.670000, 0.360000, 0.950000], [180, 180, 180], [179, 227, 245], 1.90, 2.27, 1.54 ],	
            'Mg' : [ 12,  [0.540000, 1.000000, 0.000000], [130,  90,  30], [171,  92, 242], 1.45, 1.73, 1.30 ],	
            'Al' : [ 13,  [0.750000, 0.650000, 0.650000], [ 90, 130,  30], [138, 255,   0], 1.18, 0.30, 1.18 ],	
            'Si' : [ 14,  [0.500000, 0.600000, 0.600000], [100, 100, 150], [191, 166, 166], 1.11, 2.10, 1.11 ],	
            'P'  : [ 15,  [1.000000, 0.500000, 0.000000], [ 60,  60,  60], [240, 200, 160], 0.98, 1.80, 1.06 ],	
            'S'  : [ 16,  [1.000000, 1.000000, 0.190000], [120, 100,  10], [255, 128,   0], 0.88, 1.80, 1.02 ],	
            'Cl' : [ 17,  [0.120000, 0.940000, 0.120000], [110, 120,  30], [255, 255,  48], 0.79, 1.75, 0.99 ],	
            'Ar' : [ 18,  [0.500000, 0.820000, 0.890000], [ 10, 105, 120], [ 31, 240,  31], 0.71, 1.88, 0.97 ],	
            'K'  : [ 19,  [0.560000, 0.250000, 0.830000], [180, 180, 180], [128, 209, 227], 2.43, 2.75, 1.96 ],	
            'Ca' : [ 20,  [0.240000, 1.000000, 0.000000], [130,  90,  30], [143,  64, 212], 1.94, 0.30, 1.74 ],	
            'Sc' : [ 21,  [0.900000, 0.900000, 0.900000], [ 90, 130,  30], [ 61, 255,   0], 1.84, 0.30, 1.44 ],	
            'Ti' : [ 22,  [0.750000, 0.760000, 0.780000], [180, 180,  30], [230, 230, 230], 1.76, 0.30, 1.36 ],	
            'V'  : [ 23,  [0.650000, 0.650000, 0.670000], [180, 180,  30], [191, 194, 199], 1.71, 0.30, 1.25 ],	
            'Cr' : [ 24,  [0.540000, 0.600000, 0.780000], [180, 180,  30], [166, 166, 171], 1.66, 0.30, 1.27 ],	
            'Mn' : [ 25,  [0.610000, 0.480000, 0.780000], [180, 180,  30], [138, 153, 199], 1.61, 0.30, 1.39 ],	
            'Fe' : [ 26,  [0.500000, 0.480000, 0.780000], [180, 180,  30], [156, 122, 199], 1.56, 0.30, 1.25 ],	
            'Co' : [ 27,  [0.440000, 0.480000, 0.780000], [180, 180,  30], [224, 102,  51], 1.52, 0.30, 1.26 ],	
            'Ni' : [ 28,  [0.360000, 0.480000, 0.760000], [180, 180,  30], [240, 144, 160], 1.49, 1.63, 1.21 ],	
            'Cu' : [ 29,  [1.000000, 0.480000, 0.380000], [180, 180,  30], [ 80, 208,  80], 1.45, 1.40, 1.38 ],	
            'Zn' : [ 30,  [0.490000, 0.500000, 0.690000], [180, 180,  30], [200, 128,  51], 1.42, 1.39, 1.31 ],	
            'Ga' : [ 31,  [0.760000, 0.560000, 0.560000], [180, 180,  30], [125, 128, 176], 1.36, 1.87, 1.26 ],	
            'Ge' : [ 32,  [0.400000, 0.560000, 0.560000], [100, 100, 150], [194, 143, 143], 1.25, 0.30, 1.22 ],	
            'As' : [ 33,  [0.740000, 0.500000, 0.890000], [ 60,  60,  60], [102, 143, 143], 1.14, 1.85, 1.19 ],	
            'Se' : [ 34,  [1.000000, 0.630000, 0.000000], [120, 100,  10], [189, 128, 227], 1.03, 1.90, 1.16 ],	
            'Br' : [ 35,  [0.650000, 0.160000, 0.160000], [110, 120,  30], [255, 161,   0], 0.94, 1.85, 1.14 ],	
            'Kr' : [ 36,  [0.360000, 0.720000, 0.820000], [ 10, 105, 120], [166,  41,  41], 0.88, 2.02, 1.10 ],	
            'Rb' : [ 37,  [0.440000, 0.180000, 0.690000], [180, 180, 180], [ 92, 184, 209], 2.65, 0.30, 2.11 ],	
            'Sr' : [ 38,  [0.000000, 1.000000, 0.000000], [130,  90,  30], [112,  46, 176], 2.19, 0.30, 1.92 ],	
            'Y'  : [ 39,  [0.580000, 1.000000, 1.000000], [ 90, 130,  30], [  0, 255,   0], 2.12, 0.30, 1.62 ],	
            'Zr' : [ 40,  [0.580000, 0.880000, 0.880000], [110, 110,  30], [148, 255, 255], 2.06, 0.30, 1.48 ],	
            'Nb' : [ 41,  [0.450000, 0.760000, 0.790000], [110, 110,  30], [148, 224, 224], 1.98, 0.30, 1.37 ],	
            'Mo' : [ 42,  [0.330000, 0.710000, 0.710000], [110, 110,  30], [115, 194, 201], 1.90, 0.30, 1.45 ],	
            'Tc' : [ 43,  [0.230000, 0.620000, 0.620000], [110, 110,  30], [ 84, 181, 181], 1.83, 0.30, 1.56 ],	
            'Ru' : [ 44,  [0.140000, 0.560000, 0.560000], [110, 110,  30], [ 59, 158, 158], 1.78, 0.30, 1.26 ],	
            'Rh' : [ 45,  [0.040000, 0.490000, 0.550000], [110, 110,  30], [ 36, 143, 143], 1.73, 0.30, 1.35 ],	
            'Pd' : [ 46,  [0.000000, 0.410000, 0.520000], [110, 110,  30], [ 10, 125, 140], 1.69, 1.63, 1.31 ],	
            'Ag' : [ 47,  [0.880000, 0.880000, 1.000000], [110, 110,  30], [  0, 105, 133], 1.65, 1.72, 1.53 ],	
            'Cd' : [ 48,  [1.000000, 0.850000, 0.560000], [110, 110,  30], [192, 192, 192], 1.61, 1.58, 1.48 ],	
            'In' : [ 49,  [0.650000, 0.460000, 0.450000], [110, 110,  30], [255, 217, 143], 1.56, 1.93, 1.44 ],	
            'Sn' : [ 50,  [0.400000, 0.500000, 0.500000], [100, 100, 150], [166, 117, 115], 1.45, 2.17, 1.41 ],	
            'Sb' : [ 51,  [0.620000, 0.390000, 0.710000], [ 90,  90,  90], [102, 128, 128], 1.33, 0.30, 1.38 ],	
            'Te' : [ 52,  [0.830000, 0.480000, 0.000000], [120, 100,  10], [158,  99, 181], 1.23, 2.06, 1.35 ],	
            'I'  : [ 53,  [0.580000, 0.000000, 0.580000], [110, 120,  30], [212, 122,   0], 1.15, 1.98, 1.33 ],	
            'Xe' : [ 54,  [0.260000, 0.620000, 0.690000], [ 10, 105, 120], [148,   0, 148], 1.08, 2.16, 1.30 ],	
            'Cs' : [ 55,  [0.340000, 0.090000, 0.560000], [180, 180, 180], [ 66, 158, 176], 2.98, 0.30, 2.25 ],	
            'Ba' : [ 56,  [0.000000, 0.790000, 0.000000], [130,  90,  30], [ 87,  23, 143], 2.53, 0.30, 1.98 ],	
            'La' : [ 57,  [0.440000, 0.830000, 1.000000], [ 90, 130,  30], [  0, 201,   0], 1.95, 0.30, 1.69 ],	
            'Ce' : [ 58,  [1.000000, 1.000000, 0.780000], [150, 150,  30], [112, 212, 255], 1.85, 0.30, 0.30 ],	
            'Pr' : [ 59,  [0.850000, 1.000000, 0.780000], [ 10, 105,  10], [255, 255, 199], 2.47, 0.30, 0.30 ],	
            'Nd' : [ 60,  [0.780000, 1.000000, 0.780000], [ 10, 105,  10], [217, 255, 199], 2.06, 0.30, 0.30 ],	
            'Pm' : [ 61,  [0.640000, 1.000000, 0.780000], [ 10, 105,  10], [199, 255, 199], 2.05, 0.30, 0.30 ],	
            'Sm' : [ 62,  [0.560000, 1.000000, 0.780000], [ 10, 105,  10], [163, 255, 199], 2.38, 0.30, 0.30 ],	
            'Eu' : [ 63,  [0.380000, 1.000000, 0.780000], [ 10, 105,  10], [143, 255, 199], 2.31, 0.30, 0.30 ],	
            'Gd' : [ 64,  [0.270000, 1.000000, 0.780000], [ 10, 105,  10], [ 97, 255, 199], 2.33, 0.30, 0.30 ],	
            'Tb' : [ 65,  [0.190000, 1.000000, 0.780000], [ 10, 105,  10], [ 69, 255, 199], 2.25, 0.30, 0.30 ],	
            'Dy' : [ 66,  [0.120000, 1.000000, 0.780000], [ 10, 105,  10], [ 48, 255, 199], 2.28, 0.30, 0.30 ],	
            'Ho' : [ 67,  [0.000000, 1.000000, 0.610000], [ 10, 105,  10], [ 31, 255, 199], 2.26, 0.30, 0.30 ],	
            'Er' : [ 68,  [0.000000, 0.900000, 0.460000], [ 10, 105,  10], [  0, 255, 156], 2.26, 0.30, 0.30 ],	
            'Tm' : [ 69,  [0.000000, 0.830000, 0.320000], [ 10, 105,  10], [  0, 230, 117], 2.22, 0.30, 0.30 ],	
            'Yb' : [ 70,  [0.000000, 0.750000, 0.220000], [ 10, 105,  10], [  0, 212,  82], 2.22, 0.30, 0.30 ],	
            'Lu' : [ 71,  [0.000000, 0.670000, 0.140000], [ 10, 105,  10], [  0, 191,  56], 2.17, 0.30, 1.60 ],	
            'Hf' : [ 72,  [0.300000, 0.760000, 1.000000], [ 10, 105,  10], [  0, 171,  36], 2.08, 0.30, 1.50 ],	
            'Ta' : [ 73,  [0.300000, 0.650000, 1.000000], [150, 150,  30], [ 77, 194, 255], 2.00, 0.30, 1.38 ],	
            'W'  : [ 74,  [0.130000, 0.580000, 0.840000], [150, 150,  30], [ 77, 166, 255], 1.93, 0.30, 1.46 ],	
            'Re' : [ 75,  [0.150000, 0.490000, 0.670000], [150, 150,  30], [ 33, 148, 214], 1.88, 0.30, 1.59 ],	
            'Os' : [ 76,  [0.150000, 0.400000, 0.590000], [150, 150,  30], [ 38, 125, 171], 1.85, 0.30, 1.28 ],	
            'Ir' : [ 77,  [0.090000, 0.330000, 0.530000], [150, 150,  30], [ 38, 102, 150], 1.80, 0.30, 1.37 ],	
            'Pt' : [ 78,  [0.960000, 0.930000, 0.820000], [150, 150,  30], [ 23,  84, 135], 1.77, 1.75, 1.28 ],	
            'Au' : [ 79,  [0.800000, 0.820000, 0.120000], [150, 150,  30], [208, 208, 224], 1.74, 1.66, 1.44 ],	
            'Hg' : [ 80,  [0.710000, 0.710000, 0.760000], [150, 150,  30], [255, 209,  35], 1.71, 1.55, 1.49 ],	
            'Tl' : [ 81,  [0.650000, 0.330000, 0.300000], [150, 150,  30], [184, 184, 208], 1.56, 1.96, 1.48 ],	
            'Pb' : [ 82,  [0.340000, 0.350000, 0.380000], [100, 100, 150], [166,  84,  77], 1.54, 2.02, 1.47 ],	
            'Bi' : [ 83,  [0.620000, 0.310000, 0.710000], [ 90,  90,  90], [ 87,  89,  97], 1.43, 0.30, 1.46 ],	
            'Po' : [ 84,  [0.670000, 0.360000, 0.000000], [120, 100,  10], [158,  79, 181], 1.35, 0.30, 0.30 ],	
            'At' : [ 85,  [0.460000, 0.310000, 0.270000], [110, 120,  30], [171,  92,   0], 1.27, 0.30, 0.30 ],	
            'Rn' : [ 86,  [0.260000, 0.510000, 0.590000], [ 10, 105, 120], [117,  79,  69], 1.20, 0.30, 1.45 ],	
            'Fr' : [ 87,  [0.260000, 0.000000, 0.400000], [180, 180, 180], [ 66, 130, 150], 0.01, 0.30, 0.30 ],	
            'Ra' : [ 88,  [0.000000, 0.490000, 0.000000], [130,  90,  30], [ 66,   0, 102], 0.01, 0.30, 0.30 ],	
            'Ac' : [ 89,  [0.440000, 0.670000, 0.980000], [ 90, 130,  30], [  0, 125,   0], 1.95, 0.30, 0.30 ],	
            'Th' : [ 90,  [0.000000, 0.730000, 1.000000], [180, 180,  30], [112, 171, 250], 1.80, 0.30, 0.30 ],	
            'Pa' : [ 91,  [0.000000, 0.630000, 1.000000], [120, 100,  10], [  0, 186, 255], 1.80, 0.30, 0.30 ],	
            'U'  : [ 92,  [0.000000, 0.560000, 1.000000], [120, 100,  10], [  0, 161, 255], 1.75, 1.86, 0.30 ],	
            'Np' : [ 93,  [0.000000, 0.500000, 1.000000], [120, 100,  10], [  0, 143, 255], 1.75, 0.30, 0.30 ],	
            'Pu' : [ 94,  [0.000000, 0.420000, 1.000000], [120, 100,  10], [  0, 128, 255], 1.75, 0.30, 0.30 ],	
            'Am' : [ 95,  [0.330000, 0.360000, 0.950000], [120, 100,  10], [  0, 107, 255], 1.75, 0.30, 0.30 ],	
            'Cm' : [ 96,  [0.470000, 0.360000, 0.890000], [120, 100,  10], [ 84,  92, 242], 0.01, 0.30, 0.30 ],	
            'Bk' : [ 97,  [0.540000, 0.310000, 0.890000], [120, 100,  10], [120,  92, 227], 0.01 ],
            'Cf' : [ 98,  [0.630000, 0.210000, 0.830000], [120, 100,  10], [138,  79, 227], 0.01 ],
            'Es' : [ 99,  [0.700000, 0.120000, 0.830000], [120, 100,  10], [161,  54, 212], 0.01 ],
            'Fm' : [ 100, [0.700000, 0.120000, 0.730000], [120, 100,  10], [179,  31, 212], 0.01 ],
            'Md' : [ 101, [0.700000, 0.050000, 0.650000], [120, 100,  10], [179,  31, 186], 0.01 ],
            'No' : [ 102, [0.740000, 0.050000, 0.530000], [120, 100,  10], [179,  13, 166], 0.01 ],
            'Lr' : [ 103, [0.780000, 0.000000, 0.400000], [120, 100,  10], [189,  13, 135], 0.01 ],
            'Rf' : [ 104, [0.800000, 0.000000, 0.350000], [120, 100,  10], [199,   0, 102], 0.01 ],
            'Db' : [ 105, [0.820000, 0.000000, 0.310000], [230, 230, 230], [204,   0,  89], 0.01 ],
            'Sg' : [ 106, [0.850000, 0.000000, 0.270000], [230, 230, 230], [209,   0,  79], 0.01 ],
            'Bh' : [ 107, [0.880000, 0.000000, 0.220000], [179,   0, 179], [217,   0,  69], 0.01 ],
            'Hs' : [ 108, [0.900000, 0.000000, 0.180000], [179,   0, 179], [224,   0,  56], 0.01 ],
            'Mt' : [ 109, [0.920000, 0.000000, 0.150000], [179,   0, 179], [230,   0,  46], 0.01 ],
            'Xx' : [ 0,   [0.070000, 0.500000, 0.700000], [179,   0, 179], [235,   0,  38], 0.01 ],
            'X'  : [ 0,   [0.070000, 0.500000, 0.700000], [179,   0, 179], [235,   0,  38], 0.01 ]
            }

def get_color_rgb(name):
    """ Return the color of an atom in RGB. Note that the returned
	value is in scale of 0 to 1, but you can change this in the
	index. If the atomname does not match any of the names
	given, it returns the default dummy value of atom X.
    """
    try:
	color = ATOM_TYPES[name][1]
    except KeyError:
	if name[0] == 'H' or name in hydrogen:
	    color = ATOM_TYPES['H'][1]
	elif name[0] == 'C':
	    color = ATOM_TYPES['C'][1]
	elif name[0] == 'O':
	    color = ATOM_TYPES['O'][1]
	elif name[0] == 'N':
	    color = ATOM_TYPES['N'][1]
	elif name[0] == 'S':
	    color = ATOM_TYPES['S'][1]
	else:
	    color = ATOM_TYPES['X'][1]
    color = [int(color[0]*250), int(color[1]*250), int(color[2]*250)]
    return color

def get_color(name):
    """ Return the color of an atom in RGB. Note that the returned
	value is in scale of 0 to 1, but you can change this in the
	index. If the atomname does not match any of the names
	given, it returns the default dummy value of atom X.
    """
    try:
	color = ATOM_TYPES[name][1]
    except KeyError:
	if name[0] == 'H' or name in hydrogen:
	    color = ATOM_TYPES['H'][1]
	elif name[0] == 'C':
	    color = ATOM_TYPES['C'][1]
	elif name[0] == 'O':
	    color = ATOM_TYPES['O'][1]
	elif name[0] == 'N':
	    color = ATOM_TYPES['N'][1]
	elif name[0] == 'S':
	    color = ATOM_TYPES['S'][1]
	else:
	    color = ATOM_TYPES['X'][1]
	    print name
    return color

def get_cov_rad(name):
    """
    """
    try:
	rad = ATOM_TYPES[name][6]
    except KeyError:
	if name[0] == 'H' or name in hydrogen:
	    rad = ATOM_TYPES['H'][6]
	elif name[0] == 'C':
	    rad = ATOM_TYPES['C'][6]
	elif name[0] == 'O':
	    rad = ATOM_TYPES['O'][6]
	elif name[0] == 'N':
	    rad = ATOM_TYPES['N'][6]
	elif name[0] == 'S':
	    rad = ATOM_TYPES['S'][6]
	else:
	    rad = 0.30
    return rad

def get_radius(name):
    """
    """
    try:
	rad = ATOM_TYPES[name][4]
    except KeyError:
	if name[0] == 'H' or name in hydrogen:
	    rad = ATOM_TYPES['H'][4]
	elif name[0] == 'C':
	    rad = ATOM_TYPES['C'][4]
	elif name[0] == 'O':
	    rad = ATOM_TYPES['O'][4]
	elif name[0] == 'N':
	    rad = ATOM_TYPES['N'][4]
	elif name[0] == 'S':
	    rad = ATOM_TYPES['S'][4]
	else:
	    rad = 0.30
    return rad

def get_vdw_rad(name):
    """
    """
    try:
	vdw = ATOM_TYPES[name][5]
    except KeyError:
	if name[0] == 'H' or name in hydrogen:
	    vdw = ATOM_TYPES['H'][5]
	elif name[0] == 'C':
	    vdw = ATOM_TYPES['C'][5]
	elif name[0] == 'O':
	    vdw = ATOM_TYPES['O'][5]
	elif name[0] == 'N':
	    vdw = ATOM_TYPES['N'][5]
	elif name[0] == 'S':
	    vdw = ATOM_TYPES['S'][5]
	else:
	    vdw = 0.40
    return vdw

def get_ball_rad(name):
    """
    """
    try:
	ball = ATOM_TYPES[name][4]
    except KeyError:
	if name[0] == 'H' or name in hydrogen:
	    ball = ATOM_TYPES['H'][4]
	elif name[0] == 'C':
	    ball = ATOM_TYPES['C'][4]
	elif name[0] == 'O':
	    ball = ATOM_TYPES['O'][4]
	elif name[0] == 'N':
	    ball = ATOM_TYPES['N'][4]
	elif name[0] == 'S':
	    ball = ATOM_TYPES['S'][4]
	else:
	    ball = 0.30
    return ball/2.0

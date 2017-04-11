#from AtomTypes import ATOMTYPES
import numpy as np
import pprint as pprint 

ATOMTYPES = {
            'H'  :  [ 1,    'Hydrogen',      ['H','HA','HB2','HB3','HG','HD11','HD12','HD13','HD21','HD22','HD23','HNC','H14','H15','H16','H17','H18','H19','H20','H21','H22','H24'],[0.9, 0.9, 0.9],  [204, 204, 204] ,[250,22,145 ]  ],        #if a.symbol == "C":
            'He' :  [ 2,    'Helium',        ['He'],                                                                                                                                 [1.0, 1.0, 1.0],  [140, 140, 180] ,[255,255,255]  ],        #	#glColor3f(0.4, 0.4, 0.4) # grey
            'Li' :  [ 3,    'Lithium',       ['Li'],                                                                                                                                 [1.0, 1.0, 1.0],  [180, 180, 180] ,[217,255,255]  ],        #	glColor3f(0.1, 0.1, 0.1) # grey
            'Be' :  [ 4,    'Beryllium',     ['Be'],                                                                                                                                 [1.0, 1.0, 1.0],  [130, 90, 30  ] ,[204,128,255]  ],        #
            'B'  :  [ 5,    'Boron',         ['B'],                                                                                                                                  [1.0, 1.0, 1.0],  [90, 130, 30  ] ,[194,255,0]   ],         #elif a.symbol == "H":
            'C'  :  [ 6,    'Carbon',        ['CA','C','CB','CG','CD1','CD2','CE1','CE2','CZ '],                                                                                     [0.4, 0.4, 0.4],  [80, 180, 180 ] ,[255,181,181] ],         #	glColor3f(0.9, 0.9, 0.9) # white
            'N'  :  [ 7,    'Nitrogen',      ['N','NE2','NE2'],                                                                                                                      [0.1, 0.1, 0.9],  [0, 160, 0    ] ,[144,144,144] ],         #elif a.symbol == "O":
            'O'  :  [ 8,    'Oxygen',        ['O','OD1','OD2', 'OW', 'OH', 'OH2', 'OXT'],                                                                                            [0.9, 0.1, 0.1],  [60, 60, 150  ] ,[48,80,248]   ],         #	glColor3f(0.9, 0.1, 0.1) # red
            'F'  :  [ 9,    'Fluorine',      ['F' ],                                                                                                                                 [1.0, 1.0, 1.0],  [160, 0, 0    ] ,[255,13,13]   ],         #elif a.symbol == "S":
            'Ne' :  [ 10,   'Neon',          ['Ne'],                                                                                                                                 [1.0, 1.0, 1.0],  [0, 160, 160  ] ,[144,224,80]  ],         #	glColor3f(0.9, 0.9, 0.0) # yellow
            'Na' :  [ 11,   'Sodium',        ['Na'],                                                                                                                                 [1.0, 1.0, 1.0],  [180, 180, 180] ,[179,227,245] ],         #elif a.symbol ==  "N":
            'Mg' :  [ 12,   'Magnesium',     ['Mg'],                                                                                                                                 [1.0, 1.0, 1.0],  [130, 90, 30  ] ,[171,92,242]  ],         #	glColor3f(0.1, 0.1, 0.9) # blue
            'Al' :  [ 13,   'Aluminium',     ['Al'],                                                                                                                                 [1.0, 1.0, 1.0],  [90, 130, 30  ] ,[138,255,0]   ],         #elif a.symbol in ["CL", "B"]:
            'Si' :  [ 14,   'Silicon',       ['Si'],                                                                                                                                 [1.0, 1.0, 1.0],  [100, 100, 150] ,[191,166,166]  ],        #	glColor3f(0.1, 0.9, 0.1) # green
            'P'  :  [ 15,   'Phosphorus',    ['P' ],                                                                                                                                 [1.0, 1.0, 1.0],  [60, 60, 60   ] ,[240,200,160]  ],        #elif a.symbol in ["P", "FE", "BA"]:
            'S'  :  [ 16,   'Sulphur',       ['S' ],                                                                                                                                 [1.0, 1.0, 1.0],  [120, 100, 10 ] ,[255,128,0]   ],         #	glColor3f(0.9, 0.6, 0.0) # orange   
            'Cl' :  [ 17,   'Chlorine',      ['Cl'],                                                                                                                                 [1.0, 1.0, 1.0],  [110, 120, 30 ] ,[255,255,48]  ],         #elif a.symbol == "NA":
            'Ar' :  [ 18,   'Argon',         ['Ar'],                                                                                                                                 [1.0, 1.0, 1.0],  [10, 105, 120 ] ,[31,240,31]   ],         #	glColor3f(0.0, 0.0, 1.0) # bright blue
            'K'  :  [ 19,   'Potassium',     ['K' ],                                                                                                                                 [1.0, 1.0, 1.0],  [180, 180, 180] ,[128,209,227]  ],        #elif a.symbol in ["F", "SI", "AU"]:
            'Ca' :  [ 20,   'Calcium',       ['Ca'],                                                                                                                                 [1.0, 1.0, 1.0],  [130, 90, 30  ] ,[143,64,212]  ],         #	glColor3f(.85, .65, .13) # goldenrod
            'Sc' :  [ 21,   'Scandium',      ['Sc'],                                                                                                                                 [1.0, 1.0, 1.0],  [90, 130, 30  ] ,[61,255,0]    ],         #elif a.symbol in ["ZN", "CU", "NI", "BR"]:
            'Ti' :  [ 22,   'Titanium',      ['Ti'],                                                                                                                                 [1.0, 1.0, 1.0],  [180, 180, 30 ] ,[230,230,230]  ],        #	glColor3f(.65, .16, .16) # brown
            'V'  :  [ 23,   'Vanadium',      ['V' ],                                                                                                                                 [1.0, 1.0, 1.0],  [180, 180, 30 ] ,[191,194,199]  ],        #elif a.symbol == "I":
            'Cr' :  [ 24,   'Chromium',      ['Cr'],                                                                                                                                 [1.0, 1.0, 1.0],  [180, 180, 30 ] ,[166,166,171]  ],        #	glColor3f(.63, .12, .94) # purple
            'Mn' :  [ 25,   'Manganese',     ['Mn'],                                                                                                                                 [1.0, 1.0, 1.0],  [180, 180, 30 ] ,[138,153,199]  ],        #elif a.symbol == "MG":
            'Fe' :  [ 26,   'Iron',          ['Fe'],                                                                                                                                 [1.0, 1.0, 1.0],  [180, 180, 30 ] ,[156,122,199]  ],        #	glColor3f(.13, .55, .13) # forest green
            'Co' :  [ 27,   'Cobalt',        ['Co'],                                                                                                                                 [1.0, 1.0, 1.0],  [180, 180, 30 ] ,[224,102,51]  ],         #elif a.symbol in ["CA", "MN", "AL", "TI", "CR", "AG"]:
            'Ni' :  [ 28,   'Nickel',        ['Ni'],                                                                                                                                 [1.0, 1.0, 1.0],  [180, 180, 30 ] ,[240,144,160]  ],        #	glColor3f(.50, .50, .56) # dark grey
            'Cu' :  [ 29,   'Copper',        ['Cu'],                                                                                                                                 [1.0, 1.0, 1.0],  [180, 180, 30 ] ,[80,208,80]   ],         #elif a.symbol == "LI":
            'Zn' :  [ 30,   'Zinc',          ['Zn'],                                                                                                                                 [1.0, 1.0, 1.0],  [180, 180, 30 ] ,[200,128,51]  ],         #	glColor3f(.70, .13, .13) # firebrick
            'Ga' :  [ 31,   'Gallium',       ['Ga'],                                                                                                                                 [1.0, 1.0, 1.0],  [180, 180, 30 ] ,[125,128,176]  ],        #elif a.symbol == "HE":
            'Ge' :  [ 32,   'Germanium',     ['Ge'],                                                                                                                                 [1.0, 1.0, 1.0],  [100, 100, 150] ,[194,143,143]  ],        #	glColor3f(1.0, .75, .80) # pink
            'As' :  [ 33,   'Arsenic',       ['As'],                                                                                                                                 [1.0, 1.0, 1.0],  [60, 60, 60   ] ,[102,143,143]  ],        #else:
            'Se' :  [ 34,   'Selenium',      ['Se'],                                                                                                                                 [1.0, 1.0, 1.0],  [120, 100, 10 ] ,[189,128,227]  ],        #	glColor3f(0.9, 0.1, 0.6) # deep pink
            'Br' :  [ 35,   'Bromine',       ['Br'],                                                                                                                                 [1.0, 1.0, 1.0],  [110, 120, 30 ] ,[255,161,0]   ],
            'Kr' :  [ 36,   'Krypton',       ['Kr'],                                                                                                                                 [1.0, 1.0, 1.0],  [10, 105, 120 ] ,[166,41,41]   ],
            'Rb' :  [ 37,   'Rubidium',      ['Rb'],                                                                                                                                 [1.0, 1.0, 1.0],  [180, 180, 180] ,[92,184,209]  ],
            'Sr' :  [ 38,   'Strontium',     ['Sr'],                                                                                                                                 [1.0, 1.0, 1.0],  [130, 90, 30  ] ,[112,46,176]  ],
            'Y'  :  [ 39,   'Yttrium',       ['Y' ],                                                                                                                                 [1.0, 1.0, 1.0],  [90, 130, 30  ] ,[0,255,0]     ],
            'Zr' :  [ 40,   'Zirconium',     ['Zr'],                                                                                                                                 [1.0, 1.0, 1.0],  [110, 110, 30 ] ,[148,255,255]  ],
            'Nb' :  [ 41,   'Niobium',       ['Nb'],                                                                                                                                 [1.0, 1.0, 1.0],  [110, 110, 30 ] ,[148,224,224]  ],
            'Mo' :  [ 42,   'Molybdenum',    ['Mo'],                                                                                                                                 [1.0, 1.0, 1.0],  [110, 110, 30 ] ,[115,194,201]  ],
            'Tc' :  [ 43,   'Technetium',    ['Tc'],                                                                                                                                 [1.0, 1.0, 1.0],  [110, 110, 30 ] ,[84,181,181]  ],
            'Ru' :  [ 44,   'Ruthenium',     ['Ru'],                                                                                                                                 [1.0, 1.0, 1.0],  [110, 110, 30 ] ,[59,158,158]  ],
            'Rh' :  [ 45,   'Rhodium',       ['Rh'],                                                                                                                                 [1.0, 1.0, 1.0],  [110, 110, 30 ] ,[36,143,143]  ],
            'Pd' :  [ 46,   'Palladium',     ['Pd'],                                                                                                                                 [1.0, 1.0, 1.0],  [110, 110, 30 ] ,[10,125,140]  ],
            'Ag' :  [ 47,   'Silver',        ['Ag'],                                                                                                                                 [1.0, 1.0, 1.0],  [110, 110, 30 ] ,[0,105,133]   ],
            'Cd' :  [ 48,   'Cadmium',       ['Cd'],                                                                                                                                 [1.0, 1.0, 1.0],  [110, 110, 30 ] ,[192,192,192]  ],
            'In' :  [ 49,   'Indium',        ['In'],                                                                                                                                 [1.0, 1.0, 1.0],  [110, 110, 30 ] ,[255,217,143]  ],
            'Sn' :  [ 50,   'Tin',           ['Sn'],                                                                                                                                 [1.0, 1.0, 1.0],  [100, 100, 150] ,[166,117,115]  ],
            'Sb' :  [ 51,   'Antimony',      ['Sb'],                                                                                                                                 [1.0, 1.0, 1.0],  [90, 90, 90   ] ,[102,128,128]  ],
            'Te' :  [ 52,   'Tellurium',     ['Te'],                                                                                                                                 [1.0, 1.0, 1.0],  [120, 100, 10 ] ,[158,99,181]  ],
            'I'  :  [ 53,   'Iodine',        ['I' ],                                                                                                                                 [1.0, 1.0, 1.0],  [110, 120, 30 ] ,[212,122,0]   ],
            'Xe' :  [ 54,   'Xenon',         ['Xe'],                                                                                                                                 [1.0, 1.0, 1.0],  [10, 105, 120 ] ,[148,0,148]   ],
            'Cs' :  [ 55,   'Cesium',        ['Cs'],                                                                                                                                 [1.0, 1.0, 1.0],  [180, 180, 180] ,[66,158,176]  ],
            'Ba' :  [ 56,   'Barium',        ['Ba'],                                                                                                                                 [1.0, 1.0, 1.0],  [130, 90, 30  ] ,[87,23,143]   ],
            'La' :  [ 57,   'Lanthanum',     ['La'],                                                                                                                                 [1.0, 1.0, 1.0],  [90, 130, 30  ] ,[0,201,0]     ],
            'Ce' :  [ 58,   'Cerium',        ['Ce'],                                                                                                                                 [1.0, 1.0, 1.0],  [150, 150, 30 ] ,[112,212,255]  ],
            'Pr' :  [ 59,   'Praseodymium',  ['Pr'],                                                                                                                                 [1.0, 1.0, 1.0],  [10, 105, 10  ] ,[255,255,199]  ],
            'Nd' :  [ 60,   'Neodymium',     ['Nd'],                                                                                                                                 [1.0, 1.0, 1.0],  [10, 105, 10  ] ,[217,255,199]  ],
            'Pm' :  [ 61,   'Promethium',    ['Pm'],                                                                                                                                 [1.0, 1.0, 1.0],  [10, 105, 10  ] ,[199,255,199]  ],
            'Sm' :  [ 62,   'Samarium',      ['Sm'],                                                                                                                                 [1.0, 1.0, 1.0],  [10, 105, 10  ] ,[163,255,199]  ],
            'Eu' :  [ 63,   'Europium',      ['Eu'],                                                                                                                                 [1.0, 1.0, 1.0],  [10, 105, 10  ] ,[143,255,199]  ],
            'Gd' :  [ 64,   'Gadolinium',    ['Gd'],                                                                                                                                 [1.0, 1.0, 1.0],  [10, 105, 10  ] ,[97,255,199]  ],
            'Tb' :  [ 65,   'Terbium',       ['Tb'],                                                                                                                                 [1.0, 1.0, 1.0],  [10, 105, 10  ] ,[69,255,199]  ],
            'Dy' :  [ 66,   'Dysprosium',    ['Dy'],                                                                                                                                 [1.0, 1.0, 1.0],  [10, 105, 10  ] ,[48,255,199]  ],
            'Ho' :  [ 67,   'Holmium',       ['Ho'],                                                                                                                                 [1.0, 1.0, 1.0],  [10, 105, 10  ] ,[31,255,199]  ],
            'Er' :  [ 68,   'Erbium',        ['Er'],                                                                                                                                 [1.0, 1.0, 1.0],  [10, 105, 10  ] ,[0,255,156]   ],
            'Tm' :  [ 69,   'Thulium',       ['Tm'],                                                                                                                                 [1.0, 1.0, 1.0],  [10, 105, 10  ] ,[0,230,117]   ],
            'Yb' :  [ 70,   'Ytterbium',     ['Yb'],                                                                                                                                 [1.0, 1.0, 1.0],  [10, 105, 10  ] ,[0,212,82]    ],
            'Lu' :  [ 71,   'Lutetium',      ['Lu'],                                                                                                                                 [1.0, 1.0, 1.0],  [10, 105, 10  ] ,[0,191,56]    ],
            'Hf' :  [ 72,   'Hafnium',       ['Hf'],                                                                                                                                 [1.0, 1.0, 1.0],  [10, 105, 10  ] ,[0,171,36]    ],
            'Ta' :  [ 73,   'Tantalum',      ['Ta'],                                                                                                                                 [1.0, 1.0, 1.0],  [150, 150, 30 ] ,[77,194,255]  ],
            'W'  :  [ 74,   'Tungsten',      ['W' ],                                                                                                                                 [1.0, 1.0, 1.0],  [150, 150, 30 ] ,[77,166,255]  ],
            'Re' :  [ 75,   'Rhenium',       ['Re'],                                                                                                                                 [1.0, 1.0, 1.0],  [150, 150, 30 ] ,[33,148,214]  ],
            'Os' :  [ 76,   'Osmium',        ['Os'],                                                                                                                                 [1.0, 1.0, 1.0],  [150, 150, 30 ] ,[38,125,171]  ],
            'Ir' :  [ 77,   'Iridium',       ['Ir'],                                                                                                                                 [1.0, 1.0, 1.0],  [150, 150, 30 ] ,[38,102,150]  ],
            'Pt' :  [ 78,   'Platinum',      ['Pt'],                                                                                                                                 [1.0, 1.0, 1.0],  [150, 150, 30 ] ,[23,84,135]   ],
            'Au' :  [ 79,   'Gold',          ['Au'],                                                                                                                                 [1.0, 1.0, 1.0],  [150, 150, 30 ] ,[208,208,224]  ],
            'Hg' :  [ 80,   'Mercury',       ['Hg'],                                                                                                                                 [1.0, 1.0, 1.0],  [150, 150, 30 ] ,[255,209,35]  ],
            'Tl' :  [ 81,   'Thallium',      ['Tl'],                                                                                                                                 [1.0, 1.0, 1.0],  [150, 150, 30 ] ,[184,184,208]  ],
            'Pb' :  [ 82,   'Lead',          ['Pb'],                                                                                                                                 [1.0, 1.0, 1.0],  [100, 100, 150] ,[166,84,77]   ],
            'Bi' :  [ 83,   'Bismuth',       ['Bi'],                                                                                                                                 [1.0, 1.0, 1.0],  [90, 90, 90   ] ,[87,89,97]    ],
            'Po' :  [ 84,   'Polonium',      ['Po'],                                                                                                                                 [1.0, 1.0, 1.0],  [120, 100, 10 ] ,[158,79,181]  ],
            'At' :  [ 85,   'Astatine',      ['At'],                                                                                                                                 [1.0, 1.0, 1.0],  [110, 120, 30 ] ,[171,92,0]    ],
            'Rn' :  [ 86,   'Radon',         ['Rn'],                                                                                                                                 [1.0, 1.0, 1.0],  [10, 105, 120 ] ,[117,79,69]   ],
            'Fr' :  [ 87,   'Francium',      ['Fr'],                                                                                                                                 [1.0, 1.0, 1.0],  [180, 180, 180] ,[66,130,150]  ],
            'Ra' :  [ 88,   ' radium',       ['Ra'],                                                                                                                                 [1.0, 1.0, 1.0],  [130, 90, 30  ] ,[66,0,102]    ],
            'Ac' :  [ 89,   'Actinium',      ['Ac'],                                                                                                                                 [1.0, 1.0, 1.0],  [90, 130, 30  ] ,[0,125,0]     ],
            'Th' :  [ 90,   'Thorium',       ['Th'],                                                                                                                                 [1.0, 1.0, 1.0],  [180, 180, 30 ] ,[112,171,250]  ],
            'Pa' :  [ 91,   'Protactinium',  ['Pa'],                                                                                                                                 [1.0, 1.0, 1.0],  [120, 100, 10 ] ,[0,186,255]   ],
            'U'  :  [ 92,   'Uranium',       ['U' ],                                                                                                                                 [1.0, 1.0, 1.0],  [120, 100, 10 ] ,[0,161,255]   ],
            'Np' :  [ 93,   'Neptunium',     ['Np'],                                                                                                                                 [1.0, 1.0, 1.0],  [120, 100, 10 ] ,[0,143,255]   ],
            'Pu' :  [ 94,   'Plutionium',    ['Pu'],                                                                                                                                 [1.0, 1.0, 1.0],  [120, 100, 10 ] ,[0,128,255]   ],
            'Am' :  [ 95,   'Americium',     ['Am'],                                                                                                                                 [1.0, 1.0, 1.0],  [120, 100, 10 ] ,[0,107,255]   ],
            'Cm' :  [ 96,   'Curium',        ['Cm'],                                                                                                                                 [1.0, 1.0, 1.0],  [120, 100, 10 ] ,[84,92,242]   ],
            'Bk' :  [ 97,   'Berkelium',     ['Bk'],                                                                                                                                 [1.0, 1.0, 1.0],  [120, 100, 10 ] ,[120,92,227]  ],
            'Cf' :  [ 98,   'Californium',   ['Cf'],                                                                                                                                 [1.0, 1.0, 1.0],  [120, 100, 10 ] ,[138,79,227]  ],
            'Es' :  [ 99,   'Einsteinium',   ['Es'],                                                                                                                                 [1.0, 1.0, 1.0],  [120, 100, 10 ] ,[161,54,212]  ],
            'Fm' :  [ 100,  'Fermium',       ['Fm'],                                                                                                                                 [1.0, 1.0, 1.0],  [120, 100, 10 ] ,[179,31,212]  ],
            'Md' :  [ 101,  'Mendelevium',   ['Md'],                                                                                                                                 [1.0, 1.0, 1.0],  [120, 100, 10 ] ,[179,31,186]  ],
            'No' :  [ 102,  'Nobelium',      ['No'],                                                                                                                                 [1.0, 1.0, 1.0],  [120, 100, 10 ] ,[179,13,166]  ],
            'Lr' :  [ 103,  'Lawrencium',    ['Lr'],                                                                                                                                 [1.0, 1.0, 1.0],  [120, 100, 10 ] ,[189,13,135]  ],
            'Rf' :  [ 104,  'Rutherfordium', ['Rf'],                                                                                                                                 [1.0, 1.0, 1.0],  [120, 100, 10 ] ,[199,0,102]   ],
            'Db' :  [ 105,  'Dubnium',       ['Db'],                                                                                                                                 [1.0, 1.0, 1.0],  [230, 230, 230] ,[204,0,89]   ],
            'Sg' :  [ 106,  'Seaborgium',    ['Sg'],                                                                                                                                 [1.0, 1.0, 1.0],  [230, 230, 230] ,[209,0,79]   ],
            'Bh' :  [ 107,  'Bohrium',       ['Bh'],                                                                                                                                 [1.0, 1.0, 1.0],  [179, 0, 179 ]  ,[217,0,69]   ],
            'Hs' :  [ 108,  'Hassium',       ['Hs'],                                                                                                                                 [1.0, 1.0, 1.0],  [179, 0, 179 ]  ,[224,0,56]   ],
            'Mt' :  [ 109,  'Meitnerium',    ['Mt'],                                                                                                                                 [1.0, 1.0, 1.0],  [179, 0, 179 ]  ,[230,0,46]   ],
            'Xx' :  [ 0,    'Dummy',         ['Xx'],                                                                                                                                 [1.0, 1.0, 1.0],  [179, 0, 179 ]  ,[235,0,38]   ],
            'X'  :  [ 0,    'Dummy',         ['X' ],                                                                                                                                 [1.0, 1.0, 1.0],  [179, 0, 179 ]  ,[235,0,38]   ]
            }




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



def parse_MOL2File (lines):
    """ Function doc """
    try:
        i_HEADER = lines.index('@<TRIPOS>MOLECULE\n')
    except:
        print ' - - invalid mol2 file - - '
    
    try:
        i_ATOMS = lines.index('@<TRIPOS>ATOM\n')
    except:
        print ' - - invalid mol2 file - - '

    try:
        i_BONDS = lines.index('@<TRIPOS>BOND\n')
    except:
        print ' - - invalid mol2 file - - '
    
    #----------------------------------#
    #              HEADER              #
    #----------------------------------#
    lines_header = []
    for line in lines[i_HEADER+1:i_ATOMS]:
        line = line.split()
        if len(line) == 5:
            lines_header.append(line)
    #print lines_header
    
    #----------------------------------#
    #              ATOMS               #
    #----------------------------------#
    lines_atoms = []
    for line in lines[i_ATOMS+1:i_BONDS]:
        line = line.split()
        if len(line) == 9:
            lines_atoms.append(line)
    #print lines_atoms
    
    #----------------------------------#
    #              BONDS               #
    #----------------------------------#
    lines_bonds = []
    for line in lines[i_BONDS+1:]:
        line = line.split()
        #print line
        if len(line) == 4:
            lines_bonds.append(line)
    
    return lines_header, lines_atoms, lines_bonds
    #----------------------------------#

def parse_LinesToMatrix (lines_atoms = None, matrix = None):
    """ Function doc """
    n = len(lines_atoms)
    #a_position = np.zeros(n, 3)
    
    
    n = 0
    for line in lines_atoms:
        index  = line[0]
        a_name = line[1]
        x      = line[2]
        y      = line[3]
        z      = line[4]
        a_type = line[5]
        resi   = line[6]
        resn   = line[7]
        chrg   = line[8]
        symbol = ATOMTYPES[a_name][1]
        
        matrix['a_position'][n][0] = float(x)
        matrix['a_position'][n][1] = float(y)
        matrix['a_position'][n][2] = float(z)
        matrix['a_symbol'][n]      = symbol
        matrix['a_name'][n]        = a_name
        matrix['a_charge'][n]      = float(chrg)
        
        
        if a_name == "H":
            matrix['a_size'] [n] = 0.25
            
        else:
            matrix['a_size'][n] = 0.4
        
        matrix['a_color'][n] = ATOMTYPES[a_name][3]
        
        
        #print index, a_name, symbol
        n += 1
    return matrix


def import_MOL2FileToSystem (filein = None, log = False):
    """ Function doc """
    filein =  open(filein, 'r')
    filein = filein.readlines()
    lines_header, lines_atoms, lines_bonds = parse_MOL2File (filein)
    
    #print lines_atoms
   
    m_size = len(lines_atoms)
    data = np.zeros(m_size, [('a_position', np.float32, 3),
                             ('a_color'   , np.float32, 3),
                             ('a_name'    , np.str,     1),
                             ('a_symbol'  , np.str,     1),
                             ('a_number'  , np.float32, 1),
                             ('a_charge'  , np.float32, 1),
                             ('a_size'    , np.float32, 1)])
    
    b_size = len (lines_atoms)
    bonds  = np.zeros(m_size, [('bonds', np.int, 2)])
    n = 0
    for line in lines_bonds:
        bonds['bonds'][n+1][0] = line[1]
        bonds['bonds'][n+1][1] = line[2]
        n += 1
    
    
    #print bonds
    data = parse_LinesToMatrix(lines_atoms, data)
    return data , bonds
    

#data = import_MOL2FileToSystem(filein = '/home/fernando/Dropbox/PyOpenMOL/PyOpenMol2/examples/mol2/molecule02.mol2')


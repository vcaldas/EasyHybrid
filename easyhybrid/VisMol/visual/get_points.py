#!/usr/bin/env python

import math, sys

def get_puntos(nivel):
    puntos = []
    angulo = 2*math.pi/nivel
    mitad = angulo/2.0
    #mitad = 0
    for i in range(nivel):
        puntos.append(math.cos(angulo*i+mitad))
        puntos.append(0.0)
        puntos.append(math.sin(angulo*i+mitad))
    return puntos

niv = int(sys.argv[1])
puntos = get_puntos(niv)
for i in range(len(puntos)/3):
    print '%1.12f, %1.12f, %1.12f,' %(puntos[i*3], puntos[i*3+1], puntos[i*3+2])


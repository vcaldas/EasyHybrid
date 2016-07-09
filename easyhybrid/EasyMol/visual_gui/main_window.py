#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main_window.py
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


    
    
    def switch_ball_stick(self, button):
	""" Turn on/off Ball-Stick representation.
	"""
	self.BALL_STICK = not self.BALL_STICK
	self.draw_ball_stick()
	self.queue_draw()
	return True
    
    
    def switch_dots(self, button):
	""" Turn on/off Dots representation.
	"""
	self.DOTS = not self.DOTS
	self.draw_dots()
	self.queue_draw()
	return True
    
    def switch_lines(self, button):
	""" Turn on/off Lines representation.
	"""
	self.LINES = not self.LINES
	self.draw_lines()
	self.queue_draw()
	return True
    
    def switch_pretty_vdw(self, button):
	""" Turn on/off the Pretty VDW representation.
	"""
	self.PRETTY_VDW = not self.PRETTY_VDW
	self.draw_pretty_vdw()
	self.queue_draw()
	return True
    
    def switch_ribbon(self, button):
	""" Turn on/off the Ribbon representation.
	"""
	self.RIBBON = not self.RIBBON
	self.draw_ribbon()
	self.queue_draw()
	return True
    
    def switch_spheres(self, button):
	""" Turn on/off the Sphere representation.
	"""
	self.SPHERES = not self.SPHERES
	self.draw_spheres()
	self.queue_draw()
	return True
    
    def switch_vdw(self, button):
	""" Turn on/off the Van-Der-Waals representation.
	"""
	self.VDW = not self.VDW
	self.draw_vdw()
	self.queue_draw()
	return True
    
    def switch_wires(self, button):
	""" Turn on/off the Wires representation.
	"""
	self.WIRES = not self.WIRES
	self.draw_wires()
	self.queue_draw()
	return True
    















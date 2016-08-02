#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  shaders.py
#  
#  Copyright 2016 Labio <labio@labio-XPS-8300>
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

my_glLigth = """
struct gl_LightSourceParameters {
   vec4 ambient;              // Aclarri
   vec4 diffuse;              // Dcli
   vec4 specular;             // Scli
   vec4 position;             // Ppli
   vec4 halfVector;           // Derived: Hi
   vec3 spotDirection;        // Sdli
   float spotExponent;        // Srli
   float spotCutoff;          // Crli
                              // (range: [0.0,90.0], 180.0)
   float spotCosCutoff;       // Derived: cos(Crli)
                              // (range: [1.0,0.0],-1.0)
   float constantAttenuation; // K0 
   float linearAttenuation;   // K1 
   float quadraticAttenuation;// K2
};

uniform gl_LightSourceParameters gl_LightSource[gl_MaxLights];
"""

my_glMaterial = """
struct gl_MaterialParameters {
   vec4 emission;    // Ecm 
   vec4 ambient;     // Acm 
   vec4 diffuse;     // Dcm 
   vec4 specular;    // Scm 
   float shininess;  // Srm
};


uniform gl_MaterialParameters gl_FrontMaterial;
uniform gl_MaterialParameters gl_BackMaterial;
"""

vertex_shader = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 projection_mat;

in vec3 coordinate;
in vec3 vert_color;

out vec3 sh_color;

void main()
{
   gl_Position = projection_mat * view_mat * model_mat * vec4(coordinate, 1.0);
   sh_color = vert_color;
}
"""

fragment_shader = """
#version 330

in vec3 sh_color;

out vec4 final_color;

void main()
{
   final_color = vec4(sh_color, 1.0);
}
"""

geometry_shader = """
#version 330

in Coords {
    vec4 my_cords;
    vec3 my_col;
} corners[];

out vec3 sh_color;

void main(){
    gl_Position = corners[0].my_cords;
    sh_color = corners[0].my_col;
}
"""

vertex_shader2 = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 projection_mat;
uniform vec3 vert_cam_pos;

in vec3 coordinate;
in vec3 vert_color;
//in vec3 vert_cam_pos;

out vec3 frag_vert;
out vec3 frag_color;
out vec3 frag_normal;
out vec3 frag_cam_pos;

void main(){
   gl_Position = projection_mat * view_mat * model_mat * vec4(coordinate, 1.0);
   frag_vert = coordinate;
   frag_color = vert_color;
   frag_normal = coordinate;
   frag_cam_pos = vert_cam_pos;
}
"""

fragment_shader2 = """
#version 330

struct Light {
   vec3 position;
   vec3 color;
   vec3 intensity;
   vec3 specular_color;
   float ambient_coef;
   float shininess;
};

uniform mat4 model_mat;
uniform Light my_light;

in vec3 frag_vert;
in vec3 frag_color;
in vec3 frag_normal;
in vec3 frag_cam_pos;

out vec4 final_color;

void main(){
   mat3 normal_mat = transpose(inverse(mat3(model_mat)));
   vec3 normal = normalize(normal_mat * frag_normal);
   
   vec3 frag_pos = vec3(model_mat * vec4(frag_vert, 1.0));
   
   vec3 vert_to_light = normalize(my_light.position - frag_pos);
   
   float diffuse_coef = max(0.0, dot(normal, vert_to_light));
   vec3 diffuse = diffuse_coef * my_light.color * frag_color;
   
   vec3 ambient = my_light.ambient_coef * frag_color * my_light.intensity;
   
   vec3 incidence_vec = -vert_to_light;
   vec3 reflection_vec = reflect(incidence_vec, normal);
   vec3 vert_to_cam = normalize(frag_cam_pos - frag_vert);
   float cos_angle = max(0.0, dot(vert_to_cam, reflection_vec));
   float specular_coef = pow(cos_angle, my_light.shininess);
   vec3 specular = specular_coef * my_light.specular_color * my_light.intensity;
   
   final_color = vec4(ambient + diffuse + specular, 1.0);
}
"""













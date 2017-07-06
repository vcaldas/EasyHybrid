#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  vismol_shaders.py
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

vertex_shader_dots = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 projection_mat;
uniform mat3 normal_mat;
uniform float vert_ext_linewidth;
uniform float vert_int_antialias;
uniform float vert_dot_factor;

in vec3 vert_coord;
in vec3 vert_color;
in float vert_dot_size;
out vec4 crd_dist;
attribute vec4 bckgrnd_color;

varying float frag_dot_size;
varying float frag_ext_linewidth;
varying float frag_int_antialias;
varying vec4 frag_dot_color;
varying vec4 frag_bckgrnd_color;

void main(){
    frag_dot_size = vert_dot_size * vert_dot_factor;
    frag_ext_linewidth = vert_ext_linewidth;
    frag_int_antialias = vert_int_antialias;
    frag_dot_color = vec4(vert_color, 1.0);
    frag_bckgrnd_color = bckgrnd_color;
    crd_dist = view_mat * model_mat * vec4(vert_coord, 1);
    gl_Position = projection_mat * view_mat * model_mat * vec4(vert_coord, 1);
    gl_PointSize = vert_dot_size + 2*(vert_ext_linewidth + 1.5*vert_int_antialias);
}
"""
fragment_shader_dots = """
#version 330

uniform vec4 fog_color;
uniform float fog_start;
uniform float fog_end;

in vec4 crd_dist;
out vec4 final_color;

varying vec4 frag_bckgrnd_color;
varying vec4 frag_dot_color;
varying float frag_dot_size;
varying float frag_ext_linewidth;
varying float frag_int_antialias;

float disc(vec2 P, float size)
{
     float r = length((P.xy - vec2(0.5,0.5))*size);
     r -= frag_dot_size/2;
     return r;
}

void main(){
    // Calculate the distance of the object
    float dist =  abs(crd_dist.z);
    float size = frag_dot_size +2*(frag_ext_linewidth + 1.5*frag_int_antialias);
    float t = frag_ext_linewidth/2.0-frag_int_antialias;
    
    // gl_PointCoord is the pixel in the coordinate
    float r = disc(gl_PointCoord, size);
    float d = abs(r) - t;
    
    // This if else statement makes the circle ilusion
    if( r > (frag_ext_linewidth/2.0+frag_int_antialias)){
        discard;
    }
    else{
        if( d < 0.0 ){
            final_color = frag_bckgrnd_color;
        }
        else{
            float alpha = d/frag_int_antialias;
            alpha = exp(-alpha*alpha);
            if (r > 0){
                final_color = frag_bckgrnd_color;
            }
            else{
                float fog_factor = (fog_end-dist)/(fog_end-fog_start);
                vec4 my_color = mix(frag_dot_color, frag_bckgrnd_color, alpha);
                final_color = mix(fog_color, my_color, fog_factor);
            }
        }
    }
}
"""

vertex_shader_lines = """
#version 330

in vec3 vert_coord;
in vec3 vert_color;

out vec3 geom_color;

void main(){
    gl_Position = vec4(vert_coord, 1.0);
    geom_color = vert_color;
}
"""
geometry_shader_lines = """
#version 330

layout (lines) in;
layout (line_strip, max_vertices = 4) out;

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 projection_mat;

in vec3 geom_color[];

out vec3 frag_color;
out vec4 crd_dist;

void main(){
    vec4 mid_coord = vec4((gl_in[1].gl_Position.xyz + gl_in[0].gl_Position.xyz)/2, 1.0);
    gl_Position = projection_mat * view_mat * model_mat * gl_in[0].gl_Position;
    frag_color = geom_color[0];
    crd_dist = view_mat * model_mat * gl_in[0].gl_Position;
    EmitVertex();
    gl_Position = projection_mat * view_mat * model_mat * mid_coord;
    frag_color = geom_color[0];
    crd_dist = view_mat * model_mat * mid_coord;
    EmitVertex();
    EndPrimitive();
    gl_Position = projection_mat * view_mat * model_mat * mid_coord;
    frag_color = geom_color[1];
    crd_dist = view_mat * model_mat * mid_coord;
    EmitVertex();
    gl_Position = projection_mat * view_mat * model_mat * gl_in[1].gl_Position;
    crd_dist = view_mat * model_mat * gl_in[1].gl_Position;
    frag_color = geom_color[1];
    EmitVertex();
    EndPrimitive();
}
"""
fragment_shader_lines = """
#version 330

uniform vec4 fog_color;
uniform float fog_start;
uniform float fog_end;

in vec3 frag_color;
in vec4 crd_dist;

out vec4 final_color;

void main(){
    float dist = abs(crd_dist.z);
    if(dist>=fog_start){
        float fog_factor = (fog_end-dist)/(fog_end-fog_start);
        final_color = mix(fog_color, vec4(frag_color, 1.0), fog_factor);
    }
    else{
       final_color = vec4(frag_color, 1.0);
    }
}
"""






'''
################################################################################

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

in vec3 coordinate;
in vec3 vert_color;

out vec3 frag_vert;
out vec3 frag_color;
out vec3 frag_normal;

void main(){
   gl_Position = projection_mat * view_mat * model_mat * vec4(coordinate, 1.0);
   frag_vert = vec3(view_mat * model_mat * vec4(coordinate, 1.0));
   frag_color = vert_color;
   frag_normal = frag_vert;
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

uniform Light my_light;
uniform mat4 model_mat;
uniform mat3 normal_mat;
uniform vec3 cam_pos;

in vec3 frag_vert;
in vec3 frag_color;
in vec3 frag_normal;

out vec4 final_color;

void main(){
   vec3 normal = normalize(normal_mat * frag_normal);
   
   vec3 vert_to_light = normalize(my_light.position - frag_vert);
   
   float diffuse_coef = max(0.0, dot(normal, vert_to_light));
   vec3 diffuse = diffuse_coef * my_light.color * frag_color;
   
   vec3 ambient = my_light.ambient_coef * frag_color * my_light.intensity;
   
   vec3 incidence_vec = -vert_to_light;
   vec3 reflection_vec = reflect(incidence_vec, normal);
   vec3 vert_to_cam = normalize(cam_pos - frag_vert);
   float cos_angle = max(0.0, dot(vert_to_cam, reflection_vec));
   float specular_coef = pow(cos_angle, my_light.shininess);
   vec3 specular = specular_coef * my_light.specular_color * my_light.intensity;
   
   final_color = vec4(ambient + diffuse + specular, 1.0);
}
"""

vertex_shader3 = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 projection_mat;

in vec3 coordinate;
in vec3 vert_color;

out vec3 frag_coord;
out vec3 frag_color;
out vec3 frag_normal;

void main(){
   gl_Position = projection_mat * view_mat * model_mat * vec4(coordinate, 1.0);
   frag_coord = vec3(model_mat * vec4(coordinate, 1.0));
   frag_normal = coordinate;
   frag_color = vert_color;
}
"""
fragment_shader3 = """
#version 330

struct Light {
   vec3 position;
   vec3 color;
   vec3 intensity;
   vec3 specular_color;
   float ambient_coef;
   float shininess;
};

uniform Light my_light;
uniform mat4 model_mat;
uniform mat3 normal_mat;
uniform vec3 cam_pos;

in vec3 frag_coord;
in vec3 frag_color;
in vec3 frag_normal;

out vec4 final_color;

void main(){
   vec3 normal = normalize(normal_mat * frag_normal);
   
   vec3 vert_to_light = normalize(my_light.position - frag_coord);
   vec3 vert_to_cam = normalize(cam_pos - frag_coord);
   
   vec3 ambient = my_light.ambient_coef * frag_color * my_light.intensity;
   
   float diffuse_coef = max(0.0, dot(normal, vert_to_light));
   vec3 diffuse = diffuse_coef * frag_color * my_light.intensity;
   
   float specular_coef = 0.0;
   if (diffuse_coef > 0.0)
      specular_coef = pow(max(0.0, dot(vert_to_cam, reflect(-vert_to_light, normal))), my_light.shininess);
   vec3 specular = specular_coef * vec3(1) * my_light.intensity;
   specular = specular * (vec3(1) - diffuse);
   
   final_color = vec4(ambient + diffuse + specular, 1.0);
}
"""

vertex_shader4 = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 projection_mat;
uniform mat3 normal_mat;

in vec3 coordinate;
in vec3 center;
in vec3 vert_color;

out vec3 frag_coord;
out vec3 frag_color;
out vec3 frag_normal;

void main(){
   mat4 modelview = view_mat * model_mat;
   gl_Position = projection_mat * modelview * vec4(coordinate, 1.0);
   frag_coord = -vec3(modelview * vec4(coordinate, 1.0));
   frag_normal = normalize(normal_mat * (coordinate - center));
   frag_color = vert_color;
}
"""
fragment_shader4 = """
#version 330

struct Light {
   vec3 position;
   vec3 color;
   vec3 intensity;
   vec3 specular_color;
   float ambient_coef;
   float shininess;
};

uniform Light my_light;
uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat3 normal_mat;
uniform vec3 cam_pos;

in vec3 frag_coord;
in vec3 frag_color;
in vec3 frag_normal;

out vec4 final_color;

void main(){
   //vec3 normal = normalize(frag_normal);
   //vec3 eye = normalize(frag_coord);
   //
   //vec3 vert_to_light = normalize(vec3(view_mat*vec4(my_light.position, 0.0)));
   ////vec3 vert_to_cam = normalize(frag_coord);
   //
   //vec3 spec = vec3(0.0);
   //float intensity = max(dot(normal, vert_to_light), 0.0);
   //if (intensity>0.0){
   //   vec3 h = normalize(vert_to_light + eye);
   //   float int_spec = max(dot(h, normal), 0.0);
   //   spec = my_light.intensity * pow(int_spec, my_light.shininess);
   //}
   //vec3 ambient = my_light.ambient_coef * frag_color * my_light.intensity;
   //float diffuse_coef = max(0.0, dot(normal, vert_to_light));
   //vec3 diffuse = diffuse_coef * frag_color * my_light.intensity;
   //final_color = vec4(intensity * diffuse + spec + ambient, 1.0);
   
   vec3 normal = normalize(frag_normal);
   vec3 vert_to_light = normalize(my_light.position);
   vec3 vert_to_cam = normalize(frag_coord);
   
   // Ambient Component
   vec3 ambient = my_light.ambient_coef * frag_color * my_light.intensity;
   
   // Diffuse component
   float diffuse_coef = max(0.0, dot(normal, vert_to_light));
   vec3 diffuse = diffuse_coef * frag_color * my_light.intensity;
   
   // Specular component
   float specular_coef = 0.0;
   if (diffuse_coef > 0.0)
      specular_coef = pow(max(0.0, dot(vert_to_cam, reflect(-vert_to_light, normal))), my_light.shininess);
   vec3 specular = specular_coef * my_light.intensity;
   specular = specular * (vec3(1) - diffuse);
   
   final_color = vec4(ambient + diffuse + specular, 1.0);
}
"""

vertex_shader_sphere = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 projection_mat;
uniform mat3 normal_mat;

in vec3 coordinate;
in vec3 center;
in vec3 vert_color;

out vec3 frag_coord;
out vec3 frag_color;
out vec3 frag_normal;

void main(){
   mat4 modelview = view_mat * model_mat;
   gl_Position = projection_mat * modelview * vec4(coordinate, 1.0);
   frag_coord = -vec3(modelview * vec4(coordinate, 1.0));
   frag_normal = normalize(normal_mat * (coordinate - center));
   frag_color = vert_color;
}
"""
fragment_shader_sphere = """
#version 330

struct Light {
   vec3 position;
   vec3 color;
   vec3 intensity;
   vec3 specular_color;
   float ambient_coef;
   float shininess;
};

uniform Light my_light;
uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat3 normal_mat;
uniform vec3 cam_pos;

in vec3 frag_coord;
in vec3 frag_color;
in vec3 frag_normal;

out vec4 final_color;

void main(){
   vec3 normal = normalize(frag_normal);
   vec3 vert_to_light = normalize(my_light.position);
   vec3 vert_to_cam = normalize(frag_coord);
   
   // Ambient Component
   vec3 ambient = my_light.ambient_coef * frag_color * my_light.intensity;
   
   // Diffuse component
   float diffuse_coef = max(0.0, dot(normal, vert_to_light));
   vec3 diffuse = diffuse_coef * frag_color * my_light.intensity;
   
   // Specular component
   float specular_coef = 0.0;
   if (diffuse_coef > 0.0)
      specular_coef = pow(max(0.0, dot(vert_to_cam, reflect(-vert_to_light, normal))), my_light.shininess);
   vec3 specular = specular_coef * my_light.intensity;
   specular = specular * (vec3(1) - diffuse);
   
   final_color = vec4(ambient + diffuse + specular, 1.0);
}
"""

vertex_shader_crystal = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 projection_mat;
uniform mat3 normal_mat;

in vec3 coordinate;
in vec3 center;
in vec3 vert_color;

out vec3 frag_coord;
out vec3 frag_normal;
out vec3 frag_color;

void main(){
   mat4 modelview = view_mat * model_mat;
   gl_Position = projection_mat * modelview * vec4(coordinate, 1.0);
   frag_coord = -vec3(modelview * vec4(coordinate, 1.0));
   frag_normal = normalize(normal_mat * (coordinate - center));
   frag_color = vert_color;
}
"""
fragment_shader_crystal = """
#version 330

struct Light {
   vec3 position;
   vec3 color;
   vec3 intensity;
   vec3 specular_color;
   float ambient_coef;
   float shininess;
};

uniform Light my_light;
uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat3 normal_mat;
uniform vec3 cam_pos;

in vec3 frag_coord;
in vec3 frag_color;
in vec3 frag_normal;

out vec4 final_color;

void main(){
   vec3 normal = normalize(frag_normal);
   vec3 vert_to_light = normalize(my_light.position);
   vec3 vert_to_cam = normalize(frag_coord);
   
   // Ambient Component
   vec3 ambient = my_light.ambient_coef * frag_color * my_light.intensity;
   
   // Diffuse component
   float diffuse_coef = max(0.0, dot(normal, vert_to_light));
   vec3 diffuse = diffuse_coef * frag_color * my_light.intensity;
   
   final_color = vec4(ambient + diffuse, 0.6);
}
"""

vertex_shader_dots = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 projection_mat;
uniform mat3 normal_mat;

in vec3 coordinate;
in vec3 vert_color;

out vec3 frag_color;

void main(){
   gl_Position = projection_mat * view_mat * model_mat * vec4(coordinate, 1.0);
   frag_color = vert_color;
}
"""
fragment_shader_dots = """
#version 330

in vec3 frag_color;

out vec4 final_color;

void main(){
   final_color = vec4(frag_color, 1.0);
}
"""

vertex_shader_directional_light = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 projection_mat;
uniform mat3 normal_mat;

in vec3 coordinate;
in vec3 center;
in vec3 vert_color;

out vec3 frag_coord;
out vec3 frag_color;
out vec3 frag_normal;

void main(){
   mat4 modelview = view_mat * model_mat;
   gl_Position = projection_mat * modelview * vec4(coordinate, 1.0);
   frag_coord = -vec3(modelview * vec4(coordinate, 1.0));
   frag_normal = normalize(normal_mat * (coordinate - center));
   frag_color = vert_color;
}
"""
fragment_shader_directional_light = """
#version 330

struct Light {
   vec3 position;
   vec3 color;
   vec3 intensity;
   vec3 specular_color;
   float ambient_coef;
   float shininess;
};

uniform Light my_light;
uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat3 normal_mat;
uniform vec3 cam_pos;

in vec3 frag_coord;
in vec3 frag_color;
in vec3 frag_normal;

out vec4 final_color;

void main(){
   vec3 normal = normalize(frag_normal);
   vec3 vert_to_light = normalize(my_light.position);
   vec3 vert_to_cam = normalize(frag_coord);
   
   // Ambient Component
   vec3 ambient = my_light.ambient_coef * frag_color * my_light.intensity;
   
   // Diffuse component
   float diffuse_coef = max(0.0, dot(normal, vert_to_light));
   vec3 diffuse = diffuse_coef * frag_color * my_light.intensity;
   
   // Specular component
   float specular_coef = 0.0;
   if (diffuse_coef > 0.0)
      specular_coef = pow(max(0.0, dot(vert_to_cam, reflect(-vert_to_light, normal))), my_light.shininess);
   vec3 specular = specular_coef * my_light.intensity;
   specular = specular * (vec3(1) - diffuse);
   
   final_color = vec4(ambient + diffuse + specular, 1.0);
}
"""

vertex_shader_point_light = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 projection_mat;

in vec3 coordinate;
in vec3 vert_color;

out vec3 frag_coord;
out vec3 frag_color;
out vec3 frag_normal;

void main(){
   gl_Position = projection_mat * view_mat * model_mat * vec4(coordinate, 1.0);
   frag_coord = vec3(model_mat * vec4(coordinate, 1.0));
   frag_normal = coordinate;
   frag_color = vert_color;
}
"""
fragment_shader_point_light = """
#version 330

struct Light {
   vec3 position;
   vec3 color;
   vec3 intensity;
   vec3 specular_color;
   float ambient_coef;
   float shininess;
};

uniform Light my_light;
uniform mat4 model_mat;
uniform mat3 normal_mat;
uniform vec3 cam_pos;

in vec3 frag_coord;
in vec3 frag_color;
in vec3 frag_normal;

out vec4 final_color;

void main(){
   vec3 normal = normalize(normal_mat * frag_normal);
   
   vec3 vert_to_light = normalize(my_light.position - frag_coord);
   vec3 vert_to_cam = normalize(cam_pos - frag_coord);
   
   vec3 ambient = my_light.ambient_coef * frag_color * my_light.intensity;
   
   float diffuse_coef = max(0.0, dot(normal, vert_to_light));
   vec3 diffuse = diffuse_coef * frag_color * my_light.intensity;
   
   float specular_coef = 0.0;
   if (diffuse_coef > 0.0)
      specular_coef = pow(max(0.0, dot(vert_to_cam, reflect(-vert_to_light, normal))), my_light.shininess);
   vec3 specular = specular_coef * vec3(1) * my_light.intensity;
   specular = specular * (vec3(1) - diffuse);
   
   final_color = vec4(ambient + diffuse + specular, 1.0);
}
"""

################################################################################
'''

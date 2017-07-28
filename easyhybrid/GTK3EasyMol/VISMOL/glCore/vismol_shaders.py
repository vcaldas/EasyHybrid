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


vertex_shader_picking_dots = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 projection_mat;

in vec3  vert_coord;
in vec3  vert_color;

out vec3 index_color;

void main(){
    gl_Position  = projection_mat * view_mat * model_mat * vec4(vert_coord, 1.0);
    gl_PointSize = 15;
    index_color = vert_color;
}
"""
fragment_shader_picking_dots = """
#version 330

in vec3 index_color;

void main(){
    gl_FragColor = vec4(index_color,1);
}

"""

vertex_shader_dots = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 projection_mat;
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
                if (dist > fog_start){
                    float fog_factor = (fog_end-dist)/(fog_end-fog_start);
                    vec4 my_color = mix(frag_dot_color, frag_bckgrnd_color, alpha);
                    final_color = mix(fog_color, my_color, fog_factor);
                }
                else{
                    final_color = mix(frag_dot_color, frag_bckgrnd_color, alpha);
                }
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


vertex_shader_spheres = """
#version 330

uniform vec3 light_position;
uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 projection_mat;

attribute vec3 vert_coord;
attribute vec3 vert_color;
attribute float radius;

varying vec3 frag_color;
varying vec3 frag_light_direction;
varying vec4 frag_eye_position;
varying float frag_size;
varying float frag_radius;

void main (void){
    frag_color = vert_color;
    frag_radius = radius;
    frag_eye_position = view_mat * model_mat * vec4(vert_coord, 1.0);
    frag_light_direction = normalize(light_position);
    gl_Position = projection_mat * view_mat * model_mat * vec4(vert_coord, 1);
    vec4 p = projection_mat * vec4(radius, radius, frag_eye_position.z, frag_eye_position.w);
    frag_size = 512.0 * p.x / p.w;
    gl_PointSize = frag_size + 5.0;
}
"""
fragment_shader_spheres = """
#version 330

uniform mat4 projection_mat;
uniform vec4 fog_color;
uniform float fog_start;
uniform float fog_end;

varying vec3 frag_color;
varying vec3 frag_light_direction;
varying vec4 frag_eye_position;
varying float frag_size;
varying float frag_radius;

out vec4 final_color;

vec4 outline(float distance, float linewidth, float antialias, vec4 fg_color, vec4 bg_color){
    vec4 frag_color;
    float t = linewidth/2.0 - antialias;
    float signed_distance = distance;
    float border_distance = abs(signed_distance) - t;
    float alpha = border_distance/antialias;
    alpha = exp(-alpha*alpha);
    if (border_distance < 0.0){
        frag_color = fg_color;
    }
    else{
        if (signed_distance < 0.0){
            frag_color = mix(bg_color, fg_color, sqrt(alpha));
        }
        else{
            if (abs(signed_distance) < (linewidth/2.0 + antialias)){
                frag_color = vec4(fg_color.rgb, fg_color.a * alpha);
            }
            else{
                discard;
            }
        }
    }
    return frag_color;
}

void main(){
    float dist =  abs(frag_eye_position.z);
    vec2 P = gl_PointCoord.xy - vec2(0.5, 0.5);
    float point_size = frag_size  + 5.0;
    float distance = length(P*point_size) - frag_size/2;
    vec2 texcoord = gl_PointCoord * 2.0 - vec2(1.0);
    float x = texcoord.x;
    float y = texcoord.y;
    float d = 1.0 - x*x - y*y;
    if (d <= 0.0){
        discard;
    }
    float z = sqrt(d);
    vec4 pos = frag_eye_position;
    pos.z += frag_radius*z;
    vec3 pos2 = pos.xyz;
    pos = projection_mat * pos;
    gl_FragDepth = 0.5*(pos.z / pos.w)+0.5;
    vec3 normal = vec3(x,y,z);
    float diffuse = clamp(dot(normal, frag_light_direction), 0.0, 1.0);
    vec4 color = vec4((0.5 + 0.5 * diffuse) * frag_color, 1.0);
    if (dist > fog_start){
        float fog_factor = (fog_end-dist)/(fog_end-fog_start);
        final_color = mix(fog_color, color, fog_factor);
        //vec4 my_color = mix(fog_color, color, fog_factor);
        //final_color = outline(distance, 1.0, 1.0, vec4(0,0,0,1), color);
    }
    else{
        //final_color = outline(distance, 1.0, 1.0, vec4(0,0,0,1), color);
        final_color = color;
    }
}
"""
vertex_shader_pseudospheres = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;

in vec3 vert_coord;
in vec3 vert_color;
in float vert_rad;

out vec4 geom_coord;
out vec3 geom_color;
out float geom_rad;

void main(){
    geom_color = vert_color;
    geom_coord = view_mat * model_mat * vec4(vert_coord, 1);
    geom_rad = vert_rad;
}
"""
geometry_shader_pseudospheres = """
#version 330

layout (points) in;
layout (triangle_strip, max_vertices = 37) out;

uniform mat4 projection_mat;

const float cos15 = 0.9659258262890683;
const float cos30 = 0.8660254037844387;
const float cos45 = 0.7071067811865476;
const float cos60 = 0.5000000000000001;
const float cos75 = 0.2588190451025207;
const float sin15 = 0.2588190451025207;
const float sin30 = 0.4999999999999999;
const float sin45 = 0.7071067811865475;
const float sin60 = 0.8660254037844386;
const float sin75 = 0.9659258262890683;
const vec3 shadow_col = vec3(0, 0, 0);

in vec4 geom_coord[];
in vec3 geom_color[];
in float geom_rad[];

out vec3 frag_color;

void main(){
    gl_Position = projection_mat * (geom_coord[0] + vec4(geom_rad[0], 0, 0, 0)); // Point 1
    frag_color = mix(geom_color[0], shadow_col, 0.5);
    EmitVertex();
    gl_Position = projection_mat * geom_coord[0]; // Point 2
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = projection_mat * (geom_coord[0] + vec4(cos15*geom_rad[0], sin15*geom_rad[0], 0, 0)); // Point 3
    frag_color = mix(geom_color[0], shadow_col, 0.5);
    EmitVertex();
    gl_Position = projection_mat * (geom_coord[0] + vec4(cos30*geom_rad[0], sin30*geom_rad[0], 0, 0)); // Point 4
    frag_color = mix(geom_color[0], shadow_col, 0.5);
    EmitVertex();
    gl_Position = projection_mat * geom_coord[0]; // Point 5
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = projection_mat * (geom_coord[0] + vec4(cos45*geom_rad[0], sin45*geom_rad[0], 0, 0)); // Point 6
    frag_color = mix(geom_color[0], shadow_col, 0.5);
    EmitVertex();
    gl_Position = projection_mat * (geom_coord[0] + vec4(cos60*geom_rad[0], sin60*geom_rad[0], 0, 0)); // Point 7
    frag_color = mix(geom_color[0], shadow_col, 0.5);
    EmitVertex();
    gl_Position = projection_mat * geom_coord[0]; // Point 8
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = projection_mat * (geom_coord[0] + vec4(cos75*geom_rad[0], sin75*geom_rad[0], 0, 0)); // Point 9
    frag_color = mix(geom_color[0], shadow_col, 0.5);
    EmitVertex();
    gl_Position = projection_mat * (geom_coord[0] + vec4(0, geom_rad[0], 0, 0)); // Point 10
    frag_color = mix(geom_color[0], shadow_col, 0.5);
    EmitVertex();
    gl_Position = projection_mat * geom_coord[0]; // Point 11
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = projection_mat * (geom_coord[0] + vec4(-cos75*geom_rad[0], sin75*geom_rad[0], 0, 0)); // Point 12
    frag_color = mix(geom_color[0], shadow_col, 0.5);
    EmitVertex();
    gl_Position = projection_mat * (geom_coord[0] + vec4(-cos60*geom_rad[0], sin60*geom_rad[0], 0, 0)); // Point 13
    frag_color = mix(geom_color[0], shadow_col, 0.5);
    EmitVertex();
    gl_Position = projection_mat * geom_coord[0]; // Point 14
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = projection_mat * (geom_coord[0] + vec4(-cos45*geom_rad[0], sin45*geom_rad[0], 0, 0)); // Point 15
    frag_color = mix(geom_color[0], shadow_col, 0.5);
    EmitVertex();
    gl_Position = projection_mat * (geom_coord[0] + vec4(-cos30*geom_rad[0], sin30*geom_rad[0], 0, 0)); // Point 16
    frag_color = mix(geom_color[0], shadow_col, 0.5);
    EmitVertex();
    gl_Position = projection_mat * geom_coord[0]; // Point 17
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = projection_mat * (geom_coord[0] + vec4(-cos15*geom_rad[0], sin15*geom_rad[0], 0, 0)); // Point 18
    frag_color = mix(geom_color[0], shadow_col, 0.5);
    EmitVertex();
    gl_Position = projection_mat * (geom_coord[0] + vec4(-geom_rad[0], 0, 0, 0)); // Point 19
    frag_color = mix(geom_color[0], shadow_col, 0.5);
    EmitVertex();
    gl_Position = projection_mat * geom_coord[0]; // Point 20
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = projection_mat * (geom_coord[0] + vec4(-cos15*geom_rad[0], -sin15*geom_rad[0], 0, 0)); // Point 21
    frag_color = mix(geom_color[0], shadow_col, 0.5);
    EmitVertex();
    gl_Position = projection_mat * (geom_coord[0] + vec4(-cos30*geom_rad[0], -sin30*geom_rad[0], 0, 0)); // Point 22
    frag_color = mix(geom_color[0], shadow_col, 0.5);
    EmitVertex();
    gl_Position = projection_mat * geom_coord[0]; // Point 23
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = projection_mat * (geom_coord[0] + vec4(-cos45*geom_rad[0], -sin45*geom_rad[0], 0, 0)); // Point 24
    frag_color = mix(geom_color[0], shadow_col, 0.5);
    EmitVertex();
    gl_Position = projection_mat * (geom_coord[0] + vec4(-cos60*geom_rad[0], -sin60*geom_rad[0], 0, 0)); // Point 25
    frag_color = mix(geom_color[0], shadow_col, 0.5);
    EmitVertex();
    gl_Position = projection_mat * geom_coord[0]; // Point 26
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = projection_mat * (geom_coord[0] + vec4(-cos75*geom_rad[0], -sin75*geom_rad[0], 0, 0)); // Point 27
    frag_color = mix(geom_color[0], shadow_col, 0.5);
    EmitVertex();
    gl_Position = projection_mat * (geom_coord[0] + vec4(0, -geom_rad[0], 0, 0)); // Point 28
    frag_color = mix(geom_color[0], shadow_col, 0.5);
    EmitVertex();
    gl_Position = projection_mat * geom_coord[0]; // Point 29
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = projection_mat * (geom_coord[0] + vec4(cos75*geom_rad[0], -sin75*geom_rad[0], 0, 0)); // Point 30
    frag_color = mix(geom_color[0], shadow_col, 0.5);
    EmitVertex();
    gl_Position = projection_mat * (geom_coord[0] + vec4(cos60*geom_rad[0], -sin60*geom_rad[0], 0, 0)); // Point 31
    frag_color = mix(geom_color[0], shadow_col, 0.5);
    EmitVertex();
    gl_Position = projection_mat * geom_coord[0]; // Point 32
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = projection_mat * (geom_coord[0] + vec4(cos45*geom_rad[0], -sin45*geom_rad[0], 0, 0)); // Point 33
    frag_color = mix(geom_color[0], shadow_col, 0.5);
    EmitVertex();
    gl_Position = projection_mat * (geom_coord[0] + vec4(cos30*geom_rad[0], -sin30*geom_rad[0], 0, 0)); // Point 34
    frag_color = mix(geom_color[0], shadow_col, 0.5);
    EmitVertex();
    gl_Position = projection_mat * geom_coord[0]; // Point 35
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = projection_mat * (geom_coord[0] + vec4(cos15*geom_rad[0], -sin15*geom_rad[0], 0, 0)); // Point 36
    frag_color = mix(geom_color[0], shadow_col, 0.5);
    EmitVertex();
    gl_Position = projection_mat * (geom_coord[0] + vec4(geom_rad[0], 0, 0, 0)); // Point 37
    frag_color = mix(geom_color[0], shadow_col, 0.5);
    EmitVertex();
    EndPrimitive();
}
"""
fragment_shader_pseudospheres = """
#version 330

in vec3 frag_color;

out vec4 final_color;

void main(){
    final_color = vec4(frag_color, 1);
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

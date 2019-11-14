#version 120

uniform mat4 u_model;
uniform mat4 u_view;
uniform mat4 u_projection;
uniform float u_antialias;
uniform float u_radius_multiplier;

attribute vec3  a_position;
attribute vec4  a_fg_color;
attribute vec4  a_bg_color;
attribute float a_linewidth;
attribute float a_radius;

varying vec4 v_fg_color;
varying vec4 v_bg_color;
varying float v_radius;
varying float v_linewidth;
varying float v_antialias;

void main (void) {
    v_radius = a_radius * u_radius_multiplier;
    v_linewidth = a_linewidth;
    v_antialias = u_antialias;
    v_fg_color  = a_fg_color;
    v_bg_color  = a_bg_color;
    gl_Position = u_projection * u_view * u_model * vec4(a_position, 1.0);
    gl_PointSize = v_radius + 2 * (v_linewidth + 1.5 * v_antialias);
}